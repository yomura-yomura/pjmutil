#!/usr/bin/env python3
import sys
import numpy as np
import pathlib
import pjmutil
from pjmutil.throw_processes.corsika import throw
import colorama


def make_seeds(third_seed):
    seeds = np.array([
        (None, None, None),
        (None, None, None),
        (None, None, None),
        (None, None, None)
    ])
    seeds[:, 2] = third_seed
    return seeds.tolist()


def main():
    n_processes = 10
    i_seeds_starts = 0
    all_inputs_file = pathlib.Path("/path/to/all-inputs")
    resource_group = "c"
    memory_limit = 4

    if not all_inputs_file.exists():
        raise FileNotFoundError(all_inputs_file)
    elif resource_group not in pjmutil.config.resource_groups:
        raise ValueError(f"'{resource_group}' not defined in {pjmutil.config.resource_groups}")

    base_process_name = all_inputs_file.name

    colorama.init(autoreset=True)

    for i in np.arange(n_processes) + i_seeds_starts:
        process_name = f"{base_process_name}_ts{i}"
        print(colorama.Fore.MAGENTA + f"* {process_name}")
        throw(
            all_inputs_file, resource_group,
            output=process_name, seeds=make_seeds(i),
            memory_limit=memory_limit
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
