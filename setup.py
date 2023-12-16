"""wordscapesolver package setup module"""
from setuptools import find_packages, setup

config = {
    "version": "0.4.0",
    "name": "wordscapesolver",
    "description": "<MODULE_DESCRIPTION>",
    "url": "",
    "author": "Ian Roberts",
    "author_email": "ian.roberts@cantab.net",
    "packages": find_packages(
        include=[
            "wordscapesolver",
            "wordscapesolver.*",
            "imageparser",
            "imageparser.*",
            "wordscapesolver.cli.solveit",
            "wordscapesolver.cli.solveit.*"
        ]
    ),
    "include_package_data": True,
    "package_data": {"": ["etc/*.txt", "etc/*.ini"]},
}

setup(**config)
