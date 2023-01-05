from argparse import ArgumentParser
from os import path
from random import shuffle

presets = {
    "911": ("train,val,test", "0.81,0.09,0.1"),
    "822": ("train,val,test", "0.64,0.16,0.2"),
    "55": ("train,test", "0.5,0.5"),
}


def main():
    parser = ArgumentParser()

    parser.add_argument("--names", default="train,test,val")
    parser.add_argument("--ratio", default="0.64,0.2,0.16")
    parser.add_argument("--preset",
                        dest="preset",
                        choices=["911", "822", "55"],
                        default=None)
    parser.add_argument("input")

    # Process args
    args = parser.parse_args()

    # Presets if specified
    if args.preset is not None:
        args.names, args.ratio = presets[args.preset]

    args.names = args.names.split(",")
    args.ratio = [float(r) for r in args.ratio.split(",")]
    args.ratio = [r / sum(args.ratio) for r in args.ratio]

    with open(args.input, encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
        lines = [line for line in lines if len(line) > 0]

    # Split data
    shuffle(lines)
    n = len(lines)
    endpoints = [0]
    for r in args.ratio:
        endpoints.append(int(endpoints[-1] + n * r))
    splits = [lines[slice(s, e)] for (s, e) in zip(endpoints, endpoints[1:])]

    # Write output
    output_dir = path.dirname(args.input)
    _, ext = path.splitext(args.input)
    for split, name in zip(splits, args.names):
        output_path = path.join(output_dir, name + ext)
        with open(output_path, 'w', encoding='utf-8') as io:
            io.write('\n'.join(split))
