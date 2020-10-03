#!/usr/bin/env python3
import pjmutil.config
import pjmutil.util
import argparse
import subprocess


def main():
    all_id = pjmutil.util.get_all_job_id()
    all_names = pjmutil.util.get_all_job_names()
    parser = argparse.ArgumentParser(description='tail log of process')
    parser.add_argument("pjm_jobid", choices=all_id + all_names)
    parser.add_argument("-n", "--lines", type=int, default=10)
    args = parser.parse_args()

    try:
        i = all_id.index(args.pjm_jobid)
        name = all_names[i]
    except ValueError:
        name = args.pjm_jobid

    log_dir = pjmutil.config.base_log_path / name
    for log_file in reversed(list(log_dir.glob("*"))):
        print("* {}:".format(log_file.relative_to(pjmutil.config.base_log_path)))
        subprocess.run(["tail", "-n", str(args.lines), str(log_file)])
        print("")


if __name__ == "__main__":
    main()
