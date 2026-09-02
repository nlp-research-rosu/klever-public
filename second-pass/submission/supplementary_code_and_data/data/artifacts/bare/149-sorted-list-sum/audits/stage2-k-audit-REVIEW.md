# Independent adversarial audit: 149-sorted-list-sum

The candidate is not a legitimate proof of the generated Python program over
the stated `list[str]` domain. Fresh reconstruction does produce `#Top`, the
claim is result-constraining, and the K program term is mechanically pinned to
the trusted translation. The decisive defect is instead in the generated
language semantics: it equates Python `len(str)` with K `lengthString`, which
counts UTF-8 bytes in both freshly built backends. Python counts Unicode code
points. The result-bearing comprehension and sorting bridges therefore prove
false results for ordinary satisfying Unicode inputs.

The smallest filtering witness is `["😀"]`: both the trusted canonical and the
submitted Python function return `[]` because Python length is 1, while the
fresh LLVM and Haskell K definitions return `["😀"]` because the K length used
by the rules is 4. A separate ordering witness is `["😀😀", "aaaa"]`: Python
sorts code-point lengths 2 then 4 and returns `["😀😀", "aaaa"]`; K sorts byte
lengths 4 then 8 and returns `["aaaa", "😀😀"]`. These are in the unrestricted
source-contract domain, so this is a material language-model/domain failure,
not a nonfatal testing limitation.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `bare`, problem
`149-sorted-list-sum`, and `GENERATED_SEMANTICS`. I read and checked:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the complete structured trace at
  `/generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T07-40-15-019f89d7-4b4f-7063-88a7-a0437ab8a11e.jsonl`;
- the immutable candidate tree and all three trusted reference files.

The absence of `runtime-metrics.json` is allowed for this
`legacy-selected-stage1` record. `usage.json` is present and was checked.

Independent results:

- Every required mount and record is a real readable file/directory; no
  symlink or unsupported entry was found.
- The campaign block in `/audit-input.json` equals
  `/audit-campaign-lock.json`, whose recomputed SHA-256 is the recorded
  `ad5df...d745`.
- Every recorded per-file provenance hash recomputed exactly, including the
  run/task/result/invocation records, generation prompt/output/last/metrics/
  usage, trusted prompt, translator, and canonical.
- All seven files named by `generation-result.json.outputs.evidence` match
  their recorded hashes.
- The one trace file contains 201 valid JSON records. Its independently
  recomputed pipeline tree digest is
  `86001a...e64`, matching `usage.json.source_trace_sha256`.
- The independently recomputed candidate pipeline tree digest is
  `2e61e1...622`, matching
  `generation-result.json.outputs.workspace_sha256`.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- `/reference/reference-semantics` is absent, as required in
  `GENERATED_SEMANTICS`.

There is no infrastructure breach. Full machine output is in
[provenance_check.log](evidence/provenance_check.log), with the reviewer script
in [provenance_check.py](evidence/provenance_check.py). Generation logs and
traces were treated only as untrusted historical claims.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt and canonical establish this return contract: for a finite
list of Python strings, remove every string whose Python length is odd; retain
duplicates; return the remainder ordered first by length and then
lexicographically. The prompt contains no ASCII restriction or finite size
bound. Its sentence saying all words may have the same length is inconsistent
with its mixed-length examples, but the canonical and surrounding ordering
requirements implement the general mixed-length domain.

The submitted [solution.py](/candidate/solution.py) is:

```python
def sorted_list_sum(lst):
    return sorted(
        [word for word in lst if len(word) % 2 == 0],
        key=lambda word: (len(word), word),
    )
```

This is extensionally equivalent to the canonical return value on the intended
domain. Trusted `/reference/py2mpy.py` regenerated `solution.mpy` byte-for-byte
(both SHA-256 `7448e9...554`). Independently regenerating
`solution-program.k` also gave byte identity (both SHA-256
`abcfab...fed`). See
[translation_identity.log](evidence/translation_identity.log).

[differential_test.py](evidence/differential_test.py) imports the immutable
canonical and the exact scratch copy of the generated entry point. It checks 11
named cases plus the complete Cartesian products of an 11-word pool at list
sizes 0 through 4: 16,116 total cases. The pool/cases cover both prompt
examples, empty list/string, all-odd and all-even branches, length transitions,
lexicographic ties, duplicates, escaping, composed/decomposed Unicode, Greek,
and emoji. Against an independently written contract oracle:

```text
total_cases=16116
return_value_mismatches=0
DIFFERENTIAL_OK
```

The canonical sorted its argument in place on 14,748 cases while the submitted
function did not. This is an incidental canonical side effect: the prompt
specifies the returned list, and even the canonical does not delete odd words
from the input object. The K claim only concerns the generated program's
returned value. Full results are in
[differential_test.log](evidence/differential_test.log).

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/reconstruction`; candidate
definitions, `__pycache__`, outputs, and caches were not reused. The live
toolchain is K 7.1.293 and Python 3.10.12
([toolchain.log](evidence/toolchain.log)).

Fresh builds:

```text
kompile semantic.k --main-module MPY-SEMANTIC
  --syntax-module MPY-SYNTAX --backend llvm
  --output-definition concrete-kompiled -w none
# exit 0

kompile verification.k --main-module SORTED-LIST-VERIFICATION
  --syntax-module MPY-SYNTAX --backend haskell
  --output-definition proof-kompiled -w none
# exit 0
```

The build logs are
[kompile_concrete.log](evidence/kompile_concrete.log) and
[kompile_proof.log](evidence/kompile_proof.log).

I ran every positive claim separately. `universal-correctness`, `base`,
`symbolic-two`, `symbolic-two-reverse`, `symbolic-three`,
`prompt-example-one`, and `prompt-example-two` each exited 0 and printed
exactly `#Top`. See
[prove_each_claim.sh](evidence/prove_each_claim.sh) and
[prove_each_claim.log](evidence/prove_each_claim.log).

Nine fresh ASCII/ground concrete executions—including empty, all-odd,
empty-string, duplicates, both key branches, differing lengths, and concrete
witnesses for every symbolic precondition—agreed with Python. See
[concrete_semantics_tests.log](evidence/concrete_semantics_tests.log).

Generated-semantics reconstruction nevertheless fails its required real-Python
comparison on Unicode. The following results were reproduced in *both* the
LLVM concrete definition and the Haskell proof definition:

```text
input ["😀"]
Python canonical/candidate: []
K LLVM/Haskell:             ["😀"]

input ["😀😀", "aaaa"]
Python canonical/candidate: ["😀😀", "aaaa"]
K LLVM/Haskell:             ["aaaa", "😀😀"]
```

Exact constructors, commands, and outputs are in
[unicode_semantics_mismatch.sh](evidence/unicode_semantics_mismatch.sh) and
[unicode_semantics_mismatch.log](evidence/unicode_semantics_mismatch.log).
This is a candidate semantics failure, not a K build/backend failure.

## 4. Adequacy and real-program pinning

### Claim meanings

| Claim | Plain-language precondition | Exact result obligation |
|---|---|---|
| `universal-correctness` | None; `INPUT` is any finite K `Words` sequence | Running the submitted function must return `VList(sortedListSumSpec(INPUT))`. |
| `base` | The input is empty | Return `VList(evenSorted(.Words))`, which reduces to empty. |
| `symbolic-two` | K lengths of `A` and `B` are 2 and `A <String B` | Return `VList(evenSorted(A,B))`. |
| `symbolic-two-reverse` | K lengths are 2 and `notBool(A <String B)` | Return `VList(evenSorted(A,B))`. |
| `symbolic-three` | K lengths of `A,B,C` are 4,2,3 | Return `VList(evenSorted(A,B,C))`. |
| `prompt-example-one` | Fixed input `["aa","a","aaa"]` | Return exactly `["aa"]`. |
| `prompt-example-two` | Fixed input `["ab","a","aaa","cd"]` | Return exactly `["ab","cd"]`. |

Every claim starts with
`Run(solutionProgram, Call(Name("sorted_list_sum"), ...))`, consumes that
computation, and has a fixed `Result(VList(...))`; there is no free/right-only
result variable, tautological `ensures`, or one-way result implication.

Trusted translation plus an independent constructor-level comparison shows
that `solutionProgram` is exactly the regenerated `Module(FuncDef(...))` term.
The only normalization changes the surface spelling of empty `CellVars()` and
`FreeVars()` lists to their K units `.Strings`. All seven entry claims use this
constant. See [program_pinning.log](evidence/program_pinning.log).

Satisfying ground states exist for every precondition:

- universal: `["bb","a"]` -> `["bb"]`;
- base: `[]` -> `[]`;
- symbolic two: `["aa","ab"]` -> `["aa","ab"]`;
- reverse: `["ba","ab"]` -> `["ab","ba"]`;
- three: `["zzzz","aa","bbb"]` -> `["aa","zzzz"]`;
- the two fixed prompt examples produce their stated results.

For all seven, the formal ground RHS, canonical Python result, and submitted
Python result agree. The preserved table is
[claim_witnesses.log](evidence/claim_witnesses.log).

