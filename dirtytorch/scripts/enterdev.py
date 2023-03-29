import os
import sys
import pwd
from os import listdir, path
from subprocess import run, PIPE, STDOUT, call

HOME = os.environ["HOME"]
USER = os.environ["USER"]
PWD = path.realpath(os.curdir)
UID = pwd.getpwnam(USER).pw_uid
GID = pwd.getpwnam(USER).pw_gid
DISPLAY = os.environ.get("DISPLAY", None)

mount_directories = [
    ("/tmp", None),
    ("/dev/video0", None),
    ("/dev/video1", None),
    (f"{HOME}/.Xauthority", "/home/dev/.Xauthority"),
    (f"{HOME}/.deepface", "/home/dev/.deepface"),
    (f"{HOME}/.cache/", "/home/dev/.cache"),
]

if USER != "dev":
    mount_directories.append((f"{HOME}", None))

default_args = [
    "-v", f"{PWD}:/home/dev/working",
    "--rm", "-it",
    "--network", "host",
    "--user", f"{UID}:{GID}",
    "--gpus", "all",
    "--ipc", "host",
    "--env", f"DISPLAY={DISPLAY}",
]

if path.isfile("/etc/timezone"):
    with open("/etc/timezone") as f:
        tz = f.read().strip()
        default_args.append("-e")
        default_args.append(f'TZ=${tz}')


def mount_if_exist(args, filepath, target=None):
    if target is None:
        target = filepath
    if path.exists(filepath):
        return args + ["-v", f"{filepath}:{target}"]
    else:
        return args


def enter_dev_new(alt_args):
    cmds = [
        "docker",
        "run",
    ] + alt_args + default_args

    for (filepath, target) in mount_directories:
        cmds = mount_if_exist(cmds, filepath, target)

    cmds.append("ndgnuh/torch-dev-env")
    print(' '.join(cmds))
    exit_code = call(cmds, stderr=PIPE)

    # TODO better check
    if exit_code == 125:
        cmds = ["docker", "exec", "-it"] + alt_args + ["bash"]
        call(cmds)


def main():
    alt_args = sys.argv[1:]
    enter_dev_new(alt_args)


if __name__ == "__main__":
    main()
