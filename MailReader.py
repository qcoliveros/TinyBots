import email
import html
import imaplib
import logging
import re
import socket
import typing

from Helper import *
from Mail import *
from MailBody import *
from MailData import *
from MailDataType import *

class MailReader(Mail):
    mailbox: typing.Optional[imaplib.IMAP4_SSL] = None
    last_uid = ''
    
    def connect(self):
        try:
            response = self.refresh_token()
            auth_str = self.generate_oauth2_str(response['access_token'], base64_encode=False)
            
            self.mailbox = imaplib.IMAP4_SSL(self.config.imap_server)
            #self.mailbox.debug = 4
            
            rv, data = self.mailbox.authenticate('XOAUTH2', lambda x: auth_str)
            if rv != 'OK':
                raise self.MailError('Unable to connect to mailbox: %s' % (', '.join(map(str, error.args))))
            
            rv, mailboxes = self.mailbox.list()
            if rv != 'OK':
                self.disconnect()
                raise self.MailError('Unable to get the list of mail folders: %s' % str(rv))
            else:
                logging.debug(mailboxes)
                
            rv, data = self.mailbox.select(self.config.imap_folder)
            if rv != 'OK':
                raise self.MailError('Unable to open the mailbox: %s' % str(rv))
            else:
                logging.debug(data)
        except Exception as error:
            raise self.MailError('Unable to connect to mailbox: %s' % (', '.join(map(str, error.args))))
        
    def is_connected(self):
        if self.mailbox is not None:
            try:
                rv, data = self.mailbox.noop()
                if rv == 'OK':
                    return True
            except Exception as error:
                logging.error('Error during connection check: %s' % (', '.join(map(str, error.args))))
                pass
        return False
        
    def disconnect(self):
        if self.mailbox is not None:
            try:
                self.mailbox.close()
                self.mailbox.logout()
            except Exception as error:
                logging.debug("Unable to close the mailbox: %s" % ', '.join(error.args))
                pass
            finally:
                self.mailbox = None

    def get_last_uid(self):
        rv, data = self.mailbox.uid('search', 'UID *')
        if rv != 'OK':
            return ''
        return Helper.decode_binary(data[0])
    
    def decode_body(self, msg):
        content_part = None
        content_type = None
        
        for part in msg.walk():
            if part.get_content_type().startswith('multipart/') \
                or part.get_content_type() == 'message/rfc822' \
                or part.get_content_type() == 'text/calendar' \
                or part.get_content_charset() is None:
                continue
            elif part.get_content_type() == 'text/plain' \
                or part.get_content_type() == 'text/html':
                # extract plain text body
                content_part = part.get_payload(decode=True)
                encoding = part.get_content_charset()
                if not encoding:
                    encoding = 'utf-8'
                content_part = bytes(content_part).decode(encoding).strip()
                content_type = MailDataType.TEXT if part.get_content_type() == 'text/plain' else MailDataType.HTML
                
        body = MailBody()
        body.content = content_part
        body.type = content_type
        return body
    
    def decode_mail_data(self, value):
        result = ''
        for msg_part in email.header.decode_header(value):
            part, encoding = msg_part
            result += Helper.decode_binary(part, encoding=encoding)
        return result
    
    def parse_mail(self, uid, mail):
        try:
            msg = email.message_from_bytes(mail)
            body = self.decode_body(msg)
            
            mail_data = MailData()
            mail_data.uid = uid
            mail_data.raw = msg
            mail_data.type = body.type
            mail_data.mail_from = self.decode_mail_data(msg['From'])
            mail_data.mail_subject = self.decode_mail_data(msg['Subject'])
            mail_data.mail_body = body.content
            
            return mail_data
        except Exception as error:
            logging.critical("Unable to parse mail: %s" % error.args[0] if len(parse_error.args) > 0 else error.__str__())
    
    def search_mails(self):
        if self.last_uid is None or self.last_uid == '':
            self.last_uid = self.get_last_uid()
        
        search_string = self.config.imap_search
        if not search_string:
            search_string = "(UID %s:* UNSEEN)" % str(self.last_uid)
        else:
            search_string = re.sub(r'\${lastUID}', str(self.last_uid), search_string, flags=re.IGNORECASE)

        if re.match(r'.*\bUID\b\s*:.*', search_string) and self.last_uid == '':
            logging.debug('The mailbox is empty.')
            return
        
        try:
            rv, data = self.mailbox.uid('search', search_string)
            if rv != 'OK':
                logging.debug('No message was found in the mailbox.')
                return
        except Exception as error:
            self.disconnect()
            return self.MailError('The mailbox cannot be searched: %s' % ', '.join(map(str, error.args)))
                                  
        mails = []
        max_uid = self.last_uid
        for data_current_uid in sorted(data[0].split()):
            current_uid = Helper.decode_binary(data_current_uid)
            try:
                rv, data = self.mailbox.uid('fetch', data_current_uid, '(RFC822)')
                if rv != 'OK':
                    logging.debug('Error getting message for %s.' % current_uid)
                    return
                
                mail = self.parse_mail(current_uid, data[0][1])
                if mail is not None:
                    mails.append(mail)
            except Exception as error:
                logging.critical("Unable to process mail with UID '%s': %s" % (current_uid, ', '.join(map(str, mail_error.args))))
            finally:
                max_uid = current_uid
                
        return mails

        