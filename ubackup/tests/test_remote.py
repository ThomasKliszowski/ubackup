import unittest
import mock
import os
import shutil
from uuid import uuid4
from StringIO import StringIO
from ubackup.remote.dropbox import DropboxRemote
from ubackup.remote.local import LocalRemote
from ubackup.remote.base import Remote


class DropboxRequest(object):
    def json(*args, **kwargs):
        return {}


class RemoteTest(unittest.TestCase):

    def test_remote_base(self):
        remote = Remote()
        self.assertRaises(NotImplementedError, remote.pull, 'filename')
        self.assertRaises(NotImplementedError, remote.push, StringIO('stream'), 'filename')
        self.assertRaises(NotImplementedError, remote.exists, 'filename')

    @mock.patch('requests.request')
    def test_dropbox_remote(self, mock_method):
        mock_method.return_value = DropboxRequest()

        # Test pull/push
        remote = DropboxRemote(token="coucou")
        remote.pull('filename')
        remote.pull('filename', rev=1)
        remote.push(StringIO('test'), 'filename')
        self.assertFalse(remote.exists('foo'))

        # Test revisions
        class DropboxRequest2(object):
            def json(*args, **kwargs):
                return [{
                    'rev': 1,
                    'bytes': 1000,
                    'modified': 'Fri, 16 Sep 2011 01:01:25 +0000'
                }, {
                    'rev': 2,
                    'bytes': 1000,
                    'modified': 'Fri, 16 Sep 2011 01:01:25 +0000'
                }]
        mock_method.return_value = DropboxRequest2()
        self.assertEqual(len(remote.get_revisions('filename')), 2)

        self.assertTrue(mock_method.called)

    def test_local_remote(self):
        temp_dir = uuid4().hex
        os.mkdir(temp_dir)
        temp_dir = os.path.abspath(temp_dir)

        # Test versioning
        remote = LocalRemote(path=temp_dir, files_limit=2)
        remote.push(StringIO('test'), 'foo', versioning=True)
        remote.push(StringIO('test'), 'foo', versioning=True)
        self.assertEqual(len(remote.get_revisions('foo')), 2)

        # Test files limit
        remote.push(StringIO('test'), 'foo', versioning=True)
        remote.push(StringIO('test'), 'foo', versioning=True)
        self.assertEqual(len(remote.get_revisions('foo')), 2)

        # Test pull
        self.assertEqual(remote.pull('foo').read(), 'test')

        # Test pull with rev
        rev = remote.get_revisions('foo')[-1]['id']
        self.assertEqual(remote.pull('foo', rev=rev).read(), 'test')

        # Test exists
        self.assertTrue(remote.exists('foo'))
        self.assertFalse(remote.exists('bar'))

        shutil.rmtree(temp_dir)
