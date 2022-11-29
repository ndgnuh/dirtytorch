from importlib import import_module
from argparse import ArgumentParser

scripts = [
    "split_image_folder",
    "split_image_index"
]


def main():
    parser = ArgumentParser()
    parser.add_argument("action")
    args = parser.parse_args()

    assert args.action in scripts, f"action should be one of: {', '.join(scripts)}"

    module = import_module(
        f".scripts.{args.action}",
        package=__package__
    )
    module.main()


if __name__ == "__main__":
    main()