Body sensitivity is also genuine. I changed the executed function body to
return the even-filtered comprehension without `sorted`, regenerated both the
`.mpy` and `solutionProgram` term, and freshly rebuilt the proof. The build
exited 0; the universal claim exited 1 with a meaningful residual
`filterEven(INPUT) =/= sortByKey(filterEven(INPUT))`. See
[body-mutation-solution.py](evidence/body-mutation-solution.py) and
[body_sensitivity_test.log](evidence/body_sensitivity_test.log).

Thus source/term pinning and result constraint pass. Adequacy does not: the
executed term is interpreted by materially false Python string-length
semantics.

## 5. Rule-by-rule static soundness review

The independent source inventory is
[k_source_inventory.log](evidence/k_source_inventory.log), generated by
[k_source_inventory.py](evidence/k_source_inventory.py). It found:

- 31 syntax sentences, 58 ordinary rules, and one configuration in
  `semantic.k`;
- one function declaration and one rule in `solution-program.k`;
- two syntax sentences and 10 ordinary rules in `verification.k`;
- seven claims in `spec.k`.

There are 69 local ordinary rules in total. There are 31 local `[function]`
symbols (24 semantic evaluators/helpers, `solutionProgram`, and six
verification/specification helpers). There are no `[total]`, `[functional]`,
`[simplification]`, `[concrete]`, priority, `context`, or `alias`
declarations, and no fresh/opaque result oracle. Constructor `[symbol]`
attributes are opaque data constructors only.

The complete declaration list and an individual decision for every rule are in
[RULE-ASSESSMENT.md](evidence/RULE-ASSESSMENT.md). The exhaustive rule-ID
summary is:

| Inventory rules | Decision |
|---|---|
| Semantic R01-R18 | Sound on the actual typed/pure path; list singleton overlaps R12/R13 and R16/R17 normalize to the same results. |
| Semantic R19-R25 | Arithmetic/comparison dispatch is sound on used operands; unused cases are partial and visibly stick. |
| Semantic R26-R27 | Does not model Python short-circuiting/general arity, but is unused and yields no false result on the modeled pure two-Boolean domain; evidence/coverage gap only. |
| Semantic R28 | Structurally dispatches `len`, but inherits false R34 for strings. |
| Semantic R29 | **Unsound task-specific comprehension bridge** on intended Unicode inputs; `["😀"]` is the concrete false-result witness. |
| Semantic R30 | **Unsound task-specific sorted/key bridge**; `["😀😀","aaaa"]` is the concrete false-order witness. |
| Semantic R31-R33 | Sound function lookup/call/return for the exact one-function, one-parameter pure program. |
| Semantic R34 | **Unsound bridge:** K `lengthString("😀")` behavior is 4 while Python `len("😀")` is 1. |
| Semantic R35-R38 | Sound modeled list length/word projection/filter base. |
| Semantic R39 | **Unsound parity computation** using K byte length; same `["😀"]` witness. |
| Semantic R40-R45 | Guard pairs are disjoint/exhaustive and recursive equations descend; sound conditional on supplied Booleans/key. |
| Semantic R46 | **Unsound key computation** using byte length; `("😀😀","aaaa")` reverses Python's length ordering. |
| Semantic R47-R58 | Insertion branches, subscript fragment, empty/return/if sequencing, and return propagation are sound on their modeled typed domains; unsupported unused cases stick. |
| `solution-program.k` R01 | Exact regenerated constructor term; sound and body-sensitive. |
| Verification R01 | Repeats the false byte-length key; same ordering witness. |
| Verification R02 | Internally consistent definition, but circular as an independent property: `sortedListSumSpec` is exactly the semantic `sortByKey(filterEven(...))` already returned by R29/R30. |
| Verification R03-R10 | Structurally descending filter/insertion equations and disjoint Boolean branches; R04 is false relative to Python Unicode because it also uses `lengthString`, and R08-R10 inherit R01. |

### Construct/control mapping

`solution.mpy` uses `Module`, `FuncDef`, `Params`, `Return`, `Call`, `Name`,
`ListComp`, `CompFor`, `Compare`, `BinOp`, `Int`, `CmpOp`, `KwArg`, `Lambda`,
`CellVars`, `FreeVars`, and `TupleExpr`. The module, binding, call, and abrupt
return path executes through semantic R02-R06, R31-R33, and R53.

The material comprehension iteration, binder lookup, `len`, modulo, and
comparison do **not** execute through general per-node semantics. R29 matches
the entire exact expression and returns `filterEven`. Likewise R30 matches the
entire exact `sorted` call/lambda/tuple and returns `sortByKey`. These are
result-bearing, task-specific big-step operational bridges. Their recursive
RHS equations are not unconstrained, but the universal postcondition reuses
those same symbols via verification R02, so `#Top` is largely definitional and
does not independently validate the source meaning. No bridge-free universal
connection theorem exists.

