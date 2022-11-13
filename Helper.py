import logging

from Config import *
from Mail import *

class Helper:
    
    '''
    Utility method to generate the Gmail URL to authorize the application.
    Update the AuthorizeCode in application.conf based on the obtained authorization code.
    '''
    @staticmethod
    def get_mail_permission_url():
        config = Config()
        mail = Mail(config)
        print(mail.generate_permission_url())
        
    '''
    Utility method to generate the refresh token.
    Update the RefreshToken in application.conf based on the obtained refresh token.
    '''
    @staticmethod
    def get_mail_refresh_token():
        config = Config()
        mail = Mail(config)
        response = mail.authorize_token()
        print(response['refresh_token'])
        
    @staticmethod
    def decode_binary(value, **kwargs):
        encoding = kwargs.get('encoding')
        if not encoding:
            encoding = 'utf-8'
        if type(value) is bytes:
            try:
                return str(value.decode(encoding=encoding, errors='strict'))
            except UnicodeDecodeError as error:
                logging.error("Unable to decode %s: %s" % (value, error.reason))
                return ''
        else:
            return str(value)
