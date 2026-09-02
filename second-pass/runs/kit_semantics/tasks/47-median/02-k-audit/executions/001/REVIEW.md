# Independent adversarial review: 47-median

## Executive finding

The candidate has a reproducible, non-vacuous K reachability proof of the
submitted `solution.mpy` **under the supplied MPY theory**. All ten entry claims
close independently from a fresh Haskell build, the program term is mechanically
pinned to `solution.py`, and there is no candidate-added operational bridge.

It is nevertheless not a legitimate proof of the benchmark program contract.
The submitted Python program changed the canonical divisor from `2.0` to `2`.
That is observable on an unbounded, model-representable `Int` input:

```text
input = [10**308, 10**308]
trusted canonical: OverflowError
submitted Python:  1e308 (0x1.1ccf385ebc8a0p+1023)
supplied MPY:       Infinity
```

The first difference is candidate-versus-canonical on a value class represented
by the fixed model. The second shows that the proof's result-bearing `divII`
primitive does not denote submitted CPython behavior at that same input.
`PROOF.md` contains only a general warning about untested float/rounding edges;
it gives no concrete divergence witness and also calls the even result the
model's “exact Python numeric average.” Thus the campaign amendment's
documented-supplied-model-gap exception does not apply. More decisively, that
exception expressly does not protect a submitted program that diverges from
canonical on a model-representable input.

The docstring's `15.0` example is independently wrong: canonical and submitted
Python both return `8.0`. The candidate explicitly reported that contradiction,
so campaign amendment 2 would make that issue alone `CONCERNS / LEGIT`. It does
not cure the separate divisor and numeric-model failures.

## 1. Input and provenance integrity

### Records and mounts

`/audit-input.json` declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, and
`mount_reference_semantics = true`. I read:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the sole structured trace JSONL below
  `/generation-evidence/codex-trace/`.

The trace has 487 valid JSON objects, one session id, and the expected terminal
task-complete event. Generation prose and prior `#Top` reports were not used as
authority.

`/audit-campaign-lock.json` is byte-hash correct and its parsed object exactly
equals the `audit_campaign` block in `/audit-input.json`. All launcher-recorded
hashes having direct mounted-file targets match. The trusted prompt, canonical,
translator, all required pipeline records, prompt record, usage record, and
trace file match their recorded SHA-256 values. See
[01-provenance.log](evidence/01-provenance.log) and the reviewer script
[provenance_check.py](evidence/provenance_check.py).

### Candidate/reference comparison

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- `/reference/reference-semantics` is present as required.
- Candidate and trusted reference-semantics trees have identical relative
  entries, file types, modes, and contents. There are no missing, additional,
  changed, mistyped, special, or symlinked entries.
- No symlink occurs anywhere in `/candidate`, `/reference`, or
  `/generation-evidence`.

The independent recursive semantics manifest contains 25 entries and has
reviewer digest
`c37bad009b1b81c192611ecb7fc84f92ab1bceda1017b64fc4d97707e1301f20`.
Candidate proof-source hashes and an independent manifest of all 840 candidate
regular files are in
[01-candidate-source-hashes.log](evidence/01-candidate-source-hashes.log).

The candidate's precompiled `runtime-kompiled`,
`verification-kompiled`, and mutant definition were ignored. Only source
artifacts were copied to `/tmp/audit-work/47-median`.

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From `/reference/prompt.py` and `/reference/canonical.py`: sort the input list
ascending; return its center element when its length is odd; otherwise return
the true-division average of the two center elements. Canonical spells the even
division as `/ 2.0`. Empty input, incomparable elements, or unsupported center
arithmetic can raise rather than return a median.

The second docstring example is self-contradictory. Sorting
`[-10, 4, 6, 1000, 10, 20]` gives
`[-10, 4, 6, 10, 20, 1000]`, hence canonical returns `(6 + 10) / 2.0 = 8.0`,
not the documented `15.0`.

### Translation and proof-term regeneration

The exact commands were:

```bash
python3 /tmp/audit-work/47-median/trusted/py2mpy.py \
  /tmp/audit-work/47-median/candidate-src/solution.py \
  > /tmp/audit-work/47-median/regenerated-solution.mpy
cmp regenerated-solution.mpy candidate-src/solution.mpy

(cd candidate-src &&
  python3 generate_program_k.py solution.py) \
  > /tmp/audit-work/47-median/regenerated-program.k
cmp regenerated-program.k candidate-src/program.k
```

