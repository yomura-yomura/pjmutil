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
        time_limits=None,  # seconds
        crsk_path=None,
        runner=None,
    )

    with config_path.open("w") as f:
        json.dump(config, f, indent=4)

setup(
    name='pjmutil',
    version='1.6.1',
    description='',
    author='yomura',
    author_email='yomura@hoge.jp',
    url='https://github.com/yomura-yomura/pjmutil',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            "pjm-run = pjmutil.scripts.pjm_run:main",
            "pjm-logfile-foreach = pjmutil.scripts.pjm_logfile_foreach:main",
            "pjm-salvage = pjmutil.scripts.pjm_salvage:main"
        ],
    },
    package_data={"pjmutil": ["scripts/template-run-batch-job.txt", "scripts/template-salvage-data.txt"]},
    include_package_data=True,
    install_requires=[
        "numpy",
        "colorama",
        "pycrskrun @ git+https://github.com/yomura-yomura/pycrskrun"
    ]
)
