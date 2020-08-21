"""Setup.py file."""

import os
from setuptools import find_packages, setup

PWD = os.path.abspath(os.path.dirname(__name__))
REQUIREMENTS_FILE = os.path.join(PWD, "requirements.txt")
REQUIREMENTS = []
with open(REQUIREMENTS_FILE, "r") as req_file:
    REQUIREMENTS = req_file.read().splitlines()

README_FILE = os.path.join(PWD, "README.md")
with open(README_FILE, "r") as readme:
    README_TEXT = readme.read()

setup(
    name="Launchpad Fork",
    version="20.1",
    description="Create forks of upstream Launchpad repos",
    long_description=README_TEXT,
    long_description_content_type="text/markdown",
    author="Joshua Powers",
    author_email="josh.powers@canonical.com",
    url="https://github.com/powersj/lp-fork",
    download_url=("https://github.com/powersj/lp-fork/tarball/master"),
    install_requires=REQUIREMENTS,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    keywords=["ubuntu", "launchpad", "git", "cli"],
    packages=find_packages(),
    entry_points={"console_scripts": ["lp-fork=lp_fork.__main__:launch"]},
    zip_safe=True,
)