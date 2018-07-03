from . import TemplateBaseModule


class TestModule(TemplateBaseModule):
    TEMPLATE_NAME = 'test.sh.jinja2'

    def execute_test(self, state, args):
        print('Hello from python called via the Taskfile')
        print(args)
    execute_test.task_executable = True

    #def get_script(self):
    #    script = [super(TestModule, self).get_script()]
    #    script.append(self._script_function_call('test'))
    #    return '\n'.join(script)
