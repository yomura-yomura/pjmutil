import numpy as np
import subprocess
import pathlib
import pycrskrun.particle_type
import pjmutil
import pjmutil.throw_processes.template_run_batch_job
import shutil


template_run_batch_job_script = open(pathlib.Path(__file__).parent / "template-run-batch-job.txt").read()


def throw(all_inputs_path, resource_group, memory_limit=4, output=None, force=False,
          seeds=None, particle_type=None):
    if output is None:
        process_name = all_inputs_path.name
    else:
        process_name = output

    crsk_config = pjmutil.config.get_crsk_config()

    log_path = crsk_config["log_path"] / process_name
    data_path = (crsk_config["data_path"] / process_name).with_suffix(".dat")

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

    if particle_type is not None:
        particle_id = pycrskrun.particle_type.type_to_id(particle_type)
    else:
        particle_id = None

    script = pjmutil.throw_processes.template_run_batch_job.load(
        resource_group=resource_group,
        memory_limit=memory_limit,
        time_limit=int(pjmutil.config.time_limits[resource_group].total_seconds()),
        log_path=log_path,
        bash_profile_path=pjmutil.config.bash_profile_path,
        python_code=f"""
from pjmutil.batch_job_processes.corsika import run
run('$PJM_JOBID', '{all_inputs_path}', '{process_name}', '{resource_group}', {seeds}, {particle_id})
"""
    )

    p = subprocess.Popen(["pjsub", "--name", process_name], stdin=subprocess.PIPE)
    p.communicate(input=script.encode())
    return p.returncode
