import logging

class Helper:

    @staticmethod
    def decode_binary(value, **kwargs):
        encoding = kwargs.get('encoding')
        if not encoding:
            encoding = 'utf-8'
        if type(value) is bytes:
            try:
                return str(value.decode(encoding=encoding, errors='strict'))
            except UnicodeDecodeError as error:
                logging.error("Unable to decode %s: %s" % (value, error.reason))
                return ''
        else:
            return str(value)
