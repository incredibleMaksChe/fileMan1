from setuptools import setup, find_packages

setup(
    name="fileMan1",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={"console_scripts": ["manager = main:main"]},
)