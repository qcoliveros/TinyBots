import logging

from Config import *

class Forwarder:
    config: Config
    
    def __init__(self):
        logging.basicConfig(#filename='tinybots.log', 
                            encoding='utf-8', 
                            format='[%(asctime)s %(name)s %(levelname)s %(module)s.%(funcName)s:%(lineno)d] : %(message)s',
                            level=logging.DEBUG)
        
        self.config = Config()
