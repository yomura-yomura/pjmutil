import sys
import pycrskrun.all_input
import pycrskrun.particle_type
import subprocess
import threading
import time
from ..config import *


# def run(pjm_job_id,  process_name, resource_group):
#     log_path = base_log_path / process_name
#
#     if not all_inputs_path.is_file():
#         print("process_name list: {}".format([p.name for p in base_all_inputs_path.glob("*") if p.is_file()]),
#               file=sys.stderr)
#         raise FileNotFoundError(all_inputs_path)
#
#     run_data_dir = base_data_path / process_name
#     run_data_dir.mkdir(parents=True, exist_ok=True)
#     run_data_file = (run_data_dir / process_name).with_suffix(".dat")
#     if run_data_file.exists():
#         raise FileExistsError(run_data_file)
#
#     log_path.mkdir(exist_ok=True)
#
#     print(f"* Start {pjm_job_id=}, {resource_group=}")
#
#     ai = pycrskrun.all_input.all_input(all_inputs_path)
#     ai.change_args("TELFIL", run_data_file)
#     ai.change_args("DIRECT", f"{run_data_dir}/")
#
#     if seeds is not None:
#         for seed, args in zip(seeds, ai["SEED"]["args"]):
#             for i, s in enumerate(seed):
#                 if s is not None:
#                     args[i] = s
#
#     if particle_id is not None:
#         ai.change_args("PRMPAR", particle_id)
#
#     def _run():
#         subprocess.Popen(
#             [f"./{simulator}"], cwd=corsika_path, stdin=subprocess.PIPE,
#             stdout=(log_path / "mc.out").open("w"), stderr=(log_path / "mc.err").open("w")
#         ).communicate(str(ai).encode())
#
#     thread = threading.Thread(target=_run)
#     thread.start()
#
#     print("* Start CORSIKA")
#     limit = time_limits[resource_group].total_seconds() - 1 * 60
#
#     t0 = time.time()
#
#     while True:
#         elapsed_time = time.time() - t0
#         if not thread.is_alive():
#             print("* Process has finished")
#             break
#         elif limit <= elapsed_time:
#             left = dt.timedelta(seconds=elapsed_time)
#             print(f"* Process will be stopped due to the time limit ({left} left; at {dt.datetime.now()})")
#             break
#         print(f"[DEBUG] {dt.timedelta(seconds=elapsed_time)} left.")
#         time.sleep(60)
#
#     print("All processes have finished.")
