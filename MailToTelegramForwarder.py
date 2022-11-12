import logging

from Config import *
from Mail import *
from Telegram import *

if __name__ == '__main__':
    logging.basicConfig(filename='tinybots.log', encoding='utf-8', level=logging.DEBUG)
    
    config = Config()
    mail = Mail(config)
    telegram = Telegram(config)