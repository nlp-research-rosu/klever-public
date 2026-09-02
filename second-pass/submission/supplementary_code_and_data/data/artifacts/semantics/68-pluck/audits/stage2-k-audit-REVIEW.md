# Independent adversarial review: 68-pluck

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted program over the material HumanEval domain: finite lists of
nonnegative mathematical integers, including the explicitly documented empty
case. Fresh builds and both positive claims close. The entry claim executes the
constructor term regenerated from `solution.py`, and its result is constrained
to an independently understandable fold computing the minimum even value and
its first index.

The verdict is `CONCERNS / LEGIT`, rather than an unqualified pass, because the
proof-local iterator specialization uses `asInt(V)` under the generated
predicate `isInt(V)`. A bridge-free theorem over arbitrary `I:Int` closes, and
there is no false ground witness on the intended domain, but K cannot prove the
syntactically broader connection from `isInt(V)` alone. This leaves a
machine-auditability limitation around a result-bearing cast that appears in
both execution and the summary. It does not narrow the HumanEval domain or
enable an incorrect concrete result for an intended input.

## 1. Input and provenance integrity

Status: PASS. No infrastructure breach was found.

- `/audit-input.json` declares `record_layout =
  legacy-selected-stage1`, condition `semantics`, and
  `semantics_mode = SUPPLIED_SEMANTICS`. The launcher-declared container paths
  resolve to real regular files/directories; no required path is a symlink.
- `/reference/reference-semantics` is present, as required for the rendered
  mode. It contains 24 K source files. Recursive relative paths, entry types,
  and every file byte are identical to `/candidate/reference-semantics`.
  There are no missing, additional, mistyped, or linked entries.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts. Their SHA-256 values are respectively
  `cd3be7d4325387ffeafdc0c15742e1e5f66dfe1e94b683910809f5c17a9c3a74`
  and
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- The campaign-lock file hash is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the hash in `/audit-input.json`; its parsed JSON equals the complete
  `audit_campaign` block.
- All records required for `legacy-selected-stage1` are present and readable:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace. The optional
  `usage.json` is also present and checked. Historical runtime metrics are not
  required for this layout.
- Every recorded evidence-file hash matches. The complete structured trace has
  one real JSONL file, its recorded SHA-256 matches, and all 497 JSON records
  parse. The generation log and trace were read only as untrusted claims; they
  report earlier `#Top` runs but were not used as proof results.
- Independent manifest digests also match the recorded semantics manifest,
  retained workspace, and usage trace fields. Recursive byte/type comparison,
  rather than a host provenance path, establishes the critical semantics
  identity.

Reproducible evidence:
[integrity script](/audit-output/evidence/stage1_integrity.py),
[integrity log](/audit-output/evidence/stage1_integrity.log),
[generation-record reader](/audit-output/evidence/generation_records_inspect.py),
and
[generation-record log](/audit-output/evidence/generation_records_inspect.log).
The final integrity command exited 0 with `STAGE1_INTEGRITY=PASS`.

## 2. Program fidelity and candidate-versus-canonical checks

Status: PASS.

The trusted prompt asks `pluck(arr)` to return
`[smallest_even_value, first_index_of_that_value]` for a branch of nonnegative
integer nodes, or `[]` when the list is empty or contains no even value. The
prompt explicitly demonstrates the empty list even though its constraints also
say `1 <= nodes.length`; the executable contract therefore includes empty and
otherwise permits lengths through 10,000.

The trusted canonical implementation filters evens, takes their minimum, and
uses `arr.index` for the first occurrence. The candidate scans once, keeps
`-1` as a sentinel, replaces the candidate only for the first even or a
strictly smaller later even, and increments the index on every iteration.
Because input values are nonnegative, `-1` cannot collide with a legitimate
result. Equal minima do not replace the saved index.

Running the trusted translator from scratch produced a file byte-identical to
the submitted `solution.mpy`:

