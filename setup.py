import setuptools
import os
import sys
import platform
import warnings

__version__ = '0.0.0'

with open("README.md", "r") as f:
    long_description = f.read()

# Manage requirements
install_requires = [
    # 'omf>=1.0.0',
    # 'vectormath>=0.2.1',
    # 'pyvista>=0.20.1',
    # 'numpy',
    # 'matplotlib',
    # TODO: properly set this from requirements file
]

setuptools.setup(
    name="gdc19",
    version=__version__,
    author="Bane Sullivan",
    author_email="info@opengeovis.org",
    description="2019 Geothermal Design Challenge",
    long_description=long_description,
    long_description_content_type="text/md",
    url="https://github.com/OpenGeoVis/GeothermalDesignChallenge",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=(
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        'Natural Language :: English',
    ),
)
