# Independent adversarial audit: 129-minPath

## Decision

The candidate contains a legitimate, non-vacuous reachability proof of the
actual submitted `solution.mpy`, but the theorem is substantially narrower than
the HumanEval contract. It proves two concrete examples and all valid 2-by-2
grids only for `k = 4`; it does not prove arbitrary `N >= 2` or arbitrary
positive `k`. The proof is therefore legitimate but merits `CONCERNS`, not
`PASS`.

All candidate-built definitions, caches, prior logs, `#Top`, and prose were
ignored as proof authority. The dynamic checks below used only sources copied
to `/tmp/audit-work/129-minPath` and definitions rebuilt there.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted mount is consistent
with it: `/reference/reference-semantics` exists as a real directory. This is
not an infrastructure-error case.

The independent integrity script checked file types, symlinks, and SHA-256
digests recursively:

- All required candidate artifacts are present as regular files:
  `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `solution.py`, `solution.mpy`, `spec.k`, `verification.k`, `prompt.py`, and
  `py2mpy.py`.
- A structured trace is present under `codex-trace/`; it is a regular JSONL
  file, parses without JSON errors, and was treated only as an account of what
  generation claimed to have done.
- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`
  (`417c9ed7...29adb`).
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (`406485ea...db16`).
- The candidate and trusted `reference-semantics/` inventories each contain 26
  entries including directories. There are zero missing, additional,
  type-changed, byte-changed, or symlinked entries.
- No required-artifact integrity defect was found. Candidate-provided
  `runtime-kompiled/`, `verification-kompiled/`, `__pycache__/`, and prior
  output files were recognized as untrusted extra evidence and were not copied
  into or used by the reconstruction.

The untrusted generation metadata claims a successful, non-timeout generation,
a prior `#Top`, and a `SOUND-BUT-LIMITED` result. Those claims were scanned from
the complete log and 522-line JSONL trace but were not used to establish the
verdict.

Evidence:

- `evidence/check_integrity.py`
- `evidence/stage1-integrity.log` — command exit `0`
- `evidence/summarize_generation_claims.py`
- `evidence/stage1-generation-claims.log` — complete-file scan, command exit
  `0`

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt requires a square permutation grid of size `N >= 2`, with
each integer `1..N*N` appearing once, and positive `k`. A legal path visits
exactly `k` cells, moves only across shared edges, may revisit cells, and the
function returns the lexicographically least value sequence.

The trusted canonical implementation finds the cell containing the global
minimum `1`, computes the smallest value in its orthogonal neighborhood, and
returns an alternating sequence `1, neighbor, 1, neighbor, ...`.

The submitted implementation uses a different loop form but the same
algorithm:

1. scan the grid with nested `while` loops to locate `1`;
2. append each in-bounds orthogonal neighbor to a fresh list;
3. compute `min(neighbors)`; and
4. append `1` on even indices and that minimum neighbor on odd indices.

On the stated domain, this matches the natural-language problem. Every path's
first value is minimized by starting at the unique global minimum `1`. The
second value is minimized by selecting its smallest neighbor. From that
neighbor, returning to `1` is again optimal; induction gives the alternating
sequence. `N >= 2` ensures the cell containing `1` has at least two neighbors,
so the `min` input is nonempty.

### Translation identity

In scratch, the trusted translator was run as:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

The regenerated and submitted files have the same SHA-256,
`a7137b7b...1c6c67b`, and `cmp` returned `0`. Thus the K program is byte-for-byte
the trusted translation of the submitted Python source.

### Independent differential testing

`evidence/differential_audit.py` independently imports
`/reference/canonical.py` and the scratch copy of candidate `solution.py`. Its
scope was:

- both documented examples;
- all 24 valid 2-by-2 grids for every `k` from 1 through 8;
- all nine positions of `1` in a 3-by-3 grid, covering corner, edge, and
  interior truth values for all four neighbor guards;
- 400 deterministic generated grids across `N = 3, 4, 5` and
  `k = 1, 2, 3, 7, 12`;
- an independent exhaustive-walk oracle on 231 small cases; and
- four explicit beyond-contract empty/boundary probes.

