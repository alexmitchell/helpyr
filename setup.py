#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="helpyr",
    version="0.0.1",
    author="Alex Mitchell",
    author_email="ebpvyeuj@gmail.com",
    description="Helpful miscellaneous python functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexmitchell/helpyr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
