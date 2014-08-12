import unittest
import os
import shutil
import sys
import mock
from uuid import uuid4
from ubackup.cli import main


class CliTest(unittest.TestCase):

    @mock.patch('sys.exit')
    @mock.patch('requests.request')
    @mock.patch('ubackup.log.set_config')
    @mock.patch('ubackup.log.set_level')
    def test_cli(self, *args, **kwargs):
        temp_dir = uuid4().hex
        os.mkdir(temp_dir)
        temp_dir = os.path.abspath(temp_dir)

        with open(os.path.join(temp_dir, 'foo'), 'w') as fp:
            fp.write('bar')

        sys.argv = [
            None,
            '--remote=dropbox',
            'backup',
            'path',
            '--path=%s' % temp_dir]
        main()

        shutil.rmtree(temp_dir)
