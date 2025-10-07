import os
import tempfile
from types import TracebackType
from typing import Any, BinaryIO, ClassVar, TextIO

import yaml


class StoredState:
    def __init__(self, state: "State") -> None:
        self.state = state
        if self.state.stored_name is not None:
            raise RuntimeError('You may only store the state once')

        self.file_handle = tempfile.NamedTemporaryFile(suffix='b5-state', mode='w', encoding='utf-8', delete=False)
        self.state.stored_name = self.name
        yaml.dump({
            key: getattr(self.state, key)
            for key in state.KEYS
        }, self.file_handle, default_flow_style=False)
        self.file_handle.close()

    def close(self) -> None:
        os.unlink(self.file_handle.name)
        self.state.stored_name = None

    def __enter__(self) -> "StoredState":
        return self

    def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc: BaseException | None,
            traceback: TracebackType | None,
    ) -> None:
        self.close()

    @property
    def name(self) -> str:
        return self.file_handle.name


class State:
    KEYS: ClassVar = ('project_path', 'run_path', 'taskfiles', 'configfiles', 'config', 'args', 'stored_name')
    DEFAULTS: ClassVar = {"taskfiles": list, "configfiles": list, "args": dict}

    taskfiles: list
    configfiles: list
    args: dict

    def __init__(self, **kwargs: Any) -> None:
        for key in self.KEYS:
            if not hasattr(self, key):
                default = self.DEFAULTS.get(key, None)
                if callable(default):
                    default = default()
                setattr(self, key, default)
        for key in kwargs:
            if key not in self.KEYS:
                raise RuntimeError(f'Key {key} is not a valid state attribute')
            setattr(self, key, kwargs[key])

    def stored(self) -> StoredState:
        return StoredState(self)

    @classmethod
    def load(cls, file_handle: BinaryIO | TextIO) -> "State":
        return cls(**yaml.safe_load(file_handle))
