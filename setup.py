from setuptools import setup


setup(
    name="gitlabci-jsonschema-lint",
    packages=["gitlabci_lint"],
    entry_points={"console_scripts": ["gitlabci-jsonschema-lint = gitlabci_lint:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
