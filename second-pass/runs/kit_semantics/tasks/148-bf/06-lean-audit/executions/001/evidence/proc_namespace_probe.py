#!/usr/bin/env python3

import os


pid_path = f"/proc/{os.getpid()}/exe"
print(f"pid={os.getpid()}")
for path in (pid_path, "/proc/self/exe"):
    try:
        print(f"{path} -> {os.readlink(path)}")
    except OSError as error:
        print(f"{path} -> ERROR {error!r}")
