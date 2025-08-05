from setuptools import setup, find_packages

setup(
    name="bot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["aiogram==3.20", "redis==6.2.0"],
)
