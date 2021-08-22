import argparse
import json
import sys
from typing import Tuple, List
import os

import ruamel.yaml
from jsonschema import Draft7Validator

yaml = ruamel.yaml.YAML(typ="safe")

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
GITLABCI_SCHEMA_PATH = os.path.join(CUR_DIR, "gitlab-ci.json")


def read_json_schema(filepath: str):
    with open(filepath) as f:
        return json.load(f)


def read_gitlabci(filepath: str):
    with open(filepath) as f:
        return yaml.load(f)


def lint_it(gitlabci_content, json_schema: dict) -> List[Tuple[str, str]]:
    v = Draft7Validator(json_schema)
    linting_errors = []
    for error in sorted(v.iter_errors(gitlabci_content), key=str):
        node_path = [str(x) for x in error.path] or ["<root>"]
        node_path = ".".join(x if "." not in x else f'"{x}"' for x in node_path)
        linting_errors.append((node_path, error.message))
    return linting_errors


def run_check(args) -> Tuple[bool, List[str]]:
    schema = read_json_schema(GITLABCI_SCHEMA_PATH)

    failures = {}
    for instancefile in args.instancefiles:
        doc = read_gitlabci(instancefile)
        error_details = lint_it(doc, schema)
        if error_details:
            failures[instancefile] = error_details

    messages = []
    if failures:
        messages.append("Schema validation errors were encountered.")
        for filename in args.instancefiles:
            if filename in failures:
                for node_path, error_msg in failures[filename]:
                    messages.append(
                        f"  \033[0;33m{filename}::{node_path}: \033[0m{error_msg}"
                    )
    else:
        messages.append("ok -- validation done")

    return not failures, messages


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("instancefiles", nargs="+", help="JSON or YAML files to check.")

    args = parser.parse_args()

    success, messages = run_check(args)

    for message in messages:
        print(message)

    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
