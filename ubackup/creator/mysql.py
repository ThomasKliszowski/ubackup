from __future__ import absolute_import

from .base import Creator
from ubackup.utils import stream_shell


class MysqlCreator(Creator):
    TYPE = "mysql"

    def __init__(self, databases):
        self.databases = databases

    @property
    def data(self):
        return {
            'databases': self.databases
        }

    @property
    def unique_name(self):
        return "mysql-" + "-".join(self.databases)

    @property
    def stream(self):
        cmd = 'mysqldump -uroot --skip-comments'

        if len(self.databases) == 0:
            cmd += ' --all-databases'
        else:
            cmd += ' --databases %s' % " ".join(self.databases)
        return stream_shell(cmd)
