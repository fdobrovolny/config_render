# -*- coding: utf-8 -*-

'''
Created on 13. 12. 2015

@author: Tomas Dobrovolny
'''

from setuptools import setup
from NAME import __version__
import os
import io

HERE = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

setup(
    name='NAME',
    version=__version__,
    platforms=['OS Independent'],
    description='Filter to convert whitespaces to &nbps; in django templates.',
    # long_description=read('README.txt', 'CHANGES.txt'),
    keywords='django filter whitespace nbsp',
    url='https://tomas.dobrovolny.eu/django-nbsp-filter',
    author='Tomas Dobrovolny',
    author_email='sdobrtomas@gmail.com',
    license='MIT',
    maintainer='Tomas Dobrovolny',
    maintainer_email='sdobrtomas@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=['NAME'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django',
    ],
)
