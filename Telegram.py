import logging
import re
#import telegram

from Config import *
from Helper import *

class Telegram:
    config: Config
    #bot: telegram.Bot
    #chat: telegram.Chat
    
    def __init__(self, config):
        self.config = config
        #self.bot: telegram.Bot = telegram.Bot(self.config.tg_bot_token)
        #self.chat: telegram.Chat = bot.get_chat(self.config.tg_chat_id)
        
    '''
    Parse HTML message and remove HTML elements not supported by Telegram.
    Refer to https://core.telegram.org/bots/api#sendmessage.
    '''
    def cleanup_html(self, message):
        tg_body = message
        tg_msg = ''
        
        try:
            # Extract HTML body to get payload from mail.
            tg_body = re.sub(r'.*<body[^>]*>(?P<body>.*)</body>.*$', 
                             '\g<body>', 
                             tg_body,
                             flags=(re.DOTALL | re.MULTILINE | re.IGNORECASE))
            # Remove control characters.
            tg_body = "".join(ch for ch in tg_body if "C" != unicodedata.category(ch)[0])
            # Remove all HTML comments.
            tg_body = re.sub(r'<!--.*?-->', '', tg_body, flags=(re.DOTALL | re.MULTILINE))
            # Remove multiple line breaks and spaces.
            tg_body = re.sub(r'\s\s+', ' ', tg_body).strip()
            # Remove attributes from elements but href of "a"- elements.
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
            # Remove multiple line breaks.
            tg_msg = re.sub(r'\s*[\r\n](\s*[\r\n])+', "\n", tg_msg)
            # Preserve nbsp.
            tg_msg = re.sub(r'&nbsp;', ' ', tg_msg, flags=re.IGNORECASE)
        except Exception as error:
            logging.critical(error)

        return 
    
    '''
    Send message to Telegram.
    '''
    def send_message(self, mails: [MailData]):
        tg_chat_title = self.chat.full_name
        if not tg_chat_title:
            tg_chat_title = self.chat.title
        if not tg_chat_title:
            tg_chat_title = self.chat.description

        for mail in mails:
            try:
                if self.config.tg_markdown_version == 2:
                    parser = telegram.ParseMode.MARKDOWN_V2
                else:
                    parser = telegram.ParseMode.MARKDOWN
                    
                if mail.type == MailDataType.HTML:
                    parser = telegram.ParseMode.HTML
                    
                message = mail.summary

                response = self.bot.send_message(chat_id=self.config.tg_chat_id,
                                              parse_mode=parser,
                                              text=message,
                                              disable_web_page_preview=False)
                logging.info('Successfully sent UID %s message to %s with message id %s' \
                             % (mail.uid, str(self.config.tg_chat_id), str(response.message_id)))
            except telegram.TelegramError as error:
                logging.critical('Failed to send UID %s message to %s: %s' \
                                 % (mail.uid, str(self.config.tg_chat_id), error.message))
            except Exception as exception:
                error_msgs = [Helper.decode_binary(arg) for arg in exception.args]
                logging.critical('Failed to send UID %s message to %s: %s' \
                                 % (mail.uid, str(self.config.tg_chat_id), ', '.join(error_msgs)))
