# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from mesos_demo import __version__

requirements = [
    "argh",
    "coloredlogs",
]

setup(
    name="mesos_demo",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
)
