from setuptools import setup, find_packages

setup(
    name="utils",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pydantic-settings==2.6.1", "python-dotenv==1.0.1"],
)