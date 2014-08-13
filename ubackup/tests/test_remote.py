import unittest
import mock
from StringIO import StringIO
from ubackup.remote.dropbox import DropboxRemote
from ubackup.remote.base import Remote


class DropboxRequest(object):
    def json(*args, **kwargs):
        return {}


class RemoteTest(unittest.TestCase):

    def test_remote_base(self):
        remote = Remote()
        self.assertRaises(NotImplementedError, remote.pull, 'filename')
        self.assertRaises(NotImplementedError, remote.push, StringIO('stream'), 'filename')

    @mock.patch('requests.request')
    def test_dropbox_remote(self, mock_method):
        mock_method.return_value = DropboxRequest()

        remote = DropboxRemote(token="coucou")
        remote.pull('filename')
        remote.push(StringIO('test'), 'filename')
        self.assertFalse(remote.exists('foo'))

        self.assertTrue(mock_method.called)
