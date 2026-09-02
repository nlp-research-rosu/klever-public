# Independent adversarial audit: 99-closest-integer

Decision: **FAIL / NOT_LEGIT**.

The fresh K proof does close and is non-vacuous, but it proves a handwritten
copy of the function body rather than the submitted `solution.mpy`. A fresh
body-sensitivity test changed the submitted scratch program to `return 777`;
after rebuilding from source, the unchanged target proof still returned
`#Top`. In addition, the proof's `nearestAway` expression is not the requested
closest-integer result for all valid decimal strings. These are material
real-program-pinning and intent-adequacy failures, not tool or infrastructure
failures.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. This is internally consistent, so
there is no infrastructure breach and the candidate verdict markers are
appropriate.

I recursively compared `/candidate/reference-semantics` against the trusted
tree with `diff --no-dereference -r`, independently listed the type of every
entry, and searched for symlinks. The trees are byte-identical, have the same
directory/regular-file entry types, contain no missing or additional semantics
entries, and contain no symlinks. The candidate did not modify the supplied
semantics. See [01-integrity.log](evidence/01-integrity.log).

The candidate copies of `prompt.py` and `py2mpy.py` are byte-identical to their
trusted mounted versions:

- `prompt.py`: SHA-256
  `53ad185333496f1faa011070d323b24af3e23506e32f52ced0b3c0f9867d2719`;
- `py2mpy.py`: SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

Four specifically requested generation/provenance artifacts are absent from
the candidate:

- `run-input.json`;
- `metrics.json`;
- `codex-last.txt`;
- `codex-output.log`.

No structured generation trace was present. Therefore those untrusted claims
could not be inspected. This is a provenance/evidence gap, but it is not the
basis for converting a tool uncertainty into the verdict. The candidate also
contains an untrusted `__pycache__`; it was ignored and not copied into the
audit build.