Both `cmp` commands exited 0. The submitted and regenerated MPY files share
SHA-256
`657af2d20b8f454d508a964dacc06c04e7aa1d98626a0c05743e1316824bbdcb`;
the submitted and regenerated program K files share
`efa842f53b4f636abcd57639e0825f5e64f6b6f9ba0a7ee9d42d7152a54dba4f`.
Full output is in
[02-fidelity-differential.log](evidence/02-fidelity-differential.log).

### Independent differential

[differential.py](evidence/differential.py) imports the trusted canonical and
submitted entry points independently. It covers both examples, empty and
singleton lists, odd/even boundaries, duplicates, negative numbers, booleans,
mixed int/float/bool values, signed zero, infinities, NaNs, large integers,
strings, incomparable values, complex values, nested lists, and generated
products over ten numeric boundary atoms through length three.

Command:

```bash
python3 /audit-output/evidence/differential.py
```

Result: 1,135 built-in cases, one mismatch, exit 1:

```text
BUILTIN_MISMATCH
  huge_int_divisor_literal_divergence
  canonical = OverflowError
  generated = float 1e308
```

The cause is exact source text:

- `/reference/canonical.py:18`: `/ 2.0`
- `/candidate/solution.py:13`: `/ 2`

This is a model-representable `Int` input and the source contract has no integer
magnitude bound. Campaign amendment 1 explicitly leaves such
program-versus-canonical divergence at `FAIL / NOT_LEGIT`.

The differential also records two unrepresented numeric-object divergences:
`Fraction` produces a `float` canonically but a `Fraction` in the candidate,
and `Decimal` raises canonically but returns a `Decimal` in the candidate.
Those are not needed for the verdict because the built-in `Int` witness is
already decisive.

The docstring contradiction was confirmed separately:

```text
documented=15.0 canonical=8.0 generated=8.0
```

## 3. Clean proof reconstruction

Tool versions are preserved in
[00-toolchain.log](evidence/00-toolchain.log): K 7.1.293 and Python 3.10.12.

### Fresh Haskell definition

From `/tmp/audit-work/47-median/candidate-src`, with no candidate-built
definition on the command line:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition \
    /tmp/audit-work/47-median/fresh-verification-kompiled
```

It exited 0. The only messages were unused-variable warnings in `str.k`.
See [03-kompile-haskell.log](evidence/03-kompile-haskell.log).

Every positive claim was then run independently, not only as an aggregate:

```bash
kprove spec.k \
  --definition /tmp/audit-work/47-median/fresh-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.<label>
```

Each of the following exited 0 and printed exactly one `#Top`:

| Claim | Exit | `#Top` lines |
|---|---:|---:|
| `median-odd` | 0 | 1 |
| `median-even-int-int` | 0 | 1 |
| `median-even-int-bool` | 0 | 1 |
| `median-even-bool-int` | 0 | 1 |
| `median-even-bool-bool` | 0 | 1 |
| `median-even-float-float` | 0 | 1 |
| `median-even-int-float` | 0 | 1 |
| `median-even-float-int` | 0 | 1 |
| `median-even-bool-float` | 0 | 1 |
| `median-even-float-bool` | 0 | 1 |

The runner and summary are
[run_positive_claims.sh](evidence/run_positive_claims.sh) and
[03-positive-claims-summary.log](evidence/03-positive-claims-summary.log);
the ten complete bounded logs are adjacent in `evidence/03-kprove-*.log`.

### Fresh LLVM definition and concrete execution

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/47-median/fresh-runtime-kompiled
```

This exited 0. Its non-exhaustiveness warnings concern deliberately partial
helpers such as out-of-bounds `valSeqAt`; that totalization is included in the
trust accounting below. See
[03-kompile-llvm.log](evidence/03-kompile-llvm.log).

The independently authored
[concrete_smoke.py](evidence/concrete_smoke.py) passed in CPython, translated
with the trusted translator, and reached `<k> .K </k>`, `<exc> NoExc </exc>`,
and `<exit-code> 0 </exit-code>` with the fresh LLVM definition. It covers both
branches and every built-in center class used by representative claims. See
[03-concrete-smoke.log](evidence/03-concrete-smoke.log).

Clean reconstruction therefore confirms the candidate's narrow claim:
`#Top` is real under the supplied theory. It does not resolve the theory-to-
CPython and candidate-to-canonical divergences.

