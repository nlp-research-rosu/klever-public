# Independent adversarial audit: 19-sort-numbers

## Decision

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted translated program under the supplied semantics. It does not,
inside K, prove that the returned sequence is a numerically ordered permutation:
the result is constrained to the supplied opaque
`sortKeyVS(VS, numberKeyFunction)` primitive. The concrete semantics and
independent Python comparisons support that bridge only on finitely many inputs.
The formal entry domain also represents words with exactly one ASCII space,
whereas both Python implementations accept leading, trailing, and repeated
ASCII spaces.

Those are material but disclosed intent-bridge limitations, not proof-local
unsoundness or vacuity. The resulting classification is `CONCERNS / LEGIT`.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` directory is present, so the mounts do not
contradict the rendered mode.

The independent integrity scanner is
[stage1_integrity.py](evidence/scripts/stage1_integrity.py), with its exact
command, exit status, and output in
[stage1-integrity.log](evidence/stage1-integrity.log). It used `lstat` and a
recursive manifest without following links.

Results:

- All required candidate artifacts checked by the audit are regular files:
  `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `spec.k`, and
  `verification.k`.
- One structured JSONL trace is present as a regular file. All 375 records
  parsed; its event counts and hash are recorded in the Stage 1 log.
- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256 `61b0d963...e5c940`).
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (SHA-256 `406485ea...4db16`).
- The trusted and candidate semantics manifests each contain 25 entries.
  Missing: none. Additional: none. Changed or mistyped: none. Symlinked: none.
- No required top-level artifact was missing, changed, mistyped, or symlinked.
  Candidate-provided compiled definitions and caches were present but were
  explicitly ignored; they are not source-integrity evidence.

`run-input.json`, `metrics.json`, the 1.66 MB `codex-output.log`,
`codex-last.txt`, and the structured trace were read only as untrusted
generation claims. The scanner read the complete large log and trace and
recorded hashes, line/event counts, claim-pattern counts, first/last fragments,
and parse errors. Their assertions of `#Top`, mutation failures, and
“VALIDATED” did not enter the verdict.

Stage result: pass; no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt requires `sort_numbers(numbers: str) -> str`. The intended
input consists of the words `zero` through `nine`, space-delimited; the output
must contain those words ordered by numeric value from smallest to largest.
Duplicates are retained. The documented example maps `"three one five"` to
`"one three five"`.

The trusted canonical implementation splits on literal ASCII space, drops empty
tokens, performs a stable keyed sort using the ten-word rank dictionary, and
joins with one ASCII space. The submitted implementation uses Python's
whitespace-splitting `split()` and otherwise the same ten ranks and stable
`sorted(..., key=...)`. Thus it agrees on valid ASCII-space inputs, including
extra ASCII spaces. It is deliberately more permissive for tabs, newlines, and
nonbreaking spaces; those are outside the prompt's stated space-delimited
domain and are reported rather than hidden.

### Translation identity

The audit ran the trusted translator from scratch:

```text
python3 /tmp/audit-work/19-sort-numbers/trusted/py2mpy.py \
  /tmp/audit-work/19-sort-numbers/source/solution.py \
  > /tmp/audit-work/19-sort-numbers/regenerated-solution.mpy
cmp -s regenerated-solution.mpy source/solution.mpy
```

Translation and comparison both exited 0. Both files have SHA-256
`33a5008e...fc76d`. See
[stage2-translation.log](evidence/stage2-translation.log) and the preserved
[regenerated artifact](evidence/stage2-regenerated-solution.mpy).

### Independent differential testing

The reviewer-authored
[stage2_differential.py](evidence/scripts/stage2_differential.py) loads the
trusted canonical and candidate entry points independently. It does not import
candidate tests or reuse proof equations.

It ran 375 intended-domain cases:

- the documented example and empty input;
- every singleton word;
- all 100 ordered pairs, covering equality and every relative rank direction;
- ascending, descending, duplicate-heavy, leading-space, trailing-space,
  repeated-space, and spaces-only boundaries;
- 256 deterministic generated sequences of lengths 0 through 30.

