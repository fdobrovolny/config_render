from __future__ import unicode_literals

import os

import yaml

from .exceptions import (ConfigurationNotFoundException, OutputFileNotSpecifiedException,
                         TemplateNameNotSpecifiedException)


class Configuration(object):
    template_path = None
    template_path_var = None
    output_file_path = None
    output_file_path_var = None
    env_variables = {}
    variables = {}

    def __init__(self, name, configuration_dictionary=None):
        self.name = name
        if configuration_dictionary:
            self.parse(configuration_dictionary)

    def parse(self, configuration_dictionary):
        """Transform configuration_dictionary into Configuration varibles."""
        self.set_if_exists(configuration_dictionary, "template_path")
        self.set_if_exists(configuration_dictionary, "template_path_var")
        self.set_if_exists(configuration_dictionary, "output_file_path")
        self.set_if_exists(configuration_dictionary, "output_file_path_var")
        self.set_if_exists(configuration_dictionary, "env_variables")
        self.set_if_exists(configuration_dictionary, "variables")

    def set_if_exists(self, dict, name):
        """If name exists in dict than set self.<name> to provided value."""
        setattr(self, name, dict.get(name, getattr(self, name)))

    def get_context(self):
        """Return context dictionary for Jinja2."""
        out = {}
        out.update(self.variables)

        for key, value in self.env_variables.items():
            # Try to look for env var `key` if not found try to look for `key` in `variables`
            # If it is not even there set variable as None
            out[key] = os.environ.get(value, self.variables.get(key, None))
        return out

    def get_filename(self, output_file=None):
        """Get filename or OutputFileNotSpecified"""
        filename = output_file or os.environ.get(self.output_file_path_var, self.output_file_path)
        if filename is None:
            raise OutputFileNotSpecifiedException()
        return filename

    def get_template(self, template_name=None):
        """Get template or TemplateNameNotSpecified"""
        template = template_name or os.environ.get(self.template_path_var, self.template_path)
        if template is None:
            raise TemplateNameNotSpecifiedException()
        return template

    def write(self, config_render, template_name=None, output_file=None):
        """Call config_render.write() with parameters."""
        with open(self.get_filename(output_file), "w") as f:
            config_render.write(self.get_template(template_name), f, self.get_context())


class Config(object):
    configurations = {}

    def __getitem__(self, name):
        """Get configuration from config."""
        try:
            return self.configurations.get(name)
        except KeyError:
            raise ConfigurationNotFoundException(name)

    def register_configuration(self, configuration):
        """Register configuration in config."""
        self.configurations[configuration.name] = configuration


class Parser(object):
    yaml_dict = None

    def __init__(self, file):
        """Initialize Parser.

        :param file: file which should be parsed
        :type file: file
        """
        self.file = file

    def parse(self):
        """Parse File.

        :return: Config instance.
        :rtype: Config
        """
        self.yaml_dict = yaml.load(self.file.read())
        config = Config()
        for name, value in self.yaml_dict.items():
            config.register_configuration(Configuration(name, value))
        return config
