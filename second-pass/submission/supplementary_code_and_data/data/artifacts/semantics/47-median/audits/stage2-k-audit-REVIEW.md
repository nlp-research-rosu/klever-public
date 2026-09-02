# Independent adversarial audit: 47-median

## Executive finding

The candidate has a reproducible, non-vacuous K reachability proof of a narrow
execution summary for the exact submitted `solution.mpy`. It is not a legitimate
proof of HumanEval/47 median.

The decisive counterexample is `[4, 1, 3, 2]`: the submitted program and its
even claim select sorted indices 2 and 3 and return `3.5`, while the trusted
canonical implementation selects indices 1 and 2 and returns `2.5`. The even
claim also excludes length two, for which canonical returns `1.5` on `[2, 1]`
but the submitted program raises `IndexError`. Both claims require every element
to be an `Int`, although the source signature says only `list` and canonical
validly handles numeric float lists.

There is also a proof-boundary limitation: `verification.k` rewrites the
result-bearing term `valSeqAt(sortVS(VS), I)` to a fresh opaque
`sortedIntAt(VS, I)` and uses that same symbol in both postconditions. There is
no bridge-free K theorem connecting this proof-local symbol to fixed-semantics
execution or to the mathematical sorted element. The fresh mutation tests show
that the postcondition constrains this symbol syntactically, but they do not
supply its missing meaning.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`semantics_mode = SUPPLIED_SEMANTICS`, problem `47-median`, and condition
`semantics` in `/audit-input.json`.

I read and checked:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `legacy-metrics.json`, `legacy-run-input.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- all 234 JSONL records in the structured trace at
  `/generation-evidence/codex-trace/2026/07/22/`;
- the trusted prompt, canonical implementation, translator, and supplied
  semantics mounts.

Results:

- The campaign lock SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  matching `/audit-input.json`, and its parsed JSON object exactly equals the
  recorded `audit_campaign` block.
- Every required `legacy-selected-stage1` record is a regular readable file.
  `usage.json` is present and its hash matches. Historical runtime metrics are
  not required by this layout.
- All directly recorded hashes for the run/task/result/invocation manifests,
  generation logs, structured trace, canonical, prompt, and translator match.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
  trusted mounts.
- The required trusted `/reference/reference-semantics` exists. A recursive,
  type-aware comparison found 25 entries on each side and no missing,
  additional, changed, mistyped, or symlinked entry in
  `/candidate/reference-semantics`.
- The required candidate proof files are regular files. No candidate-built
  definition or cache was used.

The untrusted generation trace records that the generator first implemented
the canonical middle-pair algorithm, observed that the prompt's second doctest
said `15.0`, deliberately changed to the upper-pair algorithm, and later
restricted the proof to integer lists and even lengths at least four. This is
historical evidence only; the verdict below rests on fresh reconstruction and
source comparison.

Evidence:

- `evidence/01_provenance_integrity.py`
- `evidence/01_provenance_integrity.log` — exit 0
- `evidence/01_generation_trace_summary.py`
- `evidence/01_generation_trace_summary.log` — exit 0

There is no infrastructure breach, so a candidate verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

`/reference/prompt.py` asks `median(l: list)` to return the median of the
elements. `/reference/canonical.py` sorts the list, returns the middle element
for odd length, and for even length averages sorted indices `n // 2 - 1` and
`n // 2`. Thus the material intended domain is nonempty, mutually sortable
numeric lists on which the indicated addition and division are defined.

The trusted prompt is internally inconsistent: its six-element doctest expects
`15.0`, whereas both ordinary median and trusted canonical return `8.0`. This
is not a mount or semantics-mode breach. The natural-language operation and
trusted canonical agree with each other, while the submitted program follows
the anomalous doctest and disagrees on the whole non-degenerate even branch.

### Translation fidelity

Fresh translation in scratch used the trusted `/reference/py2mpy.py`:

```text
python3 /tmp/audit-work/reconstruction/py2mpy.py \
  /tmp/audit-work/reconstruction/solution.py \
  > /tmp/audit-work/reconstruction/regenerated-solution.mpy
```

It exited 0. `cmp -s` against submitted `solution.mpy` exited 0; both files
have SHA-256
`46472179c37533da4848d842f580c0fa01e88180c5c1a13d9f307eebd315bef2`.

### Independent differential test

