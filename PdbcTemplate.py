import logging
import sqlite3

from Config import *
from sqlite3 import Error

class PdbcTemplate:
    config: Config
    conn = None
    
    def __init__(self, config):
        self.config = config
        self.connect()
    
    def connect(self):
        try:
            self.conn = sqlite3.connect(self.config.db_file)
            self.conn.execute('CREATE TABLE IF NOT EXISTS user_message (id INTEGER PRIMARY KEY, user TEXT, last_message_id INTEGER)')
        except Error as error:
           raise DatabaseError('Failed to connect to the database: %s' % error.msg)
            
    def disconnect(self):
        self.conn.close()

class DatabaseError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors
