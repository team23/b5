import datetime
import os
import sys
from typing import List

import jinja2
import termcolor

from b5 import VERSION

from ..lib.argumentparser import TemplateArgumentParser
from ..lib.state import State
from . import BaseModule


class TemplateModule(BaseModule):
    def execute_render(self, state: State, sys_args: List[str]) -> None:  # noqa: C901
        parser = TemplateArgumentParser('{name}:render'.format(name=self.name))
        parser.add_arguments()
        args = parser.parse(sys_args)

        template_file = os.path.realpath(os.path.join(state.run_path, args.template_file))
        output_file = None
        if args.output_file:
            output_file = os.path.realpath(os.path.join(state.run_path, args.output_file))
        overwrite = args.overwrite

        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader([state.run_path]),
            autoescape=jinja2.select_autoescape(),
            keep_trailing_newline=True,
        )
        try:
            template = env.get_template(args.template_file)
        except jinja2.TemplateNotFound:
            termcolor.cprint('Template file could not be found (%s)' % args.template_file, color='red')
            sys.exit(1)

        if output_file:
            output_path = os.path.dirname(output_file)
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            if os.path.exists(output_file):
                if overwrite == 'no':
                    return
                if overwrite in ('if-older', 'ask-if-older'):
                    template_file_stat = os.stat(template_file)
                    output_file_stat = os.stat(output_file)
                    if template_file_stat.st_mtime < output_file_stat.st_mtime:
                        return
                if overwrite in ('ask', 'ask-if-older'):
                    yesno = None
                    while yesno not in ('y', 'n', 'yes', 'no'):
                        if yesno is not None:
                            termcolor.cprint('Invalid input: %s' % yesno, color='yellow')
                        if overwrite == 'ask-if-older':
                            yesno = input('Template output file (%s) already exists, '
                                          'but is older than template, overwrite? [Yn] ' % args.output_file)
                            if yesno == '':
                                yesno = 'y'
                        else:
                            yesno = input('Template output file (%s) already exists, '
                                          'overwrite? [yN] ' % args.output_file)
                            if yesno == '':
                                yesno = 'n'
                        yesno = yesno.lower()
                    if yesno in ('n', 'no'):
                        return

        try:
            rendered = template.render(
                env=dict(os.environ),  # convert type to plain dict
                state=state,
                config=state.config,
                module=self,
                # Add some meta information about template rendering
                meta={
                    'version': VERSION,
                    'now': datetime.datetime.now().isoformat(),
                    'template_file': template_file,
                    'output_file': output_file if output_file else '-',
                },
            )
        except jinja2.UndefinedError as error:
            termcolor.cprint('Template could not be rendered (%s), error message' % args.template_file, color='red')
            termcolor.cprint(error.message, color='yellow')
            sys.exit(1)

        if output_file:
            try:
                with open(output_file, 'w') as file_handle:
                    file_handle.write(rendered)
            except IOError as error:
                termcolor.cprint('Template output could not be saved (%s)' % args.output_file, color='red')
                termcolor.cprint(str(error), color='yellow')
                sys.exit(1)
        else:
            print(rendered)
    execute_render.task_executable = True

    def get_script(self) -> str:
        script = [super(TemplateModule, self).get_script()]

        script.append(self._script_config_vars())

        script.append(self._script_function_call('render'))

        return '\n'.join(script)
