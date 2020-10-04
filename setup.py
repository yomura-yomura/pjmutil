from setuptools import find_packages, setup
import pathlib
import json

config_dir = pathlib.Path.home() / ".pjmutil"
config_dir.mkdir(exist_ok=True)
config_path = config_dir / "config"

if not config_path.exists():
    default_result_dir = pathlib.Path.home() / "pjutil"
    config = dict(
        log_dir=str(default_result_dir / "log/"),
        data_dir=str(default_result_dir / "data/"),
        all_inputs_dir=str(default_result_dir / "all-inputs/"),
        bash_profile_file=pathlib.Path.home() / ".bash_profile",
        resource_groups=None,
        time_limits=None,
        crsk_path=None,
        runner=None,
    )

    with config_path.open("w") as f:
        json.dump(config, f, indent=4)

setup(
    name='pjmutil',
    version='1.0.3',
    description='',
    author='yomura',
    author_email='yomura@hoge.jp',
    url='https://github.com/yomura-yomura/pjmutil',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            "run_batch_job = pjmutil.scripts.run_batch_job:main",
            "tail_log_of_batch_job = pjmutil.scripts.tail_log_of_batch_job:main"
        ],
    },
    package_data={"pjmutil": ["template-batch-job.txt"]},
    include_package_data=True,
    install_requires=[
        "pycrskrun @ git+https://github.com/yomura-yomura/pycrskrun",
        "colorama"
    ]
)
