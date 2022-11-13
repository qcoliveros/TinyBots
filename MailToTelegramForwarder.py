import logging

from Config import *
from MailReader import *
from Telegram import *

if __name__ == '__main__':
    logging.basicConfig(#filename='tinybots.log', 
                        #encoding='utf-8', 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    
    config = Config()
    mail = MailReader(config)
    telegram = Telegram(config)

    try:
        mail.connect()
        mails = mail.search_mails()
        
        # TODO: push email to telegram. 
    except Exception as error:
        logging.error('Unable to check the mailbox: %s' % error)
    finally:
        mail.disconnect()