`evidence/02_differential.py` independently imports the trusted canonical and
submitted entry points. It covers both prompt examples, empty, lengths 1
through 4, duplicates, negative values, float and mixed numeric lists, and
seeded integer/float cases for every length 1 through 12. The complete 156
inputs and both observations are in `evidence/02_fidelity.log`.

The run deliberately exits 1 on divergence:

```text
cases=156 matches=79 mismatches=77 seed=470047
```

Material witnesses include:

| Input | Canonical | Candidate |
|---|---:|---:|
| `[-10, 4, 6, 1000, 10, 20]` | `8.0` | `15.0` |
| `[2, 1]` | `1.5` | raises `IndexError` |
| `[4, 1, 3, 2]` | `2.5` | `3.5` |
| `[8.0, 1.5, -3.25, 2.0]` | `1.75` | `5.0` |

Empty input raises `IndexError` in both, and odd-length inputs agree in the
tested corpus. Both implementations leave inputs unchanged.

Evidence:

- `evidence/02_fidelity.sh`
- `evidence/02_differential.py`
- `evidence/02_fidelity.log` — translation/cmp exit 0; differential exit 1
  because the candidate is materially different

Stage 2 fails program fidelity.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/reconstruction`, used the
trusted supplied-semantics tree, and confirmed before building that no
`*-kompiled` directory existed. Tool versions were independently reported as
K `v7.1.293`.

Fresh concrete reconstruction:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

The compile exited 0. `krun solution.mpy` exited 0, and an independently
translated concrete smoke module exercising the submitted behavior exited 0.
These runs show that the supplied concrete semantics executes the submitted
program; they are not evidence of agreement with canonical.

Fresh proof reconstruction:

```text
kompile verification.k --backend haskell \
  --main-module MEDIAN-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k --definition verification-kompiled \
  --spec-module MEDIAN-SPEC
```

The build exited 0; the combined proof exited 0 and printed `#Top`.
Each positive claim was then selected and run independently:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module MEDIAN-SPEC \
  --claims MEDIAN-SPEC.median-odd

kprove spec.k --definition verification-kompiled \
  --spec-module MEDIAN-SPEC \
  --claims MEDIAN-SPEC.median-even
```

Both exited 0 and printed `#Top`.

The first reconstruction script also records two exit-113 attempts using
unqualified filters `median-odd` and `median-even`; K rejected those filters as
unused labels. This was an auditor command-selection error, not a failed
claim. The corrected fully qualified commands above are preserved separately.

Evidence:

- `evidence/03_clean_reconstruction.sh`
- `evidence/03_clean_reconstruction.log`
- `evidence/03b_individual_claims.sh`
- `evidence/03b_individual_claims.log` — both individual claims exit 0 with
  `#Top`

The narrow formal claims pass clean reconstruction.

## 4. Adequacy and real-program pinning

### Plain-language claims

`median-odd` quantifies over a `ValSeq` containing only K `Int` values, with
positive odd length. From a pristine module configuration it loads the
submitted `median`, calls it on `list(VS)`, and requires the returned `<k>`
value to be:

```text
sortedIntAt(VS, (vsLen(VS) - 1) / 2)
```

`median-even` quantifies over an all-`Int` sequence of even length at least
four. It requires the returned value to be:

```text
intFloatDiv(
  sortedIntAt(VS, vsLen(VS) / 2)
  + sortedIntAt(VS, vsLen(VS) / 2 + 1),
  2.0)
```

Both postconditions constrain the final `<k>` result syntactically; neither is
a free result variable or tautology. Final scopes, heap, and allocation
counters are existential, which is reasonable for this pure return-value
contract. There are no helper or loop claims.

### Program pinning

I mechanically extracted both `#loadAll(...)` arguments from `spec.k`,
normalized only K's internal empty-list token `.Stmts` to the external MPY
parser's empty argument notation, and parsed the submitted and both extracted
modules with `kast --output kore`. All three KORE files are byte-identical with
SHA-256:

```text
675cedbb35d3f092a97ce9196d00d18534bfd9440567a8a85ad3e4891cf4aa1d
```

Thus both claims load and execute the real submitted function body.

### Satisfiable states and concrete substitution

Every entry precondition is satisfiable:

- Odd witness `[3, 1, 2]`: `allInts = true`, length 3, remainder 1. The
  interpreted claim result, submitted Python, and canonical are all `2`.
- Even witness `[4, 1, 3, 2]`: `allInts = true`, length 4, remainder 0. The
  interpreted claim result and submitted Python are `3.5`; canonical is `2.5`.
- The six-element doctest also satisfies the even precondition. The claim and
  submitted Python give `15.0`; canonical gives `8.0`.

