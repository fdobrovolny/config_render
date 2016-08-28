import unittest

from jinja2 import TemplateNotFound

from config_render import config_render
from config_render.config_render import FileTemplateLoader

import six

if six.PY2:
    import mock
else:
    from unittest import mock


class TestFileTemplateLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loader = FileTemplateLoader()

    @mock.patch.object(config_render, "exists", autospec=True)
    def test_get_source_not_exists(self, exists_mock):
        """Test raising Template not found exception when file does not exists."""
        exists_mock.return_value = False
        with self.assertRaises(TemplateNotFound):
            self.loader.get_source(None, "some_template")

        exists_mock.assert_called_once_with("some_template")

    @mock.patch.object(config_render, "file", create=True)
    @mock.patch("config_render.config_render.getmtime", autospec=True)
    @mock.patch("config_render.config_render.exists", autospec=True)
    def test_get_source(self, exists_mock, getmtime_mock, file_mock):
        exists_mock.return_value = True
        getmtime_mock.return_value = 0.0
        file_handle = file_mock.return_value.__enter__.return_value
        file_handle.read.return_value = "Foo template"

        out = self.loader.get_source(None, "some_template")

        file_handle.read.assert_called_once()
        file_mock.assert_called_once_with("some_template")
        self.assertEqual("Foo template", out[0])
        self.assertEqual("some_template", out[1])


class TestConfigRender(unittest.TestCase):

    @mock.patch("config_render.config_render.FileTemplateLoader", create=True)
    @mock.patch.object(config_render, "Environment", create=True)
    def test___init__(self, env_mock, floader_mock):
        """Test __init__."""
        context = {"Test": "foo"}
        kwargs = {"arg1": "foo"}
        cr = config_render.ConfigRender(context=context, environment_args=[None],
                                        loader=floader_mock, environment_kwargs=kwargs)

        self.assertEqual(cr.context, context)
        env_mock.assert_called_once_with(None, loader=floader_mock, **kwargs)

    @mock.patch.object(config_render, "file", create=True)
    @mock.patch.object(config_render.Environment, "get_template", create=True)
    def test_write(self, get_template_mock, file_mock):
        context = {"Test": "foo", "Test2": "foo2"}
        cr = config_render.ConfigRender(context=context)

        cr.write("some_template", file_mock, {"Test": "bar", "Test3": "foo"})
        get_template_mock.assert_called_once_with("some_template")
        get_template_mock.return_value.render.assert_called_once_with(Test='bar', Test2='foo2',
                                                                      Test3='foo')
