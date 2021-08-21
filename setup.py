from setuptools import setup

INSTALL_REQUIRES = [
    "jsonschema>=3.0.0",
    "ruamel.yaml>=0.16.0",
]

VERSION = "0.0.0"

setup(
    name="gitlabci-jsonschema-lint",
    version=VERSION,
    maintainer="Bastien Gerard",
    maintainer_email="bast.gerard@gmail.com",
    url="https://github.com/bagerard/gitlabci-jsonschema-lint",
    keywords="gitlab-ci linter ",
    license="MIT License",
    packages=["gitlabci_lint"],
    install_requires=INSTALL_REQUIRES,
    entry_points={"console_scripts": ["gitlabci-jsonschema-lint = gitlabci_lint:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
