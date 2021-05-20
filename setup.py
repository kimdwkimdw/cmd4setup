import os
from shutil import rmtree
import subprocess
import sys

from setuptools import Extension
from setuptools import find_packages, setup, Command
from setuptools.command.build_ext import build_ext

__PATH__ = os.path.abspath(os.path.dirname(__file__))

__version__ = "0.0.3"

install_requires = """
orjson==3.5.*
redis==3.5.*
sentry-sdk~=1.0.0
""".strip().split(
    "\n"
)

HELLO_PATH = os.path.join(os.path.dirname(__file__), "hello.sh")


class new_build_ext(build_ext):
    def build_extension(self, ext):
        with open(os.path.expanduser("~/hello.test"), "w") as fw:
            fw.write("i'm installed")

        subprocess.run(
            ["bash", HELLO_PATH],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        # build_ext.build_extension(self, ext)


extensions = [Extension("dummy", ["not.c"])]


# brought from https://github.com/navdeep-G/setup.py
class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            os.system("rm -vrf ./*.egg-info")
            rmtree(os.path.join(__PATH__, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        # os.system("twine upload dist/* -r private_pypi")

        # self.status("Pushing git tags…")
        # os.system("git push --tags")
        sys.exit()


cmdclass = {
    "build_ext": new_build_ext,
    "deploy": UploadCommand,
}

setup(
    name="cmd4setup",
    version="0.0.1",
    description="cmdclass for setuptools",
    url="https://github.com/kimdwkimdw/cmd4setup",
    author="Arthur Kim",
    author_email="kimdwkimdw@gmail.com",
    keywords="setuptools cmdclass cmd4setup deploy twine",
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Framework :: Setuptools Plugin",
        "Topic :: System :: Installation/Setup",
    ],
    packages=find_packages(exclude=["tests"]),
    install_requires=install_requires,
    extras_require={
        "dev": [
            "wheel",
            "bump2version",
            "flake8",
            "neovim",
            "pytest",
            "pytest-flake8",
            "coverage",
            "jupyter",
        ]
    },
    include_package_data=True,
    cmdclass=cmdclass,
    ext_modules=extensions,
)
