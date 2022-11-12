import logging

class Helper:
    
    @staticmethod
    def byte_to_string(value, **kwargs) -> str:
        encoding = kwargs.get('encoding')
        if not encoding:
            encoding = 'utf-8'
        if type(value) is bytes:
            try:
                return str(bytes.decode(value, encoding=encoding, errors='replace'))
            except UnicodeDecodeError as decode_error:
                logging.error('Unable to decode %s: %s' % (value, decode_error.reason))
                return None
        else:
            return str(value)