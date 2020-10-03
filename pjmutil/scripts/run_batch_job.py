#!/usr/bin/env python3
import subprocess
import pathlib
from pjmutil.config import base_log_path, get_data_file_path, resource_groups, bash_profile_path
import argparse
import shutil

template_batch_job_script = open(pathlib.Path(__file__).parent/"template-batch-job.txt").read()


def main():
    rg_dict = {rg.lower(): rg for rg in resource_groups}

    parser = argparse.ArgumentParser(description='run process')
    parser.add_argument("all_inputs_path", type=pathlib.Path)
    parser.add_argument("resource_group", type=str.lower, choices=list(rg_dict.keys()))
    parser.add_argument("-o", "--output", type=str, default="")
    parser.add_argument("-f", "--force", action="store_true")
    args = parser.parse_args()

    all_inputs_path = args.all_inputs_path.resolve()
    print(f"{all_inputs_path = }")

    if args.output == "":
        process_name = all_inputs_path.name
    else:
        process_name = args.output

    log_path = base_log_path / process_name
    data_path = get_data_file_path(process_name)

    if args.force:
        if log_path.exists():
            print(f"{log_path} is removed")
            shutil.rmtree(log_path)
        if data_path.exists():
            print(f"{data_path} is removed")
            data_path.unlink()

    log_path.mkdir()

    if data_path.exists():
        raise FileExistsError(data_path)

    script = template_batch_job_script.format(
        resource_group=rg_dict[args.resource_group],
        log_path=log_path,
        bash_profile_path=bash_profile_path,
        all_inputs_path=all_inputs_path,
        process_name=process_name
    )

    subprocess.Popen(["pjsub", "--name", process_name], stdin=subprocess.PIPE).communicate(script.encode())


if __name__ == "__main__":
    main()

