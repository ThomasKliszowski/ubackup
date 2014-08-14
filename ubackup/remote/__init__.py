from __future__ import absolute_import

from .dropbox import DropboxRemote
from .local import LocalRemote


REMOTES = {
    'dropbox': DropboxRemote,
    'local': LocalRemote
}
