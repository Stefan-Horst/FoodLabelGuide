# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="supermarket-label-detector",
    version="1.0",
    description="Web app built on YOLOv4-tiny object detection model to detect labels on food products and show information for them",
    author="AISSCV Group6",
    author_email="group6@aisscv",
	package_data={"": ["libdarknet.so"]},
	include_package_data=True,
    packages=find_packages(exclude=("frontend/resources", 
									"frontend/old", 
									"frontend/image/static", 
                                    "frontend/image/static", 
									"frontend/video/templates", 
                                    "frontend/video/templates", 
									"backend/model/data", 
									"backend/model/output", 
									"backend/input_images")),
)