### Body sensitivity

A fresh mutation changed the program term actually executed by the even claim
from `values[middle + 1]` to `values[middle]`, leaving its postcondition
unchanged. The mutated claim parsed, ran, exited 1, and produced a stuck
residual contrasting the two `intFloatDiv(...)` terms. It did not print
`#Top`. The proof therefore is sensitive to the submitted body.

Evidence:

- `evidence/04_extract_claim_program.py`
- `evidence/04_ground_claims.py`
- `evidence/04_pinning.sh`
- `evidence/04_pinning.log`
- `evidence/05_make_body_mutation.py`
- `evidence/05_body_sensitivity.sh`
- `evidence/05_body_sensitivity.log`

Real-program pinning passes, but intent adequacy fails: the exact pinned
program is wrong on even inputs, and the theorem excludes valid source-domain
inputs.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/04_rule_inventory.txt` inventories every declaration from the
assembled supplied semantics, all 23 helper K files, `verification.k`, and
`spec.k`, with source line, normalized statement, and attributes. It contains:

| Kind/attribute | Count |
|---|---:|
| Total records | 937 |
| Syntax declarations | 229 |
| Rules | 700 |
| Contexts | 5 |
| Configurations | 1 |
| Claims | 2 |
| Function declarations | 148 |
| Total declarations | 109 |
| Symbol/opaque declarations | 26 |
| Priority rules | 45 |
| Concrete rules | 35 |
| `owise` rules | 27 |
| Simplification rules | 2 |

There are no local `[functional]` declarations. The companion
`evidence/04_rule_assessment.txt` gives an explicit disposition and rationale
for all 937 records: 167 active fixed-semantics records accepted on the used
integer-list path, 4 active trusted-primitive records, 738 inert fixed records,
19 inert opaque boundaries, all 7 proof-local verification records, and both
claims.

### Used-construct map

| Submitted construct | Declaration and material behavior |
|---|---|
| `Module`, `Stmts` | `syntax.k`; `core.k` `#loadAll` and statement sequencing |
| `FuncDef`, `Params`, call, return | `functions.k` frame/binding/return/pop rules and `call.k` left-to-right callee/argument routing |
| `Assign`, `Name` | strict RHS evaluation in `syntax.k`, scope update in `controls.k`, chained lookup in `core.k` |
| `sorted(l)` | builtins binding in `core.k`; call dereference in `call.k`; fresh allocation of `list(sortVS(VS))` in `sort.k` |
| `len(values)` | `applyBuiltin("len", ...)`, `seqLen`, and structural `vsLen` in `builtins.k`/`core.k` |
| `//`, `%`, integer `+` | sequential `BinOp` evaluation in `operators.k`; `pyMod` and integer rules in `int.k` |
| `==`, `If` | comparison dispatch in `operators.k`/`int.k`; truth conversion and branch rules in `core.k`/`controls.k` |
| `Subscript` | receiver/index contexts, heap dereference, `normIdx`, and `valSeqAt` in `subscript.k` |
| `/ 2.0` | float literal and opaque symbolic `intFloatDiv`, with a concrete LLVM twin, in `float.k` |

The relevant priority rules only preempt generic dispatch to dereference the
heap list or route a more specific list/call case. Their bindings, evaluation
order, continuation, heap allocation, and return-frame effects match the
submitted control flow. The claim guards make every selected index in bounds:
odd `n > 0`; even `n >= 4`, so both `n/2` and `n/2 + 1` are below `n`.
Therefore the supplied `valSeqAt` totalization for out-of-bounds access is not
used to close these claims.

### Proof-local rules

1. `vsLen(sortVS(VS)) => vsLen(VS) [simplification]` is a proof extension.
   It is true conditional on the supplied `sortVS` contract that sorting is a
   permutation. It is not independently proved in K, but no intended-domain
   false witness exists because real sorting preserves length.
2. `allInts` and its three equations form a disjoint, terminating structural
   predicate: empty is true, an `Int` head recurses, and the `owise` non-`Int`
   head is false. These rules are sound.
3. `sortedIntAt` is fresh, `[function,total,symbol,no-evaluators]`, with no
   value equations.
4. The guarded simplification
   `valSeqAt(sortVS(VS), I) => sortedIntAt(VS, I)` applies only to all-`Int`,
   in-bounds inputs. Its Int typing is plausible under sort's type-preserving
   permutation contract. However, it is the only connection, it imports the
   proposed abstraction itself, and the same symbol is used in both final
   postconditions. There is no bridge-free universal connection theorem.

I do not label any inventoried equation globally false, so no false-rule
witness is asserted. The narrower finding is that the proof-local,
result-bearing abstraction is not independently validated and does not
establish the numerical meaning of the selected sorted element. The concrete
false witnesses in Stages 2 and 4 instead establish program/contract and
claim/intent mismatches.

Evidence:

- `evidence/04_rule_inventory.py`
- `evidence/04_rule_inventory.txt`
- `evidence/04_rule_inventory.log`
- `evidence/04_rule_assessment.py`
- `evidence/04_rule_assessment.txt`
- `evidence/04_rule_assessment.log`

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`, so I created a fresh one only in
scratch. It retains the exact odd program and precondition but changes the
returned obligation to:

```text
sortedIntAt(VS, (vsLen(VS) - 1) / 2) + 1
```

`VS = vCons(3, .ValSeq)` is a satisfying witness: the actual result is 3 and
the mutation demands 4.

Command:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module MEDIAN-SPEC-VACUITY
```

The mutation parsed and ran, exited 1, printed no `#Top`, and produced
`WarnStuckClaimState` with the expected failed implication:

```text
sortedIntAt(...) +Int 1 #Equals sortedIntAt(...)
```

This is meaningful non-vacuity evidence, not a parser failure, timeout, or
unreachable mutation.

Evidence:

- `evidence/06_nonvacuity.sh`
- `evidence/06_nonvacuity.log`

Stage 6 passes.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Relative to the supplied MPY semantics plus `verification.k`, the two
reachability claims establish partial correctness of the exact submitted
function for:

- nonempty odd-length lists consisting exclusively of K `Int` values, returning
  the opaque selected upper-middle term; and
- even-length all-`Int` lists of length at least four, returning the opaque
  average of sorted positions `n/2` and `n/2 + 1`.

It does not establish canonical median on even lists, length-two behavior,
float-list behavior, or a universal bridge from the opaque sorted terms to
ordinary Python values.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| Supplied `sortVS` | Opaque symbolic ascending-sort/permutation primitive; controls length, indexing, and both returned values. LLVM has a concrete insertion-sort twin. | Allowed as a supplied-semantics trust boundary, but its Python connection is not proved by these claims. |
| Proof-local length lemma | Lets symbolic `len(sorted(l))` reduce to `len(l)`, affecting branch and indices. | Mathematically true conditional on `sortVS`; not machine-derived here. |
| Proof-local `sortedIntAt` | Determines every selected value and both postconditions. | Program-derived, result-bearing, and lacks a bridge-free connection theorem; same-symbol use is circular as validation evidence. |
| Supplied `intFloatDiv` | Determines the even float result. Haskell keeps it opaque; LLVM computes `Int2Float(I)/Float F`. | Acceptable fixed primitive conditional on its concrete/Python contract. |
| Supplied `valSeqAt [total]` | Selects list elements and remains abstract on opaque sequences/OOB. | In-bounds guards avoid the concerning OOB totalization. |
| K integer/Boolean hooks, maps, lists, reachability engine, and SMT backend | Execute control/state and discharge length/parity arithmetic. | Standard toolchain trust. |
| Trusted translator | Connects Python AST to MPY constructors. | Byte regeneration succeeded; constructor-level claim pinning also succeeded. |
| Differential tests | Compare canonical and candidate on 156 finite inputs. | Valid empirical evidence of observed divergence, not a universal proof. |

All 26 opaque/symbol declarations are explicitly inventoried. The active ones
are `sortVS`, `intFloatDiv`, and proof-local `sortedIntAt`. Imported but inert
for this program are:

- `md5hexCodes`;
- `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`, `ceilF`,
  `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
  `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and `sqrtF`;
- `sortKeyVS`.

### Gate accounting

- Real-program pinning and syntactic non-vacuity pass.
- Real-program validation does not pass the result-bearing abstraction
  procedure because `sortedIntAt` has no independent connection theorem.
- Intent adequacy fails decisively: the submitted even algorithm disagrees
  with canonical median, and the formal preconditions materially narrow the
  source-contract domain.
- Evidence auditability is good, but the fresh differential evidence
  contradicts the candidate's correctness claim.

Under the benchmark's decision boundary, the wrong even program and material
domain narrowing are each independently `FAIL / NOT_LEGIT`; a clean `#Top`
for the narrower execution summary cannot cure either defect.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
