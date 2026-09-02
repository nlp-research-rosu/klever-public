# Independent adversarial review: 47-median

This is a completed independent audit in `SUPPLIED_SEMANTICS` mode. I treated
all candidate prose, scripts, caches, and alleged results as untrusted. All
executions used source copies under `/tmp/audit-work/work`; no candidate
compiled definition or cache was used.

The candidate is **not a legitimate proof of the requested median function**.
A fresh reconstruction does produce `#Top`, and the reachability claims execute
the literal submitted program. However:

1. the submitted program is materially different from the trusted canonical
   implementation on even-length lists;
2. the even claim formalizes that wrong computation, not the canonical median;
3. the only even claim excludes the important length-two case, on which the
   submitted program raises `IndexError`; and
4. `verification.k` replaces the result-bearing sorted-list access with a fresh
   opaque `sortedIntAt` term also used verbatim in the postcondition, without an
   independent connection theorem or value characterization.

The prompt itself contains a contradictory even example: it says the
six-element example is `15.0`, while the trusted canonical implementation
returns `8.0`. That trusted-input disagreement is documented below. It is not
the semantics-mode infrastructure contradiction that would require
`AUDIT_ERROR`: the required supplied-semantics mount is present and internally
consistent with the candidate copy.

## 1. Input and provenance integrity

### Semantics-mode boundary

`/reference/reference-semantics` exists, as required in
`SUPPLIED_SEMANTICS` mode. A recursive, no-symlink comparison found:

- 25 entries below each trusted and candidate semantics root;
- no candidate semantics symlinks;
- no missing, additional, mistyped, or changed entry; and
- recursive byte identity (`diff_status=0`).

Evidence: `evidence/commands/stage1_semantics_cmp.log` and the final repeated
check in `evidence/commands/stage7_final_integrity.log`.

The candidate `prompt.py` and `py2mpy.py` are regular files and byte-identical
to the trusted mounted files. Their respective SHA-256 values are:

- prompt: `12794c9b475e4c41b878cf4d466feb8fa24d9d3dd6311f9845760f64b4748fd4`;
- translator: `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

Evidence: `evidence/commands/stage1_prompt_cmp.log`,
`evidence/commands/stage1_translator_cmp.log`, and
`evidence/commands/stage1_trusted_inventory.log`.

### Required and supporting artifacts

The candidate contains regular-file source artifacts `solution.py`,
`solution.mpy`, `spec.k`, `verification.k`, `prompt.py`, `py2mpy.py`,
`prove.sh`, `concrete-tests.py`, and `concrete-tests.mpy`. It also contains an
untrusted `__pycache__/solution.cpython-310.pyc`; I ignored that cache. No entry
under the supplied-semantics subtree is a symlink.

The following requested provenance artifacts are absent:

- `/candidate/run-input.json`;
- `/candidate/metrics.json`;
- `/candidate/codex-last.txt`;
- `/candidate/codex-output.log`; and
- any structured generation-trace file discoverable by a trace/generation or
  JSONL filename.

There is also no candidate `spec-vacuity.k`. The absence of a candidate
vacuity test is not substituted with an assumption; Stage 6 creates a fresh
reviewer-authored one.

Evidence: the complete typed inventory is
`evidence/commands/stage1_candidate_inventory.log`. The missing generation
metadata is an auditability deficiency, but it does not prevent independent
source reconstruction and is not the reason for the candidate verdict.

### Isolation

The sources needed for execution were copied explicitly into
`/tmp/audit-work/work/candidate-src` and trusted inputs into
`/tmp/audit-work/work/trusted`. The copy command and status are recorded in
`evidence/commands/stage1_copy_sources.log`. All definitions named
`runtime-kompiled` and `verification-kompiled`, all proof variants, regenerated
programs, and mutation inputs were created below that scratch root. The
candidate tree remained read-only.

Stage 1 result: **PASS for the supplied-semantics integrity boundary; provenance
concern for the four missing metadata files and absent structured trace.**

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language and canonical contract

`/reference/prompt.py` asks for `median(l)` and says to return the median of the
elements in a list. The trusted `/reference/canonical.py` operationalizes that
as:

1. sort the list in ascending order;
2. for an odd length, return the element at `len(l) // 2`; and
3. for an even length, return the arithmetic mean of the elements at
   `len(l) // 2 - 1` and `len(l) // 2`.

