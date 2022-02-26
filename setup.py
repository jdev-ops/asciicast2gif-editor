import setuptools
import pathlib

from setuptools import find_packages

here = pathlib.Path(__file__).parent.resolve()

install_requires = (
    (here / "requirements/common.txt").read_text(encoding="utf-8").splitlines()
)


setuptools.setup(
    name="asciicast2gif-editor",
    version="0.0.1",
    author="J. Albert Cruz",
    author_email="jalbertcruz@gmail.com",
    license="MIT",
    package_dir={
        "": "lib",
    },
    packages=find_packages("lib"),
    scripts=["bin/gif-coalesce", "bin/gif-combine"],
    entry_points={
        "console_scripts": [
            "_gif_combine=asciicast2gif.combine:main",
            "_gen_metadata=asciicast2gif.combine:gen_metadata",
        ],
    },
)
