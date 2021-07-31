from setuptools import find_packages, setup
import pathlib
import json


config_dir = pathlib.Path.home() / ".pjmutil"
config_dir.mkdir(exist_ok=True)
config_path = config_dir / "config"

if not config_path.exists():
    default_result_dir = pathlib.Path.home() / "pjmutil"
    config = dict(
        resource_groups=None,
        time_limits=None,  # seconds
        bash_profile_file=str(pathlib.Path.home() / ".bash_profile"),

        crsk_path=None,
        crsk_output_path=default_result_dir/"corsika",
        crsk_runner_name=None,

        tjv_log_path=default_result_dir/"tajava"/"log"
    )

    with config_path.open("w") as f:
        json.dump(config, f, indent=4)


setup(
    name='pjmutil',
    version='4.2.2',
    description='',
    author='yomura',
    author_email='yomura@hoge.jp',
    url='https://github.com/yomura-yomura/pjmutil',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            "pjm-logfile-foreach = pjmutil.scripts.pjm_logfile_foreach:main",
        ],
    },
    package_data={"pjmutil": ["throw_processes/template-run-batch-job.txt"]},
    include_package_data=True,
    install_requires=[
        "numpy",
        "colorama",
        "pycrskrun @ git+https://github.com/yomura-yomura/pycrskrun"
    ]
)
