import logging

from Config import *
from MailReader import *
from Telegram import *

if __name__ == '__main__':
    logging.basicConfig(filename='tinybots.log', 
                        encoding='utf-8', 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    
    config = Config()
    mail = MailReader(config)
    telegram = Telegram(config)

    mail.connect()
    