For ASCII strings the recursive equations implement the intended filter and
insertion sort, keep duplicates, use strict insertion consistently, and
terminate structurally. The direct rules have no mutable state/control effect
to preserve because this generated program is pure. The generated configuration
needs only `<k>` for that actual path. Missing general Python constructs and
unused partial cases are permissible in generated-semantics mode; they are not
the verdict basis.

The verdict basis is narrower and witnessed: R34/R39/R46 make R29/R30 false on
valid program inputs, and the circular postcondition then proves the same wrong
K answer.

## 6. Fresh non-vacuity test

I ignored any candidate vacuity evidence (none was submitted) and authored
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k). It uses the satisfying
ground input `["aa"]` but deliberately requires the false result `[]`.

The mutation dry-run parsed/compiled successfully and exited 0. The actual
proof exited 1 with `WarnStuckClaimState`; the residual is the reached
configuration:

```text
<k>
  Result ( VList ( "aa" , .Words ) ) ~> .K
</k>
```

This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash. See
[nonvacuity_test.sh](evidence/nonvacuity_test.sh) and
[nonvacuity_test.log](evidence/nonvacuity_test.log). The theorem is therefore
non-vacuous/result-discriminating under its supplied theory. That does not make
the supplied theory a sound model of Python.

## 7. Proven versus assumed accounting

### What `#Top` actually establishes

Under the candidate's K theory, for every finite K `Words` value `INPUT`,
evaluating the pinned `sorted_list_sum` term reaches:

```text
Result(VList(sortByKey(filterEven(INPUT))))
```

The six auxiliary/ground claims establish the corresponding byte-length-based
base, selected branch, and example reductions. Because the program semantics
R29/R30 and postcondition R02 share `filterEven` and `sortByKey`, the universal
claim mostly establishes consistency between a task-specific evaluator summary
and the same summary named as the specification.

It does **not** establish that those helpers denote Python's
code-point-length filter/order for all `list[str]`. The two Unicode witnesses
disprove that bridge.

### Trust ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| Trusted CPython AST translator | Determines `solution.mpy` and therefore the program term in every claim | Acceptable here: immutable trusted translator, byte-identical regeneration, and constructor-level term comparison. |
| K `BOOL`, `INT`, `MAP`, `STRING` hooks | Arithmetic, maps, string length/order; all positive claims depend on them | Low-level K primitives are normally acceptable, but interpreting K `lengthString` as Python `len(str)` is **illegitimate** without an encoding bridge and concretely false for Unicode. |
| R29 exact comprehension summary | Determines filtering and hence every result | Program-derived, task-specific bridge with no independent universal connection theorem; materially false through R39/R34. |
| R30 exact `sorted`/lambda summary | Determines output ordering | Program-derived, task-specific bridge with no independent universal connection theorem; materially false through R46. |
| Verification R02 `sortedListSumSpec` | Universal postcondition | Reuses the exact result-bearing semantic helpers; circular as evidence of source meaning. |
| Verification `evenSorted`/`keyLess` | Auxiliary symbolic and ground claims | Fully equational but repeats the same false K string-length interpretation. |
| Python differential | Supports candidate-vs-canonical return equivalence over 16,116 cases | Strong finite evidence for the Python implementation only; not a universal proof and not a K/Python bridge. |
| ASCII concrete K tests | Supports modeled operation on nine normal/boundary inputs | Finite support only; the Unicode tests explicitly refute full-domain adequacy. |
| Input mutation/state | Not represented in the one-cell K configuration | Acceptable for the generated program's specified return value: the candidate is pure and the prompt/canonical do not establish a required post-state. |
| Termination | Partial correctness assumes termination; recursive K helpers descend on finite lists | Acceptable. The Python program and used K equations terminate on finite `list[str]`/`Words`. |

There are no fresh existential result symbols, opaque oracles, trusted claims,
simplification lemmas, or priority rules. Exact commands and statuses are
indexed in [COMMANDS.md](evidence/COMMANDS.md).

### Gate and benchmark decision

- Real-program soundness: **FAIL**. The rebuilt theorem is
  result-constraining and body-sensitive, but its result-bearing semantics
  produces demonstrably false Python results on satisfying Unicode inputs.
- Intent/domain adequacy: **FAIL**. The source says `list[str]` and does not
  restrict inputs to ASCII/one-byte strings. Treating the proof as ASCII-only
  would materially narrow the HumanEval contract.
- Evidence auditability: **PASS as evidence quality**, but testing cannot
  repair the failed semantics bridge.

The benchmark explicitly maps a material source-domain narrowing to
`FAIL / NOT_LEGIT`, not `CONCERNS`. The concrete false conclusions make that
mapping mandatory here even though every K claim freshly prints `#Top`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