## 4. Adequacy and real-program pinning

Let `S = sortVS(VS)` and `L = vsLen(S)`. Every claim also requires `HL` not to
be a key of arbitrary initial heap `HP`, starts with the exact module binding
`"median" |-> solutionMedianClosure`, empty stack, `noRet`, `NoExc`, and exit
code 0. Every post-state adds exactly `HL |-> list(S)`, increments `heapLoc`,
and preserves the other observable cells.

The entry claims mean:

| Claim | Additional precondition | Required result |
|---|---|---|
| odd | `L > 0`, `L % 2 = 1` | `S[(L-1)/2]` |
| int/int | even; centers `I1`, `I2` | `divII(I1+I2, 2)` |
| int/bool | even; centers `I`, `B` | `divII(I + bool(B), 2)` |
| bool/int | even; centers `B`, `I` | `divII(bool(B) + I, 2)` |
| bool/bool | even; centers `B1`, `B2` | `divII(bool(B1)+bool(B2), 2)` |
| float/float | even; centers `F1`, `F2` | `divFloatIntV(addF(F1,F2),2)` |
| int/float | even; centers `I`, `F` | `divFloatIntV(addF(intToF(I),F),2)` |
| float/int | even; centers `F`, `I` | `divFloatIntV(addF(F,intToF(I)),2)` |
| bool/float | even; centers `B`, `F` | promoted float sum divided by 2 |
| float/bool | even; centers `F`, `B` | promoted float sum divided by 2 |

[claim_witnesses.py](evidence/claim_witnesses.py) gives a distinct satisfying
ground state for every precondition with `HP = {}` and `HL = 0`. All ten
witnesses have the required sorted center types and agree between canonical and
submitted Python on those small values. The command exited 0; see
[04-claim-witnesses.log](evidence/04-claim-witnesses.log).

### Program-term identity

`generate_program_k.py` parses the sole `median` function, uses the trusted
translator emitter, checks the capture-free one-parameter signature, and emits
the exact closure body. Fresh regeneration is byte-identical to submitted
`program.k`; fresh translation is byte-identical to submitted `solution.mpy`.
Thus the claim executes the submitted function binding/body, not a hand-written
summary. The nullary `solutionMedianClosure` equation merely names that exact
closure and does not match a `<k>` cell.

A fresh body-sensitivity test changed the odd return to `0`, regenerated the
closure actually bound by the mutant claim, and produced a constructor-level
diff at the return term. The mutant definition compiled with exit 0; its claim
requiring the original result `2` for `[3,1,2]` failed with exit 1 and residual
`<k> 0 ~> .K </k>`. Evidence:

- [audit-solution-mutant.py](evidence/audit-solution-mutant.py)
- [audit-program-mutant.k](evidence/audit-program-mutant.k)
- [04-body-program-term.diff](evidence/04-body-program-term.diff)
- [04-kompile-body-mutant.log](evidence/04-kompile-body-mutant.log)
- [04-body-mutation-proof.log](evidence/04-body-mutation-proof.log)

Pinning therefore passes. Intent adequacy does not: the pinned body differs
materially from canonical, and its K numeric result differs from its own CPython
execution at the huge-int witness.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[rule_inventory.py](evidence/rule_inventory.py) inventories every local
`syntax`, configuration, context, equation, operational rule, and target claim
in the supplied semantics tree, `program.k`, `verification.k`, and `spec.k`.
The complete 1,026-record table is
[05-rule-inventory.tsv](evidence/05-rule-inventory.tsv). Counts:

| Kind | Count |
|---|---:|
| syntax declarations | 245 |
| configuration | 1 |
| contexts | 5 |
| equational rules | 510 |
| operational rules | 255 |
| target claims | 10 |

Attribute-bearing inventory records include 162 `function`, 114 `total`, 24
`no-evaluators` opaque declarations, 27 `symbol`, 60 `concrete`, 48 priority,
28 `owise`, four macro, and two strict/seqstrict declaration groups. There are
zero local `functional` and zero simplification rules. Summary and exit 0 are
in [05-rule-inventory-summary.log](evidence/05-rule-inventory-summary.log).

The table decides each record as one of:

