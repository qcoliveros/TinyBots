import logging

from Config import *

class Mail:
    config: Config
    
    def __init__(self, config):
        self.config = config
        