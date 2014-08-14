
class Bucket(object):
    def __init__(self):
        pass

    def push(self, stream, name, versioning=False):
        raise NotImplementedError

    def pull(self, name):
        raise NotImplementedError

    def exists(self, name):
        raise NotImplementedError
