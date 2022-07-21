# graphviz-dot-hooks

This is a [pre-commit hook](https://pre-commit.com/) that uses graphviz python library to validate or render .dot files

## Installation

Whether you use it as a cli or through [pre-commit hook](https://pre-commit.com/),
this tool requires [graphviz](https://www.graphviz.org/) to be installed

Thus, if you are on Debian, that is:

    sudo apt install graphviz
    
## Rationale

    Linters are cool but auto-generated documentation are even cooler

## CLI Usage

### check-dot

Verify the syntax of .dot files:
    
    check-dot your-dot-file1.dot your-dot-file2.dot

### render-dot
Render .dot files to png. This command can work in 2 ways

    # will (re)generate 2 png files, simply appending .png to the source files 
    render-dot your-dot-file1.dot your-dot-file2.dot

    # will (re)generate 2 png files at custom locations
    render-dot your-dot-file1.dot your-dot-file2.dot --only your-dot-file1.dot:other_location.png,your-dot-file2.dot:other_location2.png

## Pre-commit integration

An example `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/bagerard/graphviz-dot-hooks
    rev: master
    hooks:
      - id: check-dot
      - id: render-dot
        # optionally command: ["--only somefile.dot:doc/somefile.png"]
```

