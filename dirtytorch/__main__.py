from argparse import ArgumentParser
from subprocess import run
from .utils.functable import Functable
from . import list_snippets, get_snippet
from os import makedirs, path

import json

allowed_actions = ["list", "dump", "update"]

add_subparser = Functable()
dispatch = Functable()


@add_subparser("update")
def dump_parser(subparsers):
    return


@add_subparser("dump")
def dump_parser(parser):
    parser.add_argument("name",
                        help="Snippet name")
    parser.add_argument("--from-file", "-f", dest="from_file",
                        help="Dump from file, default=false",
                        action="store_true", default=False)
    parser.add_argument("--output", "-o", dest="output",
                        help="Write snippet to output file")
    return parser


@add_subparser("list")
def list_parser(parser):
    parser.add_argument("-f", "--full",
                        action="store_true",
                        help="Show description",
                        dest="full",
                        default=False)
    return parser


@dispatch("list")
def list_action(args):
    # SHORT PRINT
    if not args.full:
        print("List of snippet names:")
        for name, snippet in list_snippets().items():
            print(" " * 3 + name)
        return

    # LONG PRINT
    columns = [["Name", "File", "Descriptions"]]
    lengths = [len(c) for c in columns[0]]
    for name, snippet in list_snippets().items():
        columns.append([name, snippet["file"], snippet["short_desc"]])
        lengths = [
            max(lengths[i], len(columns[-1][i]))
            for i in range(3)
        ]
    spacing = 2
    lengths = [ln + spacing for ln in lengths]
    fmt = "| ".join([f"%{-ln}s" for ln in lengths])  # noqa: E741
    for i, row in enumerate(columns):
        print(fmt % tuple(row))
        if i == 0:
            total_length = sum(lengths)
            total_length += 2 * (len(lengths) - 1)
            print('-' * total_length)


@dispatch("update")
def update_action(args):
    origin = "dirtytorch@git+https://github.com/ndgnuh/dirtytorch"
    run(["pip", "install", origin, "--force"])


def dump_single(name, output, **kwargs):
    snip = get_snippet(name, output, **kwargs)
    if output is None:
        print(snip)
    else:
        print(f"Snippet {name} written to {output}")


@dispatch("dump")
def dump_action(args):
    if args.from_file:
        with open(args.name) as f:
            snips = json.load(f)
            for name, output in snips.items():
                if output is not None:
                    d = path.dirname(output)
                    try:
                        makedirs(d, exist_ok=True)
                    except Exception:
                        pass
                with open(output, "w") as f:
                    f.write("")
            for name, output in snips.items():
                dump_single(name, output, append=True)
    else:
        dump_single(args.name, args.output)


helps = dict(
    list="List snippets",
    dump="Write snippets to stdout or file",
    update="Update dirtytorch"
)


def main():
    parser = ArgumentParser()
    # parser.add_argument("action", choices=allowed_actions)
    subparsers = parser.add_subparsers(
        dest="action", help="Action", required=True)
    for action in allowed_actions:
        subparser = subparsers.add_parser(action, help=helps[action])
        add_subparser[action](subparser)
    args = parser.parse_args()

    action = args.action
    dispatch[action](args)


if __name__ == "__main__":
    main()
