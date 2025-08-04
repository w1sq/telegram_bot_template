from setuptools import setup, find_packages

setup(
    name="db",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "sqlmodel==0.0.24",
        "asyncpg==0.30.0",
        "redis==6.2.0",
    ],
)
