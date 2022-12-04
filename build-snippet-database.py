#!/bin/env python3
import os
import re
import json
from os import path
from dirtytorch import thisdir, get_snippet_spec_from_path
from pprint import pprint

output_file = path.join(thisdir, "snippets.json")
excludes = [
    "__init__.py",
    "__main__.py",
    r".*__pycache__.*"
]

specs = dict()
for (root, _, files) in os.walk(thisdir):
    files = [
        path.join(root, file) for file in files if file.endswith(".py")
        if not any(
            re.match(exclude, file) is not None
            for exclude in excludes
        )
    ]
    for file in files:
        spec = get_snippet_spec_from_path(file)
        name = spec['name']
        specs[name] = spec

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(specs, f, ensure_ascii=False, indent=2)
    print(f"Done, database written to {path.basename(output_file)}")
