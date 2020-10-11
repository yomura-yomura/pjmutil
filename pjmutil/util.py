import sys
import pycrskrun.all_input
import subprocess
import re
import shutil
import datetime as dt
import threading
import time
from .config import *


def get_run_dir(pjm_jobid):
    return pathlib.Path(f"/tmp/job{pjm_jobid}/")


def run_batch_job(pjm_jobid, all_inputs_process, process_name, resource_group,
                  seeds=None):
    log_path = base_log_path / process_name
    all_inputs_path = pathlib.Path(all_inputs_process)
    run_dir = get_run_dir()
    run_data_dir = run_dir / "data/"

    if not all_inputs_path.is_file():
        print("process_name list: {}".format([p.name for p in base_all_inputs_path.glob("*") if p.is_file()]),
              file=sys.stderr)
        raise FileNotFoundError(all_inputs_path)
    elif run_dir.exists():
        raise FileExistsError(run_dir)

    log_path.mkdir(exist_ok=True)
    run_data_dir.mkdir(parents=True)
    run_data_file = (run_data_dir / process_name).with_suffix(".dat")

    print(f"* Start {pjm_jobid=}")

    ai = pycrskrun.all_input.all_input(all_inputs_path)
    ai.change_args("TELFIL", run_data_file)

    if seeds is not None:
        # assert np.ndim(seeds) == 2
        # assert np.shape(seeds)[-1] == 3
        for seed, args in zip(seeds, ai["SEED"]["args"]):
            for i, s in enumerate(seed):
                if s is not None:
                    args[i] = s

    def run():
        subprocess.Popen(
            [f"./{simulator}"], cwd=corsika_path, stdin=subprocess.PIPE,
            stdout=(log_path / "mc.out").open("w"), stderr=(log_path / "mc.err").open("w")
        ).communicate(str(ai).encode())

    thread = threading.Thread(target=run)
    thread.start()

    print("* Start CORSIKA")
    # 3 minutes before
    # limit = get_limit_elapsed_time(pjm_jobid) - 3 * 60
    limit = time_limits[resource_group] - 3 * 60
    t0 = time.time()

    while True:
        # elapsed_time = get_elapsed_time(pjm_jobid)
        elapsed_time = time.time() - t0
        if not thread.is_alive():
            print("* Process has finished")
            break
        elif limit <= elapsed_time:
            left = dt.timedelta(seconds=elapsed_time)
            print(f"* Process will be stopped due to the time limit ({left} left)")
            break
        print(f"[DEBUG] {dt.timedelta(seconds=elapsed_time)} left.")
        time.sleep(60)

    print(f"* Move {run_data_file} to {base_data_path}")
    shutil.move(str(run_data_file), str(base_data_path/run_data_file.name))
    run_data_dir.rmdir()
    run_dir.rmdir()


def get_salvage_data_path():
    return base_data_path / "_salvaged"


def salvage_data():
    job_dict = get_stored_all_job_names_id()

    salvaged_data_dir = get_salvage_data_path()

    maxlen_name = max(len(n) for n in job_dict.keys())

    for name, jobid in job_dict.items():
        run_dir = get_run_dir(jobid)
        print(f"* Checking {name:>{maxlen_name}} ({str(run_dir):<20}): ", end="")

        if not run_dir.exists():
            print("Not Found")
            continue
        else:
            print("Found")

        target_dir = salvaged_data_dir / name

        print(f"\t** Copy {run_dir} to {target_dir}")
        shutil.copytree(str(run_dir), str(target_dir))
    print("All processes have been done.")


def get_elapsed_time(pjm_jobid):
    stdout = subprocess.run(["pjstat", "-s", "--choose", "elp", str(pjm_jobid)], capture_output=True).stdout.decode()
    lines = stdout.splitlines()
    assert len(lines) == 3
    matched = re.search(r" ELAPSE TIME \(USE\) .* \((\d+)\)", lines[1])
    assert matched is not None
    return int(matched[1])


def get_limit_elapsed_time(pjm_jobid):
    stdout = subprocess.run(["pjstat", "-s", "--choose", "elpl", str(pjm_jobid)], capture_output=True).stdout.decode()
    lines = stdout.splitlines()
    assert len(lines) == 3
    matched = re.search(r" ELAPSE TIME \(LIMIT\) .* \((\d+)\) .*", lines[1])
    assert matched is not None
    return int(matched[1])


def get_all_job_id():
    stdout = subprocess.run(["pjstat", "--choose", "jid", "-s"], capture_output=True).stdout.decode()
    return [int(m[1]) for m in re.finditer(r"^ JOB ID .* : (.*)$", stdout, re.MULTILINE)]


def get_all_job_names():
    stdout = subprocess.run(["pjstat", "--choose", "jnam", "-s"], capture_output=True).stdout.decode()
    return [m[1] for m in re.finditer(r"^ JOB NAME .* : (.*)$", stdout, re.MULTILINE)]


def get_stored_all_job_names_id():
    return {
        p.name: int(splited[1]) if len(splited := pjm_file.open().readline().split("'")) == 3 else None
        for p in base_log_path.glob("*")
        if p.is_dir() and (pjm_file := p/"pjm.out").exists()
    }


def kill_batch_job(id=None, name=None):
    if id is not None:
        pass
    elif name is not None:
        id = get_all_job_id()[get_all_job_names().index(name)]
    else:
        raise ValueError
    p = subprocess.run(["pjdel", str(id)])
    return p.returncode
