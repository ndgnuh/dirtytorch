# DIRTYTORCH

Serve as a snippet holder. This module has zero dependencies.

## Usage

```python
from dirtytorch import get_snippet

# Set to False or None to disable writing to files
output_file = "modules_reshape.py"

# The snippet name
snippet = "shape-modules"

# Write snippet to output file
get_snippet(snippet, output_file)
```

## List of snippets

```python
from dirtytorch import list_snippets

list_snippets()
```

## TODO

- move the dev env to another repo
- docs for each modules
