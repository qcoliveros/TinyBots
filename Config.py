import argparse
import configparser
import logging
import sys

class Config:
    config_parser = None
    
    # Configuration for mail.
    imap_folder = 'INBOX'
    imap_search = None
    
    imap_server = 'imap.googlemail.com'
    smtp_server = 'smtp.gmail.com:587'
    
    mail_user = None
    
    mail_auth_method = 'OAuth2'
    
    # Configuration for mail - oauth2.
    mail_client_id = None
    mail_client_secret = None
    mail_auth_uri = None
    mail_token_uri = None
    mail_redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
    mail_scope_uri = 'https://mail.google.com/'
    
    mail_auth_code = None
    mail_refresh_token = None
    
    # Configuration for mail - application password.
    mail_app_password = None

    # Configuration for Telegram.
    tg_bot_token = None
    tg_chat_id = None
    tg_html_format = True
    
    # Configuration for database.
    db_file = None
    
    def __init__(self):
        try:
            args_parser = argparse.ArgumentParser()
            args_parser.add_argument('-c', '--config', type=str, required=True)
            args, unknown = args_parser.parse_known_args()
            
            self.config_parser = configparser.ConfigParser()
            files = self.config_parser.read(args.config)
            if len(files) == 0:
                logging.critical('Cannot find the provided configuration file %s.' % args.config)
                raise Exception
            
            self.imap_folder = self.get_config('Mail', 'ImapFolder', self.imap_folder)
            self.imap_search = self.get_config('Mail', 'ImapSearch', self.imap_search)
            
            self.imap_server = self.get_config('Mail', 'ImapServer', self.imap_server)
            self.smtp_server = self.get_config('Mail', 'SmtpServer', self.smtp_server)
            
            self.mail_user = self.get_config('Mail', 'User', self.mail_user)
            
            self.mail_auth_method = self.get_config('Mail', 'AuthenticationMethod', self.mail_auth_method)
            if self.mail_auth_method == 'OAuth2':
                self.mail_client_id = self.get_config('Mail', 'ClientId', self.mail_client_id)
                self.mail_client_secret = self.get_config('Mail', 'ClientSecret', self.mail_client_secret)
                self.mail_auth_uri = self.get_config('Mail', 'AuthUri', self.mail_auth_uri)
                self.mail_token_uri = self.get_config('Mail', 'TokenUri', self.mail_token_uri)
                self.mail_redirect_uri = self.get_config('Mail', 'RedirectUri', self.mail_redirect_uri)
                self.mail_scope_uri = self.get_config('Mail', 'ScopeUri', self.mail_scope_uri)
                self.mail_auth_code = self.get_config('Mail', 'AuthorizeCode', self.mail_auth_code)
                self.mail_refresh_token = self.get_config('Mail', 'RefreshToken', self.mail_refresh_token)
            else:
                self.mail_app_password = self.get_config('Mail', 'AppPassword', self.mail_app_password)
            
            self.tg_bot_token = self.get_config('Telegram', 'BotToken', self.tg_bot_token)
            self.tg_chat_id = self.get_config('Telegram', 'ChatId', self.tg_chat_id, int)
            
            self.db_file = self.get_config('Database', 'File', self.db_file)
            
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
        