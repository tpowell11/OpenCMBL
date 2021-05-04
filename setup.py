import pathlib
from opencmbl import __init__
from setuptools import PackageFinder, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name = "opencmbl",
    version = "0.0.1",
    description = "Parser for LoggerPro .cmbl files",
    long_description = README,
    long_description_content_type = "text/markdown",
    url="",
    author = "Tom Powell",
    author_email="thomastruittpowell@gmail.com",
    license = "GPL3",
    classifiers = [
        "License :: OSI Approved :: GPL3",
        "Programming Lanuguage :: Python :: 3"
    ],
    packages = ["opencmbl"],
    include_package_data = True,
    install_requires = ["lxml"],
)