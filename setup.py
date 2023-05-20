"""Install packages as defined in this file into the Python environment."""
from setuptools import setup, find_namespace_packages

setup(
    name="tokenfinderbot",
    author="Farzad Z",
    url="https://github.com/farzadex-eth/tokenfinderbot",
    description="TokenPoolBot is a simple bot for scanning new ERC-20 token pools created and filtering them based on the time created, liquidity and market cap. On each run it shows potential good token pools based on the filters.",
    version="0.1.0",
    package_dir={"": "tokenfinderbot"},
    packages=find_namespace_packages(where="tokenfinderbot", exclude=["tests"]),
    install_requires=[
        "setuptools>=45.0",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.0",
        "Topic :: Utilities",
    ],
)