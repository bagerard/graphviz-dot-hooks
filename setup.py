from setuptools import setup

INSTALL_REQUIRES = [
    "graphviz",
]

VERSION = "0.1.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="graphviz-dot-hooks",
    version=VERSION,
    maintainer="Bastien Gerard",
    maintainer_email="bast.gerard@gmail.com",
    url="https://github.com/bagerard/graphviz-dot-hooks",
    keywords="dot gv linter",
    license="MIT License",
    description="Python pre-commit hook to check .dot files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["graphviz_dot_hooks"],
    install_requires=INSTALL_REQUIRES,
    entry_points={"console_scripts": ["check-dot = graphviz_dot_hooks.check_dot:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Quality Assurance",
    ],
    include_package_data=True,
)
