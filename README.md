# gitlabci-jsonschema-lint

This is a [pre-commit hook](https://pre-commit.com/) that uses the `json schema` from https://json.schemastore.org/gitlab-ci
to validate the contents of your `.gitlab-ci.yml` file.

## Rationale

Other similar tool exist like this [hook](https://github.com/kadrach/pre-commit-gitlabci-lint) but since the beginning of 2021,
Gitlab updated their API and it is no longer possible to make unauthenticated calls to the Gitlab endpoint `/api/v4/ci/lint`
that is used by the hook, and which makes it harder to integrate as it would require some shared token.

As an alternative to that, I created this hook which works completely offline 

## CLI Usage

    gitlabci-jsonschema-lint ../some_projects/.gitlab-ci.yml


## Pre-commit integration

An example `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/bagerard/gitlabci-jsonschema-lint
    rev: master
    hooks:
      - id: gitlabci-jsonschema-lint
```