```text
5475741a3170980a2cf1714b3ba196e9afdb76777d1910af137995663b48ba7b
```

The exact command, both hashes, translator exit 0, and `cmp` exit 0 are in
[translation_identity.log](/audit-output/evidence/translation_identity.log).

The independent differential test imports the trusted canonical and candidate
entry points separately and also uses a third, independently written
`min((value,index),...)` oracle. It checks:

- all four prompt examples;
- empty, singleton zero/even/odd, and no-even inputs;
- the first-even sentinel path;
- later smaller, later greater, and equal-tie branch boundaries;
- duplicate zero and zero-after-positive-even cases;
- arbitrary-precision nonnegative integers;
- the documented 10,000-element maximum;
- 2,000 seeded lists of lengths 0–128 and 20 seeded lists of lengths
  1,000–10,000.

All 2,035 cases agree, with zero mismatches. See
[differential_test.py](/audit-output/evidence/differential_test.py),
[the exact corpus](/audit-output/evidence/differential_corpus.json), and
[differential_test.log](/audit-output/evidence/differential_test.log).
This is finite adequacy evidence, not a replacement for the K proof.

## 3. Clean proof reconstruction

Status: PASS.

Only source artifacts were copied to `/tmp/audit-work/candidate`. The supplied
semantics was copied from the trusted reference mount, not from a compiled
candidate definition. No candidate-provided cache or compiled definition was
used. The independently observed tools are K v7.1.293.

Fresh concrete build:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/runtime-kompiled
```

This exited 0. `krun solution.mpy` and `krun concrete_tests.mpy` against that
definition also exited 0, leaving `.K`, an empty stack, `NoExc`, and exit code
0. Evidence:
[kompile_concrete.log](/audit-output/evidence/kompile_concrete.log),
[krun_solution.log](/audit-output/evidence/krun_solution.log), and
[krun_candidate_tests.log](/audit-output/evidence/krun_candidate_tests.log).
Compiler warnings concern nonexhaustive functions or unused variables in
unrelated supplied modules; none is on the submitted execution path.

Fresh proof build:

```text
kompile verification.k --backend haskell \
  --main-module PLUCK-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/proof-kompiled
```

This exited 0; see
[kompile_proof.log](/audit-output/evidence/kompile_proof.log).

Every positive target claim was then run:

```text
kprove spec.k --definition /tmp/audit-work/proof-kompiled \
  --spec-module PLUCK-SPEC --claims PLUCK-SPEC.pluck-loop --output pretty
```

Result: `#Top`, exit 0
([kprove_pluck_loop.log](/audit-output/evidence/kprove_pluck_loop.log)).

```text
kprove spec.k --definition /tmp/audit-work/proof-kompiled \
  --spec-module PLUCK-SPEC \
  --claims PLUCK-SPEC.pluck-correct,PLUCK-SPEC.pluck-loop \
  --trusted PLUCK-SPEC.pluck-loop --output pretty
```

Result: `#Top`, exit 0
([kprove_pluck_correct.log](/audit-output/evidence/kprove_pluck_correct.log)).
The second command trusts only the loop lemma that the first command proved
without trusting it. This is a legitimate modular proof dependency.

## 4. Adequacy and real-program pinning

Status: PASS.

Plain-language claims:

- `pluck-loop` says that, from a real loop head over tail `VS` and arbitrary
  current locals `B`, `BI`, `I`, and `LAST`, execution consumes the tail,
  resumes the exact arbitrary continuation `K`, preserves `arr` and the scope
  parent, and changes the four loop locals to `scanPluck(VS,B,BI,I,LAST)`.
  Its precondition requires every remaining element to be a nonnegative K
  integer.
