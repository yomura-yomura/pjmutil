#!/usr/bin/env python3
import pjmutil.config
import pjmutil.util
import argparse
import pathlib
import subprocess
import sys


template_salvage_data = open(pathlib.Path(__file__).parent / "template-salvage-data.txt").read()


def main():
    parser = argparse.ArgumentParser(description='Salvage data')
    # args = parser.parse_args()
    parser.parse_args()

    salvage_data_path = pjmutil.util.get_salvage_data_path()
    if salvage_data_path.exists():
        raise FileExistsError(salvage_data_path)
    salvage_data_path.mkdir()

    tmp_log_dir = pathlib.Path("/tmp/pjmutil")
    tmp_log_dir.mkdir()

    script = template_salvage_data.format(
        resource_group="A",
        bash_profile_path=pjmutil.config.bash_profile_path,
        log_path=tmp_log_dir
    )

    p = subprocess.Popen(["pjsub", "--name", "salvage_data"], stdin=subprocess.PIPE)
    p.communicate(input=script.encode())
    if p.returncode != 0:
        raise RuntimeError(f"{p.returncode = }")

    import time
    output_file = tmp_log_dir / "pjm.out"

    while True:
        time.sleep(1)
        if output_file.exists():
            break
        print(f"'salvage_data' not accepted yet. check it again 1 second later.")

    with output_file.open("r") as f:
        full_txt = ""
        while True:
            read = f.read()
            print(read)
            full_txt += read
            if "All processes have been done." in full_txt:
                break
    return 0


if __name__ == "__main__":
    sys.exit(main())





