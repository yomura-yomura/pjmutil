#!/usr/bin/env python3
import pjmutil.config
import pjmutil.util
import argparse
import subprocess
import sys
import colorama


def main():
    all_id = pjmutil.util.get_all_job_id()
    all_names = pjmutil.util.get_all_job_names()
    parser = argparse.ArgumentParser(description='tail log of process')
    parser.add_argument("pjm_jobid", choices=all_id + all_names)
    parser.add_argument("-n", "--lines", type=int, default=10)
    args = parser.parse_args()

    colorama.init(autoreset=True)

    try:
        i = all_id.index(args.pjm_jobid)
        name = all_names[i]
    except ValueError:
        name = args.pjm_jobid

    log_dir = pjmutil.config.base_log_path / name
    log_files = sorted(log_dir.glob("*"), reverse=True)
    if len(log_files) == 0:
        print(colorama.Fore.RED + f"No log files under {log_dir}")
        sys.exit(1)
    for log_file in log_files:
        print(colorama.Fore.CYAN + "* {}:".format(log_file.relative_to(pjmutil.config.base_log_path)))
        subprocess.run(["tail", "-n", str(args.lines), str(log_file)])
        print("")


if __name__ == "__main__":
    main()
