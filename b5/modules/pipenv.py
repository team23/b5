import shlex
import os

from . import TemplateBaseModule


class PipenvModule(TemplateBaseModule):
    '''Pipenv module
    '''

    TEMPLATE_NAME = 'pipenv.sh.jinja2'
    DEFAULT_CONFIG = {
        'base_path': '.',
        'pipenv_bin': 'pipenv',
        'pyenv_bin': 'pyenv',
        'use_pyenv': True,
        'install_dev': True,
        'store_venv_in_project': True,  # Sets PIPENV_VENV_IN_PROJECT to 1
        'pipfile': 'Pipfile',  # Sets PIPENV_PIPFILE
    }

    def prepare_config(self):
        self.config['base_path'] = os.path.realpath(os.path.join(
            self.state.run_path,
            self.config['base_path'],
        ))

    #def _pipenv_environment(self):
    #    return '''
    #        {pyenv_init}
    #        export PIPENV_VENV_IN_PROJECT="{store_venv_in_project}"
    #        export PIPENV_PIPFILE={pipfile}
    #    '''.format(
    #        pyenv_init='eval "$( {pyenv_bin} init - )"'.format(pyenv_bin=shlex.quote(self.config['pyenv_bin'])) \
    #                    if self.config['use_pyenv'] else '',
    #        store_venv_in_project='1' if self.config['store_venv_in_project'] else '',
    #        pipfile=shlex.quote(self.config['pipfile']),
    #    )