There were 2,230 intended-domain comparisons, zero candidate/canonical
mismatches, and zero mismatches against the exhaustive-walk oracle. Two
empty-grid probes diverged: the canonical returns a value while the candidate
raises `ValueError`. Both violate `N >= 2`, so this is documented excluded
behavior, not an intended-domain defect. A valid 2-by-2 grid with `k = 0`
returned `[]` in both implementations, although `k = 0` is also outside the
prompt.

Evidence:

- `evidence/stage2-regeneration.log` — translator exit `0`, comparison exit `0`
- `evidence/differential_audit.py`
- `evidence/stage2-differential.log` — script exit `0`
- `evidence/stage2-differential-cases.json` — all inputs and per-case results

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/129-minPath`. No
candidate-built definition or cache was copied. The available tools were K
v7.1.293 and Python 3.10.12.

### Concrete definition and execution

The concrete definition was rebuilt from the verified semantics copy:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

Exit status was `0`. A fresh `concrete-check.mpy`, translated with the trusted
translator, contains the exact candidate function followed by assertions for
the examples and top, bottom, left, right, and interior neighbor cases:

```text
krun concrete-check.mpy --definition runtime-audit-kompiled
```

This exited `0` with final `.K`, `NoExc`, and exit code `0`.

One reviewer-authored expected value was initially mistyped as `2` for a center
cell whose actual smallest neighbor is `3`. That preliminary run correctly
raised `AssertionError`. The expectation alone was corrected, and both the
failed audit-input run and the final successful run are preserved. This was an
auditor test-data error, not candidate evidence and not a candidate defect.

### Proof definition and positive target

The proof definition was rebuilt independently:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

Exit status was `0`. An independent source scan found exactly one positive
claim, `SPEC.prompt-examples`, and no claim in `verification.k` or the supplied
semantics. It was run as:

```text
kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC
```

The command printed `#Top` and exited `0`. This is a fresh success signal; the
candidate's prior compiled definition and prior `positive.kprove.out` were not
used.

Evidence:

- `evidence/stage3-tool-versions.log`
- `evidence/stage3-kompile-llvm.log` — exit `0`
- `evidence/stage3-concrete-translate.log` — exit `0`
- `evidence/stage3-krun-concrete.log` — exit `0`
- `evidence/stage3-krun-concrete-author-test-error.log` — preserved preliminary
  reviewer error, exit `1`
- `evidence/stage3-kompile-haskell.log` — exit `0`
- `evidence/stage3-positive-claim-inventory.log` — one claim, exit `0`
- `evidence/stage3-kprove-positive.log` — `#Top`, exit `0`

## 4. Adequacy and real-program pinning

### Plain-language claim

The sole claim begins from the full initial MPY configuration. Its symbolic
precondition says that `A`, `B`, and `C` are pairwise-distinct integers in
`[2,4]`; consequently they are exactly a permutation of `2,3,4`.

The `<k>` cell loads one `minPath` function and sequentially asserts:

- result `[1,2,1]` for the first 3-by-3 prompt example;
- result `[1]` for the second 3-by-3 prompt example; and
- for `k = 4`, the appropriate
  `[1, min(neighbor1,neighbor2), 1, min(neighbor1,neighbor2)]` result for each
  of the four possible positions of `1` in a 2-by-2 grid.

The destination requires the computation to be consumed at `.K`, module
environment `0`, empty call stack, `noRet`, `NoExc`, and exit code `0`. Final
scope, heap, and heap-location values are existential because the theorem does
not constrain leftover allocation.

### Pinning and result constraint

The `FuncDef("minPath", ...)` embedded in the claim is textually identical to
the submitted `solution.mpy` function after normalizing only explicit versus
omitted `.Stmts` and `.Exprs` list units. Both normalized terms have length
1,750 and SHA-256 `955e6186...17e23`. The claim therefore executes the actual
submitted program; it does not substitute a summary or a different function.

There is no helper or loop claim. The fixed semantics executes every call,
lookup, loop, subscript, append, `min`, and return. Because the claim uses
executable `Assert(Compare(..., "==", expected))` statements and requires
`NoExc`/exit `0`, the returned lists must equal the stated results. They are not
free variables, tautologies, or one-way implications.

