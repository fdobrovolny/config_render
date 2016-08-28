import unittest

import six

from config_render import config, exceptions

if six.PY2:
    import mock
else:
    from unittest import mock


class TestConfiguration(unittest.TestCase):
    @mock.patch.object(config.Configuration, "parse")
    def test___init___configuration_dictionary(self, mock_parse):
        """Test passing configuration_dictionary to __init__."""
        mock_dict = mock.MagicMock()
        config.Configuration("Foo", mock_dict)
        mock_parse.assert_called_once_with(mock_dict)

    def test___init__(self):
        """Test __init__ method."""
        conf = config.Configuration("Foo")

        self.assertEqual(conf.name, "Foo")
        self.assertEqual(conf.env_variables, {})
        self.assertEqual(conf.variables, {})

    def test_set_if_exists_not_exits(self):
        """Test test_set_if_exists with non existing value."""
        conf = config.Configuration("Foo")
        self.assertEqual(conf.template_path, None)

        conf.set_if_exists({}, "template_path")

        self.assertEqual(conf.template_path, None)

    def test_set_if_exists_exits(self):
        """Test test_set_if_exists with existing value."""
        some_obj = mock.MagicMock()
        conf = config.Configuration("Foo")
        self.assertEqual(conf.template_path, None)

        conf.set_if_exists({"template_path": some_obj}, "template_path")

        self.assertEqual(conf.template_path, some_obj)

    @mock.patch.object(config.Configuration, "set_if_exists")
    def test_parse(self, set_if_exists_mock):
        """Test parse"""
        some_dict = mock.MagicMock()
        conf = config.Configuration("Foo")

        conf.parse(some_dict)

        calls = [
            mock.call(some_dict, "template_path"),
            mock.call(some_dict, "template_path_var"),
            mock.call(some_dict, "output_file_path"),
            mock.call(some_dict, "output_file_path_var"),
            mock.call(some_dict, "env_variables"),
            mock.call(some_dict, "variables"),
        ]
        set_if_exists_mock.assert_has_calls(calls, any_order=True)

    def test_get_context_var_only(self):
        """Test get_context with variables only."""
        conf = config.Configuration("Foo")
        conf.variables = {"Foo": "Bar", "Foo2": "Bar2"}
        out = conf.get_context()
        self.assertDictEqual(conf.variables, out)

    def test_get_context_env_only(self):
        """Test get_context with env variables only."""
        conf = config.Configuration("Foo")
        conf.env_variables = {"Alpha": "ENV_VAR"}
        with mock.patch.dict('os.environ', {"ENV_VAR": "Bar"}):
            out = conf.get_context()
        self.assertDictEqual({"Alpha": "Bar"}, out)

    def test_get_context_env_only_empty(self):
        """Test get_context with env variables only, but os.environ empty."""
        conf = config.Configuration("Foo")
        conf.env_variables = {"Alpha": "ENV_VAR"}
        with mock.patch.dict('os.environ', {}):
            out = conf.get_context()
        self.assertDictEqual({"Alpha": None}, out)

    def test_get_context_env_empty(self):
        """Test get_context with env variables empty."""
        conf = config.Configuration("Foo")
        conf.variables = {"Alpha": "Bar"}
        conf.env_variables = {"Alpha": "ENV_VAR"}
        with mock.patch.dict('os.environ', {}):
            out = conf.get_context()
        self.assertDictEqual({"Alpha": "Bar"}, out)

    def test_get_context(self):
        """Test get_context with env variables only."""
        conf = config.Configuration("Foo")
        conf.variables = {"Alpha": "Foo", "Beta": "Boo"}
        conf.env_variables = {"Beta": "ENV_VAR"}
        with mock.patch.dict('os.environ', {"ENV_VAR": "Bar"}):
            out = conf.get_context()
        self.assertDictEqual({"Alpha": "Foo", "Beta": "Bar"}, out)

    def test_get_filename_param_only(self):
        """Test get_filename with param only."""
        conf = config.Configuration("Foo")
        self.assertEqual(conf.get_filename("Foo"), "Foo")

    def test_get_filename_param_path(self):
        """Test get_filename with param and path."""
        conf = config.Configuration("Foo")
        conf.output_file_path = "Bar"
        self.assertEqual(conf.get_filename("Foo"), "Foo")

    def test_get_filename_param_env(self):
        """Test get_filename with param and env."""
        conf = config.Configuration("Foo")
        conf.output_file_path_var = "ENV_VAR"
        with mock.patch.dict('os.environ', {"ENV_VAR": "Bar"}):
            self.assertEqual(conf.get_filename("Foo"), "Foo")

    def test_get_filename_param_env_path(self):
        """Test get_filename with param env, path."""
        conf = config.Configuration("Foo")
        conf.output_file_path = "Path"
        conf.output_file_path_var = "ENV_VAR"
        with mock.patch.dict('os.environ', {"ENV_VAR": "Bar"}):
            self.assertEqual(conf.get_filename("Foo"), "Foo")

    def test_get_filename_env(self):
        """Test get_filename with env only."""
        conf = config.Configuration("Foo")
        conf.output_file_path_var = "ENV_VAR"
        with mock.patch.dict('os.environ', {"ENV_VAR": "Bar"}):
            self.assertEqual(conf.get_filename(), "Bar")

    def test_get_filename_env_path(self):
        """Test get_filename with env and path."""
        conf = config.Configuration("Foo")
        conf.output_file_path = "Foo"
        conf.output_file_path_var = "ENV_VAR"
        with mock.patch.dict('os.environ', {"ENV_VAR": "Bar"}):
            self.assertEqual(conf.get_filename(), "Bar")

    def test_get_filename_path(self):
        """Test get_filename with path only."""
        conf = config.Configuration("Foo")
        conf.output_file_path = "Foo"
        self.assertEqual(conf.get_filename(), "Foo")

    def test_get_filename_empty(self):
        """Test get_filename with empty all."""
        conf = config.Configuration("Foo")
        with self.assertRaises(exceptions.OutputFileNotSpecifiedException):
            conf.get_filename()

    def test_get_filename_env_empty(self):
        """Test get_filename with empty env."""
        conf = config.Configuration("Foo")
        conf.output_file_path_var = "ENV_VAR"
        with mock.patch.dict('os.environ', {}):
            with self.assertRaises(exceptions.OutputFileNotSpecifiedException):
                conf.get_filename()

    def test_get_template_param_only(self):
        """Test get_template with param only."""
        conf = config.Configuration("Foo")
        self.assertEqual(conf.get_template("Foo"), "Foo")

    def test_get_template_param_path(self):
        """Test get_template with param and path."""
        conf = config.Configuration("Foo")
        conf.template_path = "Bar"
        self.assertEqual(conf.get_template("Foo"), "Foo")

    def test_get_template_param_env(self):
        """Test get_template with param and env."""
        conf = config.Configuration("Foo")
        conf.template_path_var = "ENV_VAR"
        with mock.patch.dict('os.environ', {"ENV_VAR": "Bar"}):
            self.assertEqual(conf.get_template("Foo"), "Foo")

    def test_get_template_param_env_path(self):
        """Test get_template with param env, path."""
        conf = config.Configuration("Foo")
        conf.template_path = "Path"
        conf.template_path_var = "ENV_VAR"
        with mock.patch.dict('os.environ', {"ENV_VAR": "Bar"}):
            self.assertEqual(conf.get_template("Foo"), "Foo")

    def test_get_template_env(self):
        """Test get_template with env only."""
        conf = config.Configuration("Foo")
        conf.template_path_var = "ENV_VAR"
        with mock.patch.dict('os.environ', {"ENV_VAR": "Bar"}):
            self.assertEqual(conf.get_template(), "Bar")

    def test_get_template_env_path(self):
        """Test get_template with env and path."""
        conf = config.Configuration("Foo")
        conf.template_path = "Foo"
        conf.template_path_var = "ENV_VAR"
        with mock.patch.dict('os.environ', {"ENV_VAR": "Bar"}):
            self.assertEqual(conf.get_template(), "Bar")

    def test_get_template_path(self):
        """Test get_template with path only."""
        conf = config.Configuration("Foo")
        conf.template_path = "Foo"
        self.assertEqual(conf.get_template(), "Foo")

    def test_get_template_empty(self):
        """Test get_template with empty all."""
        conf = config.Configuration("Foo")
        with self.assertRaises(exceptions.TemplateNameNotSpecifiedException):
            conf.get_template()

    def test_get_template_env_empty(self):
        """Test get_template with empty env."""
        conf = config.Configuration("Foo")
        conf.template_path_var = "ENV_VAR"
        with mock.patch.dict('os.environ', {}):
            with self.assertRaises(exceptions.TemplateNameNotSpecifiedException):
                conf.get_template()

    @mock.patch.object(config.Configuration, "get_template")
    @mock.patch.object(config.Configuration, "get_filename")
    @mock.patch.object(config.Configuration, "get_context")
    @mock.patch.object(config, "open", create=True)
    @mock.patch("config_render.config_render.ConfigRender", autospec=True)
    def test_write(self, crender_mock, file_mock, context_mock, filename_mock, template_mock):
        conf = config.Configuration("Foo")
        template_name = mock.MagicMock()
        output_file = mock.MagicMock()
        file_handle = file_mock.return_value.__enter__.return_value

        conf.write(crender_mock, template_name, output_file)

        filename_mock.assert_called_once_with(output_file)
        file_mock.assert_called_once_with(filename_mock.return_value, "w")
        template_mock.assert_called_once_with(template_name)
        self.assertEqual(context_mock.call_count, 1)
        crender_mock.write.assert_called_once_with(template_mock.return_value, file_handle,
                                                   context_mock.return_value)


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.conf = config.Config()
        self.mock_configuration1 = mock.MagicMock(spec=config.Configuration)
        self.mock_configuration1.name = "Foo"
        self.mock_configuration2 = mock.MagicMock(spec=config.Configuration)
        self.mock_configuration2.name = "Bar"
        self.mock_configuration_default = mock.MagicMock(spec=config.Configuration)
        self.mock_configuration_default.name = "default"

    def test_register_configuration(self):
        """Test register_configuration()"""
        self.conf.register_configuration(self.mock_configuration1)
        self.assertIn("Foo", self.conf.configurations)
        self.assertEqual(self.conf.configurations["Foo"], self.mock_configuration1)
        self.assertNotIn("Bar", self.conf.configurations)

        self.conf.register_configuration(self.mock_configuration2)
        self.assertIn("Foo", self.conf.configurations)
        self.assertIn("Bar", self.conf.configurations)
        self.assertEqual(self.conf.configurations["Bar"], self.mock_configuration2)

    def test___getitem___NotFound(self):
        """Test getting with empty self.configurations."""
        with self.assertRaises(exceptions.ConfigurationNotFoundException):
            self.conf["Foo"]

    def test___getitem__(self):
        """Test getting an Item."""
        self.conf.register_configuration(self.mock_configuration1)
        self.assertEqual(self.conf["Foo"], self.mock_configuration1)

    def test___getitem__None_default(self):
        """Test getting default Item."""
        self.conf.register_configuration(self.mock_configuration_default)
        self.assertEqual(self.conf[None], self.mock_configuration_default)

    def test___getitem__None_onlyone(self):
        """Test getting the only Item."""
        self.conf.register_configuration(self.mock_configuration1)
        self.assertEqual(self.conf[None], self.mock_configuration1)

    def test___getitem___None_NotFound(self):
        """Test getting with empty self.configurations."""
        with self.assertRaises(exceptions.ConfigurationNotFoundException):
            self.conf[None]

    def test___init__(self):
        """Test _init__"""
        self.assertEqual(self.conf.configurations, {})


class TestParse(unittest.TestCase):

    @mock.patch.object(config, "file", create=True)
    def test___init__(self, file_mock):
        """Test __init__ and file handling."""
        file_mock = mock.MagicMock()
        p = config.Parser(file=file_mock)
        self.assertEqual(file_mock, p.file)

    @mock.patch.object(config, "Configuration", create=True)
    @mock.patch.object(config.Config, "register_configuration", create=True)
    @mock.patch.object(config, "file", create=True)
    @mock.patch.object(config.yaml, "load", create=True)
    def test_parse(self, yaml_load_mock, file_mock, register_configuration_mock,
                   configuration_mock):
        """Test parse method."""
        yaml_load_mock.return_value = {"Foo": "bar", "Foo2": "bar2"}
        p = config.Parser(file=file_mock)
        p.parse()

        yaml_load_mock.assert_called_once_with(file_mock.read.return_value)
        self.assertEqual(register_configuration_mock.call_count, 2)
        configuration_mock.assert_has_calls([mock.call("Foo", "bar"), mock.call("Foo2", "bar2")],
                                            any_order=True)
