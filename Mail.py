import base64
import json
import sys

if sys.version_info[0] == 3:
    from urllib.request import urlopen
    from urllib.parse import urlencode, quote, unquote
    raw_input = input
else:
    from urllib import urlopen, urlencode, quote, unquote

from Config import *
from enum import Enum

'''
Register with Google as an OAuth application and obtain an OAuth client ID and client secret.
See https://developers.google.com/identity/protocols/OAuth2 for instructions on
registering and for documentation of the APIs invoked by this code.
'''
class Mail:
    config: Config
    
    def __init__(self, config):
        self.config = config
    
    def escape_url(self, text):
        return quote(text, safe='~-._')
    
    def format_url_params(self, params):
        param_fragments = []
        for param in sorted(params.items(), key=lambda x: x[0]):
            param_fragments.append('%s=%s' % (param[0], self.escape_url(param[1])))
            
        return '&'.join(param_fragments)
        
    def generate_permission_url(self):
        params = {}
        params['client_id'] = self.config.mail_client_id
        params['redirect_uri'] = self.config.mail_redirect_uri
        params['scope'] = self.config.mail_scope_uri
        params['response_type'] = 'code'
        params['prompt'] = 'consent'
        params['access_type'] = 'offline'
        params['include_granted_scopes'] = 'true'
        
        return '%s?%s' % (self.config.mail_auth_uri, self.format_url_params(params))
    
    def authorize_token(self):
        params = {}
        params['client_id'] = self.config.mail_client_id
        params['client_secret'] = self.config.mail_client_secret
        params['code'] = self.config.mail_auth_code
        params['redirect_uri'] = self.config.mail_redirect_uri
        params['grant_type'] = 'authorization_code'
        params['access_type'] = 'offline'
        params['include_granted_scopes'] = 'true'
        
        response = urlopen(self.config.mail_token_uri, urlencode(params).encode()).read()
        return json.loads(response.decode())
    
    def refresh_token(self):
        params = {}
        params['client_id'] = self.config.mail_client_id
        params['client_secret'] = self.config.mail_client_secret
        params['refresh_token'] = self.config.mail_refresh_token
        params['grant_type'] = 'refresh_token'
        params['access_type'] = 'offline'
        params['include_granted_scopes'] = 'true'
        
        response = urlopen(self.config.mail_token_uri, urlencode(params).encode()).read()
        return json.loads(response.decode())
  
    def generate_auth_str(self, access_token, base64_encode=True):
        auth_str = 'user=%s\1auth=Bearer %s\1\1' % (self.config.mail_user, access_token)
        if base64_encode:
            auth_str = base64.b64encode(auth_str.encode()).decode()
        
        return auth_str
    
class MailError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors

class MailAuthenticationMethod(str, Enum):
    APP_PASSWORD = 'AppPassword'
    OAUTH2 = 'OAuth2'

class MailDataType(Enum):
    TEXT = 1
    HTML = 2

class MailBody:
    content = ''
    type = MailDataType.TEXT
    
    def __str__(self):
        return '{type:%s, content:%s}' % (self.type, self.content)
    
    def __repr__(self):
        return self.__str__()
    
class MailData:
    uid = ''
    raw = ''
    type = MailDataType.TEXT
    sender = ''
    subject = ''
    body = ''
    
    def __str__(self):
        return '{uid:%s, type:%s, sender:%s, subject:%s, body:%s}' % (self.uid, self.type, self.sender, self.subject, self.body) 
    
    def __repr__(self):
        return self.__str__()
