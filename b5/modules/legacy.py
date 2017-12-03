import os

from .. import B5_PATH
from . import BaseModule


class LegacyModule(BaseModule):
    def get_script(self):
        script = [super(LegacyModule, self).get_script()]
        script.append(open(os.path.join(B5_PATH, 'legacy', 'legacy.sh'), 'r').read())
        return '\n'.join(script)
