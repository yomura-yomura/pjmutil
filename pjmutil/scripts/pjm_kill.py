import argparse
import sys
import pjmutil.job_status
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pattern", help="", default="*", type=str)
    parser.add_argument("-d", "--dry-run", action="store_true", default=False)
    args = parser.parse_args()
    data = pjmutil.job_status.get_job_info(args[0])

    if args.dry_run:
        return 0

    if data.size == 0:
        raise ValueError(f"No process names matched")

    print("\n".join(data["job_name"]))
    yn = input("Are you sure that all running processes shown above will be killed? [y/n] ")
    if yn == "y":
        subprocess.run(["pjdel", " ".join(data["job_id"])])
        print("Processes shown above have been killed.")
    else:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

