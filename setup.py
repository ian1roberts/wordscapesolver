"""wordscapesolver package setup module"""
from setuptools import find_packages, setup

config = {
    "version": "0.0.1",
    "name": "wordscapesolver",
    "description": "<MODULE_DESCRIPTION>",
    "url": "",
    "author": "Ian Roberts",
    "author_email": "ian.roberts@cantab.net",
    "packages": find_packages(
        include=[
            "wordscapesolver",
            "wordscapesolver.*",
        ]
    ),
}

setup(**config)
