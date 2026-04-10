from setuptools import setup, find_packages

setup(
    name="wrathops",
    version="0.1",
    packages=find_packages(include=["wrathops_cli", "wrathops_cli.*", "shared", "shared.*"]),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "wrathops=wrathops_cli.main:main"
        ]
    },
)