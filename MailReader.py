import imaplib
import logging
import socket
import typing

from Helper import *
from Mail import *

class MailReader(Mail):
    mail: typing.Optional[imaplib.IMAP4_SSL] = None
    
    def connect(self):
        response = self.refresh_token()
        auth_str = self.generate_oauth2_str(response['access_token'], base64_encode=False)
        
        mail = imaplib.IMAP4_SSL(self.config.imap_server)
        mail.debug = 4
        mail.authenticate('XOAUTH2', lambda x: auth_str)
        
        mail.list()
        mail.select("INBOX")
    
   