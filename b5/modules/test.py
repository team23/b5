from . import BaseModule


class TestModule(BaseModule):
    def test(self, args):
        print('Hello from python called via the Taskfile')
        print(args)
    test.task_executable = True

    def get_script(self):
        script = super(TestModule, self).get_script()
        script += self._script_function_call('test')
        return script
