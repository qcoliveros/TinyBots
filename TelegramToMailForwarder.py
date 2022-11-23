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

            # self.mail.send_mail('<tinybots238@gmail.com>', '<bkenlim@yahoo.com>', 'IS 238 Test-before msg received', 'Hello, this is a test email from python.')

            # message = self.telegram.receive_message()
            @self.telegram.bot.message_handler(func=lambda message: True)
            def handle_message(message):
                # self.telegram.bot.reply_to(message, message.text)
                # print(message.reply_to_message.text)
                
                self.mail.send_mail(message.reply_to_message.text, message.text)

            self.telegram.bot.infinity_polling();
            

        except Exception as error:
            logging.error(error)

if __name__ == '__main__':
    forwarder = TelegramToMailForwarder()
    forwarder.start()