There were zero mismatches and no exceptions. Complete inputs and results are
preserved in [stage2-inputs.json](evidence/stage2-inputs.json) and
[stage2-results.json](evidence/stage2-results.json); the command exited 0 in
[stage2-differential.log](evidence/stage2-differential.log).

Three separately labeled out-of-domain probes (`tab`, `newline`, and
nonbreaking-space separators) show the expected difference: the canonical
raises `KeyError`, while the candidate accepts and normalizes them. This does
not create an intended-domain divergence.

Stage result: pass.

## 3. Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/19-sort-numbers`. No candidate `*-kompiled` directory or cache
was copied or referenced. The audit used K v7.1.293 and Python 3.10.12; version
logs are under `evidence/toolchain-*-version.log`.

Fresh concrete compilation:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/19-sort-numbers/runtime-kompiled
```

This exited 0; see
[stage3-kompile-llvm.log](evidence/stage3-kompile-llvm.log).

Fresh proof compilation:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/19-sort-numbers/verification-kompiled
```

This exited 0; see
[stage3-kompile-haskell.log](evidence/stage3-kompile-haskell.log).

The compiler warnings identify existing non-exhaustive `total` declarations in
the supplied semantics. They are addressed in Stage 5; none blocks the used
domain.

Each positive claim was selected and run independently with:

```text
kprove spec.k \
  --definition /tmp/audit-work/19-sort-numbers/verification-kompiled \
  --spec-module SPEC --claims SPEC.<label>
```

The following 11 labels each printed `#Top` and exited 0:

| Label | Evidence |
|---|---|
| `sort-numbers` | [entry log](evidence/stage3-proof-sort-numbers.log) |
| `key-zero` | [log](evidence/stage3-proof-key-zero.log) |
| `key-one` | [log](evidence/stage3-proof-key-one.log) |
| `key-two` | [log](evidence/stage3-proof-key-two.log) |
| `key-three` | [log](evidence/stage3-proof-key-three.log) |
| `key-four` | [log](evidence/stage3-proof-key-four.log) |
| `key-five` | [log](evidence/stage3-proof-key-five.log) |
| `key-six` | [log](evidence/stage3-proof-key-six.log) |
| `key-seven` | [log](evidence/stage3-proof-key-seven.log) |
| `key-eight` | [log](evidence/stage3-proof-key-eight.log) |
| `key-nine` | [log](evidence/stage3-proof-key-nine.log) |

The summary is
[stage3-key-claims-summary.log](evidence/stage3-key-claims-summary.log).

A reviewer-authored concrete harness, preserved as
[Python](evidence/stage3-concrete-witness.py) and
[MPY](evidence/stage3-concrete-witness.mpy), tested empty input, the prompt
example, duplicates, descending order, and repeated ASCII spaces. Fresh LLVM
execution ended with `.K`, empty stack, `NoExc`, and exit code 0; see
[stage3-concrete.log](evidence/stage3-concrete.log).

Stage result: pass.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

For every finite `ValSeq` whose elements are exactly the ten permitted string
values, the precondition supplies:

- input equal to the elements joined by exactly one ASCII space;
- environment 0;
- a scope-0 binding of `"sort_numbers"` to `sortNumbersFunction`, with the
  supplied builtins as parent;
- empty heap and stack, next scope location 1, next heap location 0, no pending
  return or exception, and exit code 0.

If execution terminates, the postcondition requires:

- return value
  `str(joinCodes(space, sortKeyVS(VS, numberKeyFunction)))`;
- heap object 0 equal to the split input list and heap object 1 equal to the
  opaque keyed-sort result;
- next heap location 2;
- restored environment, scopes, scope location, empty stack, no pending return
  or exception, and exit code 0.

This is an equality-like reachability destination, not a one-way implication
about an unconstrained return. `sortKeyVS` is opaque but is a fixed function of
the input sequence and exact key closure; the returned value is not a fresh
existential or free variable.

### Key claims in plain language

Each of the ten claims starts an exact call to the submitted key lambda with one
specific numeral word, in the real caller frame and with arbitrary continuation
`CONT`. It executes the dictionary literal and lookup and returns the
corresponding integer 0 through 9 before the same continuation, preserving the
arbitrary heap, heap location, and exit code and restoring call state. There is
no loop claim because the submitted source contains no loop.

