import datetime
import os
import sys

import jinja2
import termcolor

from b5 import VERSION

from ..lib.argumentparser import TemplateArgumentParser
from ..lib.state import State
from . import BaseModule


class TemplateModule(BaseModule):
    def execute_render(self, state: State, sys_args: list[str]) -> None:
        parser = TemplateArgumentParser(f'{self.name}:render')
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
            termcolor.cprint(f'Template file could not be found ({args.template_file})', color='red')
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
                            termcolor.cprint(f'Invalid input: {yesno}', color='yellow')
                        if overwrite == 'ask-if-older':
                            yesno = input(f'Template output file ({args.output_file}) already exists, '
                                          f'but is older than template, overwrite? [Yn] ')
                            if yesno == '':
                                yesno = 'y'
                        else:
                            yesno = input(f'Template output file ({args.output_file}) already exists, '
                                          f'overwrite? [yN] ')
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
            termcolor.cprint(
                f'Template could not be rendered ({args.template_file}), error message',
                color='red',
            )
            termcolor.cprint(error.message, color='yellow')
            sys.exit(1)

        if output_file:
            try:
                with open(output_file, 'w') as file_handle:
                    file_handle.write(rendered)
            except OSError as error:
                termcolor.cprint(f'Template output could not be saved ({args.output_file})', color='red')
                termcolor.cprint(str(error), color='yellow')
                sys.exit(1)
        else:
            print(rendered)  # noqa: T201
    execute_render.task_executable = True

    def get_script(self) -> str:
        script = [super().get_script()]

        script.append(self._script_config_vars())

        script.append(self._script_function_call('render'))

        return '\n'.join(script)
