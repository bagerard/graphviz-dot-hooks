# graphviz-dot-hooks

This is a [pre-commit hook](https://pre-commit.com/) that uses graphviz python library to validate or render .dot files

## Installation

This tool requires the system package [graphviz](https://www.graphviz.org/) to be installed.
If you are on Debian, that is:

    sudo apt install graphviz
    
## Rationale

    Main goal of this was to auto-generate PNG files out of .dot files so that we have both version in repositories
    and we are sure that both version match and that developers don't forget to render the PNG's.

## Hooks available

### `check-dot`
Verify the syntax of .dot files:


### `render-dot`
Render .dot files to png. This command can work in 2 ways

  - Called without argument, it will render the .png next to the .dot files (simply appending ".png" to the .dot file path)
  - `--only src1,src2` can be used to select the files to be rendered
  - `--only src1:target1,src2:target2` can be used to specify custom locations for the PNG (specified per .dot source)


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

