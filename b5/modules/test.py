
from ..lib.state import State
from . import BaseModule


class TestModule(BaseModule):
    def execute_test(self, state: State, args: list[str]) -> None:  # noqa: ARG002
        print('Hello from python called via the Taskfile')  # noqa: T201
        print(args)  # noqa: T201
    execute_test.task_executable = True

    def get_script(self) -> str:
        script = [super().get_script()]
        script.append(self._script_function_call('test'))
        return '\n'.join(script)
