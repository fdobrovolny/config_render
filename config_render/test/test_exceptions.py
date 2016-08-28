import unittest

from config_render.exceptions import ConfigRenderException, ConfigurationNotFoundException

import six

if six.PY2:
    import mock
else:
    from unittest import mock


class TestConfigRenderException(unittest.TestCase):
    def test___init__(self):
        """Test __init__ working properly with message."""
        class SomeException(ConfigRenderException):
            message = "foo"
        self.assertEqual("foo", SomeException().args[0])


class TestConfigurationNotFoundException(unittest.TestCase):
    def test___init__(self):
        """Test __init__ working properly with message formating."""
        e = ConfigurationNotFoundException("foo")
        self.assertEqual("Configuration 'foo' not found.", e.args[0])