The entry precondition is satisfiable. With `A=2`, `B=3`, `C=4`, all six
asserted calls were evaluated by both Python implementations:

- the prompt calls produce `[1,2,1]` and `[1]`;
- the top-left, top-right, and bottom-left 2-by-2 cases produce `[1,2,1,2]`;
  and
- the bottom-right case produces `[1,3,1,3]`.

A fresh body-sensitivity check changed only `min(neighbors)` to
`max(neighbors)`. Concrete K execution then produced `[1,4,1]` for the first
example, raised `AssertionError`, set exit code `1`, and exited nonzero. This
supports that the real function body, rather than merely its name, determines
the proved result.

### Adequacy limitation

This is not a universal entry-point theorem. It is one top-level execution
claim containing six calls. It covers two ground 3-by-3 inputs and every valid
2-by-2 grid only at `k = 4`. It has no symbolic `N`, no arbitrary grid, no
arbitrary positive `k`, and no loop invariant establishing the implementation
for the full prompt domain. This material scope gap is the reason for
`CONCERNS`; it does not make the narrower theorem unsound.

Evidence:

- `evidence/check_claim_pinning.py`
- `evidence/stage4-claim-pinning.log` — identity check exit `0`
- `evidence/claim_witnesses.py`
- `evidence/stage4-ground-witnesses.log` — witness checks exit `0`
- `evidence/body-audit-mutant.py`
- `evidence/stage4-body-mutation-translate.log` — exit `0`
- `evidence/stage4-body-mutation-krun.log` — expected `AssertionError`, exit `1`

## 5. Rule-by-rule static soundness review

### Exhaustive inventory and provenance

`evidence/stage5-rule-inventory.log` contains the source location, complete
declaration/rule block, attributes, and provenance disposition for every
relevant K source record. Across the supplied semantics, `verification.k`, and
`spec.k`, it inventories:

- 695 rules;
- 227 syntax declarations;
- 107 declarations carrying `total`;
- 145 declarations carrying `function`;
- zero `functional` declarations;
- zero simplification rules;
- 45 priority rules;
- 35 concrete rules;
- 26 `owise` rules;
- 25 symbol/opaque declarations;
- one configuration and five contexts; and
- one target claim.

All 695 rules and all semantic syntax declarations come from the supplied tree
that is byte-identical to the trusted reference. `verification.k` contains only
`requires`, module/import, and `endmodule`: it defines zero syntax symbols,
functions, total declarations, ordinary rules, priority rules, simplification
rules, opaque symbols, lemmas, or auxiliary claims. There are no generated
helper K files. The one claim is the target theorem, not a rule used to prove a
different claim.

For each supplied rule, the inventory disposition is “trusted supplied
baseline; byte-identical candidate/reference; not a proof-local extension.”
This accepts the selected task semantics as the theorem's language model; it
does not claim a new proof that all 695 rules implement all of CPython. The
candidate made no semantic delta that could smuggle a task answer into that
baseline.

### Used-construct mapping and substantive path review

