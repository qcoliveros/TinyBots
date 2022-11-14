import argparse
import configparser
import logging
import sys

class Config:
    config_parser = None
    
    # Configuration for mail.
    client_id = None
    client_secret = None
    auth_uri = None
    token_uri = None
    redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
    scope_uri = 'https://mail.google.com/'
    email_user = None
    
    auth_code = None
    refresh_token = None
    
    imap_server = None
    imap_folder = 'INBOX'
    imap_search = '(UNSEEN)'

    # Configuration for Telegram.
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
            
            self.client_id = self.get_config('Mail', 'ClientId', self.client_id)
            self.client_secret = self.get_config('Mail', 'ClientSecret', self.client_secret)
            self.auth_uri = self.get_config('Mail', 'AuthUri', self.auth_uri)
            self.token_uri = self.get_config('Mail', 'TokenUri', self.token_uri)
            self.redirect_uri = self.get_config('Mail', 'RedirectUri', self.redirect_uri)
            self.scope_uri = self.get_config('Mail', 'ScopeUri', self.scope_uri)
            self.email_user = self.get_config('Mail', 'User', self.email_user)
            
            self.auth_code = self.get_config('Mail', 'AuthorizeCode', self.auth_code)
            self.refresh_token = self.get_config('Mail', 'RefreshToken', self.refresh_token)
            
            self.imap_server = self.get_config('Mail', 'ImapServer', self.imap_server)
            
            self.tg_bot_token = self.get_config('Telegram', 'BotToken', self.tg_bot_token)
            self.tg_chat_id = self.get_config('Telegram', 'ChatId', self.tg_chat_id, int)
            
        except Exception as exception:
            sys.exit(2)

    def get_config(self, section, key, default=None, type=None):
        try:
            value = default
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
                        
            else:
                raise configparser.NoSectionError(section)
            
            return value
        except Exception as exception:
            logging.critical('Exception encountered when getting configuration value (%s > %s).' % (section, key))
            raise exception
        