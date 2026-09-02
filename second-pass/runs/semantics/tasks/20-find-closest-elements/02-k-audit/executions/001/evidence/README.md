# Audit evidence index

Every numbered run has a `.cmd`, `.log`, and `.status` file produced by
`run_logged.sh`. Status files contain the exact process exit code.

- `01`: provenance/type/tree/hash integrity.
- `02`: trusted translation and byte comparison.
- `03`: independent differential run; complete corpus is
  `differential_inputs.json`.
- `04`–`06`: clean LLVM/Haskell builds and the positive `#Top`.
- `07b`, `22`: corrected exhaustive inventory and per-row audit decisions.
  `07` is the first inventory run; `07b` corrects guard capture.
- `08`–`10`: exact-function-AST concrete harness and fixed-semantics LLVM run.
- `11`: optional ground Haskell claim; it exits 1 on the documented missing
  `FLOAT.gt` Haskell hook. This is not used as a candidate verdict.
- `12`–`14`: LLVM proof-extension build/run and concrete equation substitution.
- `15`: submitted-program body-sensitivity mutation; wrong `solution.mpy`
  still yields `#Top`.
- `16`–`17`: false-postcondition build succeeds and proof fails as expected.
- `18`–`21`: displaced-loop operational-sensitivity mutation. `20` was an
  initial reviewer expectation error: a list literal becomes a heap ref and
  lies outside the bridge's unboxed-list match. `20b` records the corrected
  interpretation. The mutated symbolic proof remains `#Top`; fixed execution
  and the canonical oracle materially diverge on `[1.0, 10.0, 2.0]`.
- `23`–`27`: bridge removal. `25` used a spec that still required the original
  module and therefore had a duplicate-module parse error; `26` corrects the
  spec, and `27` is the bounded residual run.

Reviewer-authored scripts, mutations, ground specs, the used-construct map, and
the trust ledger are preserved alongside these logs.
