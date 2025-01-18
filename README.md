# graphviz-dot-hooks

This is a [pre-commit hook](https://pre-commit.com/) that uses graphviz python library to validate and/or render .dot files

## Installation

This tool requires the system package [graphviz](https://www.graphviz.org/) to be installed.
If you are on Debian, that is:

    sudo apt install graphviz
    
## Rationale

Main goal of this was to auto-generate PNG files from .dot files so that we have both version in the repository 
and we are sure that both version match and developers don't forget to render the PNG whenever they edit the .dot.

## Hooks available

### `check-dot`
Verify the syntax of .dot files


### `render-dot`
Is an alias for `render-dot-png`, kept for backward compatibility


### `render-dot-png`
Render .dot files to png. This command can work in 2 ways

  - Called without argument, it will render the .png next to the .dot files (simply appending ".png" to the .dot file path)
  - `--only src1,src2` can be used to select the files to be rendered
  - `--only src1:target1,src2:target2` can be used to specify custom locations for the PNG (specified per .dot source)


### `render-dot-svg`
Same as `render-dot-png` but renders to svg. Rendering to svg may be more stable as it is less sensitive to fonts and other dependencies.
Discrepancies were observed when using the png hook between ubuntu 22 and ubuntu 24 for instance.

## Pre-commit integration

An example `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/bagerard/graphviz-dot-hooks
    rev: master
    hooks:
      - id: check-dot
      - id: render-dot-png
        # args: ["--only=class_diagram.dot:docs/class_diagram.png"]
```

