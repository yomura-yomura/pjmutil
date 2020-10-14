#!/usr/bin/env python3
import argparse
import sys
import numpy as np
import subprocess
import pathlib
import pjmutil
import shutil

template_run_batch_job_script = open(pathlib.Path(__file__).parent / "template-run-batch-job.txt").read()


def main():
    rg_dict = {rg.lower(): rg for rg in pjmutil.config.resource_groups}

    parser = argparse.ArgumentParser(description='run process')
    parser.add_argument("all_inputs_path", type=pathlib.Path)
    parser.add_argument("resource_group", type=str.lower, choices=list(rg_dict.keys()))
    parser.add_argument("-o", "--output", type=str, default="")
    parser.add_argument("-f", "--force", action="store_true")
    args = parser.parse_args()

    all_inputs_path = args.all_inputs_path.resolve()
    print(f"{all_inputs_path = }")

    return run_batch_job(all_inputs_path, rg_dict[args.resource_group], output=args.output, force=args.force)


def run_batch_job(all_inputs_path, resource_group, output=None, force=False, seeds=None):
    if output is None:
        process_name = all_inputs_path.name
    else:
        process_name = output

    log_path = pjmutil.config.base_log_path / process_name
    data_path = pjmutil.config.get_data_file_path(process_name)

    if force:
        if log_path.exists():
            print(f"{log_path} is removed")
            shutil.rmtree(log_path)
        if data_path.exists():
            print(f"{data_path} is removed")
            data_path.unlink()

    if log_path.exists():
        raise FileExistsError(log_path)
    if data_path.exists():
        raise FileExistsError(data_path)
    log_path.mkdir()

    if seeds is not None:
        if isinstance(seeds, np.ndarray):
            seeds = seeds.tolist()

    script = template_run_batch_job_script.format(
        resource_group=resource_group,
        time_limit=int(pjmutil.config.time_limits[resource_group].total_seconds()),
        log_path=log_path,
        bash_profile_path=pjmutil.config.bash_profile_path,
        all_inputs_path=all_inputs_path,
        process_name=process_name,
        seeds=seeds
    )

    p = subprocess.Popen(["pjsub", "--name", process_name], stdin=subprocess.PIPE)
    p.communicate(input=script.encode())
    return p.returncode


if __name__ == "__main__":
    sys.exit(main())

