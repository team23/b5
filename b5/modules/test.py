from . import BaseModule


class TestModule(BaseModule):
    def execute_test(self, state, args):
        print('Hello from python called via the Taskfile')
        print(args)
    execute_test.task_executable = True

    def is_installed(self):
        return True  # always return True, in order to skip install check

    def get_script(self):
        script = [super(TestModule, self).get_script()]
        script.append(self._script_function_call('test'))
        return '\n'.join(script)
