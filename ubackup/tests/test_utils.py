import unittest
import hashlib
from ubackup.utils import filesizeformat, gzip_stream, md5_stream, stream_shell, crypt_stream, decrypt_stream


class UtilsTest(unittest.TestCase):

    def test_filesizeformat(self):
        size = filesizeformat(1024)
        self.assertEqual(size, '1.00KB')

        size = filesizeformat(0)
        self.assertEqual(size, '0B')

    def test_gzip_stream(self):
        gzip_stream(stream_shell(
            cmd='echo test')).read()

    def test_md5_stream(self):
        md5_hash = md5_stream(stream_shell(
            cmd='echo test'))

        m = hashlib.md5()
        m.update('test\n')
        self.assertEqual(m.hexdigest(), md5_hash)

    def test_stream_shell(self):
        stream = stream_shell(cmd='echo test')
        self.assertEqual(stream.read(), "test\n")

    def test_crypt(self):
        stream = stream_shell(cmd='echo test')
        crypted_stream = crypt_stream(stream, 'foo')
        decrypted_stream = decrypt_stream(crypted_stream, 'foo')
        self.assertEqual(decrypted_stream.read(), "test\n")
