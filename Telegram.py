import logging

from Config import *

class Telegram:
    config: Config
    
    def __init__(self, config):
        self.config = config
        