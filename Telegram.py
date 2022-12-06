import html
import logging
import re
import telebot
import unicodedata
import ssl 
import smtplib 

from email.message import EmailMessage 
from Config import *
from Helper import *
from Mail import *
from SimplePdbc import *

class Telegram:
    config: Config
    db: SimplePdbc
    bot: telebot.TeleBot
    
    def __init__(self, config, db=None):
        self.config = config
        self.db = db
        self.bot = telebot.TeleBot(self.config.tg_bot_token)
        
    '''
    Parse HTML message and remove HTML elements not supported by Telegram.
    Refer to https://core.telegram.org/bots/api#sendmessage.
    '''
    def escape_html(self, message):
        tg_body = message
        tg_msg = ''

        try:
            # Extract HTML body to get payload from mail.
            tg_body = re.sub(r'.*<body[^>]*>(?P<body>.*)</body>.*$', 
                             '\g<body>', 
                             tg_body,
                             flags=(re.DOTALL | re.MULTILINE | re.IGNORECASE))
            # Remove control characters.
            tg_body = ''.join(ch for ch in tg_body if 'C' != unicodedata.category(ch)[0])
            # Remove all HTML comments.
            tg_body = re.sub(r'<!--.*?-->', '', tg_body, flags=(re.DOTALL | re.MULTILINE))
            # Remove multiple line breaks and spaces.
            tg_body = re.sub(r'\s\s+', ' ', tg_body).strip()
            # Remove attributes from elements but href of 'a'- elements.
            tg_msg = re.sub(r'<\s*?(?P<elem>\w+)\b\s*?[^>]*?(?P<ref>\s+href\s*=\s*"[^"]+")?[^>]*?>',
                            '<\g<elem>\g<ref>>', 
                            tg_body, 
                            flags=(re.DOTALL | re.MULTILINE | re.IGNORECASE))
            # Remove style and script elements/blocks.
            tg_msg = re.sub(r'<\s*(?P<elem>script|style)\s*>.*?</\s*(?P=elem)\s*>',
                            '', 
                            tg_msg, 
                            flags=(re.DOTALL | re.MULTILINE | re.IGNORECASE))
            # Translate paragraphs and line breaks.
            tg_msg = re.sub(r'</?\s*(?P<elem>(p|div|table|h\d+))\s*>', 
                            '\n', 
                            tg_msg,
                            flags=(re.MULTILINE | re.IGNORECASE))
            tg_msg = re.sub(r'</\s*(?P<elem>(tr))\s*>', '\n', tg_msg, flags=(re.MULTILINE | re.IGNORECASE))
            tg_msg = re.sub(r'</?\s*(br)\s*[^>]*>', '\n', tg_msg, flags=(re.MULTILINE | re.IGNORECASE))
            # Prepare list items.
            tg_msg = re.sub(r'(<\s*[ou]l\s*>[^<]*)?<\s*li\s*>', '\n- ', tg_msg, flags=(re.MULTILINE | re.IGNORECASE))
            tg_msg = re.sub(r'</\s*li\s*>([^<]*</\s*[ou]l\s*>)?', '\n', tg_msg, flags=(re.MULTILINE | re.IGNORECASE))
            # Remove unsupported tags
            # Refer to https://core.telegram.org/api/entities.
            regex_filter_elem = re.compile(
                r'<\s*(?!/?\s*(?P<elem>bold|strong|i|em|u|ins|s|strike|del|b|a|code|pre)\b)[^>]*>',
                flags=(re.MULTILINE | re.IGNORECASE))
            tg_msg = re.sub(regex_filter_elem, ' ', tg_msg)
            # Remove empty links.
            tg_msg = re.sub(r'<\s*a\s*>(?P<link>[^<]*)</\s*a\s*>', 
                            '\g<link> ', 
                            tg_msg,
                            flags=(re.DOTALL | re.MULTILINE | re.IGNORECASE))
            # Remove links without text.
            tg_msg = re.sub(r'<\s*a\s*[^>]*>\s*</\s*a\s*>', 
                            ' ', 
                            tg_msg,
                            flags=(re.DOTALL | re.MULTILINE | re.IGNORECASE))
            # Remove empty elements.
            tg_msg = re.sub(r'<\s*\w\s*>\s*</\s*\w\s*>', ' ', tg_msg, flags=(re.DOTALL | re.MULTILINE))
            # Preserve nbsp.
            tg_msg = re.sub(r'&nbsp;', ' ', tg_msg, flags=re.IGNORECASE)
            # Remove multiple line breaks (keeping up to 1 empty line).
            tg_msg = re.sub(r'(\s*\r?\n){2,}', '\n\n', tg_msg)
            # Add space after links.
            tg_msg = re.sub(r'(?P<a></a>(\s*&gt;)?)\s*', '\g<a>\n\n', tg_msg, flags=re.MULTILINE)
            # Remove spaces and line breaks on start and end.
            tg_msg = re.sub(r'^\s*', '', tg_msg)
            tg_msg = re.sub(r'\s*$', '', tg_msg)

        except Exception as error:
            logging.critical(error)

        return tg_msg
    
    '''
    Send the mails to Telegram.
    '''
    def send_message(self, mails: MailData):
        for mail in mails:
            try:
                logging.debug('Original email content:\n%s' % mail.body)
                
                content = '\n\n'
                if mail.type == MailDataType.HTML:
                    content += self.escape_html(mail.body)
                else:
                    content += mail.body
                    
                if self.config.tg_html_format:
                    parser = 'HTML'
                    
                    sender = '<b>From:</b> ' + html.escape(mail.sender, quote=True)
                    subject = '\n<b>Subject:</b> ' + mail.subject
                    
                else:
                    parser = 'MarkdownV2'
                    
                    sender = '*From:* ' + telebot.formatting.escape_markdown(mail.sender)
                    subject = '\n*Subject:* ' + telebot.formatting.escape_markdown(mail.subject)
                    
                message = sender + subject + content
                logging.debug('Message to be sent to Telegram:\n%s' % message)
                
                last_message_id = self.db.get_user_message_id(mail.sender);
                logging.info('last message id for %s is %s' % (mail.sender, str(last_message_id)))
                if len(last_message_id) > 0:
                    response = self.bot.send_message(chat_id=self.config.tg_chat_id,
                                                  parse_mode=parser,
                                                  text=message,
                                                  disable_web_page_preview=False,
                                                  reply_to_message_id=last_message_id[0])
                    self.db.update_user_message_id(mail.sender, response.message_id)
                else:
                    response = self.bot.send_message(chat_id=self.config.tg_chat_id,
                                                  parse_mode=parser,
                                                  text=message,
                                                  disable_web_page_preview=False)
                    self.db.create_user(mail.sender, response.message_id)
                    
                logging.info('Successfully sent UID %s message to %s with message id %s' \
                             % (mail.uid, str(self.config.tg_chat_id), str(response.message_id)))
            except Exception as exception:
                error_msgs = [Helper.decode_binary(arg) for arg in exception.args]
                logging.critical('Failed to send UID %s message to %s: %s' \
                                 % (mail.uid, str(self.config.tg_chat_id), ', '.join(error_msgs)))

    '''
    Receive messages on Telegram.
    '''
    def receive_message(self):
        try:
            @self.bot.message_handler(func=lambda message: True)
            def handle_message(message):
                self.bot.reply_to(message, message)
                return message

            # self.bot.infinity_polling()

        except Exception as exception:
            error_msgs = [Helper.decode_binary(arg) for arg in exception.args]
            logging.critical('Failed to receive message %s : %s' \
                            % (str(self.config.tg_chat_id), ', '.join(error_msgs)))
