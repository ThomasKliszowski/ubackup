from StringIO import StringIO
import hashlib
import json

import logging
logger = logging.getLogger(__name__)


class Manager(object):
    DATA_FILE = "backup_data.json"
    CRYPT_FLAG = "crypted"

    def __init__(self, remote):
        self.remote = remote

    def build_filename(self, backup, crypt=True):
        m = hashlib.md5()
        m.update(backup.unique_name)
        filename = m.hexdigest()

        # Flag the file as crypted
        if backup.crypt_enabled and crypt:
            filename += "-%s" % self.CRYPT_FLAG

        return "%s.gz" % filename

# -----

    def pull_data(self):
        data = self.remote.pull(self.DATA_FILE).read()
        try:
            data = json.loads(data)
        except ValueError:
            data = {}
        return data

    def push_data(self):
        stream = StringIO(json.dumps(self.data))
        self.remote.push(stream, self.DATA_FILE)

    @property
    def data(self):
        # Lazy data pulling
        if not hasattr(self, '_cached_data'):
            self._cached_data = self.pull_data()
        return self._cached_data

# -----

    def push_backup(self, backup):
        checksum = backup.checksum()

        filename = self.build_filename(backup)
        if backup.TYPE not in self.data:
            self.data[backup.TYPE] = {}

        if filename in self.data[backup.TYPE]:
            backup_data = self.data[backup.TYPE][filename]
            if checksum == backup_data['checksum']:
                logger.info('Backup already exists with the same version: %s (%s)' % (filename, backup.TYPE))
                return

        stream = backup.create()
        self.remote.push(stream, filename)

        self.data[backup.TYPE][filename] = {
            'data': backup.data,
            'checksum': checksum
        }

        self.push_data()

    def restore_backup(self, restorer):
        pass
