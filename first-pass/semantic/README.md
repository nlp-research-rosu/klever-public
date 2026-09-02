# Reference semantics — the copy-select library for `.mpy` proofs

[`src/`](src/) holds the **authoritative** version of every `.mpy` construct, split
RV-style into one module per file ([`mpy-core.k`](src/mpy-core.k),
[`mpy-operators.k`](src/mpy-operators.k), …) and assembled by
[`src/semantics.k`](src/semantics.k) (the kompile entry — it just `requires` + `imports`
the pieces as `module MPY`). Each problem's own minimal `semantics.k` (under
[`../questions/`](../questions/)) is **cut from** these modules — not imported from them.

## Why copy-select, not import

Each problem's semantics must be **minimal**: only the constructs its `.mpy` uses may
be reducible, so that *every expressible reduction is sound* (the minimal-semantics
rule — see [../NOTES.md](../NOTES.md)). If a problem `imports`ed the whole reference it
would inherit constructs it never uses, breaking that guarantee. So:

- **Copy** the `MPY-CORE` block + only the syntax productions and rules the problem's
  `.mpy` actually contains, into the problem's `semantics.k`.
- **Rename** the modules from `MPY` / `MPY-SYNTAX` to the problem
  (e.g. `BELOW-ZERO` / `BELOW-ZERO-SYNTAX`).
- The reference is the **single source of truth** for *how* each construct is written,
  so the same rule never drifts between problems.

## What to copy

The file list at the top of [`src/semantics.k`](src/semantics.k) maps each construct
cluster to its file; copy from the relevant `src/mpy-*.k`. (The split is for the
reference's own navigability — a per-problem cut is still single-file and trimmed below
file granularity, because minimality requires dropping individual `Val` variants and
`applyBin`/`applyCmp` cases, which importing a whole module cannot do.)

`MPY-CORE` ([`mpy-core.k`](src/mpy-core.k)) is required by every problem — but "required"
still means **copy selectively**,
not verbatim. The scope heap, configuration, load/sequencing, and `Name` lookup are
copied as-is; the **`Val` sort skeleton** you trim to the value variants the `.mpy`
actually produces (drop `seq(IntSeq)` with no lists, `closureVal` with no functions, …).
Then pull each non-core unit your `.mpy` mentions:

| `.mpy` uses… | copy unit(s) |
| --- | --- |
| `Int(…)` / `Bool(…)` | Int / Bool literals |
| `UnaryOp("-", …)` | UnaryOp |
| `ListExpr(…)` | ListExpr (+ `appendVal`, `vals2seq` helpers) |
| `BinOp`/`AugAssign` arithmetic | `applyBin` (add the operator case you need) |
| `Compare(…, CmpOp(op, …))` | Compare (add the `op` case to `applyCmp`) |
| `Assign` / `AugAssign` | Assign / AugAssign |
| `If(…)` | If (+ `truthy`) |
| `For(…)` / `While(…)` / `break` / `continue` | For (unified `#loop` over list/str/tuple/range) / While / loop control (`<lstack>`) |
| `FuncDef` / `Call` / `Return` | Functions (frame-skip `#ret` / `#pop` return model) |
| `len` / `sum` / `abs` / `min` / `max` / `ord` / `chr` / `str` / `range` | Builtins (`isBuiltinName` + `applyBuiltin`; make the user-`Call` rule `[owise]`) |
| `Assert(…)` (smoke only) | Assert (+ `truthy`) |

Add only the `applyBin` / `applyCmp` *cases* (`"+"`, `"<"`, `"=="`, …) the program
actually evaluates — not the whole operator table.

## Maintenance

- An **improvement** to a construct (e.g. the frame-skip `#pop` return model, the loop
  stack) lands **here first**, then is propagated to the problems that copied it.
- The reference **grows**: it is seeded from HumanEval/3 and now covers the language core
  (Bundles A–G — all done) plus `break` / `continue` and the builtin-call family
  (`len` / `sum` / `abs` / `min` / `max` / `ord` / `chr` / `str`). Remaining gaps vs the unmodified
  canonicals are tracked in [`CANONICAL-GAPS.md`](CANONICAL-GAPS.md). It is split into one
  module per file under [`src/`](src/); a new construct cluster lands as a new `mpy-*.k`.
- It is kept **kompilable + tested**. Two test kinds under [`tests/`](tests/):
  - **`tests/semantics/<case>/`** — execution tests: `<case>.py` is a CPython oracle paired
    with `<case>.mpy` (what K runs); both must pass, so each is differential. Run all with
    [`tests/run.sh`](tests/run.sh) (krun; passes only if `<k> => .K`).
  - **`tests/verification/<case>/`** — proof demos (e.g. `loop-break`): a self-contained
    `semantics.k` / `verification.k` / `spec.k` that `kprove`s a property. Run all with
    [`tests/verify.sh`](tests/verify.sh) (memory-capped kprove; passes on `#Top`).

  ```sh
  bash verification/humaneval/reference/tests/run.sh      # semantics (CPython oracle + K)
  bash verification/humaneval/reference/tests/verify.sh   # verification (kprove => #Top)
  ```

  After editing a test's `.py`, regenerate its `.mpy`:

  ```sh
  python3 scripts/py2mpy.py tests/semantics/<case>/<case>.py > tests/semantics/<case>/<case>.mpy
  ```

The golden per-problem proof template is [`../questions/3-below-zero/`](../questions/3-below-zero/)
(it shows the `verification.k` / `spec.k` layout); `tests/verification/loop-break/` is the
smallest worked proof.
