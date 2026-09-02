#!/usr/bin/env python3
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory(prefix="lake-subprocess-debug-") as temporary:
    project = Path(temporary) / "project"
    shutil.copytree("/reference/klean-generation/generated", project)
    for command in (["lake", "clean"], ["lake", "build"]):
        print(f"COMMAND={command!r}")
        print(f"LD_PRELOAD={os.environ.get('LD_PRELOAD')}")
        result = subprocess.run(
            command,
            cwd=project,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print(f"EXIT={result.returncode}")
        print(result.stdout)
