import os
import shlex

from .. import B5_PATH
from . import BaseModule


class LegacyModule(BaseModule):

    def is_installed(self):
        return True  # always return True, in order to skip install check

    def get_script(self):
        script = [super(LegacyModule, self).get_script()]
        script.append('LEGACY_MODULES_PATH=%s\n' % shlex.quote(os.path.join(B5_PATH, 'legacy', 'modules')))  # legacy
        script.append(open(os.path.join(B5_PATH, 'legacy', 'legacy.sh'), 'r').read())
        return '\n'.join(script)