| Submitted/spec construct | Declaration and executing rules | Finding |
|---|---|---|
| `Module`, statement sequence | `syntax.k`; `core.k` `#loadAll` and `Stmts` sequencing | Exact module body is loaded in order; no program substitution. |
| `FuncDef`, `Call`, parameters, return | `functions.k` closure/bind/return/pop; `call.k` callee/left-to-right argument/frame rules | Actual body, binding, call stack, return value, environment restoration, and frame deallocation execute. |
| `Assign`, `Name`, integers | `controls.k` assignment; `core.k` scope lookup and integer literal rules | Locals are written/read in the current frame; builtins are found only after normal scope lookup. |
| `While` and `If` | `controls.k` `#while`, complementary truthy guards, and `#branch` | Conditions are evaluated each iteration; true/false guards are complementary. Fixed `N` and `k` make all submitted claim loops finite. |
| `BinOp` `+`, `-`, `%`; integer comparisons | `operators.k` evaluation/dispatch; `int.k` arithmetic and comparison equations | Operands evaluate before dispatch. Operators used here have exact integer rules; modulo divisor is the concrete nonzero value `2`. |
| Nested `Subscript` | `subscript.k` receiver/index contexts, heap dereference, `normIdx`, `applyIndex`, `valSeqAt` | Receiver then index evaluate; all claim accesses are in bounds due the scanned 2-by-2/3-by-3 grids and loop guards. |
| `ListExpr` and allocation | `list.k` argument evaluation and `#alloc`; `core.k` monotone heap allocation | Fresh grid rows, grids, neighbor lists, answers, and expected lists are allocated with explicit heap effects. |
| `Attribute(...,"append")` | `call.k` bound-method routing; `list.k` priority-40 append rule | The exact heap list is mutated in place and `noneV` is discarded by the expression-statement rule. |
| Builtins `len` and `min` | normal builtin binding in `core.k`; call dispatch and heap dereference in `call.k`; `builtins.k` length and iterator minimum folds | No name-based interception bypasses evaluation. `min` is seeded from the first actual neighbor and folds the nonempty neighbor list. |
| Returned/expected list equality | operand dereference in `operators.k`; list equality in `list.k`; assertions in `assert.k` | Both heap objects are compared by sequence structure; a false result sets `AssertionError` and exit code `1`. |
| `minInt` in expected terms | imported K integer theory, not a candidate-defined summary | It computes the mathematical minimum in the postcondition and is independent of program execution. |

The complete starting configuration supplies every cell read by these rules.
The proof destination checks control completion, stack, return state,
exception, and exit code; heap and scopes are framed existentially only after
the result assertions have consumed the returned lists.

The priority rules reached on this path are structural dereference/mutator
rules from the trusted semantics. Their more specific matches preempt generic
dispatch without changing the selected binding or skipping the function body.
The complementary `while`, `if`, integer-comparison, and iterator-minimum cases
do not introduce conflicting right-hand sides on the claim's domain.

### Totality, opaque symbols, and warnings

The 25 opaque/symbol declarations are:

`sortVS`, `sortKeyVS`, `md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`,
`powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, and `sqrtF`.

The submitted program and the claim contain no sort, float, hashlib, or MD5
construct, so none of these symbols can affect a branch, result, state change,
exception, or postcondition in this proof. They require no program-derived
connection theorem here because they are not reached.

LLVM compilation reports non-exhaustive total-function warnings for
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. The first
five are unused. `valSeqAt` is used, but only on explicit, finite list sequences
at provably in-range nonnegative indices in these six calls; its ordinary
equations reduce every such access. Out-of-bounds or opaque-sequence behavior
remains a semantics limitation outside this claim. No false conclusion witness
on the intended claim domain was found, so this is recorded as a narrower
trust/evidence limitation rather than mislabeled as an unsound rule.

`MPY-CONCRETE` is imported only by `MPY-KRUN` for the LLVM evidence. The
positive Haskell definition imports `MPY`, not `MPY-CONCRETE`; concrete-only
sort/deep-equality helpers did not contribute to `#Top`.

No inventoried rule encodes this task's answer, replaces the program with an
oracle, fabricates a used construct's result, or bypasses real execution. There
is therefore no candidate-local unsound rule and no false-conclusion witness to
report.

Evidence:

- `evidence/inventory_k_rules.py`
- `evidence/stage5-rule-inventory.log` — exhaustive inventory, exit `0`
- `evidence/stage3-kompile-llvm.log` — exact totality warnings
- `evidence/stage3-kompile-haskell.log` — proof-definition build

## 6. Fresh non-vacuity test

The candidate's `spec-vacuity.k` and prior failure output were inspected only
as untrusted evidence. A distinct reviewer-authored mutation was created from
the positive spec in scratch. It changes the last element required for the
bottom-right symbolic case from:

```text
minInt(B, C)
```

to:

```text
minInt(B, C) +Int 1
```

For the satisfiable precondition witness `A=2`, `B=3`, `C=4`, the real result is
`[1,3,1,3]`, while the mutation requires `[1,3,1,4]`.

First, the mutated spec was separately compiled to KORE:

