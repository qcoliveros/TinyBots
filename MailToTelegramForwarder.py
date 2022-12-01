import logging
import sched
import threading
import time

from Forwarder import *
from MailReader import *
from PdbcTemplate import *
from Telegram import *

class MailToTelegramForwarder(Forwarder):
    db: PdbcTemplate
    mail: MailReader
    telegram: Telegram
    
    def __init__(self):
        super().__init__()
        
        self.db = PdbcTemplate(self.config)
        self.mail = MailReader(self.config)
        self.telegram = Telegram(self.config, self.db)
        
    def start(self, scheduler, delay):
        try:
            self.mail.connect()
                
            # Retrieve all unread mails.
            mails = self.mail.search_mails()
                
            # Forward the mails to Telegram.
            self.telegram.send_message(mails)
                
            self.mail.disconnect()
            
            scheduler.enterabs(delay, 1, self.start, (scheduler, delay))
        except Exception as error:
            logging.error(error)

if __name__ == '__main__':
    forwarder = MailToTelegramForwarder()
    
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enterabs(60, 1, forwarder.start, (scheduler, 60))
    
    thread = threading.Thread(target=scheduler.run)
    thread.start()
