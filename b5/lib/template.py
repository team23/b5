import jinja2


# some local imports for more easy usage
from jinja2 import nodes
from jinja2.ext import Extension

TemplateNotFound = jinja2.TemplateNotFound
TemplateRuntimeError = jinja2.TemplateRuntimeError


class TemplateRenderer(object):
    def __init__(self, template_path, extensions=()):
        if not isinstance(template_path, (list, set)):
            template_path = [template_path]
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_path),
            autoescape=jinja2.select_autoescape(),
            extensions=extensions,
        )

    def load(self, template_file):
        return self.env.get_template(template_file)

    def render(self, template_file, context=None):
        if context is None:
            context = {}
        template = self.load(template_file)
        return template.render(context)

    def add_extension(self, extension):
        return self.env.add_extension(extension)


class ModuleRenderExtension(Extension):
    module = None
    tags = ('modulecallback',)

    @classmethod
    def factory(cls, _module):
        class _ModuleRenderExtension(cls):
            module = _module
        return _ModuleRenderExtension

    def parse(self, parser):
        tag = parser.stream.current.value

        if tag == 'modulecallback':
            return self._parse_modulecallback(parser)
        else:
            raise RuntimeError('Should not happen')  # just to be sure

    def _parse_modulecallback(self, parser):
        '''
        Example:
        {% modulecallback 'install' %}

        will return

        b5-execute --state-file … --module MODULENAME --method execute_install --args "$@"

        :param parser:
        :return:
        '''
        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        return nodes.CallBlock(self.call_method('_call_modulecallback', args), [], [], []).set_lineno(lineno)

    def _call_modulecallback(self, method, caller):
        return 'b5-execute --state-file "{state_file}" --module "{module}" --method "execute_{method}" --args "$@"'.format(
            module=self.module.name,
            state_file=self.module.state.stored_name,
            method=method,
        )