```text
kprove spec-audit-vacuity.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-AUDIT-VACUITY \
  --dry-run
```

This exited `0`, excluding a parser, import, or module error. The live proof:

```text
kprove spec-audit-vacuity.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-AUDIT-VACUITY
```

exited `1` with `WarnStuckClaimState`. The reachable residual has `.K` but
`AssertionError` and exit code `1`, and explicitly contains the unmet
obligation `minInt(B,C) +Int 1 = minInt(B,C)`. This is the expected semantic
failure of a reachable false result constraint, not an unrelated crash or
timeout.

Evidence:

- `evidence/spec-audit-vacuity.k`
- `evidence/stage6-vacuity-dry-run.log` — exit `0`
- `evidence/stage6-kprove-vacuity.log` — expected stuck claim, exit `1`

## 7. Proven versus assumed accounting

### What is formally established

Under the supplied `MPY` semantics and K's imported theories, the exact
submitted function body executes from the standard initial configuration and
terminates without exception for the two prompt calls and all four symbolic
2-by-2 placements described in Stage 4. For every `A,B,C` satisfying the
precondition, all six returned lists equal the asserted results. The proof is
result-constraining and non-vacuous.

The theorem does not quantify over all valid grids or all positive path
lengths. It does not formally prove the informal induction from the alternating
sequence to the lexicographically minimum path on the full prompt domain.

### Trust ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| Supplied `reference-semantics/` | Defines every value, scope, heap, call, loop, list, builtin, assertion, and exception transition used by the reachability proof. | Acceptable mandated trust boundary. Candidate tree is byte/type identical. It is a Python subset, not a machine-checked equivalence to CPython. |
| K v7.1.293, Haskell backend, SMT integration, and imported integer/map/list theories including `minInt` | Compile and discharge the positive claim and mutation obligations. | Standard verification infrastructure assumption. Fresh build/proof outputs are preserved. |
| Trusted `py2mpy.py` | Connects candidate `solution.py` to K constructor syntax. | Acceptable task input; byte identity of regenerated `solution.mpy` removes candidate control over this bridge. |
| Final existential scopes/heap/heapLoc | Leaves allocation garbage and final internal maps unconstrained. | Acceptable for this pure HumanEval observation because return values are compared before discard and control/exception cells are fixed. It would not prove a stronger heap/resource property. |
| `valSeqAt` totality outside in-bounds concrete sequences and the other LLVM non-exhaustive warnings | Could matter for other programs or invalid accesses. | Concerning in the general semantics, but not reached outside defined equations in this claim. No intended-domain false witness. |
| The 25 opaque float/sort/MD5 symbols listed in Stage 5 | Potentially result-bearing in other programs. | No influence or dependent claim here; all are unreachable from this source/spec. |
| CPython runs, trusted canonical implementation, and differential/exhaustive-walk scripts | Support source/canonical agreement and the natural-language bridge on finite inputs. | Empirical evidence only. They do not contribute to `#Top` or establish universal equivalence. |
| Informal alternating-path argument | Connects the algorithm's returned form to the prompt's lexicographic-path wording for arbitrary valid inputs. | Mathematically persuasive but not represented by a universal K claim. This and the restricted formal domain are the material limitation. |
| LLVM `MPY-KRUN` and `MPY-CONCRETE` | Concrete examples and body-sensitivity evidence only. | Does not enter the Haskell proof definition and cannot substitute for the reachability proof. |

### Gate summary

- Real-program soundness: pass. The actual translated body executes; there are
  no proof-local extensions or result-bearing oracles; `#Top` is fresh; body
  and false-result mutations are discriminating.
- Intent adequacy: limited. The implementation agrees with the trusted
  canonical and an exhaustive-walk oracle on the recorded sample, but the K
  theorem covers only six calls and fixes the symbolic portion to `N=2,k=4`.
- Trust/evidence auditability: pass with the explicit supplied-semantics,
  toolchain, translator, and finite-testing boundaries above.

The scope limitation is material enough to prevent `PASS`, but the
reconstructed theorem is sound, non-vacuous, and about the real submitted
program. It therefore remains legitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
