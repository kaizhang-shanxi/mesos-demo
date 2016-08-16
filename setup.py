# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from mesos_demo import __version__

requirements = [
    "argh",
    "coloredlogs",
    "argcomplete",
    "protobuf",
]

setup(
    name="mesos-demo",
    version=__version__,
    entry_points={"console_scripts": ["mesos-demo = mesos_demo.demo:main"]},
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
)
