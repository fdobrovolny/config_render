Config Render
=============

Render your config files automaticly with Jinja2!!

Homepage
--------

Visit the home of 'config_render' on the web:
[github.com/BrnoPCmaniak/config_render](https://github.com/BrnoPCmaniak/config_render)

Documentation
-------------

Usage:
$ config_render --help
usage: config_render [-h] [-v] [-ch] [-n config_name] [-t template] [-o FILE]
                     config

Render your files with Jinja2 templates.

positional arguments:
  config                YAML config file

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -ch, --config-help    show config file help and exit
  -n config_name, --name config_name
                        Name of configuration to be used.
  -t template, --template_name template
                        Template file
  -o FILE, --output_file FILE
                        Output File

Copyright (C) 2016 Filip Dobrovolny


Config File Explained:
# Default Configuration
default:
  # Path to template
  # This is can be override by -t option
  template_path: foo.template
  # Enviroment template varible
  # if specified we first try to use it if not we fallback to template_path
  template_path_var: SOME_TEMPLATE_PATH
  # This is can be override by -o option
  output_file_path: foo.cfg
  # if specified we first try to use if not we fallback to output_file_path
  output_file_path_var: SOME_OUTPUT_PATH
  # Load varibles from system environment
  # env_variables are superior to varibles
  env_variables:
    ip_adress: DJANGO_IP_ADDR
    hostname: DJANGO_HOSTNAME
    db_hostname: DB_HOSTNAME
  variables:
    debug: off
    server_https: "on" # Non boolean value
    db_type: postgresql
    ip_adress: 127.0.0.1 # fallback if DAJNGO_IP_ADDR does not exist
mysql:
  template_path: mysql.template
  output_file: $HOME/mysql_dir
  variables:
    user: django
    password: django
    ip_adress: 127.0.0.1


Warning:
-------------
* Numbers are automaticly convered to ints.
* '~' or 'null' is converted to None
* 'false', 'true', 'on', 'off' are converted to boolean.
* If you want to use one of these put them inside '' or ""
* Inline comments are denoted with ' #' (space then #).

Quick start Jinja2 templates:
[server]
ip_adress="{{ ip_adress }}"
user="{{ django }}"
password="{{ password }}"

For more info follow jinja2 Templates Manual (http://jinja.pocoo.org/docs/dev/templates/).