The key claims are true auxiliary execution theorems. The entry proof itself
can close without using them because the Haskell proof semantics does not
execute calls inside opaque `sortKeyVS`; this is part of the trust limitation,
not hidden circularity.

### Pinning to the submitted program

The entry starts after module loading, but its binding is not a substituted
algorithm:

- trusted translation is byte-identical to submitted `solution.mpy`;
- the `sortNumbersBody` macro is a syntax-only copy of that exact AST;
- `sortNumbersFunction` is the fixed semantics' corresponding closure;
- a fresh load claim starts with the exact `Module(FuncDef(...))` shape and
  proves that it produces precisely the entry binding without changing any
  other cell.

That claim printed `#Top` and exited 0. The source and log are
[stage4-audit-pinning.k](evidence/stage4-audit-pinning.k) and
[stage4-program-pinning.log](evidence/stage4-program-pinning.log).

### Satisfying states and substituted results

`VS = .ValSeq` is an immediate satisfying witness: `validNumberWords` reduces
to true, the input is the empty string, and both Python implementations return
the empty string. The audit also substituted the prompt sequence and a
duplicate-heavy sequence into the exact formal RHS. Under the supplied
`sortKeyVS` stable-key-sort contract, all substituted results equal both Python
implementations. Exact encodings and outputs are in
[stage4-satisfying-witnesses.log](evidence/stage4-satisfying-witnesses.log).

The K proof theory itself cannot reduce that opaque primitive. A separate,
true concrete strengthening of the prompt example to the literal result
`"one three five"` builds but exits 1 with `WarnStuckClaimState`; its residual
contains the unreduced `sortKeyVS` in both the return and heap. This is
intent-bridge evidence, not a failure of the candidate's actual claim. See
[probe source](evidence/stage4-audit-adequacy-probe.k) and
[probe log](evidence/stage4-adequacy-probe.log).

Adequacy result: the theorem pins the real program and its fixed-semantics
result, but its bridge to numeric sorting is conditional. The exact-one-space
formal domain is also narrower than all behavior accepted by the Python code.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored inventory generator is
[stage5_inventory.py](evidence/scripts/stage5_inventory.py). It read all 23
supplied helper K sources, the supplied assembler `semantics.k`,
`verification.k`, and `spec.k`, and emitted one line-addressed decision row per
declaration or rule.

The exhaustive [TSV inventory](evidence/stage5-rule-inventory.tsv) has 952 rows:

- 232 syntax declarations;
- 703 rules;
- 11 claims;
- 5 evaluation contexts;
- 1 configuration;
- 0 aliases and 0 `functional` declarations.

It classifies 148 function declarations, 109 `total` declarations, 25
opaque/symbolic declarations, 45 priority rules, 35 concrete-only rules, 27
`owise` rules, 7 macro declarations, and exactly one simplification rule. The
human-readable opaque/priority/simplification extracts are in
[stage5-rule-inventory-summary.md](evidence/stage5-rule-inventory-summary.md).
Every row includes source location, complete collapsed declaration/rule,
attributes, program relevance, and an assessment. The exact construct-to-rule
map is [stage5-used-construct-map.md](evidence/stage5-used-construct-map.md).

### Candidate-local extensions

The candidate adds:

1. Three macros (`sortNumbersBody`, `sortNumbersFunction`,
   `numberKeyFunction`). They add syntax expansions, not equations. The
   expansions match the translated AST.
2. `isNumberWord(Val) [function,total]`. The string case recognizes exactly the
   ten code sequences; the `owise` case handles non-strings. Cases are disjoint
   and exhaustive.
3. `validNumberWords(ValSeq) [function,total]`. Empty/cons cases are exhaustive,
   and recursion strictly descends on the tail.
4. One simplification:
   `splitWS(joinCodes(space, VS), empty, empty) => VS` under
   `validNumberWords(VS)`.

The split rule is an operational bridge only at the fixed semantics' pure
helper level. Its complete matched context is the three-argument function term;
there are no cells, bindings, stack, continuation, state changes, exceptions,
or abrupt control effects. Its guard forces every element to be a nonempty
whitespace-free numeral string. Structural induction on `VS`, using the supplied
`joinCodes`, `splitWS`, `flushTok`, `isWSC`, `seqConcat`, and `valSeqConcat`
equations, establishes the rewrite. Because it is a true equation, enclosing
term context does not broaden its justification.

