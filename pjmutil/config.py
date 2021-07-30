import pathlib
import json
import datetime as dt


__all__ = ["resource_groups", "time_limits", "bash_profile_path", "get_crsk_config"]


config_file = pathlib.Path.home() / ".pjmutil" / "config"
with config_file.open("r") as f:
    config = json.load(f)


def _validate_config_key(key):
    if key not in config or config[key] is None:
        raise ValueError(f"Available '{key}' must be specified. Edit {config_file}.")


def _create_dirs(path):
    if not path.exists():
        path.mkdir(parents=True)
        print(f"Info: {path} has been created.")


_validate_config_key("resource_groups")
_validate_config_key("time_limits")

resource_groups = config["resource_groups"]
time_limits = {k: dt.timedelta(seconds=v) for k, v in zip(config["resource_groups"], config["time_limits"])}
bash_profile_path = pathlib.Path(config["bash_profile_file"])


def get_crsk_config():
    _validate_config_key("crsk_path")
    _validate_config_key("crsk_runner_name")

    crsk_output_path = pathlib.Path(config["crsk_output_path"])
    crsk_config = {
        'path': pathlib.Path(config["crsk_path"]),
        'runner': config["crsk_runner_name"],
        'log_path': crsk_output_path / "log", 
        'data_path': crsk_output_path / "data"
    }

    _create_dirs(crsk_config["log_path"])
    _create_dirs(crsk_config["data_path"])

    return crsk_config


def get_tajava_config():
    _validate_config_key("tjv_log_path")

    tjv_config = {
        "log_path": pathlib.Path(config["tjv_log_path"])
    }

    _create_dirs(tjv_config["log_path"])
    
    return tjv_config