- `pluck-correct` starts from the clean supplied configuration, loads a module
  containing the complete submitted `pluck` binding, looks it up and calls it
  on the unboxed input `list(VS)`. It requires `allNonNegative(VS)` and ends
  with return value `ref(0)`, heap entry
  `0 |-> list(pluckResult(VS))`, heap counter 1, the exact module closure,
  empty call stack, `noRet`, `NoExc`, and exit code 0.

The entry result is therefore not free, tautological, or constrained only by
an implication. Both the returned reference and the contents of its heap
object are fixed.

Mechanical program identity was checked by extracting the complete `#loadAll`
argument from the entry claim, normalizing only the explicit K unit spellings
`.Stmts` and `.Exprs` to their omitted MPY parser spellings, and parsing both
the extracted term and submitted `solution.mpy` with the fresh definition.
The two KORE files are byte-identical:

```text
654006d8a26c54a989fced05684e2344550932bc422a1e81c63a20d31f8d1779
```

See
[extract_claimed_program.py](/audit-output/evidence/extract_claimed_program.py),
[raw extracted term](/audit-output/evidence/claimed_program_from_spec.kterm),
[submitted KORE](/audit-output/evidence/submitted_program.kore),
[claimed KORE](/audit-output/evidence/claimed_program.kore), and
[program_pinning.log](/audit-output/evidence/program_pinning.log).

Concrete satisfying states exist. For example:

```text
VS = vCons(4,vCons(2,vCons(3,.ValSeq)))
allNonNegative(VS) = true
pluckResult(VS) = vCons(2,vCons(1,.ValSeq))
```

Both Python functions return `[2,1]`. The empty input, duplicate-zero input,
and no-even input also satisfy the precondition and agree after substitution.
A concrete loop state with `B=BI=-1`, `I=LAST=0`, `L=1`, `K=.K`, and the same
`VS` summarizes to `pstate(2,1,3,3)`. Full substitutions are in
[claim_witnesses.py](/audit-output/evidence/claim_witnesses.py) and
[claim_witnesses.log](/audit-output/evidence/claim_witnesses.log).

Body sensitivity was tested separately from postcondition non-vacuity. Both
copies of the function body actually embedded in the entry claim were changed
to return `smallest + 1`; the closure post-state was changed consistently so
the mutation tested execution rather than module-loading syntax. `kprove`
reached the mutated returned heap and failed on the condition
`best + 1 == best`, with actual exit 1. See
[make_body_mutation.py](/audit-output/evidence/make_body_mutation.py),
[body_mutation_build.log](/audit-output/evidence/body_mutation_build.log), and
[body_mutation_kprove.log](/audit-output/evidence/body_mutation_kprove.log).

## 5. Rule-by-rule static soundness review

Status: PASS on the intended domain, with one evidence limitation.

### Exhaustive inventory

Every source item in the supplied semantics and `verification.k` was
inventoried, including all helper files:

```text
25 files
1,094 source items
716 rules
235 syntax declarations
153 function declarations
114 total declarations
46 priority rules
36 concrete rules
26 owise rules
25 symbol declarations
22 no-evaluator/opaque declarations
5 contexts
4 macro declarations and 1 macro-rec declaration
1 seqstrict and 2 strict declaration items
0 simplification rules
0 functional declarations
```

Each row contains the complete collapsed source item, its attributes, whether
it is on the submitted execution path, and a decision. See
[inventory_k_rules.py](/audit-output/evidence/inventory_k_rules.py),
[rule_inventory.md](/audit-output/evidence/rule_inventory.md), and
[rule_inventory.log](/audit-output/evidence/rule_inventory.log).

The constructor-to-rule map covers configuration, evaluation order, lookup,
binding, all control flow, state changes, allocation, calls, returns, and every
submitted AST constructor:
[construct_rule_map.md](/audit-output/evidence/construct_rule_map.md).

The actual path is:

```text
Module/load → FuncDef binding → Call/left-to-right argument evaluation
→ new function frame and parameter binding
→ Assign initializers
→ For/list iteration and target binding
→ integer modulo/comparisons/If/AugAssign
→ Return/ListExpr allocation
→ frame pop and ref(0) in the caller
```

