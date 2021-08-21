from setuptools import setup

INSTALL_REQUIRES = [
    "jsonschema>=3.0.0",
    "ruamel.yaml>=0.16.0",
    "identify>=2.2.0",
]

setup(
    name="gitlabci-jsonschema-lint",
    packages=["gitlabci_lint"],
    install_requires=INSTALL_REQUIRES,
    entry_points={"console_scripts": ["gitlabci-jsonschema-lint = gitlabci_lint:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