- 766 fixed-semantics records outside every target dependency;
- 186 reviewed operational/mathematical records in the execution slice;
- 61 records associated with supplied result-bearing model boundaries;
- one concrete fixed-model false-behavior witness (`divII`);
- two justified proof-local closure declaration/equation records;
- ten target claims, which are goals rather than assumptions.

The unused fixed-semantics records do not rewrite any term reachable in these
claims and contribute no equation to their results. Their global CPython
coverage is not claimed by this theorem. This is distinct from dismissing a
false rule used on the target path.

### Construct-to-rule map and control/state review

The actual constructor flow is:

```text
Call/Name
  -> scope lookup -> callee/left-to-right argument evaluation
  -> exact closure frame + parameter binding
  -> docstring expression discard
  -> Assign ordered = sorted(l)
       -> supplied sortVS + one fresh heap allocation
  -> Assign size = len(ordered)
  -> integer %, ==, If branch
  -> ref dereference + normalized indexing
  -> odd return, or typed addition + true division
  -> Return/#pop, restoring env/scopeLoc/stack/ret
```

Relevant declarations and rules occur in:

- `syntax.k`: `Expr`, `CmpOp`, `Exprs`, `Stmt`, `Stmts`, `Params`,
  `ParamNames`, and the used constructors;
- `core.k`: configuration/cells, allocation, statement sequencing, lookup,
  builtins scope, argument order, literals, truth, dispatch, promotions, and
  length helpers;
- `call.k` and `functions.k`: normal callee lookup, argument evaluation,
  closure invocation, frame push, parameter binding, return, and pop;
- `controls.k`: assignments, expression discard, and `If`;
- `sort.k` and `builtins.k`: `sorted`, `sortVS`, allocation, `len`, and
  `seqLen`;
- `operators.k`, `int.k`, `bool.k`, and `float.k`: evaluation order,
  parity/comparison, typed addition, promotion, and division;
- `subscript.k`: ref dereference, `normIdx`, `applyIndex`, and `valSeqAt`;
- `str.k`: evaluation of the ASCII docstring literal.

Evaluation is left-to-right where material, the selected `median` binding is
explicit, the active continuation is empty, the sorted copy is allocated once,
the input is not mutated, and the claim explicitly tracks every active state
cell. No helper or loop claim replaces control flow. There is no loop.

### Proof-local extensions

`verification.k` only imports `MEDIAN-PROGRAM`; it adds no rule. The sole
proof-local function is:

```k
syntax Val ::= "solutionMedianClosure" [function, total]
rule solutionMedianClosure => closureVal("l", exactBody, 0)
```

It is nullary, exhaustive, terminating, non-overlapping, pure, and generated
from the exact source AST. It is a justified definitional name, not an
operational bridge or result oracle. The ten claims do not serve as lemmas for
one another.

### Result-bearing supplied boundaries

The target depends on these fixed-model boundaries:

- `sortVS`: opaque symbolic ascending/stable sort and implicit length
  preservation; concrete int/string/mixed-numeric insertion-sort legs;
- total opaque `valSeqAt(sortVS(...), i)`;
- opaque float/numeric functions `divII`, `addF`, `intToF`, and
  `divFloatIntV`, plus numeric comparison during concrete sorting;
- `[total]` declarations which let opaque symbolic results remain defined.

These are fixed supplied-model primitives, not candidate-written proof rules.
Finite smoke tests can support them but cannot prove their universal CPython
meaning.

### Concrete false-conclusion witness for the used numeric rule

The used concrete equation at `reference-semantics/semantics/float.k:31` is:

```k
divII(I1, I2)
  => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11)
```

Take `I1 = 2 * 10**308`, `I2 = 2`. It concludes `Infinity`, because the
numerator is converted to binary64 before division. Submitted CPython evaluates
the corresponding int/int expression to finite `1e308`.

This witness is executable and preserved twice:

- [05-model-gap-huge-int.log](evidence/05-model-gap-huge-int.log): the same
  assertion passes in CPython and fails under fresh MPY with `AssertionError`;
- [05-model-gap-huge-int-observe.log](evidence/05-model-gap-huge-int-observe.log):
  CPython records `1e308` while the final MPY scope records
  `"observed" |-> Infinity`.

