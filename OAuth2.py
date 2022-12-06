import argparse
import sys

from Config import *
from Mail import *

if __name__ == '__main__':
    try:
        config = Config()
        mail = Mail(config)
        
        args_parser = argparse.ArgumentParser()
        args_parser.add_argument('-c', '--config', type=str, required=True)
        args_parser.add_argument('--generate_permission_url', action='store_true')
        args_parser.add_argument('--generate_refresh_token', action='store_true')
        args = args_parser.parse_args()
        
        if args.generate_permission_url:
            '''
            Generate the Gmail URL to authorize the application.
            Update the AuthorizeCode in application.conf based on the obtained authorization code.
            '''
            print(mail.generate_permission_url())
            
        if args.generate_refresh_token:
            '''
            Generate the refresh token.
            Update the RefreshToken in application.conf based on the obtained refresh token.
            '''
            response = mail.authorize_token()
            print(response['refresh_token'])
        
    except Exception as exception:
        sys.exit(2)
    