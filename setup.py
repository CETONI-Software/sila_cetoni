import os
import platform
import re
from os.path import dirname, join

from setuptools import find_namespace_packages, setup


def prepare_readme():
    """README contains github-internal links, which need to be extended for PyPI"""
    content = open(join(dirname(__file__), "README.md")).read()
    link_pattern = r"\]\(([^h][^)]+)\)"
    return re.sub(link_pattern, "](https://github.com/CETONI-Software/sila_qmix/tree/master/\\1)", content)


# This has been taken from https://github.com/rickstaa/stand_alone_sub_package_folder_example and modified to fit this
# project's struture. Essentially, it takes the packages from `find_namespace_packages` and extracts the packages that
# are also standalone packages (see `standalone_ns_packages`) and installs them as if they were installed one by one
# through pip.
# The problem that this code solves is the following:
# If all of the standalone packages were installed separately we will end up with the desired directory (and package)
# structure:
# site_packages/
# |- sila_cetoni/
# |  |- application
# |  |- balance
# |  |- ...
# |  `- valves
# |- ...
# `- ...
# If we want to install all packages with a single `pip install` the resulting strcuture would be not very nice to use
# and would have a lot of redundancies:
# site_packages/
# |- sila_cetoni/
# |  |- application
# |  |  `- sila_cetoni/
# |  |     `- application/
# |  |- balance
# |  |  `- sila_cetoni/
# |  |     `- balance/
# |  |- ...
# |  `- valves
# |     `- sila_cetoni/
# |        `- valves/
# |- ...
# `- ...

standalone_ns_pkgs = [
    "application",
    "balance",
    "controllers",
    "core",
    "io",
    "motioncontrol",
    "pumps",
    "valves",
]

# Add extra virtual shortened package for each stand-alone namespace package
# NOTE: This only works if you don't have a __init__.py file in your parent folder and stand alone_ns_pkgs folder.
PACKAGES = find_namespace_packages(include=["sila_cetoni*"])

redundant_namespaces = [
    pkg
    for pkg in PACKAGES
    if pkg in [PACKAGES[0] + "." + item + "." + PACKAGES[0] + "." + item for item in standalone_ns_pkgs]
]

PACKAGE_DIR = {}
for ns in redundant_namespaces:
    split_ns = ns.split(".")
    short_ns = re.sub(r"\." + split_ns[-1] + r"\." + PACKAGES[0] + r"\.(?=" + split_ns[-1] + r")", ".", ns)
    PACKAGES.remove(".".join(split_ns[:-1]))
    PACKAGE_DIR[short_ns] = ns.replace(".", "/")
    children = [pkg for pkg in PACKAGES if ns in pkg and ns]
    for child in children:
        PACKAGES.remove(child)
        short_child = short_ns + re.sub(ns, "", child)
        if short_child not in PACKAGES:
            PACKAGES.append(short_child)
            PACKAGE_DIR[short_child] = child.replace(".", "/")

s = setup(
    packages=PACKAGES,
    package_dir=PACKAGE_DIR,
    long_description=prepare_readme(),
)

if "build" in s.command_obj:
    here = os.path.dirname(__file__)
    sdk_path = os.path.abspath(os.path.join(here, "..", ".." if platform.system() == "Windows" else ""))
    file = os.path.join(here, s.command_obj["build"].build_lib, "sila_cetoni", "config.py")
    if os.path.exists(file):
        with open(file, "r+") as f:
            data = f.read().replace("\"$CETONI_SDK_PATH\"", f"{sdk_path!r}")
            f.seek(0)
            f.write(data)