The canonical implementation has no explicit empty-list precondition, but an
empty call raises `IndexError`; for ordinary successful behavior the practical
domain is a nonempty list of mutually sortable values for which the required
addition and division are defined. The submitted formal claims further narrow
this to integer sequences.

The prompt's second documented example conflicts with its trusted canonical:

```text
input:     [-10, 4, 6, 1000, 10, 20]
sorted:    [-10, 4, 6, 10, 20, 1000]
prompt:    15.0
canonical: 8.0
```

An independent doctest run passed the odd example and failed this even example
with actual result `8.0`. Evidence:
`evidence/commands/stage2_doctest.log`.

This conflict means the prompt example alone cannot be used as an oracle for
the canonical task. The audit therefore reports results against both trusted
inputs and does not silently revise either.

### Submitted program

The candidate uses:

```python
middle = len(values) // 2
...
return (values[middle] + values[middle + 1]) / 2.0
```

For even lengths this is the upper pair, not the two central elements. It also
indexes past the end for length two. Examples:

| Input | Submitted program | Trusted canonical |
|---|---:|---:|
| `[4, 1]` | `IndexError` | `2.5` |
| `[4, 1, 3, 2]` | `3.5` | `2.5` |
| `[0, 1, 2, 3, 4, 99]` | `3.5` | `2.5` |
| prompt's six-element example | `15.0` | `8.0` |

Thus the program happens to match the contradictory prompt example but
materially diverges from the trusted canonical and the ordinary median
definition.

### Trusted translation identity

I reran the trusted `/reference/py2mpy.py` on the copied `solution.py`. The
regenerated output is byte-identical to submitted `solution.mpy`, both with
SHA-256:

`46472179c37533da4848d842f580c0fa01e88180c5c1a13d9f307eebd315bef2`.

Evidence:

- command/result: `evidence/commands/stage2_regenerate_mpy.log`;
- preserved generated term: `evidence/artifacts/regenerated-solution.mpy`;
- final repeated identity check:
  `evidence/commands/stage7_final_integrity.log`.

The K program is therefore faithful to the submitted Python source. The
problem is the algorithm in that source, not a translation mismatch.

### Independent differential test

`evidence/scripts/differential_median.py` independently imports the trusted
canonical and generated Python entry points. It compares return value and
return type, or exception class, over:

- both documented prompt examples;
- explicit lengths 0 through 6 covering empty, odd/even branch boundaries,
  length two, and the proof's even lower bound;
- every sequence over `{-2,-1,0,1,2}` for lengths 0 through 6; and
- 2,000 deterministic generated sequences, seed `47047`, with lengths 0
  through 20 and values from -1000 through 1000.

The full 21,540-input manifest is
`evidence/artifacts/differential-inputs.json`, SHA-256
`2ff46a849e53d10472dfc523b6227b1dc9fb2fd5fd03849f543b54b5ddb6399c`.

The valid run found **15,089 mismatches**, all at positive even lengths:

```text
length 2:    111
length 4:    667
length 6: 13,657
length 8:     79
length 10:   103
length 12:    93
length 14:    85
length 16:    94
length 18:    87
length 20:   113
```

The test exits 1 intentionally when it finds a mismatch. This is a completed
differential result, not a test harness error. Its bounded output and exact
command are in `evidence/commands/stage2_differential.log`. An initial
reviewer-script syntax error is transparently retained as
`stage2_differential_attempt1.log` and is not used as evidence.

Stage 2 result: **FAIL for canonical program fidelity.** The translated program
is the submitted program, but that program is not the trusted canonical median.

## 3. Clean proof reconstruction

### Toolchain

The fresh build used:

```text
kompile / krun / kprove
K version v7.1.337
Build date Thu Jun 18 07:59:56 CDT 2026
```

Evidence: `evidence/commands/stage3_tool_versions.log`.

### Concrete definition

From the scratch source copy I ran:

```bash
timeout 300s kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0. The warnings identify non-exhaustive total helper matches in
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`, plus unused
variables in two string-order rules. Most warned helpers are unreachable from
this program; `valSeqAt` is used and is discussed in Stages 5 and 7.

`krun solution.mpy` exited 0 after loading the actual median closure.
`krun concrete-tests.mpy` also exited 0. Those candidate tests are not an
independent correctness oracle: they explicitly assert the erroneous
`median([4,1,3,2]) == 3.5`.

