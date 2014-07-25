import unittest
import os
import shutil
from uuid import uuid4
from ubackup.manager import Manager
from ubackup.creator.path import PathCreator
from ubackup.utils import stream_shell


class ManagerTest(unittest.TestCase):

    def test_manager(self):
        temp_dir = uuid4().hex
        os.mkdir(temp_dir)
        temp_dir = os.path.abspath(temp_dir)

        with open(os.path.join(temp_dir, 'foo'), 'w') as fp:
            fp.write('bar')

        class TestRemote(object):

            def push(self, *args, **kwargs):
                pass

            def pull(self, *args, **kwargs):
                return stream_shell(cmd="echo 'foo'")

        manager = Manager(TestRemote())

        # Push backup
        creator = PathCreator(temp_dir)
        manager.push_backup(creator)

        # Already exists
        manager.push_backup(creator)

        # Restore backup
        manager.restore_backup(None)

        shutil.rmtree(temp_dir)
