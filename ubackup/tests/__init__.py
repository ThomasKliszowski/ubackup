from ubackup import settings, log
import mock


def setup(*args, **kwargs):
    log.set_config(settings.LOGGING)
    log.set_level('DEBUG')

    settings.CHUNK_SIZE = 100
    settings.CRYPT_KEY = "foo"
    settings.DROPBOX_TOKEN = "foo"

    class MockRequest(object):
        def json(*args, **kwargs):
            return {}

        @property
        def status_code(*args, **kwargs):
            return 200

    patcher = mock.patch('requests.request', return_value=MockRequest())
    patcher.start()