Evidence:

- `evidence/commands/stage3_kompile_runtime.log`;
- `evidence/commands/stage3_krun_solution.log`;
- `evidence/commands/stage3_krun_candidate_tests.log`.

### Proof definition and positive claims

From copied source I ran:

```bash
timeout 600s kompile verification.k \
  --backend haskell \
  --main-module MEDIAN-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0. I then independently ran each target claim and the combined spec:

| Target | Exit | Required output |
|---|---:|---|
| `MEDIAN-SPEC.median-odd` | 0 | `#Top` |
| `MEDIAN-SPEC.median-even` | 0 | `#Top` |
| full `MEDIAN-SPEC` | 0 | `#Top` |

Exact commands and bounded outputs:

- `evidence/commands/stage3_kompile_verification.log`;
- `evidence/commands/stage3_kprove_odd.log`;
- `evidence/commands/stage3_kprove_even.log`;
- `evidence/commands/stage3_kprove_all.log`.

No candidate-provided compiled directory was copied or consulted.

Stage 3 result: **PASS for clean reconstruction.** This establishes closure
under the submitted extended theory; it does not establish that the theory
states or proves the canonical median contract.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

| Claim | Initial-state and input precondition | Postcondition actually claimed |
|---|---|---|
| `median-odd` | Standard empty module state; `VS` is an all-integer sequence, `len(VS) > 0`, and its length is odd | Normal execution returns the opaque integer term `sortedIntAt(VS, (len(VS)-1)/2)` |
| `median-even` | Standard empty module state; `VS` is all integers, `len(VS) >= 4`, and its length is even | Normal execution returns `intFloatDiv(sortedIntAt(VS,len/2) + sortedIntAt(VS,len/2+1), 2.0)` |

Both claims require initial `env=0`, the module and builtins scopes, fresh
scope/heap locations, empty heap and stack, `noRet`, `NoExc`, and exit code 0.
The final scopes, heap, and allocation counters are existentially framed, while
the stack/return/exception/exit cells require normal completion.

### Actual program and control-flow pinning

The `<k>` cell in each claim contains the literal complete `Module(...)` term
from submitted `solution.mpy`, followed by
`Call(Name("median"), list(VS))`. It is not a substituted helper program.
There are no loop/helper claims and no circularity claims.

The task path uses the supplied rules for:

1. `#loadAll`, statement sequencing, and `FuncDef`;
2. `Name` lookup, callee/argument evaluation, frame allocation and parameter
   binding;
3. `sorted` dispatch, allocation, and opaque `sortVS`;
4. assignment of `values` and `middle`;
5. `len`, `vsLen`, integer `//`, `pyMod`, comparison, and the `If` branch;
6. list-reference dereference, `Subscript`, `applyIndex`, and `valSeqAt`;
7. early `Return` and frame pop; and
8. on the even branch, integer addition and `intFloatDiv`.

The exact source-to-rule map is reflected in the complete inventory
`evidence/STATIC-INVENTORY.md`; the relevant source modules are
`core.k`, `functions.k`, `call.k`, `controls.k`, `builtins.k`, `sort.k`,
`operators.k`, `int.k`, `subscript.k`, and `float.k`.

This means the formal even result is faithful to the *faulty submitted
program*: it uses indices `len/2` and `len/2+1`. It is not faithful to the
canonical even median, which uses `len/2-1` and `len/2`.

### Satisfiable entry states and ground comparison

`evidence/artifacts/claim-witnesses.json` records satisfying states:

| Claim | Satisfying `VS` | Formal target after index arithmetic | Generated Python | Canonical Python |
|---|---|---|---:|---:|
| odd | `[3,1,2,4,5]` | `sortedIntAt(VS,2)` | `3` | `3` |
| even | `[4,1,3,2]` | `intFloatDiv(sortedIntAt(VS,2)+sortedIntAt(VS,3),2.0)` | `3.5` | `2.5` |

Both satisfy `allInts`; lengths 5 and 4 satisfy their respective length and
parity guards. Python comparison is in
`evidence/commands/stage4_python_witnesses.log`.

A freshly translated K witness program asserting the generated outcomes for
both states terminates with `NoExc` and exit code 0. A separate K program
asserting the canonical even value `2.5` terminates with `AssertionError` and
exit code 1. Evidence:

