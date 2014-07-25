from ubackup import settings
from subprocess import Popen, PIPE
import math
import os
import imp


def filesizeformat(bytes, precision=2):
    """Returns a humanized string for a given amount of bytes"""
    bytes = int(bytes)
    if bytes is 0:
        return '0B'
    log = math.floor(math.log(bytes, 1024))
    return "%.*f%s" % (
        precision,
        bytes / math.pow(1024, log),
        ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        [int(log)]
    )


def stream_shell(cmd, cwd=None, stdin=None):
    with open(os.devnull, 'w') as devnull:
        params = {
            'args': [cmd],
            'stdout': PIPE,
            'stderr': devnull,
            'shell': True,
            'bufsize': 1
        }

        if cwd is not None:
            params['cwd'] = cwd
        if stdin is not None:
            params['stdin'] = stdin

        process = Popen(**params)

    return process.stdout


def gzip_stream(stream):
    return stream_shell(
        cmd='gzip -fc9',
        stdin=stream)


def md5_stream(stream):
    return stream_shell(
        cmd='md5',
        stdin=stream).read().rstrip()


def merge_settings(settings_path=None):
    import ubackup
    try:
        import ubackup.user_settings
    except ImportError:
        # Load user settings and override app settings
        if settings_path is None:
            settings_path = os.environ.get('SETTINGS_PATH', settings.DEFAULT_SETTINGS_PATH)

        if settings_path is not None and os.path.exists(settings_path):
            ubackup.user_settings = imp.load_source('ubackup.user_settings', settings_path)
            for key, value in ubackup.user_settings.__dict__.items():
                if not key.startswith('_'):
                    setattr(settings, key, value)
