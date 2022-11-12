import imaplib
import logging
import socket
import typing

from Config import *
from Helper import *

class MailReader:
    config: Config
    mail: typing.Optional[imaplib.IMAP4_SSL] = None
    
    def __init__(self, config):
        self.config = config
        self.connect(config.imap_server, config.imap_port)
        
    def connect(self, server, port):
        try:
            self.mail = imaplib.IMAP4_SSL(server, port)
            rv, data = self.mail.login(self.config.email_account, self.config.email_password)
        
        except socket.gaierror as socket_error:
            logging.critical('Unable to connect to email: %s' % socket_error.strerror)
        
        except imaplib.IMAP4_SSL.error as ssl_error:
            errors = [Helper.byte_to_string(arg) for arg in ssl_error.args]
            logging.critical('Unable to connect to email: %s' % ', '.join(errors))
            
        except Exception as login_error:
            logging.critical('Unable to connect to email: %s' % ', '.join(map(str, login_error.args)))
        