- reviewer sources:
  `evidence/scripts/k-witness-candidate.py` and
  `evidence/scripts/k-witness-canonical-result.py`;
- translated inputs:
  `evidence/artifacts/k-witness-candidate.mpy` and
  `evidence/artifacts/k-witness-canonical-result.mpy`;
- results:
  `evidence/commands/stage4_k_witness_candidate.log` and
  `evidence/commands/stage4_k_witness_canonical.log`.

### Adequacy defects

- `sortedIntAt` has result sort `Int`, so the returned term is type-constrained,
  but it has no equations characterizing which integer it is. Reusing the same
  term in execution and postcondition is not a theorem that it is a sorted
  order statistic.
- Neither claim states sortedness, permutation, or the median property.
- The even theorem explicitly states the wrong indices relative to canonical.
- Length two is excluded (`>= 4`), exactly hiding the submitted program's
  out-of-bounds failure on a valid canonical input.
- The formal domain is integer-only although the prompt says only “elements”
  and the Python implementation can accept some other sortable numeric lists.
- Empty-list behavior is excluded from both claims. That exclusion agrees with
  the canonical implementation's failure but is not stated in the prompt.

Stage 4 result: **FAIL.** The claims pin and summarize the actual submitted
program, but they do not constrain its result to the intended canonical median.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/STATIC-INVENTORY.md` is a 6,249-line, source-hashed inventory
generated from the fresh copy. It contains every local entry and its complete
source block:

```text
229 syntax declarations
1 configuration
5 contexts
700 rules
2 claims
937 total entries across 26 K files
```

It separately tags 148 function declarations, 109 total declarations, zero
`functional` declarations, 23 `symbol` plus `no-evaluators` opaque
declarations, 45 priority-bearing entries, two simplifications, and 35
concrete-bearing entries. The inventory generator, exact command, and output
hash are preserved in:

- `evidence/scripts/generate_static_inventory.py`;
- `evidence/commands/stage5_generate_inventory.log`;
- `evidence/STATIC-INVENTORY.md` (SHA-256
  `2198f2365f831ff496d7c8d0f495097bb732305cfe649087990af89fb69f7f3a`).

The source-reading logs are
`evidence/commands/stage5_semantics_group1.log` through
`stage5_semantics_group4.log`.

Every inventory entry receives the following source-module disposition; the
proof-local exceptions are then reviewed individually. No inventory entry is
left unclassified.

| Source module(s) | Entries/rule families | Static disposition for this theorem |
|---|---|---|
| `semantics.k` | Assembly imports, no local rules | Integrity-checked trusted assembly |
| `syntax.k` | 16 AST declarations, strictness annotations | Declarations cover every submitted AST construct; no truth conclusion by themselves |
| `core.k` | Values/configuration, load, lookup, allocation, shared sequence helpers | Used rules preserve the displayed cells and evaluation order; no target-domain false witness |
| `functions.k`, `call.k` | Closures, argument binding, frames, return/pop, call dispatch | Actual `median` body executes with one argument; return discards only the function suffix as Python return requires |
| `controls.k` | Assignment, `If`, loop/control machinery | Assignment and `If` rules are used and match the AST; loop/import rules are unreachable |
| `operators.k`, `int.k`, `bool.k` | Heating/dispatch and integer/Boolean operations | Used `+`, `//`, `%`, `==` cases have disjoint sorts and ordinary integer meaning; divisors are the concrete nonzero value 2 |
| `float.k` | Float literal and opaque/concrete float operations | Only `Float(2.0)` and `intFloatDiv` are used. Concrete twin agrees on witnesses; symbolic numerical meaning remains trusted, not proved |
| `builtins.k` | `len` plus many unrelated builtins | Used `len(list(VS)) -> vsLen(VS)` is structural; unrelated folds/eval/hash rules are unreachable |
| `sort.k` | Opaque `sortVS`, concrete insertion sort, keyed/reverse variants | Plain integer `sorted` route is used. Ordering/permutation of symbolic `sortVS` is an external supplied trust boundary; other variants are unreachable |
| `list.k` | List construction, concat/equality/iteration/membership | Only the list value/result structure used through shared rules is reachable; no list mutator is in the submitted AST |
| `subscript.k` | Indexing/slicing helpers | Positive in-bounds index route is used. Slice rules are unreachable. `valSeqAt` totality on opaque/OOB inputs is a modeling trust discussed below |
| `str.k`, `set.k`, `tuple.k`, `dict.k`, `methods.k`, `range.k`, `iter.k`, `comprehension.k` | Domain-specific declarations and rules | None of their domain operations occur on the submitted task path; their declarations do not create a rewrite from this program state to the target |
| `assert.k` | Assertion success/failure | Present in imported `MPY`, but no `Assert` term occurs in either entry program; exercised only by independent LLVM witness programs |
| `concrete.k` | LLVM-only deep equality and keyed sort | Imported by `MPY-KRUN`, not by proof module `MPY`; cannot contribute to symbolic `#Top` |
| `verification.k` | 2 syntax declarations, 5 rules, both simplifications | Reviewed individually below |
| `spec.k` | 2 claims | Both execute the real body, but their target property is inadequate/wrong as described in Stage 4 |

The fixed tree is the selected supplied semantics, not a candidate-generated
semantic extension. The static review found no false rewrite witness on the
claims' all-integer, positive/in-bounds task path. General warnings or
deliberately minimal rules for unused constructs are narrower language-model
gaps, not witnesses that a false median conclusion is reachable. I therefore
do not label those unused fixed rules unsound.

### Configuration, cells, order, allocation, and control

The actual path reads/writes:

- `<k>` for sequencing, call, expressions, return, and the final value;
- `<env>` and `<scopes>` for definition, parameter, and local bindings;
- `<scopeLoc>` and `<stack>` for the callee frame;
- `<heap>` and `<heapLoc>` when `sorted` allocates its result;
- `<ret>` during return/pop; and
- `<exc>` and `<exit-code>`, which remain normal.

`BinOp` is `seqstrict(2,3)`; `Assign` is strict in its RHS; `If` is strict in
its condition; `Subscript` contexts evaluate object then index; call arguments
use the left-to-right `#evalArgs` loop. The priority-40 dereference rules
preempt generic dispatch exactly when the allocated sorted-list reference is
consumed. The candidate adds no priority rule. No target claim omits a
state-changing cell that is material to the returned value.

### Proof-local extension inventory

#### `allInts`

Declaration:

```k
syntax Bool ::= allInts(ValSeq) [function, total]
```

Its empty, integer-head recursive, and `[owise]` non-integer-head equations are
covering and mutually coherent. Recursion descends structurally. It is a
truthful domain predicate and does not replace program execution.

Disposition: **acceptable definitional summary**.

#### `vsLen(sortVS(VS)) => vsLen(VS)`

This `[simplification]` equation has no cell footprint and affects both parity
control and subscript-index arithmetic. It is mathematically true if the
supplied `sortVS` contract really is a permutation. It is broader than the
claim guard because the rule itself has no `allInts` guard, but no false
conclusion witness exists on the intended all-integer claim domain. The
concrete insertion sort also preserves length.

There is no K theorem proving the symbolic permutation property; its truth is
conditional on the supplied opaque-sort contract.

Disposition: **conditionally acceptable derived fact for this domain; external
`sortVS` trust remains.**

#### `sortedIntAt`

Declaration:

```k
syntax Int ::= sortedIntAt(ValSeq, Int)
  [function, total, symbol(sortedIntAt), no-evaluators]
```

It has no defining equations. Its `Int` result sort supplies exactly the type
information needed for the submitted `+` and division proof. It affects both
entry-claim results.

Disposition: **fresh, result-bearing opaque symbol; not independently value
justified.**

#### Sorted-access simplification

```k
rule valSeqAt(sortVS(VS), I) => sortedIntAt(VS, I)
  requires allInts(VS)
   andBool I >=Int 0
   andBool I <Int vsLen(VS)
  [simplification]
```

Complete matched domain:

- a `valSeqAt` of the supplied opaque `sortVS`;
- any all-integer `VS`;
- an in-bounds nonnegative index;
- no cell or continuation restrictions, because it is a functional
  simplification rather than a `<k>` rule.

State footprint: none. Value footprint: total; the result controls the odd
return and both integer operands of the even return.

The guard is satisfiable, including the witnesses in Stage 4. On the intended
sort contract the equation can be *read* as naming the selected element, and I
do not claim a concrete algebraic counterexample to that reading. The narrower
and decisive defect is that there is no bridge-free universal connection
theorem showing that fixed semantics produces exactly this fresh symbol. The
postconditions reuse the same fresh term. That is the circular result-bearing
abstraction pattern:

```text
fixed access -> fresh opaque term
claim target = the same fresh opaque term
```

It proves no value equation such as `sortedIntAt([4,1,3,2],2) = 3`, no
sortedness or permutation fact, and no relationship to the canonical median.
Calling the symbol `[function,total]` does not supply those facts.

Disposition: **illegitimate, unconnected result-bearing bridge for a task
correctness proof.** This is a connection/adequacy failure, not an unsupported
claim that the displayed guarded equation has a concrete false case.

### Proof-critical removal tests

I rebuilt two fresh proof definitions:

| Variant | Build | Proof | Relevant residual |
|---|---:|---:|---|
| remove sorted-access bridge, keep its syntax | exit 0 | exit 1, stuck | `valSeqAt(sortVS(VS), i) = sortedIntAt(VS, i)` |
| remove length simplification | exit 0 | exit 1, stuck | unresolved `vsLen(sortVS(VS))` in parity/index and result equality |

Artifacts and logs:

- `evidence/artifacts/verification-no-sorted-bridge.k`;
- `evidence/artifacts/verification-no-length-lemma.k`;
- `evidence/commands/stage5_kompile_no-sorted-bridge.log`;
- `evidence/commands/stage5_kprove_no-sorted-bridge.log`;
- `evidence/commands/stage5_kompile_no-length-lemma.log`;
- `evidence/commands/stage5_kprove_no-length-lemma.log`.

One parallel no-bridge proof attempt encountered a transient Java-version
detection error and is retained as
`stage5_kprove_no-sorted-bridge_attempt1.log`; it is not used. The immediate
sequential rerun produced the expected genuine stuck claim.

These tests establish that both simplifications contribute materially to
closure and that fixed semantics alone does not provide the `sortedIntAt`
connection.

### False-conclusion witnesses and evidence gaps

The concrete false task conclusion is not attributed to a globally false K
equation; it is the formal theorem's mismatch with the canonical contract:

```text
VS = [4,1,3,2]
entry precondition = satisfied
formal/submitted result = 3.5
canonical median = 2.5
```

Length two gives a second witness: canonical returns `2.5`, the submitted
program raises `IndexError`, and no entry claim applies.

For the guarded sorted-access simplification I report the missing independent
connection theorem rather than asserting unsoundness without a rule-level
false witness. For unused fixed semantic rules I likewise report reachability
and model-scope limitations rather than manufacturing irrelevant
counterexamples.

Stage 5 result: **FAIL for proof-extension validation and theorem adequacy.**
The fixed task path is coherent, but the successful proof relies on a
result-bearing circular abstraction and states the wrong even computation.

## 6. Fresh non-vacuity test

The reviewer-authored mutation is
`evidence/artifacts/spec-vacuity-audit.k`. It keeps the actual submitted
program and the original even precondition, but changes the result obligation
from averaging:

```text
sortedIntAt(VS, len/2) and sortedIntAt(VS, len/2+1)
```

to the deliberately false repeated-middle target:

```text
sortedIntAt(VS, len/2) and sortedIntAt(VS, len/2)
```

For satisfying input `[4,1,3,2]`, the submitted program returns `3.5`; under
the supplied concrete sort the mutated repeated-middle value is `3.0`.

The dry run parsed and built successfully:

```text
exit 0
```

Evidence: `evidence/commands/stage6_mutation_dry_run.log`.

The actual proof then failed meaningfully:

```text
exit 1
WarnStuckClaimState
```

Its residual is exactly the unmet equality between:

```text
intFloatDiv(sortedIntAt(VS,len/2) + sortedIntAt(VS,len/2+1), 2.0)
```

and:

```text
intFloatDiv(sortedIntAt(VS,len/2) + sortedIntAt(VS,len/2), 2.0)
```

Evidence: `evidence/commands/stage6_mutation_proof.log`.

Stage 6 result: **PASS for structural non-vacuity.** The proof distinguishes
this false result mutation. Non-vacuity does not establish that the original
opaque terms denote the canonical median.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Conditional on the supplied semantics and candidate extensions, the two
`#Top` results establish partial-correctness execution summaries:

- for any nonempty odd-length all-integer `VS`, if the encoded call terminates
  normally, it returns `sortedIntAt(VS,(len-1)/2)`; and
- for any even all-integer `VS` of length at least four, if it terminates
  normally, it returns the opaque division term over `sortedIntAt(VS,len/2)`
  and `sortedIntAt(VS,len/2+1)`.

They establish that the actual submitted body is evaluated to those *formal
terms*. They do not establish:

- the canonical even result;
- correct behavior for length two;
- that any `sortedIntAt` has a particular integer value;
- sortedness or permutation of `sortVS` in K;
- an order-statistic or mathematical median theorem; or
- a symbolic IEEE/Python numerical interpretation of `intFloatDiv`.

### Trust ledger

| Boundary | Role/dependents | Assessment |
|---|---|---|
| K v7.1.337 parser/compiler/Haskell prover and builtin Int/Bool/Map/List hooks | All builds and claims | Ordinary low-level proof-tool trust |
| Trusted supplied semantics tree | Entire operational execution model | Integrity passed; selected semantics level, with its documented minimal Python subset |
| `sortVS` | `sorted`, both branches, candidate length lemma and sorted access | Opaque symbolic trusted primitive with concrete insertion-sort twin; ordering/permutation is not proved by these claims |
| `valSeqAt` marked `[total]` | Both subscript results | Fixed semantics leaves opaque and OOB accesses abstract; claim guards make the program indices in bounds, but totality remains a semantic trust |
| `intFloatDiv` | Even return | Opaque symbolic float primitive, concrete LLVM twin only; acceptable as a named low-level numerical boundary for structural execution, insufficient for a numeric median theorem by itself |
| Candidate `vsLen(sortVS(VS))` simplification | Length, parity, index guards | True conditional on `sortVS` being a permutation; no local K derivation |
| Candidate `sortedIntAt` plus bridge | Every claimed returned element | Illegitimate for task correctness: fresh result-bearing abstraction, no independent connection/value theorem, reused in postcondition |
| `allInts` | Both preconditions and bridge guard | Fully defined structural predicate; acceptable |
| Trusted translator and byte-identity check | Source-to-`solution.mpy` bridge for this artifact | Exact byte identity for the submitted file; this checks fidelity, not correctness |
| Differential and K witness tests | Canonical comparison and concrete semantic bridge | Finite empirical evidence only; here it disproves fidelity rather than proving a universal equivalence |

All local `symbol(...)` declarations are inventoried in
`evidence/STATIC-INVENTORY.md`. The fixed semantics has:

- sort/hash symbols: `sortVS`, `sortKeyVS`, and `md5hexCodes`;
- float/numeric symbols: `intFloatDiv`, `divII`, `floatMod`, `floatLt`,
  `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`,
  `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
  `roundF`, `roundFN`, and `sqrtF`; and
- the candidate adds `sortedIntAt`.

Only `sortVS`, `intFloatDiv`, and `sortedIntAt` affect these entry claims.
The others are unreachable from the submitted AST and therefore cannot
justify or invalidate the median result. `floorFI`, `toF`, and `ceilF` are
symbol declarations with concrete-only defining cases but without the
`no-evaluators` tag; the inventory records their exact attributes.

### Gate accounting

- Real-program execution/pinning: **partial pass**. The literal body executes,
  and the postconditions match the faulty body structurally.
- Proof-extension soundness/connection: **fail**. The result-bearing
  `sortedIntAt` bridge has no independent universal connection/value theorem.
- Intent/canonical adequacy: **fail**. The algorithm and even postcondition use
  the wrong indices and omit length two.
- Non-vacuity: **pass**. A meaningful false result mutation builds and is
  rejected at the expected obligation.
- Evidence auditability: **pass with provenance concern**. Reviewer commands,
  statuses, bounded outputs, scripts, inputs, and hashes are preserved; the
  candidate generation metadata is absent.

### Decision

Fresh `#Top` is genuine but proves only a structural summary of the wrong
even-length algorithm under an unconnected opaque element abstraction. The
ground satisfying witness `[4,1,3,2]` produces `3.5` from both the submitted
Python and supplied concrete K execution, while the trusted canonical returns
`2.5`. This is a material correctness failure, not a thin empirical bridge or
minor scope concern.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