Thus the candidate's postcondition term is result-constraining in K, but its
claimed Python interpretation is false on an intended, represented input.
This is not an unconstrained candidate oracle; it is a material supplied-model
behavior gap. The amendment would downgrade such a gap only if it were
explicitly ledgered with a concrete divergence witness, covered all model
inputs, and the submitted program were canonical-faithful on the gap. The
candidate has no such witness, and its `/ 2` program is not canonical-faithful.

An additional globally inaccurate but target-unused supplied rule is the float
`>=` encoding as `not floatLt`: with `NaN >= 0.0`, it yields true although
CPython yields false. It does not occur in the median dependency slice and is
not used to derive any target result; it is recorded as an unused fixed-model
limitation rather than a separate target-proof defect.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh mutation
[audit-vacuity.k](evidence/audit-vacuity.k) changes the even Int/Int result from
`divII(I1+I2,2)` to `divII(I1+I2+1,2)`. The state with input `[1,3]`,
`HP = .Map`, and `HL = 0` satisfies the entry precondition; canonical and
submitted Python both return `2.0`, whereas the mutation denotes `2.5` under
the supplied concrete contract.

Commands:

```bash
kprove audit-vacuity.k \
  --definition /tmp/audit-work/47-median/fresh-verification-kompiled \
  --spec-module AUDIT-VACUITY --dry-run

kprove audit-vacuity.k \
  --definition /tmp/audit-work/47-median/fresh-verification-kompiled \
  --spec-module AUDIT-VACUITY
```

The dry run exited 0, proving the mutation parsed and built. The proof exited 1
with `WarnStuckClaimState`; its unmet implication is exactly:

```text
divII(I1 + I2 + 1, 2) #Equals divII(I1 + I2, 2)
```

This is a reachable, result-bearing failure, not a parser error, crash, timeout,
or unrelated stuck term. Full evidence is
[06-fresh-vacuity.log](evidence/06-fresh-vacuity.log). The K proof is therefore
non-vacuous.

## 7. Proven versus assumed accounting

### What the successful K proof actually establishes

Under the supplied theory and the exact starting cells, executing the submitted
closure on any symbolic `VS` satisfying one of the ten preconditions reaches
the corresponding structural result term, allocates `list(sortVS(VS))` at the
fresh location, increments `heapLoc`, and restores all call/control cells. The
theorem is unbounded in list length and is sensitive to both body and
postcondition mutations.

It does **not** by itself establish that every opaque result term has CPython
meaning, that the submitted function is canonical-faithful, or that the wrong
docstring example is correct.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K 7.1.293 compiler/prover/backend | all proof closure | platform trust; fresh builds/runs |
| trusted `py2mpy.py` | program constructor identity | byte-identical regeneration; body mutation |
| `solutionMedianClosure` equation | selected body/binding | fully defined proof-local name; justified |
| fixed call/control/heap rules | order, frames, allocation, final cells | executed directly; no bridge |
| supplied `sortVS` | parity, indexes, result, allocated heap value | external result-bearing primitive; finite support only |
| supplied total `valSeqAt` | selected median values | external totalized primitive; intended indexes are in bounds conditionally on sort contract |
| supplied float/numeric primitives | every even result | external result-bearing primitives; concrete counterexample for `divII` |
| canonical-to-docstring interpretation | intended example | contradiction confirmed and explicitly reported |
| canonical-to-submitted program fidelity | benchmark ground truth | **fails** on represented huge ints |

### Gate accounting and decision

- Fixed-theory verification: **PASS** — ten fresh independent `#Top` results.
- Proof-local extension/pinning/non-vacuity: **PASS** — exact body, no
  operational bridge, meaningful negative mutations.
- Source/canonical fidelity: **FAIL** — `/ 2` versus `/ 2.0` changes observable
  behavior on `[10**308, 10**308]`.
- Language-model adequacy: **FAIL** — `divII` yields `Infinity` where submitted
  CPython yields `1e308`.
- Evidence/trust-boundary adequacy: **FAIL** — the candidate supplied no
  concrete witness for this fixed-model gap, and its own finite differential
  coverage missed it.
- Docstring contradiction handling: **acceptable concern**, not a candidate
  defect, because canonical and candidate agree on `8.0` and the contradiction
  was reported.

The reconstructed `#Top` is thus an honest theorem about the supplied symbolic
terms, but not a legitimate partial-correctness proof of the benchmark's real
canonical program behavior. The explicit campaign rule for a candidate program
that diverges from canonical on model-representable inputs fixes the mapping.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
