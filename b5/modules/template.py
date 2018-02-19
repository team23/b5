import argparse
import os
import sys
import termcolor
import jinja2

from . import BaseModule


class TemplateModule(BaseModule):
    def execute_render(self, state, sys_args):
        parser = argparse.ArgumentParser(
            prog='{name}:render'.format(name=self.name),
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            '-o', '--overwrite', nargs='?',
            help='Control if existing files should be overwritten',
            dest='overwrite', default='ask',
            choices=['yes', 'if-older', 'no', 'ask', 'ask-if-older']
        )
        parser.add_argument('template_file')
        parser.add_argument('output_file', nargs='?')
        args = parser.parse_args(args=sys_args)

        template_file = os.path.realpath(os.path.join(state.run_path, args.template_file))
        output_file = None
        if args.output_file:
            output_file = os.path.realpath(os.path.join(state.run_path, args.output_file))
        overwrite = args.overwrite

        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader([state.run_path]),
            autoescape=jinja2.select_autoescape(),
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
                            yesno = input('Template output file (%s) already exists, but is older than template, overwrite? [Yn] ' % args.output_file)
                            if yesno == '':
                                yesno = 'y'
                        else:
                            yesno = input('Template output file (%s) already exists, overwrite? [yN] ' % args.output_file)
                            if yesno == '':
                                yesno = 'n'
                        yesno = yesno.lower()
                    if yesno in ('n', 'no'):
                        return

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
        script = [super(TemplateModule, self).get_script()]

        script.append(self._script_config_vars())

        script.append(self._script_function_call('render'))

        return '\n'.join(script)
