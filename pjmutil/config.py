import pathlib
import json
import datetime as dt


config_file = pathlib.Path.home() / ".pjmutil" / "config"
with config_file.open("r") as f:
    config = json.load(f)

if config["resource_groups"] is None:
    raise ValueError(f"Available 'resource_groups' must be specified. Edit {config_file}.")
if config["time_limits"] is None:
    raise ValueError(f"Available 'time_limits' must be specified. Edit {config_file}.")
elif config["crsk_path"] is None:
    raise ValueError(f"Available 'crsk_path' must be specified. Edit {config_file}.")
elif config["crsk_runner_name"] is None:
    raise ValueError(f"Available 'crsk_runner_name' must be specified. Edit {config_file}.")

resource_groups = config["resource_groups"]
time_limits = {k: dt.timedelta(seconds=v) for k, v in zip(config["resource_groups"], config["time_limits"])}
base_log_path = pathlib.Path(config["log_dir"])
base_data_path = pathlib.Path(config["data_dir"])
base_all_inputs_path = pathlib.Path(config["all_inputs_dir"])
bash_profile_path = pathlib.Path(config["bash_profile_file"])

corsika_path = pathlib.Path(config["crsk_path"])
simulator = config["crsk_runner_name"]

if not base_log_path.exists():
    base_log_path.mkdir(parents=True)
    print(f"Info: {base_log_path} has been created.")
if not base_data_path.exists():
    base_data_path.mkdir(parents=True)
    print(f"Info: {base_data_path} has been created.")
if not base_all_inputs_path.exists():
    base_all_inputs_path.mkdir(parents=True)
    print(f"Info: {base_all_inputs_path} has been created.")


def get_data_file_path(process_name):
    return (base_data_path/process_name).with_suffix(".dat")
