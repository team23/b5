import os

from . import TemplateBaseModule


class ComposerModule(TemplateBaseModule):
    '''Composer module
    '''

    TEMPLATE_NAME = 'composer.sh.jinja2'
    DEFAULT_CONFIG = {
        'base_path': '.',
        'composer_bin': 'composer',
        'vendor_path': 'vendor',
    }

    def prepare_config(self):
        self.config['base_path'] = os.path.realpath(os.path.join(
            self.state.run_path,
            self.config['base_path'],
        ))
        self.config['vendor_path'] = os.path.realpath(os.path.join(
            self.config['base_path'],
            self.config['vendor_path'],
        ))
