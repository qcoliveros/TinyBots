from MailDataType import *

class MailData:
    uid: str = ''
    raw: str = ''
    type: MailDataType = MailDataType.TEXT
    mail_from: str = ''
    mail_subject: str = ''
    mail_body: str = ''
    