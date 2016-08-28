class ConfigRenderException(Exception):
    message = None

    def __init__(self):
        super(ConfigRenderException, self).__init__(self.message)


class NotSpecifiedException(ConfigRenderException):
    pass


class TemplateNameNotSpecifiedException(NotSpecifiedException):
    message = ("template_name was not specified via argument or config or it's environment"
               "variable does not exist.")


class OutputFileNotSpecifiedException(NotSpecifiedException):
    message = ("output_file was not specified via argument or config or it's environment"
               "variable does not exist.")


class ConfigurationNotFoundException(ConfigRenderException):
    message_format = "Configuration '%s' not found."

    def __int__(self, configuration):
        self.message = self.message_format % configuration
        super(ConfigurationNotFoundException, self).__init__()
