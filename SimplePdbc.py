import logging
import sqlite3

from Config import *
from sqlite3 import Error

class SimplePdbc:
    config: Config
    connection = None
    
    def __init__(self, config):
        self.config = config
    
    def connect(self):
        try:
            self.connection = sqlite3.connect(self.config.db_file)
            self.connection.execute('CREATE TABLE IF NOT EXISTS user_message (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, last_message_id INTEGER)')
        except Error as error:
           raise DatabaseError('Failed to connect to the database: %s' % error.msg)
            
    def disconnect(self):
        self.connection.close()
        
    def create_user(self, user, last_message_id):
        self.connection.execute('INSERT INTO user_message (user, last_message_id) VALUES (?, ?)', (user, last_message_id))
        self.connection.commit()
        
    def update_user_message_id(self, user, last_message_id):
        self.connection.execute('UPDATE user_message SET last_message_id = ? WHERE user = ?', (last_message_id, user))
        self.connection.commit()
        
    def get_user_message_id(self, user):
        return self.connection.execute('SELECT last_message_id FROM user_message WHERE user = ?', (user,)).fetchall()

class DatabaseError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors
