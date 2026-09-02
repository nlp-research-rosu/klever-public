#!/usr/bin/env python3
"""List the candidate debug archive without extracting or executing it."""

import tarfile
from pathlib import Path

archive = Path("/candidate/kore-exec.tar.gz")
print(f"path={archive}")
print(f"size={archive.stat().st_size}")
with tarfile.open(archive, mode="r:gz") as bundle:
    members = bundle.getmembers()
    print(f"member_count={len(members)}")
    for member in members:
        print(
            f"type={member.type!r} size={member.size} "
            f"link={member.linkname!r} name={member.name!r}"
        )
        if member.name in {"kore-exec.sh", "kore-exec.log", "error.log"}:
            extracted = bundle.extractfile(member)
            if extracted is None:
                raise RuntimeError(f"cannot read {member.name}")
            text = extracted.read(10_001)
            if len(text) > 10_000:
                raise RuntimeError(f"unexpectedly large bounded member {member.name}")
            print(f"--- {member.name} (UNTRUSTED TEXT, NOT EXECUTED) ---")
            print(text.decode("utf-8", errors="replace"))
