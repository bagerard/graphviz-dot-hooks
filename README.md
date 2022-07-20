# graphviz-dot-hooks

This is a [pre-commit hook](https://pre-commit.com/) that uses graphviz python library to validate .dot files

## Installation

Whether you use it as a cli or through [pre-commit hook](https://pre-commit.com/),
this tool requires [graphviz](https://www.graphviz.org/) to be installed

Thus, if you are on Debian, that is:

    sudo apt install graphviz
    
## Rationale

    Linters are cool

## CLI Usage

    check-dot your-dot-file1.dot your-dot-file2.dot


## Pre-commit integration

An example `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/bagerard/graphviz-dot-hooks
    rev: master
    hooks:
      - id: check-dot
```

