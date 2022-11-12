import argparse
import configparser
import logging
import sys

class Config:
    config_parser = None

    imap_host = None
    imap_port = 465
    imap_username = None
    imap_password = None
    imap_folder = 'INBOX'
    imap_search = '(UID ${lastUID}:* UNSEEN)'

    tg_bot_token = None
    tg_chat_id = None
    tg_prefer_html = True
    
    def __init__(self):
        try:
            args_parser = argparse.ArgumentParser()
            args_parser.add_argument('-c', '--config', type=str, required=True)
            args = args_parser.parse_args()
            
            self.config_parser = configparser.ConfigParser()
            files = self.config_parser.read(args.config)
            if len(files) == 0:
                logging.critical('Cannot find the provided configuration file %s.' % args.config)
                raise Exception
                
            self.imap_host = self.get_config('Mail', 'Host', self.imap_host)
            self.imap_port = self.get_config('Mail', 'Port', self.imap_port, int)    
            self.imap_username = self.get_config('Mail', 'Username', self.imap_username)
            self.imap_password = self.get_config('Mail', 'Password', self.imap_password)
            self.imap_folder = self.get_config('Mail', 'Folder', self.imap_folder)
            self.imap_search = self.get_config('Mail', 'Search', self.imap_search)
    
            self.tg_bot_token = self.get_config('Telegram', 'BotToken', self.tg_bot_token)
            self.tg_chat_id = self.get_config('Telegram', 'ChatId', self.tg_chat_id, int)
            
        except Exception as exception:
            sys.exit(2)

    def get_config(self, section, key, default=None, type=None):
        try:
            value = None
            if self.config_parser.has_section(section):
                if self.config_parser.has_option(section, key):
                    if type is int:
                        value = self.config_parser.getint(section, key)
                    elif type is float:
                        value = self.config_parser.getfloat(section, key)
                    elif type is bool:
                        value = self.config_parser.getboolean(section, key)
                    else:
                        value = self.config_parser.get(section, key)
                    logging.debug('%s = %s' % (key, value))
                    
                    return value
            else:
                raise configparser.NoSectionError(section)
                
        except Exception as exception:
            logging.critical('Exception encountered when getting configuration value (%s > %s).' % (section, key))
            raise exception
        
        