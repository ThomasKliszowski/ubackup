from ubackup.utils import md5_stream, gzip_stream, crypt_stream
from ubackup import settings

import logging
logger = logging.getLogger(__name__)


class Creator(object):

    @property
    def TYPE(self):
        raise NotImplementedError

    @property
    def data(self):
        raise NotImplementedError

    @property
    def unique_name(self):
        raise NotImplementedError

    @property
    def stream(self):
        raise NotImplementedError

    @property
    def crypt_enabled(self):
        return hasattr(settings, 'CRYPT_KEY')

    # -----

    def checksum(self):
        logger.info('Checksum: %(name)s(%(data)s)' % {
            'name': self.__class__.__name__,
            'data': self.data
        })
        return md5_stream(self.stream)

    def create(self, crypt=True):
        logger.info('Create: %(name)s(%(data)s)' % {
            'name': self.__class__.__name__,
            'data': self.data
        })
        stream = gzip_stream(self.stream)

        if crypt:
            stream = crypt_stream(stream, settings.CRYPT_KEY)

        return stream
