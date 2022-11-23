import logging

from Forwarder import *
from MailSender import *
from Telegram import *
from email.message import EmailMessage 

class TelegramToMailForwarder(Forwarder):
    mail: MailSender
    telegram: Telegram
    
    def __init__(self):
        super().__init__()
        self.mail = MailSender(self.config)
        self.telegram = Telegram(self.config)


    def start(self):
        try:
            self.mail.connect()

            @self.telegram.bot.message_handler(func=lambda message: True)
            def handle_message(message):
                if(message.reply_to_message is not None): 
                    reply_to_msg = message.reply_to_message.text
                    if(re.search('From:',reply_to_msg) is not None and re.search('Subject:',reply_to_msg) is not None): 
                        self.mail.send_mail(reply_to_msg, message.text)

            self.telegram.bot.infinity_polling();
            

        except Exception as error:
            logging.error(error)

if __name__ == '__main__':
    forwarder = TelegramToMailForwarder()
    forwarder.start()
