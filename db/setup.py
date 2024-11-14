from setuptools import setup, find_packages

setup(
    name="db",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["asyncpg==0.30.0"],
)
