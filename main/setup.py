# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="supermarket labels",
    version="0.1.0",
    description="dummy description",
    author="dummy author",
    author_email="dummy@mail",
	package_data={"": ["darknet", "libdarknet.so"]},
	include_package_data=True,
    packages=find_packages(exclude=("gui/resources", 
									"gui/old", 
									"gui/static", 
									"gui/templates", 
									"backend/model/config", 
									"backend/model/output", 
									"backend/input_images")),
)
