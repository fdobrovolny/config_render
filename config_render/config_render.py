from __future__ import unicode_literals

from os.path import exists, expandvars, getmtime

from jinja2 import BaseLoader, Environment, TemplateNotFound


class FileTemplateLoader(BaseLoader):
    """Load template from specified path."""

    def get_source(self, environment, template):
                if not exists(template):
                    raise TemplateNotFound(template)
                mtime = getmtime(template)
                with file(expandvars(template)) as f:
                    source = f.read().decode('utf-8')
                return source, template, lambda: mtime == getmtime(template)


class ConfigRender(object):
    """Class to interact with Jinja2."""
    def __init__(self, context={}, loader=FileTemplateLoader(), environment_args=[],
                 environment_kwargs={}):
        """
        Initialize ConfigRender.

        :param context: Variables to be passed into template
        :type context: Dict
        :param loader: Jinja2 Loader
        :type loader: jinja2.BaseLoader
        :param environment_args: Args to be passed to Enviroment
        :type environment_args: list
        :param environment_kwargs: Kwargs to be passed to Enviroment
        :param environment_kwargs: Dict
        """
        self.context = context
        self.environment = Environment(*environment_args, loader=loader, **environment_kwargs)

    def write(self, template_name, file, context={}):
        """
        Render and write template to file

        :param template_name: Name of the Template
        :type template_name: String
        :param file: File object to write it into it
        :type file: file
        :param context: Dictionary by which content will be updated local copy of
        ConfigRender context
        :type context: Dict
        """
        final_context = dict(self.context)
        final_context.update(context)
        template = self.environment.get_template(template_name)
        file.write(template.render(**final_context))
