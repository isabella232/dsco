import os
from pathlib import Path
import subprocess
import yaml
from dsco.subparsers import rm

cmd_name = "rmi"


def add_cmd(subparsers):
    cmd = subparsers.add_parser(cmd_name, help="remove containers")
    cmd.add_argument("--dev", action="store_true", help="include dev service")
    cmd.add_argument("--prod", action="store_true", help="include prod service")
    cmd.add_argument("--all", action="store_true", help="include prod service")


def run_cmd(args, conf):
    rm.run_cmd(args, conf)
    if conf["proj_root"]:
        dev_flag = args.dev or args.all
        prod_flag = args.prod or args.all

        proj_name = conf["pyproject"]["tool"]["poetry"]["name"]

        if prod_flag:
            subprocess.run(f"docker rmi {proj_name}_prod", shell=True)

        only_prod_flag = not dev_flag and prod_flag
        if not only_prod_flag:
            subprocess.run(f"docker rmi {proj_name}_dev", shell=True)

    else:
        print("No project found.")


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd