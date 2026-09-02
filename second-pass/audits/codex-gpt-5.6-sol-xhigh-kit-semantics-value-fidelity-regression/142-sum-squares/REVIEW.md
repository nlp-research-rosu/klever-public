# Independent adversarial review: 142-sum-squares

## Decision

The candidate contains a legitimate partial-correctness proof of the submitted
function under the supplied MPY semantics. The proof was rebuilt from source,
the two-claim target proof closed with `#Top`, the entry state pins the exact
translated function body, the result is constrained, and a fresh false-result
mutation fails at the intended obligation.

The result is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for two evidence
limitations:

1. `verification.k:30-35` adds sound integer `applyBin` sort-recovery bridges.
   The candidate's bridge-free connection claims cover syntactically
   `Int`-typed operands. Reviewer-authored claims over the bridges' exact
   `A:Val, B:Val` plus `isInt(A) andBool isInt(B)` domain do not close because
   the backend cannot derive an `Int` sort cast from `isInt`. A ground-constructor
   case analysis establishes the rules' truth, and opposite ground results are
   rejected, but the exact-domain connection is not itself machine-checked.
2. The supplied translator and MPY-to-CPython/natural-language adequacy are
   trusted/empirical bridges. Byte identity and 20,043 differential cases
   support them but do not universally prove them.

No proof-local rule was found to enable a false conclusion on the intended
all-integer domain. In particular, I do **not** call the arithmetic bridges
unsound: there is no false witness, their correct ground values close, their
wrong ground values get stuck, and their equations agree with fixed `MPY-INT`
for every ground value satisfying their guards.

## 1. Input and provenance integrity

### Infrastructure and semantics boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. There is no infrastructure-mode
contradiction.

The independent integrity script recursively compared entry type and file
SHA-256 for the trusted and candidate semantics trees:

- trusted entries: 25;
- candidate entries: 25;
- missing, additional, changed, or mistyped entries: 0;
- semantics symlinks: 0.

The candidate prompt and translator are regular files and byte-identical to
their trusted mounts:

- `prompt.py`:
  `3705edce076dd10a274c837a15bf688a69bd9c342a0576cabb0cb02ab7c53446`;
- `py2mpy.py`:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

All required candidate artifacts are present as regular files:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `spec.k`,
`verification.k`, `prove.sh`, and `PROOF.md`. There are no symlinks anywhere
under `/candidate`. The candidate also contains non-required tests, proof
probes, caches, and compiled directories; they were treated as untrusted and
none was copied into or used by the clean builds.

Evidence:

- [integrity script](evidence/check_integrity.py)
- [integrity result](evidence/01-integrity.log), exit `0`

### Untrusted generation claims

I read and classified the requested metadata solely as untrusted claims:

- `run-input.json` names problem `142-sum-squares`, condition
  `kit-semantics`, and the supplied input hashes.
- `metrics.json` claims a 1,887-second run, exit `0`, and no timeout.
- `codex-last.txt` and the tail of `codex-output.log` claim `VALIDATED`,
  positive `#Top`, 19,608 differential cases, and expected mutation failures.
- `codex-output.log` has 55,674 lines and SHA-256
  `87d7f1428c03ea34b54a5aa801fe6bef513fcc15ff7725f9614d59ab6033f760`.
- One structured JSONL trace is present. It has 605 valid JSON records, no
  malformed records, and SHA-256
  `b5d831b987f871c47b2ab75ff813b13430772244e094c5b5d9242cd736d291ef`.

None of those success markers is used below as proof evidence. The bounded
reviewer summary is [00-untrusted-provenance.log](evidence/00-untrusted-provenance.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a finite list of integers, use zero-based indices. Square an element when
its index is divisible by 3. Otherwise cube it when its index is divisible by
4. Leave every other element unchanged, then return the sum. At an index such
as 12 that is divisible by both 3 and 4, the square branch takes precedence.
The prompt examples require:

- `[1,2,3] -> 6`;
- `[] -> 0`;
- `[-1,-5,2,-1,-5] -> -126`.

The trusted canonical implementation builds the transformed sequence and uses
`sum`. The candidate uses one pass with `total` and `index`. Its `elif
index % 4 == 0` omits an explicit `index % 3 != 0`, but that condition follows
from failure of the preceding `if`. Repeated multiplication is equivalent to
square/cube exponentiation for the integer domain.

### Translator fidelity

In scratch, the exact trusted command regenerated the MPY:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
```

`cmp` returned `0`. Both submitted and regenerated files have SHA-256
`7e38e83fd449b6b33fccfd881ed3076db7bf09bbdd894b3c34e7c86743a2092a`.
See [02-regenerate-identity.log](evidence/02-regenerate-identity.log).

### Independent differential test

The reviewer script imports `/reference/canonical.py` and the scratch copy of
the candidate implementation by explicit file path. It also evaluates ground
instances of the formal `sumSquares(VS,0,0)` postcondition. Its scope was:

- 12 curated cases: all prompt examples, empty input, lengths crossing indices
  0, 3, 4, 6, 8, 9, and 12, negative branch values, and large integers;
- every list of lengths 0 through 6 over elements `-2..2` (19,531 cases);
- 500 deterministic generated lists, seed `142_20260723`, lengths 0 through
  40, values `-20..20`.

Total: 20,043 cases, zero canonical/candidate/formal-summary mismatches and
zero input mutations. The complete 2.64 MB input/result record is preserved.

Evidence:

- [reviewer differential script](evidence/reviewer_differential.py)
- [bounded result](evidence/03-python-differential.log), exit `0`
- [complete inputs and results](evidence/differential-inputs.jsonl)

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/142-sum-squares`. Candidate
compiled definitions, `__pycache__`, cache files, and prior KORE were not
copied or referenced.

### Concrete definition and execution

The supplied source semantics was freshly compiled:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

It exited `0`; see [04-llvm-kompile.log](evidence/04-llvm-kompile.log).
The build emitted supplied-semantics totality warnings for unrelated float,
sorting, joining, and indexing helpers. None is used by this program.

`krun solution.mpy --definition runtime-audit-kompiled` exited `0` and loaded
the exact closure to a final `.K`, `NoExc`, exit code `0`
([07-krun-submitted-module.log](evidence/07-krun-submitted-module.log)).

A reviewer assertion program contains an AST-identical copy of the candidate
function and eight normal/boundary assertions. It was translated with the
trusted translator and ran to `.K`, `NoExc`, exit code `0`
([concrete source](evidence/concrete_audit.py),
[translation](evidence/06-translate-concrete-audit.log),
[LLVM execution](evidence/08-krun-concrete-audit.log)).

### Proof definition and positive targets

The Haskell proof definition was freshly built:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

Exit `0`: [09-verification-kompile.log](evidence/09-verification-kompile.log).

Positive proof results:

| Command | Result |
|---|---|
| `kprove spec.k --definition verification-audit-kompiled --spec-module SPEC --claims SPEC.loop-invariant` | exit `0`, `#Top` ([log](evidence/10-kprove-loop-invariant.log)) |
| `kprove spec.k --definition verification-audit-kompiled --spec-module SPEC` | exit `0`, `#Top` ([log](evidence/12-kprove-all-targets.log)) |

The second command proves the complete two-claim proof set, including the entry
claim. The entry depends on the loop-invariant circularity. Filtering to only
`SPEC.sum-squares` removes that circularity; a depth-80 diagnostic reaches the
second symbolic loop iteration and exits `1`, as expected
([diagnostic](evidence/11-kprove-entry-filtered-depth80.log)). An earlier
unbounded filtered diagnostic was interrupted and is fully accounted for in
[11a-entry-filtered-unbounded-note.md](evidence/11a-entry-filtered-unbounded-note.md).
That filtering behavior is not a failure of the actual mutually supporting
two-claim proof.

### Arithmetic bridge reconstruction

A separate bridge-free Haskell definition importing fixed MPY and only a value
projection was freshly built (exit `0`,
[13-bridge-connection-kompile.log](evidence/13-bridge-connection-kompile.log)).
Both candidate typed connection claims independently exit `0` with `#Top`:

- addition: [14-kprove-bridge-plus.log](evidence/14-kprove-bridge-plus.log);
- multiplication: [15-kprove-bridge-times.log](evidence/15-kprove-bridge-times.log);
- combined: [16-kprove-bridge-all.log](evidence/16-kprove-bridge-all.log).

They carry `WarnTrivialClaim`: fixed MPY and the projection equations normalize
both sides to the same typed integer operation. This is a universal result over
syntactically `Int` operands, but not over the bridges' exact symbolic
`Val`-typed guard domain. Reviewer exact-domain claims build but get stuck
because the prover retains `isInt(A) == true` without recovering an `Int`
subsort cast:

- [exact-domain source](evidence/bridge-domain-spec.k);
- [addition residual](evidence/17-kprove-bridge-exact-domain-plus.log), exit `1`;
- [multiplication residual](evidence/18-kprove-bridge-exact-domain-times.log), exit `1`.

This narrower evidence gap is a concern, not an unsound-rule witness.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.loop-invariant` says: for any remaining integer sequence `VS`, starting
index `I`, and starting total `R`, executing the exact source loop over `VS`
consumes the loop, changes `total` to `sumSquares(VS,I,R)`, changes `index` to
`advanceIndex(VS,I)`, and leaves `value` as an existential final loop value.
The local `lst` binding and arbitrary surrounding scopes/continuation are
framed. Its sole precondition is `allInts(VS)`.

`SPEC.sum-squares` says: from a completely fixed initial MPY state, calling the
`sum_squares` binding on any `VS` satisfying `allInts(VS)` returns exactly
`sumSquares(VS,0,0)`. Scope/heap locations, heap, stack, return state,
exception state, and exit code are all fixed and restored.

### Program identity and control-flow pinning

The reviewer pinning check establishes:

- submitted MPY equals trusted-regenerated MPY byte-for-byte;
- the concrete assertion function is AST-identical to `solution.py`;
- the entry claim contains exactly one closure whose body is the complete
  translated function body;
- the entry `<k>` contains exactly one required symbolic call;
- the loop claim body is exactly the third argument of the translated `For`.

See [check_program_pinning.py](evidence/check_program_pinning.py) and
[05-program-pinning.log](evidence/05-program-pinning.log), exit `0`. The
preserved [05a log](evidence/05a-program-pinning-initial-script-error.log) is an
auditor-script bug from initially comparing `For` syntax directly to the
runtime `#loop` control point; it is not candidate evidence.

The symbolic entry starts after module loading, with the exact generated
closure preinstalled, rather than beginning at `Module(...)`. This does not
substitute the function: fixed call, argument binding, all assignments, loop
control, branches, name lookup, arithmetic, return, frame cleanup, and the
exact body execute. Fresh concrete execution of the submitted module confirms
the preceding deterministic `FuncDef` load step.

The loop lemma's unused `ORIG` allows a suffix unrelated to local `lst`; this is
sound because the loop has already captured its iterable and its body never
reads `lst`. The entry reaches the lemma with `VS` equal to its actual input.

### Satisfiable state and result constraint

Substitute `VS = vCons(1,vCons(2,vCons(3,.ValSeq)))` into the exact entry state
in `spec.k:47-99`. `allInts(VS)` reduces to `true`; thus the entry precondition
is satisfiable. The formal destination reduces to `6`, and both trusted
canonical and candidate Python implementations return `6`. Empty, negative,
and index-12 ground formal results also agree.

The ground K claims all close with `#Top`, exit `0`
([source](evidence/ground-summary-spec.k),
[result](evidence/21-kprove-ground-summaries.log)). The matching Python/formal
values are recorded in [03-python-differential.log](evidence/03-python-differential.log).

The returned result is not free, existential, tautological, or only constrained
by a one-way implication. It is the explicit total integer term
`sumSquares(VS,0,0)`. The only RHS existential is the loop-local final `value`,
which cannot affect the following `Return(Name("total"))`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer parser inventoried every declaration in the supplied semantics,
`verification.k`, and `spec.k`: 949 records total.

- supplied baseline: 928 declarations;
- proof-local: 19 declarations;
- target claims: 2;
- 709 rules, 232 syntax declarations, 5 contexts, 1 configuration, 2 claims;
- attributes/tags include 151 functions, 114 totals, 45 priorities, 35
  concrete declarations, 27 `owise`, 25 symbols, and 22 `no-evaluators`;
- zero `functional` declarations and zero simplification rules.

Every record contains exact file/line, full statement text, attributes,
relevance, and a review disposition:

- [inventory generator](evidence/inventory_k.py)
- [complete JSONL](evidence/k-declaration-inventory.jsonl)
- [complete TSV](evidence/k-declaration-inventory.tsv)
- [summary](evidence/k-declaration-summary.md)
- [focused proof-local/used/opaque review](evidence/20-k-inventory-focused.log)

Every supplied-baseline record is accepted only at the selected
`SUPPLIED_SEMANTICS` level after recursive identity checking. That acceptance
does not extend to `verification.k`; all 19 proof-local declarations have
individual decisions in the inventory.

The exact syntax/rule mapping for every construct used by `solution.mpy`,
including configuration, evaluation order, calls, frame state, loop protocol,
guards, priorities, allocation, returns, and overlaps, is
[construct-to-semantics-map.md](evidence/construct-to-semantics-map.md).

### Proof-local declarations

The five proof-local `[function,total]` symbols are:

- `allInts`: empty/cons constructor coverage; structural descent;
- `contribution`: three disjoint and exhaustive modulo guards;
- `intVal`: `Int` identity plus a disjoint `owise` non-Int case;
- `sumSquares`: empty plus disjoint `isInt`/`notBool isInt` cons cases,
  consuming one node;
- `advanceIndex`: empty/cons cases, consuming one node.

Their 12 defining equations are true on their complete declared domains. The
non-Int `sumSquares` and zero-valued `intVal` fallback are outside the entry
domain and do not fabricate any integer-list result. No recursion can increase
or preserve the `ValSeq` argument.

The remaining two proof-local rules are pure operational bridges:

```text
applyBin("+", A:Val, B:Val) => intVal(A) +Int intVal(B)
applyBin("*", A:Val, B:Val) => intVal(A) *Int intVal(B)
requires isInt(A) andBool isInt(B)
```

Complete matched context: any pure function term context, with no `<k>`,
continuation, control stack, binding, heap, return, exception, output, or
allocation cell. State footprint: empty. Value influence: multiplication
builds square/cube terms; addition updates total/index and therefore the final
postcondition.

Ground soundness follows by exhaustive constructor reasoning at the selected
semantics level. A ground `Val` satisfying K's generated `isInt` predicate is
an injected `Int`; `intVal` then returns that integer, while fixed `MPY-INT`
returns exactly integer `+Int` or `*Int`. On the overlap with the fixed typed
rules, both RHSs agree. Every other ground `Val` makes the guard false. The
rules have no priority and cannot preempt control/state effects.

Machine/ground checks support that review:

- fixed typed connections close (`14`-`16` logs above);
- extended correct `2+3 -> 5` and `2*3 -> 6` close
  ([22](evidence/22-kprove-bridge-correct-plus.log),
  [23](evidence/23-kprove-bridge-correct-times.log));
- opposite `2+3 -> 6` and `2*3 -> 7` fail with residual values `5` and `6`
  ([24](evidence/24-kprove-bridge-wrong-plus.log),
  [25](evidence/25-kprove-bridge-wrong-times.log)).

The exact guarded-domain theorem gap is recorded rather than mislabeled as
unsound. There is no concrete or symbolic valuation in the intended ground
domain that makes either bridge conclude a wrong value.

### Fixed semantics, opaque symbols, and warnings

Relevant fixed rules preserve left-to-right operand/argument evaluation,
evaluate `For`'s iterable once, bind each head before the body, execute the body
before looping, evaluate augmented-assignment RHS before updating the named
binding, and restore every call cell on return. The entry has no input
mutation, I/O, exception, or user heap allocation.

All 22 opaque/no-evaluator declarations belong to supplied float, sort, or
digest support and are unused. No opaque symbol affects a branch, state,
return, or postcondition here. The LLVM non-exhaustiveness warnings likewise
name unused supplied helpers. No proof-local priority or simplification can
bypass execution, and no rule encodes the task's final answer.

## 6. Fresh non-vacuity test

The reviewer copied the genuine two-claim spec, changed the module name, and
mutated only the result-constraining entry destination from:

```text
sumSquares(VS,0,0)
```

to:

```text
sumSquares(VS,0,0) +Int 1
```

For the satisfying input `[1,2,3]`, actual/formal execution returns `6`, while
the mutation demands `7`.

The mutation source is [spec-false-result.k](evidence/spec-false-result.k).
It builds/parses successfully:

```text
kprove spec-false-result.k --definition verification-audit-kompiled \
  --spec-module SPEC-FALSE-RESULT --dry-run
```

Exit `0`: [26-false-result-dry-run.log](evidence/26-false-result-dry-run.log).

The real proof command exits `1` with `WarnStuckClaimState`. Its residual has
executed to `sumSquares(VS,0,0)` and fails exactly the implication that this
equals `sumSquares(VS,0,0) +Int 1`:
[27-false-result-kprove.log](evidence/27-false-result-kprove.log).
This is meaningful non-vacuity evidence, not a parser error, missing import,
timeout, or unreachable mutation.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Conditional on the selected K definition and the sound proof-local equations,
for every finite `ValSeq VS` whose elements are K `Int` values, the exact
submitted `sum_squares` closure has this partial-correctness property:

> If its call terminates from the fully pinned initial state, it returns the
> fold that squares indices divisible by 3, otherwise cubes indices divisible
> by 4, otherwise adds the unchanged element.

The proof executes the actual body and proves its loop invariant. It does not
prove termination, resource bounds, behavior on non-integer elements, full
CPython behavior, or the correctness of arbitrary unused MPY constructs.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Trusted supplied `reference-semantics` | Defines all execution, state, control, arithmetic dispatch, and calls | Authorized selected semantics; recursively identical. It is a partial Python model, not a proof of CPython. |
| K v7.1.293, Haskell/LLVM backends, KORE prover, SMT, generated strictness/sort predicates | Proof closure and concrete execution | Standard unavoidable toolchain trust boundary. |
| Generated `isInt` means membership in the `Int` subsort, plus free ground constructor reasoning | Justifies the two sort-recovery bridges | Low-level and mathematically sound, but the exact guarded-domain connection did not machine-close; primary concern. |
| Trusted `py2mpy.py` | Connects `solution.py` to `solution.mpy` | Byte freshness is proved; translator semantic correctness is assumed. |
| Exact closure/body structural check and fixed `FuncDef` rule | Connects the call-state theorem to the submitted module | Strong pinning; module load is concretely checked, not included in the symbolic entry claim. |
| Natural-language interpretation and canonical implementation | Connects `sumSquares` to HumanEval intent | The index partition is direct ordinary mathematics; 20,043 finite differential cases provide empirical support, not universal proof. |
| K `Int` versus intended Python integers | Numeric result | Both are unbounded here; Python `bool` is excluded because MPY has a distinct `Bool` sort. |
| Supplied opaque float/sort/digest symbols | None on this program | Unused and therefore harmless to this theorem. |

There is no proof-local unconstrained oracle, opaque result, answer-encoding
shortcut, semantic fabrication for a used construct, or imported candidate
cache. Candidate `PROOF.md`, prior traces, and differential tests were not
substituted for the reconstructed K proof.

### Gate summary

- Real-program soundness: pass. Exact body and loop are pinned; the proof-local
  equations are ground-sound; correct and opposite bridge values discriminate;
  the false-result mutation fails.
- Intent adequacy: pass with the explicit finite-list-of-K-Int domain and
  partial-correctness scope. The ordinary mathematical summary matches the
  prompt and canonical behavior.
- Evidence/auditability: concern. The exact `Val`/`isInt` bridge connection is
  justified by a ground sort-membership case analysis rather than a closing
  exact-domain K theorem, and translator/intent evidence remains finite or
  trusted.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
