import logging
import sched
import time

from Forwarder import *
from MailReader import *
from Telegram import *
from SimplePdbc import *

class MailToTelegramForwarder(Forwarder):
    db: SimplePdbc
    mail: MailReader
    telegram: Telegram
    
    def __init__(self):
        super().__init__()
        self.db = SimplePdbc(self.config)
        self.mail = MailReader(self.config)
        self.telegram = Telegram(self.config, self.db)
    
    def connect(self):
        self.db.connect()
        self.mail.connect()
        
    def disconnect(self):
        self.mail.disconnect()
        self.db.disconnect()
        
    def start(self, scheduler, delay):
        # Retrieve all unread mails.
        mails = self.mail.search_mails()
        # Forward the mails to Telegram.
        self.telegram.send_message(mails)
            
        scheduler.enter(delay, 1, self.start, (scheduler, delay))

if __name__ == '__main__':
    forwarder = MailToTelegramForwarder()
    try:
        forwarder.connect()
         
        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler.enter(5, 1, forwarder.start, (scheduler, 5))
        scheduler.run()
    except Exception as error:
        logging.error(error)
        forwarder.disconnect()
