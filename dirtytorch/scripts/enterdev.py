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

if HOME != "dev":
    mount_directories.append((f"{HOME}", None))

default_args = [
    "-v", f"{PWD}:/home/dev/working",
    "--rm", "-it",
    "--network", "host",
    "--user", f"{UID}:{GID}",
    "--gpus", "all",
    "--env", f"DISPLAY={DISPLAY}",
]


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
    exit_code = call(cmds, stderr=PIPE)

    # TODO better check
    if exit_code == 125:
        call(["docker", "exec", "-it", alt_args[-1], "bash"])


def main():
    alt_args = sys.argv[1:]
    enter_dev_new(alt_args)
