import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "zeppelin_comm_layer",
    version = "0.9.3",
    author = "Bernhard Walter",
    author_email = "bwalter@gmail.com",
    description = ("A simulation of the Jupyter/IPython display/communication system "
                   "to allow libraries like Bokeh to run inline in Apache Zeppelin"),
    license = "Apache License 2.0",
    keywords = "zeppelin visualisations",
    packages=['zeppelin_comm_layer'],
    package_data={'zeppelin_comm_layer': ['js/*']},
    long_description=read('Readme.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Programming Language :: Python'",
        "Programming Language :: Python :: 2'",
        "Programming Language :: Python :: 3'"
    ]
)