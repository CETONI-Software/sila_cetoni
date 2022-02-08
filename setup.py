import re
from os.path import basename, dirname, join
from setuptools import setup, find_packages


def prepare_readme():
    """README contains github-internal links, which need to be extended for PyPI"""
    content = open(join(dirname(__file__), "README.md")).read()
    link_pattern = r"\]\(([^h][^)]+)\)"
    return re.sub(link_pattern, "](https://github.com/CETONI-Software/sila_qmix/tree/master/\\1)", content)

setup(
    long_description=prepare_readme()
)
