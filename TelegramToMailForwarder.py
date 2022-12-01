import logging

from email.message import EmailMessage 
from Forwarder import *
from MailSender import *
from Telegram import *

class TelegramToMailForwarder(Forwarder):
    mail: MailSender
    telegram: Telegram
    saved_message = ''
    saved_reply_to_msg = ''
    saved_username = ''
    user_name = ''
    
    def __init__(self):
        super().__init__()
        self.mail = MailSender(self.config)
        self.telegram = Telegram(self.config)

    def start(self):
        try:
            self.mail.connect()

            @self.telegram.bot.message_handler(func=lambda message: True)
            def handle_message(message):
                if message.reply_to_message is not None: 
                    reply_to_msg = message.reply_to_message.text
                    if re.search('From:',reply_to_msg) is not None and re.search('Subject:',reply_to_msg) is not None: 
                        # get the username info from the telegram message
                        self.user_name = ' '.join(filter(None, (message.from_user.first_name, message.from_user.last_name,)))
                        if(message.from_user.username is not None): 
                            self.user_name += '(' + message.from_user.username + ')'

                        # save the information before the bot asks  send email or not
                        self.saved_username = self.user_name
                        self.saved_message = message.text + '\n- ' + self.user_name
                        self.saved_reply_to_msg = reply_to_msg

                        # send a confirmation message
                        self.telegram.bot.reply_to(message, "Respond to Email (Y/N)?")

                    if re.search('Respond to Email',reply_to_msg) is not None and (message.text.lower() == 'y' or message.text.lower() == 'yes'): 
                        # get the username info from the confirmation message
                        self.user_name = ' '.join(filter(None, (message.from_user.first_name, message.from_user.last_name,)))
                        if message.from_user.username is not None: 
                            self.user_name += '(' + message.from_user.username + ')'

                        # check if the confirmation message is from the same user who initially responded
                        if self.saved_username == self.user_name:
                            # if so, send the email
                            self.mail.send_mail(self.saved_reply_to_msg, self.saved_message)

            self.telegram.bot.infinity_polling();
            
        except Exception as error:
            logging.error(error)
        finally:
            self.mail.disconnect()

if __name__ == '__main__':
    forwarder = TelegramToMailForwarder()
    forwarder.start()
