import pathlib


template_run_batch_job_script = open(pathlib.Path(__file__).parent / "template-run-batch-job.txt").read()


def load(resource_group, memory_limit, time_limit, log_path, bash_profile_path, python_code):
    return template_run_batch_job_script.format(
        resource_group=resource_group,
        memory_limit=memory_limit,
        time_limit=time_limit,
        log_path=log_path,
        bash_profile_path=bash_profile_path,
        python_code=python_code
    )
