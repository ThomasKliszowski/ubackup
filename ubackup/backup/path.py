from __future__ import absolute_import

from .base import Backup
from ubackup.utils import stream_shell

import logging
logger = logging.getLogger(__name__)


class PathBackup(Backup):
    TYPE = "path"

    def __init__(self, path):
        self.path = path

    @property
    def data(self):
        return {
            'path': self.path
        }

    @property
    def unique_name(self):
        return "path-" + self.path

    @property
    def stream(self):
        return stream_shell(
            cmd='tar -cp .',
            cwd=self.path)