The fixed semantics implements mathematical K integers, left-to-right
evaluation, current-scope writes, ordinary name lookup, one-time iterable
evaluation, sequential list iteration, first-class return, monotone heap
allocation, and frame restoration for this path. Float, string, dict, set,
slice, sort, MD5, comprehension, assertion, and concrete-only rules are
sort- or syntax-disjoint and cannot fire. Opaque symbols in those modules have
no dependent pluck claim. `MPY-CONCRETE` is absent from the proof definition.

### Proof-local rules

The complete extension analysis is in
[proof_extension_review.md](/audit-output/evidence/proof_extension_review.md).
In summary:

- `nextBest` and `nextBestIndex` have four pairwise-disjoint and exhaustive
  cases: odd; even with sentinel; even/non-sentinel/smaller; and
  even/non-sentinel/not-smaller. Their right-hand sides exactly implement the
  program update.
- `scanPluck` structurally removes one `ValSeq` constructor per equation.
  State projections are constructor projections. `pluckResult` partitions
  `best == -1` from `best != -1`; nonnegativity makes the sentinel sound.
  `allNonNegative` recursively checks both K integer sort membership and
  `>= 0`. `pluckTake` is truthful but unused.
- There are no proof-local opaque symbols, simplification rules, call
  interceptions, return shortcuts, heap shortcuts, or answer axioms.
- `asInt` is the identity on `Int` but is declared `total` over `Val` with no
  non-Int equation. Every intended ground use is an `Int`; outside that domain
  it may remain irreducible rather than fabricate a value.
- The sole operational bridge specializes the fixed list iterator under
  `isInt(V)` and has priority 40 over the fixed rule. It changes only `<k>`,
  accepts the same arbitrary continuation, preserves the identical remainder,
  and touches no environment, scope, heap, counter, stack, return, exception,
  or exit cell. For an integer it yields `asInt(I) = I`, exactly the fixed
  rule's value.

The bridge-free universal theorem over arbitrary typed `I:Int`, arbitrary
remainder, and arbitrary continuation closes with `#Top`:
[iterator_connection_int_domain_kprove.log](/audit-output/evidence/iterator_connection_int_domain_kprove.log).
Its definition imports fixed `MPY` and a separate identity cast, but no
operational bridge
([iterator_connection_kompile.log](/audit-output/evidence/iterator_connection_kompile.log)).

The same theorem stated with `V:Val requires isInt(V)` does not close because
the backend leaves `V == auditAsInt(V)` unproved
([iterator_connection_kprove.log](/audit-output/evidence/iterator_connection_kprove.log),
actual exit 1). This matters because `asInt` is result-bearing and also occurs
in `scanPluck`. It is the reason for `CONCERNS`. It is not labeled unsound:
there is no concrete or symbolic false-conclusion witness on the intended
ground integer domain, and the typed universal connection theorem proves every
such element. The narrower evidence gap is K's failure to turn its generated
sort predicate into typed equality.

No inventoried rule was labeled unsound; consequently there is no omitted
false-conclusion witness. The only challenged rule is reported as an evidence
gap rather than falsely called unsound.

## 6. Fresh non-vacuity test

Status: PASS.

No candidate mutation was trusted. The reviewer-created mutation changes only
the result-bearing entry postcondition:

```text
0 |-> list(pluckResult(VS))
```

became:

```text
0 |-> list(vCons(0, pluckResult(VS)))
```

The program term and loop lemma remained unchanged. `VS = .ValSeq` is a
satisfying witness: `allNonNegative(.ValSeq) = true`, both Python functions
return `[]`, and the mutation incorrectly requires `[0]`.

