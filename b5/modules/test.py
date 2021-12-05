from typing import List

from ..lib.state import State
from . import BaseModule


class TestModule(BaseModule):
    def execute_test(self, state: State, args: List[str]) -> None:
        print('Hello from python called via the Taskfile')
        print(args)
    execute_test.task_executable = True

    def get_script(self) -> str:
        script = [super(TestModule, self).get_script()]
        script.append(self._script_function_call('test'))
        return '\n'.join(script)
