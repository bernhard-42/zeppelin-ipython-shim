import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "jupytershim",
    version = "0.1.0",
    author = "Bernhard Walter",
    author_email = "bwalter@gmail.com",
    description = ("A shim of the Jupyter/IPython display/communication system "
                   "to allow libraries like Bokeh to run inline in Apache Zeppelin"),
    license = "Apache License 2.0",
    keywords = "zeppelin visualisations",
    packages=['jupytershim'],
    package_data={'jupytershim': ['js/*']},
    long_description=read('Readme.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Programming Language :: Python'",
        "Programming Language :: Python :: 3'"
    ]
)