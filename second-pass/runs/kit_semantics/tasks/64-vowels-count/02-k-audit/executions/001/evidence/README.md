# Reviewer evidence

All executable reconstruction uses source copied into `/tmp/audit-work`.
`run_logged.sh` records the exact argv-rendered command, working directory,
timestamps, combined bounded output, and exit status for each material check.
Candidate-supplied logs and compiled definitions are not reused.
