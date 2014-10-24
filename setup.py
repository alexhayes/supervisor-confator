from codecs import open
from os import path
import os

from setuptools import setup, find_packages


ROOT = path.abspath(path.dirname(__file__))

with open(os.path.join(ROOT, 'VERSION'), encoding='utf-8') as f:
    VERSION = f.read().strip()

setup(
    name = 'supervisor-confator',
    packages = ['supervisor_confator'],
    license='MIT',
    version = VERSION,
    description = 'Python interface to generate supervisor configuration files.',
    author = 'Alex Hayes',
    author_email = 'alex@alution.com',
    url = 'https://github.com/alexhayes/supervisor-confator',
    download_url = 'https://github.com/alexhayes/supervisor-confator/tarball/%s' % VERSION,
    keywords = ['supervisor', 'config', 'generator', 'server management'],
   
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
         
        # Indicate who your project is intended for
        'Intended Audience :: System Administrators',
        'Topic :: System :: Installation/Setup',
         
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
         
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],
)