For an independent operational check, the audit compiled a baseline Haskell
definition importing `MPY` but not `VERIFICATION`. In that baseline:

- empty, two-valid-word, and comma-actual-result claims printed `#Top`;
- the comma result was the single token `"one,two"`;
- a false claim that comma behaves like space exited 1 with
  `WarnStuckClaimState` on the concrete `"one,two"` residual.

Sources and logs:
[positive probes](evidence/stage5-audit-bridge-baseline.k),
[positive log](evidence/stage5-bridge-baseline-positive.log),
[false boundary](evidence/stage5-audit-bridge-boundary-false.k), and
[false log](evidence/stage5-bridge-boundary-false.log). The baseline compilation
command exited 0 in
[stage5-kompile-baseline-haskell.log](evidence/stage5-kompile-baseline-haskell.log).

There are no candidate priority rules, K-cell operational shortcuts,
proof-local opaque symbols, answer-encoding sort equations, or ordinary
semantic rules.

### Used supplied rules

The static path follows the submitted AST:

1. exact function binding and scope lookup;
2. callee-before-arguments and left-to-right argument evaluation;
3. split receiver evaluation and allocation at heap 0;
4. exact annotated key-lambda creation;
5. fixed `sorted(..., key=...)` dispatch and allocation at heap 1;
6. join receiver/argument dereference and pure separator fold;
7. return, frame pop, and restoration of all control cells.

The ten key claims additionally exercise dictionary keys and values
left-to-right, the priority-45 dictionary subscript rule, `dGet`, integer
results, and continuation-preserving return. Allocation, scope, heap, return,
exception, and stack footprints agree with the entry postcondition.

The concrete-only priority-40 keyed-sort rules are absent from the proof
definition. In `MPY-KRUN` they call the real key closure for each element,
stable-insert by integer key, allocate the output, and preserve duplicates.
Their role is finite bridge evidence only.

### Opaque symbols, totality, overlap, and priorities

Twenty-four opaque/symbolic declarations are unrelated float/MD5/unkeyed-sort
primitives and are unreachable here. The one relevant opaque declaration is:

```text
sortKeyVS(ValSeq, Val)
  [function, total, symbol(sortKeyVS), no-evaluators]
```

It is supplied, not candidate-added. It does not state a false equation or
encode this task's answer, and it produces a deterministic abstract value.
However, its claimed meaning as stable ascending sort by real callable results
is assumed. The correct concrete adequacy probe's failure demonstrates exactly
what K does not derive.

The fresh compilers warned that supplied `mapStrVS`, `floorFI`, `toF`, `ceilF`,
`joinCodes`, and `valSeqAt` are non-exhaustive despite `total`. On the submitted
path, `joinCodes` receives only string elements when structurally evaluated;
the others are unreachable. In uncovered cases these functions remain abstract
rather than enabling a false equality. This is a narrower coverage gap, not an
unsoundness claim.

Candidate function guards are disjoint/exhaustive. Baseline rules and the split
bridge agree on their overlap. Supplied priority rules used by this program
select heap dereference, dictionary subscript, and concrete keyed sort in the
intended contexts. No conflicting RHS or answer-smuggling rule was found.

No rule is labeled unsound, so there is no purported false-conclusion witness
to supply. The opaque-sort issue is reported as an assumption/evidence gap
instead.

Stage result: sound on the formal domain, with the opaque-sort concern.

## 6. Fresh non-vacuity test

The audit did not reuse candidate `spec-vacuity.k`. The fresh mutation
[stage6-false-result.k](evidence/stage6-false-result.k) preserves the entry
precondition and every state obligation but replaces the returned string by the
distinct value `noneV`.

The witness `VS = .ValSeq` satisfies the precondition, and both Python
implementations return `""`, not `None`.

First, the mutation was built without execution:

```text
kprove /audit-output/evidence/stage6-false-result.k \
  --definition /tmp/audit-work/19-sort-numbers/verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT --dry-run
```

This exited 0; see
[stage6-false-result-dry-run.log](evidence/stage6-false-result-dry-run.log).

The same command without `--dry-run` exited 1 with
`WarnStuckClaimState`. The residual contains the actual
`str(joinCodes(space, sortKeyVS(...)))` return and all expected final cells; it
fails because that `str` does not unify with `noneV`, not because of parsing,
imports, timeout, or an unrelated crash. See
[stage6-false-result-proof.log](evidence/stage6-false-result-proof.log).

Stage result: pass; the entry theorem is result-discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Conditional on the supplied semantics and the audited split equation, for
every finite sequence of the ten exact numeral strings represented with one
ASCII space between elements, execution from the exact post-load submitted
function state has the following partial-correctness result:

- the return is exactly
  `str(joinCodes(space, sortKeyVS(VS, exactKeyClosure)))`;
- split and sorted allocate exactly the two claimed list objects;
- heap location advances from 0 to 2;
- binding, environment, stack, return, exception, and exit-code cells finish in
  the claimed normal state.

Separately, exact execution of the key closure maps each permitted word to its
integer rank for any continuation admitted by the claims.

The proof is about the submitted program: translation identity, exact macro
expansion, and the successful load-pinning claim connect the file to the entry
state. The fresh `noneV` mutation demonstrates that the returned value is
constrained.

### Trust ledger

| Boundary | Effect and dependents | Judgment |
|---|---|---|
| Supplied MPY semantics | Defines all execution, state, and control used by every claim. | Acceptable foundational boundary in `SUPPLIED_SEMANTICS`; candidate tree is exactly the trusted mount. Its subset model and warned uncovered total-function cases remain explicit limitations. |
| `sortKeyVS(VS, KV)` | Determines the entry return and heap object 1; Haskell does not call `KV` or prove ordering/permutation. | Concerning but not illegitimate. It is a supplied primitive, not a proof-local answer rule. The ten key claims, concrete `#ksort`, and 375 Python comparisons provide finite/conditional support, not a universal theorem. |
| Candidate split simplification | Determines that split of the symbolic single-space join returns `VS`; entry claim depends on it. | Acceptable. Guarded pure equation with a complete induction, no state/control footprint, and independent baseline boundary checks. |
| Exact-body macros | Connect the entry binding and key symbol to program AST. | Acceptable. Syntax-only, textually exact, backed by translator byte identity and fresh load-pinning proof. |
| Trusted translator | Connects `solution.py` to submitted `.mpy`. | Acceptable empirical/tool boundary; byte identity was independently regenerated. |
| K compiler/backends v7.1.293 | Compile and execute every formal artifact. | Standard foundational toolchain trust; all commands and outputs are preserved. |
| Trusted canonical Python and CPython 3.10.12 | Support natural-language alignment on tested inputs. | Finite evidence only; never substituted for K proof. |
| Interpretation of “space-delimited” | Formal claim uses exactly one ASCII space and includes empty sequence. | Adequacy limitation. Python behavior for extra ASCII spaces is tested but not universally proved by the entry claim. Non-ASCII whitespace is outside the stated domain and differs from canonical behavior. |
| Termination | Needed to turn partial correctness into total correctness. | Not proved. The report makes no total-correctness claim; finite concrete executions terminate normally. |

### Gate accounting

- Real-program soundness: pass. Exact bodies execute under fixed semantics;
  proof-local equations are sound; state/control footprints match; the result
  is constrained; the fresh false result is rejected.
- Intent adequacy: pass with documented limitations. Numeric-order/permutation
  depends on the supplied opaque sort contract, and the formal whitespace
  domain is narrower than all accepted Python inputs.
- Evidence auditability: pass. Reviewer artifacts, exact commands, statuses,
  full differential inputs/results, independent baseline probes, rule
  inventory, and hashes are under `evidence/`. The hash manifest is
  [stage7-evidence-manifest.log](evidence/stage7-evidence-manifest.log).

The candidate therefore proves a sound fixed-semantics characterization of the
real program and is not vacuous or substituted. The opaque keyed-sort bridge
prevents a clean `PASS`, but because it is a named supplied primitive with a
faithful concrete leg—not an unsound candidate extension—the correct decision
is `CONCERNS / LEGIT`, not `FAIL`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
