#!/usr/bin/env python3
import numpy as np
import pathlib
import pjmutil
from pjmutil.throw_processes.tajava import throw
import colorama
import hybrid_analysis.sim.run.reconstruct
import datetime as dt


# dry_run = True
dry_run = False
n_processes = 10
resource_group = "b"
memory_limit = 4


def main(dry_run: bool):
    tjv_config = pjmutil.config.get_tajava_config()
    log_root_path = tjv_config["log_path"]/dt.datetime.now().isoformat()

    data_path = pathlib.Path(hybrid_analysis.sim.run.reconstruct.__file__).resolve().parent/"data"
    all_args_list = hybrid_analysis.sim.run.reconstruct.get_args_list(data_path)

    split_args_list = list(map(np.ndarray.tolist, np.array_split(all_args_list, n_processes)))

    max_n_digits = int(np.log10(n_processes)) + 1
    for i, args_list in enumerate(split_args_list):
        log_path = log_root_path/f"{i:>0{max_n_digits}}"

        print(colorama.Fore.MAGENTA + f"* n-jobs = {len(args_list)} > {log_path}")
        if dry_run == np.False_:
            throw(args_list, resource_group, memory_limit, log_path)


if __name__ == "__main__":
    main(dry_run)
