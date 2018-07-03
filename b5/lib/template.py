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
    tags = ('modulefunction', 'modulecallback',)

    @classmethod
    def factory(cls, module):
        class _ModuleRenderExtension(cls):
            module = module
        return _ModuleRenderExtension

    def parse(self, parser):
        tag = parser.stream.current.value

        if tag == 'modulefunction':
            return self._parse_modulefunction(parser)
        elif tag == 'modulecallback':
            return self._parse_modulecallback(parser)
        else:
            raise RuntimeError('Should not happen')

    def _parse_modulefunction(self, parser):
        '''
        Example:
        {% modulefunction 'install' %}
            some_command some_params
        {% endmodulefunction %}

        will return

        MODULENAME:install() {
            some_command some_params
        }

        :param parser:
        :return:
        '''
        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        body = parser.parse_statements(['name:endmodulefunction'], drop_needle=True)
        return nodes.CallBlock(self.call_method('_call_modulefunction', args),
                               [], [], body).set_lineno(lineno)

    def _call_modulefunction(self, name, caller):
        body = caller()
        return '''{module}:{name}() {
{body}
}'''.format(
            module=self.module.name,
            name=name,
            body=body,

        )

    def _parse_modulecallback(self, parser):
        '''
        Example:
        {% modulecallback 'install' %}

        will return

        MODULENAME:install() {
            b5-execute --state-file … --module MODULENAME --method install --args "$@"
        }

        AND

        {% modulecallback 'install' 'callback' %}

        will return

        MODULENAME:install() {
            b5-execute --state-file … --module MODULENAME --method callback --args "$@"
        }

        :param parser:
        :return:
        '''
        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        if parser.stream.skip_if('comma'):
            args.append(nodes.Const(None))
        else:
            args.append(parser.parse_expression())
        return nodes.CallBlock(self.call_method('_call_modulecallback', args)).set_lineno(lineno)

    def _call_modulecallback(self, name, method, caller):
        return '''{module}:{name}() {
    b5-execute --state-file {state_file} --module {module} --method {method} --args "$@"
}'''.format(
            module=self.module.name,
            state_file=self.module.state.stored_name,
            name=name,
            method=method if method else name,
        )
