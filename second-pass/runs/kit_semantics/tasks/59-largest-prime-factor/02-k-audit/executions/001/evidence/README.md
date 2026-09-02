# Reviewer evidence index

All executable work used source copied to `/tmp/audit-work/h59`; candidate
compiled directories were never copied or used.

- `provenance_check.py`, `provenance-check.log`, and the three
  `*-tree-manifest.json` files: launcher records, required hashes, symlink/type
  checks, candidate/trusted prompt and translator equality, and recursive
  supplied-semantics equality.
- `summarize_generation_trace.py` and `generation-trace-summary.log`: bounded
  structural parse of all 394 JSONL events.
- `translator-byte-identity.log`: trusted regeneration and byte comparison of
  `solution.mpy`.
- `differential_audit.py`, `differential-audit.log`, and
  `differential-inputs-results.json`: independent canonical-versus-generated
  execution on 4,342 recorded inputs.
- `toolchain.log`, `scratch-prepare.log`, `kompile-llvm.log`,
  `krun-concrete.log`, and `kompile-haskell.log`: fresh source reconstruction
  and concrete execution.
- `kprove-loop.log` and `kprove-complete-spec.log`: positive proof commands;
  each prints `#Top` and records exit 0. The complete spec contains both
  positive claims.
- `kprove-entry.log` and `kprove-entry-with-proved-loop.log`: bounded
  diagnostics showing that `--claims SPEC.entry` filters out the loop
  circularity; these are not candidate target commands and were terminated by
  the reviewer. The valid composition is the complete-spec proof.
- `extract_entry_module.py`, `program-pinning.log`, and
  `program-pinning-normalized.log`: mechanical constructor comparison. The
  first parse intentionally records why explicit `.Stmts` units cannot be
  parsed as a standalone program; removing only those five list identities
  yields identical KORE.
- `ground_claim_witness.py` and `ground-claim-witness.log`: satisfying states
  and concrete substitutions for both claim preconditions.
- `inventory_k.py`, `rule-inventory.tsv`, `assess_inventory.py`, and
  `rule-assessment.tsv`: exhaustive 932-declaration inventory and one
  assessment row per declaration. `rule-inventory-command-v2.log` records a
  shell-summary quoting error after the valid inventory had already been
  written; `rule-inventory-summary.log` and the v2 assessment are the final
  successful records.
- `make_false_mutation.py`, `spec-vacuity.k`,
  `false-mutation-dry-run.log`, and `false-mutation-proof.log`: fresh false
  result mutation, successful dry run, and expected stuck result 5 / exit 1.
- `make_body_mutation.py`, `spec-body-mutation.k`,
  `body-mutation-dry-run.log`, and `body-mutation-proof.log`: embedded program
  body mutation, successful dry run, and expected stuck result 4 / exit 1.

Every `run_logged.sh` record begins with the shell-escaped exact command and
ends with its status, except the two explicitly documented SIGINT diagnostics.
