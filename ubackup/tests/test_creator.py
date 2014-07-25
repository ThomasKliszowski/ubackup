import mock
import unittest
import os
import shutil
from uuid import uuid4
from ubackup.creator.base import Creator
from ubackup.creator.path import PathCreator
from ubackup.creator.mysql import MysqlCreator
from ubackup.utils import md5_stream, stream_shell


class RemoteTest(unittest.TestCase):

    def test_creator_base(self):
        creator = Creator()
        with self.assertRaises(NotImplementedError):
            creator.data
        with self.assertRaises(NotImplementedError):
            creator.unique_name
        with self.assertRaises(NotImplementedError):
            creator.create()
        with self.assertRaises(NotImplementedError):
            creator.checksum()

    def test_creator_path(self):
        temp_dir = uuid4().hex
        os.mkdir(temp_dir)
        temp_dir = os.path.abspath(temp_dir)

        with open(os.path.join(temp_dir, 'foo'), 'w') as fp:
            fp.write('bar')

        creator = PathCreator(temp_dir)

        # Checksum
        self.assertEqual(
            creator.checksum(),
            md5_stream(stream_shell(
                cmd='tar -cp .',
                cwd=temp_dir)))

        # Create
        stream = creator.create()
        stream.read()

        creator.data
        creator.unique_name

        shutil.rmtree(temp_dir)

    @mock.patch('ubackup.utils.stream_shell')
    def test_creator_mysql(self, mock_method):
        creator = MysqlCreator([])

        # Checksum
        mock_method.return_value = stream_shell(cmd="echo 'foo'")
        md5_processed = md5_stream(stream_shell(
            cmd="echo 'foo'"))
        mock_method.return_value = stream_shell(cmd="echo 'foo'")
        md5_by_create = creator.checksum()
        self.assertEqual(md5_processed, md5_by_create)

        # Dump
        creator.databases = []
        creator.mysql_dump()
        creator.databases = ['foo']
        creator.mysql_dump()

        # Create
        stream = creator.create()
        stream.read()

        creator.data
        creator.unique_name
