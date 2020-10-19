from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="poc-python-wrapper",
    packages=find_packages(),
    version="20201016.1a0",
    url="https://github.com/nervosum/proof-of-concepts",
    description="Proof of concept to gain insights for the python wrapper",
    author="Nervosum",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["pandas==1.1.3", "scikit-learn>0.23", "flask==1.1.2"],
    python_requires=">=3.7",
)
