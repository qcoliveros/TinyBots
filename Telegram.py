import html
import logging
import re
import telebot
import unicodedata

from Config import *
from Helper import *

class Telegram:
    config: Config
    bot: telebot.TeleBot
    
    def __init__(self, config):
        self.config = config
        self.bot = telebot.TeleBot(self.config.tg_bot_token)
    
    '''
    Send the mails to Telegram.
    '''
    def send_message(self, mails: [MailData]):
        for mail in mails:
            try:
                logging.debug(mail)
                    
                summary_line = "\n"
                
                if mail.type == MailDataType.HTML:
                    parser = 'HTML'
                    
                    sender = html.escape(mail.sender, quote=True)
                    subject = mail.subject
                    content = telebot.formatting.escape_html(mail.body)
                    
                    text = "<b>From:</b> " + sender + "\n<b>Subject:</b> "
                else:
                    parser = 'MarkdownV2'
                    
                    sender = telebot.formatting.escape_markdown(mail.sender)
                    subject = telebot.formatting.escape_markdown(mail.subject)
                    content = telebot.formatting.escape_markdown(mail.body)
                    
                    text = "*From:* " + sender + "\n*Subject:* "
                    
                message = text + subject + summary_line + content
                logging.debug(message)

                response = self.bot.send_message(chat_id=self.config.tg_chat_id,
                                              parse_mode=parser,
                                              text=message,
                                              disable_web_page_preview=False)
                
                logging.info('Successfully sent UID %s message to %s with message id %s' \
                             % (mail.uid, str(self.config.tg_chat_id), str(response.message_id)))
            except Exception as exception:
                error_msgs = [Helper.decode_binary(arg) for arg in exception.args]
                logging.critical('Failed to send UID %s message to %s: %s' \
                                 % (mail.uid, str(self.config.tg_chat_id), ', '.join(error_msgs)))
