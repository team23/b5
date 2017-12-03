import pickle
import tempfile
import os


class StoredState(object):
    def __init__(self, state):
        self.state = state
        if not self.state.stored_name is None:
            raise RuntimeError('You may only store the state once')

        self.fh = tempfile.NamedTemporaryFile(suffix='b5-state', delete=False)
        pickle.dump({
            key: getattr(self.state, key)
            for key in state.KEYS
        }, self.fh)
        self.fh.close()
        self.state.stored_name = self.name

    def close(self):
        os.unlink(self.fh.name)
        self.state.stored_name = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def name(self):
        return self.fh.name


class State(object):
    KEYS = ('project_path', 'run_path', 'taskfiles', 'config', 'args', 'stored_name')

    def __init__(self, **kwargs):
        for key in self.KEYS:
            if not hasattr(self, key):
                setattr(self, key, None)
        for key in kwargs:
            if not key in self.KEYS:
                raise RuntimeError('Key %s is not a valid state attribute' % key)
            setattr(self, key, kwargs[key])

    def stored(self):
        return StoredState(self)

    @classmethod
    def load(cls, fh):
        return cls(**pickle.load(fh))
