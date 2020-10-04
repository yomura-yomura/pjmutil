import argparse
import sys
import pjmutil.util
import re


def main():
    all_names = pjmutil.util.get_all_job_names()
    parser = argparse.ArgumentParser(description='kill process')
    parser.add_argument("process_names", nargs="+", help=f"{all_names}", type=str)
    args = parser.parse_args()

    kill_names = [name for pn in args.process_names for name in all_names if re.fullmatch(pn, name)]
    if len(kill_names) == 0:
        raise ValueError(f"No process names matched with {all_names}")

    print("")
    print("\n".join(kill_names))
    yn = input("Are you sure that all running processes shown above will be killed? [y/n] ")
    if yn == "y":
        for kn in kill_names:
            pjmutil.util.kill_batch_job(name=kn)
        print("Processes shown above have been killed.")
    else:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
