import email
import html
import smtplib
import logging
import re
import socket
import typing
import lxml.html

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Helper import *
from Mail import *

class MailSender(Mail):
    mailbox: typing.Optional[smtplib.SMTP] = None
    message = ''
    reply_to_message = ''
    reply_to_message_text = ''
    
    def connect(self):
        try:
            response = self.refresh_token()
            auth_str = self.generate_auth_str(response['access_token'], base64_encode=True)
            
            self.mailbox = smtplib.SMTP(self.config.smtp_server)
            self.mailbox.set_debuglevel(True)
            self.mailbox.ehlo(self.config.client_id)
            self.mailbox.starttls()
            self.mailbox.docmd('AUTH', 'XOAUTH2 ' + auth_str)

        except Exception as error:
            raise MailError('Unable to connect to mailbox: %s' % (', '.join(map(str, error.args))))
        
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
                self.mailbox.quit()
            except Exception as error:
                logging.debug('Unable to close the mailbox: %s' % ', '.join(error.args))
                pass
            finally:
                self.mailbox = None

    def decode_message_data(self,search_string):
        try: 
            result = ''
            lines = self.reply_to_message.split('\n')

            for line in lines: 
                words = line.split() 
                if(words): 
                    if(words[0] == search_string): 
                        result = ' '.join(words[1:])
            return result
        except Exception as error:
            logging.debug('Unable to decode message data: %s' % ', '.join(error.args))
    
    def send_mail(self,reply_to_message,message,user_name):
        try:
            self.message = message
            self.reply_to_message = reply_to_message
            self.reply_to_message_text = "\n".join(reply_to_message.split("\n")[2:])
            
            # self.reply_to_message = re.sub(r'\n','<br>',reply_to_message,flags=(re.DOTALL | re.MULTILINE))

            emailTo = self.decode_message_data('From:')
            emailSubject = self.decode_message_data('Subject:')
            if emailTo == '' or emailSubject == '': 
                return 0

            logging.debug("self.reply_to_message::: " + self.reply_to_message)
            msg = MIMEMultipart('related')
            msg['Subject'] = emailSubject
            msg['From'] = self.config.email_user
            msg['To'] = emailTo
            
            # msg_body = """<br>Reply to:<br><br>"""
            # msg_body = """<blockquote><i>"""
            # msg_body += self.reply_to_message_text
            # msg_body += """</i></blockquote><br>"""
            # msg_body += """<br>Dear """ + user_name
            msg_body = message
            msg_body += """<br><br>"""
            msg_body += """<em>Telegram response from: <strong>""" + user_name + """</strong></em>"""
            self.message = msg_body
            msg.preamble = 'This is a multi-part message in MIME format.'
            msg_alternative = MIMEMultipart('alternative')
            msg.attach(msg_alternative)
            part_text = MIMEText(lxml.html.fromstring(self.message).text_content().encode('utf-8'), 'plain', _charset='utf-8')
            part_html = MIMEText(self.message.encode('utf-8'), 'html', _charset='utf-8')
            msg_alternative.attach(part_text)
            msg_alternative.attach(part_html)
            self.mailbox.sendmail(self.config.email_user, emailTo, msg.as_string())
        except Exception as error:
            self.disconnect()
            return MailError('Unable to send email: %s' % ', '.join(map(str, error.args)))
