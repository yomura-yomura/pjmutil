import subprocess
import re
import numpy as np


patterns = [
    (" JOB NAME", "(.+)"),
    (" STATE", "(.+)"),
    (" ELAPSE TIME (LIMIT)", r".+ \((\d+)\)"),
    (" ELAPSE TIME (USE)",   r".+ \((\d+)\)"),
    (" REASON", "(.+)"),
    (" EXIT CODE", "(.+)")
]

data_types = {
    "job_name":   f"U",
    "state":      f"U",
    "limit_time": "m8[s]",
    "use_time":   "m8[s]",
    "reason":     f"U",
    "exit_code":  "i8"
}

proc = re.compile(
    "\n".join([
        re.escape("[Job Statistical Information]"),
        *(
            rf"{re.escape(k)}\W+: {p}"
            for k, p in patterns
        )
    ])
)

available_pjstat_items = {
    "job_name":   "jnam",
    "state":      "st",
    "limit_time": "elpl",
    "use_time":   "elp",
    "reason":     "ermsg",
    "exit_code":  "ec"
}


def to_ma_array(data, missing_value):
    if len(data) > 0:
        dtype = [
            (field, f"{type_}{max(map(len, col))}" if type_ in ("U", "S") else type_)
            for col, (field, type_) in zip(zip(*data), data_types.items())
        ]
    else:
        dtype = np.dtype(list(data_types.items()))

    a = np.ma.empty(len(data), dtype=dtype)
    for col, name in zip(zip(*data), a.dtype.names):
        a[name].mask = [e == missing_value for e in col]
        a[name][~a[name].mask] = [e for e in col if e != missing_value]
    return a


def get_job_info(job_name_pattern=None, show_history=False):
    pjstat_options = ["s"]
    if show_history:
        pjstat_options.append("H")

    args = [
        "pjstat",
        "-{}".format("".join(pjstat_options)),
        "--choose={}".format(",".join(available_pjstat_items.values()))
    ]
    if job_name_pattern is not None:
        args.extend(["--filter", f"jnam={job_name_pattern}"])

    result = subprocess.run(args, stdout=subprocess.PIPE)
    return to_ma_array(proc.findall(result.stdout.decode()), missing_value="-")
