import argparse
import sys

from Helper import *

if __name__ == '__main__':
    try:
        args_parser = argparse.ArgumentParser()
        args_parser.add_argument('-c', '--config', type=str, required=True)
        args_parser.add_argument('--generate_permission_url', action='store_true')
        args_parser.add_argument('--generate_refresh_token', action='store_true')
        args = args_parser.parse_args()
        
        helper = Helper()
        if args.generate_permission_url:
            helper.get_mail_permission_url()
        if args.generate_refresh_token:
            helper.get_mail_refresh_token()
    except Exception as exception:
        sys.exit(2)
    