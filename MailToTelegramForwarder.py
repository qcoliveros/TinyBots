import logging

from Forwarder import *
from MailReader import *
from Telegram import *

class MailToTelegramForwarder(Forwarder):
    mail: MailReader
    telegram: Telegram
    
    def __init__(self):
        super().__init__()
        self.mail = MailReader(self.config)
        self.telegram = Telegram(self.config)
        
    def start(self):
        try:
            self.mail.connect()
            
            # Retrieve all unread mails.
            mails = self.mail.search_mails()
            logging.debug(mails)
            
            # TODO: Push email to Telegram.
        except Exception as error:
            logging.error(error)
        finally:
            self.mail.disconnect()

if __name__ == '__main__':
    forwarder = MailToTelegramForwarder()
    forwarder.start()
