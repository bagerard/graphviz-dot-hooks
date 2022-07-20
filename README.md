# graphviz-dot-hooks

This is a [pre-commit hook](https://pre-commit.com/) that uses graphviz python library to validate .dot files

## Rationale

    ...

## CLI Usage

    ...


## Pre-commit integration

An example `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/bagerard/graphviz-dot-hooks
    rev: master
    hooks:
      - id: check-dot
```

