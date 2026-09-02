# Audit commands

The Python files named below are retained beside their raw terminal transcripts.
They import executable code only from the trusted `/reference/tools` package;
no candidate or provenance producer source was executed.

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/check_context_and_producers.py
```

Result: [`00-context-and-producer-integrity.log`](00-context-and-producer-integrity.log), exit 0.

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/reconstruct_inventory.py
```

Result: [`01-inventory-reconstruction.log`](01-inventory-reconstruction.log), exit 0.

The required preflight was first invoked without an environment workaround:

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/rerun_preflight.py
```

Result: [`02-preflight-rerun.log`](02-preflight-rerun.log), exit 1 because Lean's `/proc/<getpid()>/exe` lookup could not see its host-namespace PID.

The narrowly scoped environment shim was compiled and checked with:

```sh
gcc -shared -fPIC -O2 -Wall -Wextra -Werror -o /tmp/audit-work/libproc-self-exe.so /tmp/audit-work/proc_self_exe_shim.c -ldl
sha256sum /tmp/audit-work/proc_self_exe_shim.c /tmp/audit-work/libproc-self-exe.so
LD_PRELOAD=/tmp/audit-work/libproc-self-exe.so lean --version
```

Results: [`03a-build-proc-shim.log`](03a-build-proc-shim.log), [`03b-proc-shim-hashes.log`](03b-proc-shim-hashes.log), and [`03c-lean-environment-probe.log`](03c-lean-environment-probe.log), all exit 0. The source is retained at `/tmp/audit-work/proc_self_exe_shim.c`; the shim redirects only numeric `/proc/<pid>/exe` reads to `/proc/self/exe`.

The same required trusted function was then rerun, with only that process-environment correction:

```sh
LD_PRELOAD=/tmp/audit-work/libproc-self-exe.so PYTHONPATH=/reference python3 /audit-output/evidence/rerun_preflight.py
```

Result: [`04-preflight-rerun-with-proc-shim.log`](04-preflight-rerun-with-proc-shim.log), exit 0.

Independent hash, bijection, and target checks:

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/audit_stage4_integrity.py
```

Result: [`05-stage4-hashes-bijection-target.log`](05-stage4-hashes-bijection-target.log), exit 0.

Independent frozen-program and operational-semantics alignment checks:

```sh
python3 /audit-output/evidence/audit_semantic_alignment.py
```

Result: [`06-program-semantics-alignment.log`](06-program-semantics-alignment.log), exit 0.

Final report consistency check:

```sh
python3 /audit-output/evidence/validate_review.py
```

Result: [`07-review-validation.log`](07-review-validation.log), exit 0.
