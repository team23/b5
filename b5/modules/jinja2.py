import argparse
import os
import sys
import termcolor
import jinja2

from . import BaseModule


class Jinja2Module(BaseModule):
    def execute_render(self, state, sys_args):
        parser = argparse.ArgumentParser(
            prog='{name}:render'.format(name=self.name),
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        # parser.add_argument(
        #     '-o', '--output-file', nargs='?',
        #     help='Output file name',
        #     dest='output_file',
        # )
        parser.add_argument('template_file')
        parser.add_argument('output_file', nargs='?')
        args = parser.parse_args(args=sys_args)

        template_file = os.path.realpath(os.path.join(state.run_path, args.template_file))
        output_file = None
        if args.output_file:
            output_file = os.path.realpath(os.path.join(state.run_path, args.output_file))

        if output_file:
            output_path = os.path.dirname(output_file)
            if not os.path.exists(output_path):
                os.makedirs(output_path)

        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader([state.run_path]),
            autoescape=jinja2.select_autoescape(),
        )
        try:
            template = env.get_template(args.template_file)
        except jinja2.TemplateNotFound:
            termcolor.cprint('Template file could not be found (%s)' % args.template_file, color='red')
            sys.exit(1)

        try:
            rendered = template.render(
                state=state,
                config=state.config,
                module=self,
            )
        except jinja2.UndefinedError as e:
            termcolor.cprint('Template could not be rendered (%s), error message' % args.template_file, color='red')
            termcolor.cprint(e.message, color='yellow')
            sys.exit(1)

        if output_file:
            try:
                with open(output_file, 'w') as fh:
                    fh.write(rendered)
            except IOError as e:
                termcolor.cprint('Template output could not be saved (%s)' % args.output_file, color='red')
                termcolor.cprint(e.message, color='yellow')
                sys.exit(1)
        else:
            print(rendered)
    execute_render.task_executable = True

    def get_script(self):
        script = [super(Jinja2Module, self).get_script()]

        script.append(self._script_config_vars())

        script.append(self._script_function_call('render'))

        return '\n'.join(script)