All source artifacts used for execution were copied to
`/tmp/audit-work/99-closest-integer-audit`. No candidate-built definition or
cache was copied or reused. The read-only integrity procedure is preserved as
[01_integrity_check.sh](evidence/01_integrity_check.sh), and tool/source hashes
and versions are in [07_environment.log](evidence/07_environment.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt requires a function on a string representing a number. It
must return the closest integer; exact half-way cases round away from zero.
Thus `14.5` maps to `15`, `-14.5` maps to `-15`, and ordinary non-ties map to
the nearer integer.

The trusted canonical implementation parses with Python `float`. After a
special trailing-zero normalization, textual values ending in `.5` use
`ceil`/`floor`; other nonempty values use Python `round`.

The candidate instead parses with Python `float`, adds `0.5` for positive
values or subtracts `0.5` otherwise, and truncates with `int`. This is a
different algorithm, which would be acceptable if it agreed on the intended
domain.

### Trusted translation

I regenerated `solution.mpy` from `solution.py` with the trusted
`/reference/py2mpy.py`. The regenerated and submitted files have identical
SHA-256
`03b8b5404453ce9bc22c44f48cde9d11866c6be1cd4ce147f6a40c0781579e3`;
`cmp` exited 0. Exact commands and status are in
[02_regenerate_solution.log](evidence/02_regenerate_solution.log).

### Independent differential test

[02_differential.py](evidence/02_differential.py) independently imports the
trusted canonical entry point and the candidate entry point. It covers the
documented examples, the empty string, zero and sign-branch boundaries,
positive and negative half boundaries, trailing-zero spellings, alternate
numeric spellings, 1,020 deterministic decimal cases around integer/half
boundaries, and representative exponent forms. The complete 1,034 inputs and
per-input results are preserved in
[02_differential_inputs.json](evidence/02_differential_inputs.json) and
[02_differential_results.json](evidence/02_differential_results.json).

The test exited 1 because it found nine candidate/canonical divergences. Some
reflect quirks of the canonical parser on exponent/trailing-zero spellings, so
I also used an independent exact `Decimal` half-away-from-zero oracle. Two
candidate results conflict with both the canonical implementation and the
literal mathematical contract:

| Input | Candidate | Trusted canonical | Exact decimal contract |
|---|---:|---:|---:|
| `"0.49999999999999994"` | 1 | 0 | 0 |
| `"-0.49999999999999994"` | -1 | 0 | 0 |

These are valid finite decimal strings and are not half-way cases. Binary
floating-point addition rounds `number ± 0.5` before `int` truncates it, which
causes the error. The full bounded output is
[02_differential.log](evidence/02_differential.log). This is a material
implementation-versus-contract divergence on the intended domain.

## 3. Clean proof reconstruction

K `v7.1.337` and Python `3.10.12` were used. From the clean scratch source copy
I ran:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit 0; see
[03_kompile_runtime.log](evidence/03_kompile_runtime.log). The compiler emitted
non-exhaustiveness warnings in unused/general supplied helpers, but built the
definition.

```text
krun smoke.mpy --definition runtime-kompiled
```

Exit 0 with `.K`, empty stack/heap, `NoExc`, and exit code 0; see
[03_krun_smoke.log](evidence/03_krun_smoke.log).

```text
kompile verification.k --backend haskell \
  --main-module CLOSEST-INTEGER-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit 0; see
[03_kompile_verification.log](evidence/03_kompile_verification.log).

There is one positive target claim, in module `CLOSEST-INTEGER-SPEC`. I ran it
independently:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module CLOSEST-INTEGER-SPEC
```

It printed `#Top` and exited 0. See
[03_kprove_spec.log](evidence/03_kprove_spec.log). Therefore clean closure
under the assembled theory is confirmed; no prior candidate trace or compiled
definition was trusted.

As an additional diagnostic, a ground Haskell proof attempted to reduce the
concrete Float hook and failed with the backend's explicit “missing hook:
FLOAT.int2float” error
([04_ground_kprove.log](evidence/04_ground_kprove.log)). This was not a target
claim and is not treated as candidate failure. The independently built LLVM
definition successfully executed corresponding ground assertions for `"10"`
and `"0.49999999999999994"` in
[04_ground_concrete.log](evidence/04_ground_concrete.log).

Because the mode is supplied rather than generated semantics, no
generated-semantics validation route was invoked.

## 4. Adequacy and real-program pinning

### Plain-language claim

The entry claim has no explicit `requires` clause. Its precondition is every
term `CS:IntSeq` in the exact initial configuration:

- current environment 0;
- empty module scope 0 whose parent is builtin scope -1;
- `scopeLoc` 1;
- empty heap with `heapLoc` 0;
- empty stack;
- `noRet`, `NoExc`, and exit code 0.

It executes `runClosest(str(CS))`. The postcondition demands the exact integer
term `nearestAway(decStrToF(CS))` in `<k>`, with every other listed cell
restored unchanged. It is equality/result-constraining, not a free result,
tautology, or one-way implication.

A satisfying pre-state is obtained with
`CS = iCons(49, iCons(48, .IntSeq))`, the codes for `"10"`, and the listed
initial cells. Both Python implementations return 10 for this input, and the
fresh LLVM execution succeeds. For the also-satisfying valid decimal input
`"0.49999999999999994"`, the candidate and LLVM execution return 1 while the
trusted canonical and exact contract return 0. Thus the claimed expression is
not the intended result for every satisfying intended input.

### Failure to execute the submitted program

The claim does not load or execute the submitted `solution.mpy`:

- it never uses `Module(...)`;
- it never executes the submitted `FuncDef(...)`;
- neither `spec.k` nor `verification.k` reads or requires `solution.mpy`;
- `runClosest` directly constructs
  `closureVal(("value", .ParamNames), closestBody(), 0)`;
- `closestBody()` is a handwritten proof-local reproduction of the current
  body.

The reproduction currently matches the translated body, but byte comparison
outside K is not a connection theorem and creates no source dependency.

The fresh sensitivity test
[04_pinning_test.sh](evidence/04_pinning_test.sh) replaces the scratch
`solution.py/.mpy` with a trusted translation of:

```python
def closest_integer(value):
    return 777
```

It then rebuilds `verification-kompiled` from source and reruns the unchanged
target. `kprove` still prints `#Top` and exits 0, while Python prints `777`.
See [04_pinning_test.log](evidence/04_pinning_test.log). This is a concrete
witness that proof closure is insensitive to the submitted program body. It
meets the decision boundary's “proves a substituted program” failure case.

There are no loops, loop invariants, helper claims, or auxiliary reachability
claims. The fixed semantics does execute the copied closure's calls, assignment,
branch, and return; the problem is program identity, not a hidden loop summary.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[05_build_inventory.py](evidence/05_build_inventory.py) mechanically extracted
every top-level declaration from the fresh sources. The complete unabridged
inventory is [05_rule_inventory.md](evidence/05_rule_inventory.md) and
[05_rule_inventory.json](evidence/05_rule_inventory.json):

- 1,102 records total;
- 698 ordinary rules;
- 230 syntax blocks;
- five contexts;
- one configuration and one claim;
- 22 `[no-evaluators]` opaque symbols;
- 35 `[concrete]` rule blocks;
- 45 priority rule blocks;
- 26 `[owise]` rule blocks;
- no `[functional]` or `[simplification]` declarations.

Every fixed supplied declaration/rule is tagged as in or out of this program's
slice. Unused rules cannot contribute to this target; they are accepted only
as the byte-identical supplied baseline selected by the rendered mode, not as
candidate proof-specific reasoning. The detailed construct mapping,
configuration/control review, overlap review, and local decisions are in
[05_used_construct_review.md](evidence/05_used_construct_review.md).

### Used fixed-semantics path

For the copied body, the supplied rules implement:

1. closure invocation and one fresh local scope;
2. left-to-right callee/argument evaluation;
3. lookup of `float` and `int` through the builtin scope;
4. binding of `value`;
5. conversion to `decStrToF(CS)`;
6. assignment to local `number`;
7. comparison through `gtF`;
8. complementary true/false branches;
9. `addF` or `subF`, followed by `truncF`;
10. return, frame pop, scope deletion, and restoration of all framed cells.

No heap allocation, output, or modeled exception occurs on those symbolic
paths. Relevant type cases are disjoint. Duplicate mixed-float/type rules in
the supplied `float.k` have identical right-hand sides. Relevant priority rules
for cell/reference handling have false guards in this plain scalar frame and
do not preempt the ordinary path.

The proof uses the supplied opaque total primitives `decStrToF`, `gtF`,
`addF`, `subF`, and `truncF`. Their `[concrete]` twins call K Float hooks. The
symbolic theorem uses identical opaque applications on the execution and
postcondition sides, so it establishes structural equality without deriving
IEEE-754 facts.

### Exhaustive proof-local review

There are exactly three proof-local syntax symbols and three equations:

| Extension | Classification and decision |
|---|---|
| `closestBody()` and its sole equation | Total definitional term, complete, terminating, non-overlapping, and truthful for the copied current body. It does not formally depend on `solution.mpy`. |
| `runClosest(Str)` and its sole equation | A test-harness rewrite that invokes fixed call semantics on `closestBody`. It preserves binding, evaluation order, frame state, and return control for the copied body. It has no connection theorem to the submitted `Module/FuncDef`; the pinning witness shows the gap. |
| `nearestAway(Float)` and its sole equation | Total definitional summary, complete, terminating, and non-overlapping. It does not replace execution; it restates exactly the same opaque operations used by the copied body. It is not an independent closest-integer theorem. |

There are no proof-local priority, simplification, loop, allocation, exception,
or auxiliary-claim rules.

I do not label any of these equations mathematically unsound on its declared K
domain, so there is no unsupported “unsound rule” allegation requiring a false
rule witness. The material defects are narrower and evidenced:

- source/program-identity inadequacy, witnessed by the `return 777` rebuild;
- a false natural-language interpretation of `nearestAway`, witnessed by
  `"0.49999999999999994"`.

The fixed supplied decimal model itself documents only digits, a decimal
point, and optional leading minus. It does not model Python exponent notation,
whitespace, leading plus, or conversion exceptions. A concrete K program
asserting the real Python result for `"5e-1"` ends in `AssertionError` and exit
code 1 in [05_semantics_gap.log](evidence/05_semantics_gap.log), while Python
returns 1. This is a supplied-semantics/Python bridge limitation, not a
candidate-modified rule, but the all-`IntSeq` entry claim does not acknowledge
it.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present or trusted. I created the fresh
mutation [06_spec_false.k](evidence/06_spec_false.k), changing the required
result from:

```text
nearestAway(decStrToF(CS))
```

to:

```text
nearestAway(decStrToF(CS)) +Int 1
```

This is false for the satisfying input `"10"`: the original result is 10 and
the mutation demands 11.

First, `kprove ... --dry-run` exited 0, proving that the mutation parsed and
built successfully
([06_false_dry_run.log](evidence/06_false_dry_run.log)). The actual proof then
exited 1 with `WarnStuckClaimState` and an unmet equality of the form
`truncF(addF(...)) +Int 1 = truncF(addF(...))`; see
[06_false_kprove.log](evidence/06_false_kprove.log). This is the expected
reachable result obligation, not a parser error, missing import, timeout, or
unrelated crash.

The target is therefore discriminating and result-constraining. Non-vacuity
does not repair its source-identity or contract-adequacy failures.

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Under the supplied MPY theory plus the three local definitions, for every
`CS:IntSeq` in the exact initial configuration, symbolic execution of the
manually constructed closure body reaches:

```text
#if gtF(decStrToF(CS), 0.0)
#then truncF(addF(decStrToF(CS), 0.5))
#else truncF(subF(decStrToF(CS), 0.5))
#fi
```

with the listed environment, scope allocator, heap, stack, return, exception,
and exit cells restored. `nearestAway` is merely a name for that expression.
This is a legitimate non-vacuous partial-correctness theorem about the copied
K body, conditional on the fixed opaque primitives.

It does **not** establish that:

- `solution.mpy` is the program executed by the claim;
- changing the submitted source changes or invalidates the proof;
- the returned integer is mathematically closest for every valid numeric
  string;
- the supplied `decStrToF` matches CPython `float` on every string accepted by
  Python;
- invalid-input exceptions match Python;
- the program terminates outside the partial-correctness interpretation.

### Trust ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| Byte-identical supplied semantics and K builtins/backend | All execution and proof steps | Acceptable as the rendered supplied baseline; reconstructed from source. |
| `decStrToF`, `gtF`, `addF`, `subF`, `truncF` opaque proof symbols | Both copied-body execution and `nearestAway` | Acceptable only for the structural, interpretation-parametric theorem. Their Python/IEEE meaning is not proved. LLVM tests are finite evidence. |
| Concrete K Float hooks | Smoke and ground K runs | Empirical bridge only; Haskell cannot reduce `Int2Float`, as the quarantined diagnostic shows. |
| Trusted translator | Submitted/regenerated `solution.mpy` identity | Byte identity is established, but it does not connect that file to `runClosest`. |
| Handwritten equality between `closestBody` and the current translated body | Real-program identity | Illegitimate as the sole pinning mechanism; no K dependency/connection claim, and the mutation witness proves body insensitivity. |
| Interpretation of `nearestAway` as the requested closest integer | Natural-language correctness | Illegitimate: unproved and concretely false on the valid decimal witnesses above. |
| Trusted canonical and exact `Decimal` oracle | Program-to-intent evidence | Finite differential evidence only, not a K proof. It is sufficient to expose concrete counterexamples. |
| Missing generation/provenance files | Auditability of the generation history | Concerning evidence gap, but not needed for the decisive technical failures. |

### Verdict rationale

Fresh `#Top`, honest fixed-semantics execution of the copied body, and a
successful non-vacuity challenge are all positive evidence. They cannot
substitute for proof of the submitted program. The body-sensitivity experiment
shows that a materially different `solution.mpy` leaves the theorem unchanged,
which is exactly the decision boundary's substituted-program case. Separately,
the candidate returns a provably non-closest result on valid decimal inputs, so
the postcondition named `nearestAway` does not supply the required correctness
property.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
