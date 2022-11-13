import logging

from Config import *
from Mail import *

class Helper:
    
    '''
    Utility method to generate the Gmail URL to authorize the application.
    Update the AuthorizeCode in application.conf based on the provided authorization code.
    '''
    @staticmethod
    def get_mail_permission_url():
        config = Config()
        mail = Mail(config)
        print(mail.generate_permission_url())
        
    '''
    Utility method to generate the refresh token.
    Update the RefreshToken in application.conf based on the provided refresh token.
    '''
    @staticmethod
    def get_mail_refresh_token():
        config = Config()
        mail = Mail(config)
        response = mail.authorize_token()
        print(response['refresh_token'])
