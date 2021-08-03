import numpy as np
import subprocess
import pathlib
import pycrskrun.particle_type
import pjmutil
import shutil


template_run_batch_job_script = open(pathlib.Path(__file__).parent / "template-run-batch-job.txt").read()


def throw(args_list, resource_group, memory_limit, log_path):
    log_path.mkdir(parents=True)
    script = template_run_batch_job_script.format(
        resource_group=resource_group,
        memory_limit=memory_limit,
        time_limit=int(pjmutil.config.time_limits[resource_group].total_seconds()),
        log_path=log_path,
        bash_profile_path=pjmutil.config.bash_profile_path,
        python_code=f"""
import hybrid_analysis.java.high_level
from pathlib import PosixPath

args_list = {args_list}

for args in args_list:
    hybrid_analysis.java.high_level.reconstruct_hybrid_events(*args)
"""
    )

    process_name = "_".join(("tajava", *log_path.parts[-2:]))
    p = subprocess.Popen(["pjsub", "--name", process_name], stdin=subprocess.PIPE)
    p.communicate(input=script.encode())
    return p.returncode