The mutated spec is preserved at
[spec_false_result.k](/audit-output/evidence/spec_false_result.k), with its
generator at
[make_false_result_mutation.py](/audit-output/evidence/make_false_result_mutation.py).
A `kprove --dry-run` build exited 0
([false_result_mutation_build.log](/audit-output/evidence/false_result_mutation_build.log)).
The actual proof then exited 1 with `WarnStuckClaimState`; its reached final
heap contains `list(.ValSeq)` and cannot unify with the prefixed result. See
[false_result_mutation_kprove.log](/audit-output/evidence/false_result_mutation_kprove.log).
This is the expected unmet obligation, not a parse error, timeout, missing
import, or unrelated crash.

## 7. Proven versus assumed accounting

Status: legitimate theorem with a documented auditability limitation.

### Precisely proven

Under the supplied K semantics, for every finite `ValSeq` whose elements are K
integers at least zero, loading the exact submitted module and calling its
`pluck` binding on `list(VS)` is partially correct: if execution terminates, it
returns `ref(0)` whose heap object is `list(pluckResult(VS))`, leaves no
exception or pending return, empties the call stack, and has exit code 0.
`pluckResult` is the structural scan that returns no elements if no even was
seen and otherwise returns the least even value plus the first index at which
that least value replaced the sentinel/current candidate.

The loop theorem is stronger than the entry invariant: it characterizes
execution from arbitrary current accumulator/index/last locals over any
nonnegative integer tail and arbitrary continuation.

The theorem covers the material source-contract domain. It does not impose a
finite size bound and therefore includes, rather than excludes, all lists up to
10,000 and the prompt's empty example. It does not replace the program with a
different algorithm or finitely many unrollings.

### Trust and assumptions

| Boundary | Dependents | Accounting |
|---|---|---|
| Trusted supplied semantics and K built-in Int/Bool/Map/List theories | Both claims | Required condition boundary. Every source item was inventoried; every used operation was path-reviewed. Unused partial/opaque modules do not affect pluck. |
| K v7.1.293 kompiler and Haskell/LLVM backends | Build, proof, and concrete evidence | Standard machine-checking trust boundary; versions and fresh commands are recorded. |
| Trusted `py2mpy.py` | Python-to-MPY identity | Byte-identical regeneration mechanically connects `solution.py` to the submitted MPY term. |
| MPY subset versus CPython for the used constructs | HumanEval interpretation | Used integer/list/control behavior was statically reviewed and tested against both Python implementations. Differential evidence is finite and supports, but does not prove, this bridge. |
| `asInt` plus priority iterator specialization | Loop and entry claims | Identity for all intended typed integers is machine-checked. The broader `isInt(V)` connection is not machine-checked; this is the reported concern. |
| `scanPluck` means “least even, first index” | Human-facing postcondition | Its equations and disjoint guards give the ordinary induction argument; the concrete substitutions and 2,035-case independent differential provide additional finite evidence. No separate K theorem names the human phrase. |
| `pluck-loop` trusted in the entry command | Entry claim | Acceptable modular dependency because the loop claim was independently proved `#Top`, exit 0 first. |
| Opaque float/sort/MD5 symbols in fixed semantics | None | Inert for this program and absent from every result/control dependency. |
| Termination | Final interpretation | This review reports partial correctness as requested. Termination is not claimed as a separate theorem, although finite-list execution and the structural loop decrease are evident. |

Gate summary:

- Clean verification: PASS.
- Real-program pinning and ground-domain soundness: PASS.
- Intent/domain adequacy: PASS.
- Non-vacuity and body sensitivity: PASS.
- Trust/evidence auditability: CONCERN because the complete
  `V:Val requires isInt(V)` bridge connection does not close, despite the
  exact typed integer-domain connection closing and no false intended-domain
  witness.

This limitation is nonfatal under the benchmark decision boundary: the
candidate does not materially narrow the HumanEval domain, does not prove a
substituted term, and does not rely on a rule with an exhibited false
conclusion on an intended input. The honest result is therefore legitimate
with concerns.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
