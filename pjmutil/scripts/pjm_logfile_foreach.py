#!/usr/bin/env python3
import pjmutil.config
import pjmutil.util
import argparse
import subprocess
import sys
import colorama


def main():
    all_names, all_id = zip(*pjmutil.util.get_stored_all_job_names_id().items())

    parser = argparse.ArgumentParser(description='')
    parser.add_argument("pjm_job_id", choices=all_id + all_names)
    parser.add_argument("command", type=str)
    args = parser.parse_args()

    colorama.init(autoreset=True)

    try:
        i = all_id.index(args.pjm_job_id)
        name = all_names[i]
    except ValueError:
        name = args.pjm_job_id

    crsk_config = pjmutil.config.get_crsk_config()

    log_dir = crsk_config["log_path"] / name
    log_files = sorted(log_dir.glob("*"), reverse=True)
    if len(log_files) == 0:
        print(colorama.Fore.RED + f"No log files under {log_dir}")
        return 1
    for log_file in log_files:
        print(colorama.Fore.CYAN + "* {}:".format(log_file.relative_to(crsk_config["log_path"])))
        subprocess.run([*args.command.split(), str(log_file)])
        print("")
    return 0


if __name__ == "__main__":
    sys.exit(main())
