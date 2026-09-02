# Lean audit-container compatibility note

The first required `tools.klean_preflight.check_generation` invocation reached
its temporary copied project but `lake clean` exited 1 with:

```text
error: could not detect the configuration of the Lake installation
```

After setting the pinned toolchain's `LAKE_HOME` and `LEAN_SYSROOT`, Lake
started, but Lean itself exited with:

```text
error: failed to locate application
```

The container exposes a PID namespace inconsistency:

- `getpid()` returns the namespace PID;
- `/proc/<namespace-pid>/exe` is absent; and
- `/proc/self` resolves to a different, visible host PID.

Lean 4.22 resolves its executable with `/proc/<getpid()>/exe`. The source in
`proc_pid_shim.c` returns the PID visible through `/proc/self`, restoring that
lookup. The successful audit run uses the exact pinned Lean toolchain and
unmodified copied generated project. The shim changes no source file,
declaration, target, manifest, or build output.

The raw initial failure is in `audit-checks-initial-failed.log`; the successful
rerun and returned preflight evidence are in `audit-checks.log`.
