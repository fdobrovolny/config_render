git flow release start v$1
sed -i -e "s/__version__ = '.*'/__version__ = '$1'/g" config_render/__init__.py
git commit config_render/__init__.py -m "Update to version v$1"
git flow release finish v$1
