import os
import codecs
from setuptools import setup

__author__ = "Calgary Michael"
__contact__ = "cseth.michael@gmail.com"
__version__ = "0.0.1"

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='python-liquify',
    version=__version__,
    description='Python script that prepares class for JSON conversion',
    long_description=long_description,
    url='https://github.com/CalgaryMichael/liquify',
    author=__author__,
    author_email=__contact__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='json api',
    py_modules=["liquify.py"],
    extras_require={
        'test': ['mock'],
    }
)
