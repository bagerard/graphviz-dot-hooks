import argparse
import json
import sys
from typing import Tuple

import jsonschema
import ruamel.yaml
from identify import identify

yaml = ruamel.yaml.YAML(typ="safe")


GITLABCI_SCHEMA = "gitlab-ci.json"


def read_json_schema(filepath):
    with open(filepath) as f:
        return json.load(f)


def read_gitlabci(filepath):
    tags = identify.tags_from_path(filepath)
    if "yaml" in tags:
        loader = yaml.load
    elif "json" in tags:
        loader = json.load
    else:
        raise ValueError(f"cannot check {filepath} as it is neither yaml nor json")
    with open(filepath) as f:
        return loader(f)


def lint_it(gitlabci_content, json_schema: dict) -> Tuple[str, str]:
    try:
        jsonschema.validate(instance=gitlabci_content, schema=json_schema)
    except jsonschema.ValidationError as err:
        node_path = [str(x) for x in err.path] or ["<root>"]
        node_path = ".".join(x if "." not in x else f'"{x}"' for x in node_path)
        return node_path, err.message


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("instancefiles", nargs="+", help="JSON or YAML files to check.")
    args = parser.parse_args()

    schema = read_json_schema(GITLABCI_SCHEMA)

    failures = {}
    for instancefile in args.instancefiles:
        doc = read_gitlabci(instancefile)

        error_details = lint_it(doc, schema)
        if error_details:
            failures[instancefile] = error_details

    if failures:
        print("Schema validation errors were encountered.")
        for filename in args.instancefiles:
            if filename in failures:
                node_path, error_msg = failures[filename]
                print(f"  \033[0;33m{filename}::{node_path}: \033[0m{error_msg}")
        sys.exit(1)

    print("ok -- validation done")


if __name__ == "__main__":
    main()
