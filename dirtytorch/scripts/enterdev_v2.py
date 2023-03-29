import docker
import pwd
import os
from os import path
from argparse import ArgumentParser
from subprocess import run, PIPE, STDOUT, call


def get_default_options():
    # Default options for the dev environment container
    args = []

    HOME = os.environ["HOME"]
    USER = os.environ["USER"]
    PWD = path.realpath(os.curdir)
    UID = pwd.getpwnam(USER).pw_uid
    GID = pwd.getpwnam(USER).pw_gid
    DISPLAY = os.environ.get("DISPLAY", None)

    # Mount points
    mount_directories = [
        ("/tmp", None),
        ("/dev/video0", None),
        ("/dev/video1", None),
        (f"{HOME}/.Xauthority", "/home/dev/.Xauthority"),
        (f"{HOME}/.deepface", "/home/dev/.deepface"),
        (f"{HOME}/.cache/", "/home/dev/.cache"),
    ]
    if USER == "dev":
        mount_directories.append([HOME, "/home/user"])
    else:
        mount_directories.append([HOME, None])
    for src, trg in mount_directories:
        trg = trg or src
        if path.exists(src):
            args = args + ["-v", f"{src}:{trg}"]

    # Time zone
    if path.isfile("/etc/timezone"):
        with open("/etc/timezone") as f:
            tz = f.read().strip()
            args.append("-e")
            args.append(f'TZ={tz}')

    # Other stuffs
    args.extend([
        "-v", f"{PWD}:/home/dev/working",  # Mount current directory
        "--ipc", "host",  # Fix multiprocessing bugs
        "--gpus", "all",  # Use all GPUs
        "--user", f"{UID}:{GID}",  # Permission matching
        "--env", f"DISPLAY={DISPLAY}",  # DISPLAY MATCHING
        "-it", "--rm",  # Remove after done, interactive
    ])

    # Network is not available on windows
    if os.name != 'nt':
        args = args + ["--network", "host"]

    return args


def get_container_by_name(name):
    cli = docker.DockerClient()
    containers = cli.containers.list()
    for container in containers:
        if container.name == name:
            return container


def enter_container(container, args, extra_args=[]):
    cmds = ["docker", "exec", "-it", container.name] + extra_args + ["bash"]
    if args.debug:
        print(cmds)
    call(cmds)


def make_new_container(args, extra_args=[]):
    options = get_default_options()
    image_name = "ndgnuh/torch-dev-env"
    if args.name is not None:
        options = options + ["--name", args.name]
    cmds = ["docker", "run", *options, image_name, "bash"]
    if args.debug:
        print(cmds)
    call(cmds)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--name", required=False, default=None)
    parser.add_argument("--debug", required=False,
                        default=False, action="store_true")

    args, remain = parser.parse_known_args()

    return args, remain


def main():
    args, remain = parse_args()

    container = get_container_by_name(args.name)
    if args.debug:
        print(container, args, remain)
    if container is None:
        make_new_container(args, remain)
    else:
        enter_container(container, args, remain)


if __name__ == "__main__":
    main()
