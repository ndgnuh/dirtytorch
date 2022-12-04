# DIRTYTORCH

Serve as a snippet holder. This module has zero dependencies.

## Usage

### Command line

List snippets
```bash
python -m dirtytorch list
dirty list 
dirty list -f
```

Dump snippets
```bash
dirty dump pl-loggers
dirty dump -o /tmp/loggers.py pl-loggers
```

Dump snippets from given config
```bash
dirty dump -f dirty.json
```

where `dirty.json` is:
```json
[
	["pl-loggers", "src/utils/loggers.py"],
	["pl-callbacks", "src/utils/loggers2.py"]
]
```

Update `dirtytorch`
```bash
dirty update
```

### Programmatically

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
