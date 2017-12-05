from . import BaseModule


class TestModule(BaseModule):
    def test(self, state, args):
        print('Hello from python called via the Taskfile')
        print(args)

        from pprint import pprint
        pprint(vars(state))
    test.task_executable = True

    def get_script(self):
        script = [super(TestModule, self).get_script()]
        script.append(self._script_function_call('test'))
        return '\n'.join(script)
