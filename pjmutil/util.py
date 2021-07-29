import subprocess
import re
from .config import *


# def get_elapsed_time(pjm_jobid):
#     stdout = subprocess.run(["pjstat", "-s", "--choose", "elp", str(pjm_jobid)], capture_output=True).stdout.decode()
#     lines = stdout.splitlines()
#     assert len(lines) == 3
#     matched = re.search(r" ELAPSE TIME \(USE\) .* \((\d+)\)", lines[1])
#     assert matched is not None
#     return int(matched[1])
#
#
# def get_limit_elapsed_time(pjm_jobid):
#     stdout = subprocess.run(["pjstat", "-s", "--choose", "elpl", str(pjm_jobid)], capture_output=True).stdout.decode()
#     lines = stdout.splitlines()
#     assert len(lines) == 3
#     matched = re.search(r" ELAPSE TIME \(LIMIT\) .* \((\d+)\) .*", lines[1])
#     assert matched is not None
#     return int(matched[1])


def get_all_job_id():
    stdout = subprocess.run(["pjstat", "--choose", "jid", "-s"], capture_output=True).stdout.decode()
    return [int(m[1]) for m in re.finditer(r"^ JOB ID .* : (.*)$", stdout, re.MULTILINE)]


def get_all_job_names():
    stdout = subprocess.run(["pjstat", "--choose", "jnam", "-s"], capture_output=True).stdout.decode()
    return [m[1] for m in re.finditer(r"^ JOB NAME .* : (.*)$", stdout, re.MULTILINE)]


def get_stored_all_job_names_id():
    return {
        pjm_file.parent.name: int(splited[1]) if len(splited := pjm_file.open().readline().split("'")) == 3 else None
        for pjm_file in (p/"pjm.out" for p in base_log_path.glob("*"))
        if pjm_file.exists()
    }


def kill_batch_job(id_=None, name=None):
    if id_ is not None:
        pass
    elif name is not None:
        id_ = get_all_job_id()[get_all_job_names().index(name)]
    else:
        raise ValueError
    p = subprocess.run(["pjdel", str(id_)])
    return p.returncode
