import os

from . import TemplateBaseModule


class NpmModule(TemplateBaseModule):
    '''npm module
    '''

    TEMPLATE_NAME = 'npm.sh.jinja2'
    DEFAULT_CONFIG = {
        'base_path': '.',
        'npm_bin': 'npm',
    }

    def prepare_config(self):
        self.config['base_path'] = os.path.realpath(os.path.join(
            self.state.run_path,
            self.config['base_path'],
        ))
