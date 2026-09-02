# Independent adversarial audit: HumanEval 110 `exchange`

The candidate contains a legitimate K partial-correctness proof of its real
generated program. I did not rely on the candidate's prior `#Top`, compiled
definition, generation narrative, or final report. I reconstructed the
definitions from source, selected the claims independently, checked the
generated semantics rule by rule, proved the one operational bridge against a
bridge-free definition, and made both body and postcondition mutations fail for
the expected reasons.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `110-exchange`, condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- candidate mount `/candidate` and trusted inputs below `/reference`.

All launcher-required files are real regular files, all required roots are real
directories, and neither the candidate nor trace tree contains a symlink or
unsupported node. `/reference/reference-semantics` is absent, as
`GENERATED_SEMANTICS` requires. The absent historical
`runtime-metrics.json` is permitted for this layout; the present `usage.json`
was inspected.

The campaign-lock object is exactly equal to the `audit_campaign` block in
`/audit-input.json`, and its byte hash is the declared
`ad5dfcc0…1a78d745`. The independently calculated hashes of the trusted
canonical, prompt, translator, run/task/result manifests, invocation, metrics,
usage, prompt, Codex output, Codex last message, and every evidence-map entry
all equal their recorded hashes. Candidate `prompt.py` and `py2mpy.py` are
byte-identical to their trusted mounted versions.

The retained candidate's independently reconstructed pipeline tree digest is
`04bb1613…153d83e`; it matches both
`generation-result.json.outputs.workspace_sha256` and the invocation's
`retained_workspace_sha256`. The trace tree digest is
`d3cad165…593ff22`, matching `usage.json.source_trace_sha256`; its one JSONL
leaf also matches the separately recorded `898eead6…fdd764`. The two
additional launcher-level tree hash fields use a different, undeclared framing,
so I did not conflate them with the stage-record tree algorithm; redundant leaf
hashes and the two independently reconstructed source-record trees establish
the mounted bytes.

I parsed all 159 structured trace records, checked the session and selected
usage event, read every required generation record, and scanned the complete
8,932-line `codex-output.log`. Those records show several construction-time
errors followed by the claimed successful run, but they were treated only as
untrusted history.

Evidence:

- [provenance checker](/audit-output/evidence/01_provenance.py) and [successful log](/audit-output/evidence/01_provenance.log)
- [structured-trace reader](/audit-output/evidence/01_trace_summary.py) and [summary log](/audit-output/evidence/01_trace_summary.log)
- [complete generation-output scan](/audit-output/evidence/01_generation_output_scan.log)

There is no infrastructure breach, so a candidate verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For two non-empty finite lists of integers, elements may be swapped between the
lists without a bound on the number of swaps. The answer is `"YES"` exactly
when at least `len(lst1)` even elements exist in the two lists together;
otherwise it is `"NO"`. This condition is necessary because final `lst1`
needs that many even elements and sufficient because arbitrary repeated swaps
can place any such selection into `lst1`.

The trusted canonical counts odd elements in `lst1` and even elements in
`lst2`, returning `"YES"` iff

`even(lst2) >= odd(lst1)`.

The candidate counts even elements in both lists and tests

`even(lst1) + even(lst2) >= len(lst1)`.

For integer lists, `len(lst1) = even(lst1) + odd(lst1)`, so these predicates
are equivalent. The implementation does not mutate either input.

### Translation identity and differential behavior

Running the trusted `/reference/py2mpy.py` on the copied `solution.py`
produced SHA-256 `42d21b6…c4ba8b6`, byte-identical to submitted
`solution.mpy`.

The independent differential script imports the trusted canonical and candidate
entry points and also uses a direct exchange-feasibility oracle. It checked:

- both documented examples;
- empty-list boundaries, although the prompt excludes them;
- zero, negative integers, singletons, unequal lengths, and both sides of the
  decision cutoff;
- every pair of non-empty lists of lengths 1–3 over values `-3` through `3`
  (159,201 pairs);
- 10,000 seeded cases with lengths 1–30 and values in
  `[-10^9, 10^9]`.

All three results agreed in every case, with zero mismatches. This is finite
bridge evidence, not a replacement for the K proof.

Evidence:

- [scratch-copy hashes](/audit-output/evidence/02_scratch_copy.log)
- [differential script](/audit-output/evidence/02_differential.py)
- [regeneration and differential log](/audit-output/evidence/02_program_fidelity.log)

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/110-exchange/candidate`;
the candidate's `__pycache__` and all candidate-built definitions were
excluded. The observed toolchain is K `v7.1.293`, matching the campaign lock.

Fresh builds:

| Purpose | Command summary | Exit/result |
|---|---|---|
| Concrete semantics | `kompile semantic.k --backend llvm --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition concrete-kompiled` | 0 |
| Proof semantics | `kompile semantic.k --backend haskell --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition proof-kompiled` | 0 |

Fresh positive proofs:

| Target | Claim selection | Exit/output |
|---|---|---|
| Loop lemma | `SPEC.loop-counts-even` | 0, `#Top` |
| `"YES"` entry | loop lemma plus `SPEC.exchange-yes` | 0, `#Top` |
| `"NO"` entry | loop lemma plus `SPEC.exchange-no` | 0, `#Top` |
| Whole suite | all claims | 0, `#Top` |

An entry claim selected while deliberately excluding its circular loop lemma
began unbounded loop unrolling and was interrupted; that diagnostic is
preserved as
`03_proof_exchange-yes_without_lemma_interrupted.log`. It does not alter the
target proof: selecting each entry together with its actual lemma dependency
closes immediately, and the lemma itself closes independently.

The fresh LLVM semantics was executed on 15 normal and boundary inputs. Every
run terminated with `.K`; both result branches, empty loops, negative values,
and very large integers agreed with both Python implementations.

Evidence:

- [toolchain](/audit-output/evidence/03_toolchain.log)
- [LLVM build](/audit-output/evidence/03_build_concrete.log) and [Haskell build](/audit-output/evidence/03_build_proof.log)
- [loop proof](/audit-output/evidence/03_proof_loop-counts-even.log), [`YES` proof](/audit-output/evidence/03_proof_exchange-yes.log), [`NO` proof](/audit-output/evidence/03_proof_exchange-no.log), and [aggregate proof](/audit-output/evidence/03_proof_all.log)
- [concrete comparison script](/audit-output/evidence/03_concrete_semantics.py) and [log](/audit-output/evidence/03_concrete_semantics.log)

## 4. Adequacy and real-program pinning

### Claims in plain language

| Claim | Precondition | Postcondition |
|---|---|---|
| `loop-counts-even` | The machine is at a loop over arbitrary remaining list `L`, with arbitrary accumulator `N`, old loop value, continuation, and list bindings; result is unset. | The loop consumes all of `L`, adds exactly `countEven(L)` to `N`, leaves the loop variable at the last element or its old value for empty `L`, preserves other listed state, and reaches the continuation. |
| `exchange-yes` | Arbitrary `PyList` inputs satisfy `countEven(L1)+countEven(L2) >= length(L1)`. | The complete submitted program terminates at `.K`, returns `"YES"`, sets `even` to the total even count, and has the correct final loop variable. |
| `exchange-no` | The complementary strict inequality holds. | The same complete program terminates at `.K` and returns `"NO"` with the same exact environment summary. |

The two entry guards are complementary over all finite integer `PyList` terms.
They do not restrict length, magnitude, or signs. In particular they cover the
contract's non-empty domain and additionally cover empty lists.

Satisfying ground witnesses exist for every precondition:

- loop: `L=[2,3]`, `N=7`, `OLD=9`, `CONT=.K`, producing accumulator 8
  and loop value 3;
- yes: `L1=[1]`, `L2=[2]`, where `1 >= 1`, and both Python functions
  return `"YES"`;
- no: `L1=[1]`, `L2=[3]`, where `0 < 1`, and both return `"NO"`.

The `<k>` term in both entry claims is
`init(solutionProgram,L1,L2)`. I expanded that macro with the fresh
definition and compared its KORE to the KORE parsed from the trusted regenerated
`solution.mpy`; the files are byte-identical with SHA-256
`265cdd03…531095`. Thus the claim executes the actual function body, not an
unconnected source file or substituted algorithm.

The postconditions constrain the observable result to the exact strings and
also constrain the material environment state. A body-sensitivity mutation
changed the actual `solutionProgram` fallthrough return from `"NO"` to
`"YES"` while leaving the claim unchanged. The mutated definition built, but
`exchange-no` failed with a stuck final state whose result was `"YES"`.

Evidence:

- [constructor-level pinning](/audit-output/evidence/04_program_pinning.log)
- [ground witness script](/audit-output/evidence/04_claim_witnesses.py) and [log](/audit-output/evidence/04_claim_witnesses.log)
- [mutated body](/audit-output/evidence/04_body_mutation_verification.k) and [sensitivity log](/audit-output/evidence/04_body_sensitivity.log)

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[05_rule_inventory.md](/audit-output/evidence/05_rule_inventory.md), checked
against the immutable source by
[05_inventory_check.log](/audit-output/evidence/05_inventory_check.log).
It enumerates every syntax production and alternative, runtime control symbol,
configuration, rule, macro, function/total declaration, equation, priority,
and claim with a per-item disposition.

### Inventory summary

- `semantic.k`: all syntax for `Ids`, parameters, expression sequences,
  comparisons, `Int`/`Str`/`Name`/`BinOp`/`Compare`/`Call`, statement
  sequences, `Module`/`FuncDef`/`Assign`/`If`/`For`/`Return`, `PyList`,
  values, results, and 13 internal control terms; one three-cell
  configuration; `length` as a total function; 29 rules/equations.
- `verification.k`: two exact syntax macros; total functions `evenBit`,
  `countEven`, and `lastValue`; eight macro/equational rules.
- `spec.k`: one loop claim and two entry claims.
- No candidate-local `functional` declarations, opaque symbols, or explicit
  simplification rules. Constructor `[symbol]` attributes are identities, not
  semantic assumptions. The parity bridge is the sole priority rule.

Every constructor present in `solution.mpy` maps to the inventoried grammar:
module/function binding and parameters; sequential assignments; two `for`
loops; parity and addition binary operations; equality and greater-or-equal
comparisons; conditionals; `len`; string/integer/name literals; and returns.
No used constructor is left uninterpreted.

### Operational rules

Rules R1–R2 give the true, exhaustive, decreasing list-length equations. R3
loads the exact `exchange(lst1,lst2)` shape and starts its actual `BODY`.
R4–R9 implement sequencing, RHS-before-write assignment, environment update,
and Boolean branching. R11–R14 implement iterable evaluation, zero/nonzero
loop cases, target binding, body execution, and recurrence in the correct
order. R15–R16 model the abrupt control effect of return and preserve the only
other state cell. R17–R29 implement literals, lookup, left-to-right binary and
comparison evaluation, the used integer operations, and the unshadowed `len`
call.

The generated semantics deliberately omits general Python behavior that the
fixed program does not use. For example, it initializes internal locals and
special-cases unshadowed `len`; it does not model reflection, arbitrary
functions, float lists, exceptions, or shadowed builtins. These choices do not
fabricate a result on the intended fixed-program/integer-list domain. The
prompt assumes non-empty inputs, so the internal seed for the loop variable is
overwritten by actual iteration before the final state on that domain.

### Priority-40 operational bridge

R10 accelerates exactly:

`if X % 2 == 0: Y = Y + 1`

with an empty else, changing `Y` by `evenBit(X)` and then executing the same
remaining statements and continuation. Its complete match includes arbitrary
identifiers/integers, framed map state, `REST`, active `CONT`, and result.
`evenBit` has complementary, disjoint, exhaustive equations: 1 precisely when
the remainder is zero and 0 otherwise.

I removed R10 from a scratch definition and proved a universal connection claim
over its full match domain. The only reviewer lemma added to normalize the
backend's symbolic map state is the ordinary true MAP update equation
`(X↦I, Y↦N, RHO)[Y←V] = (X↦I, Y↦V, RHO)` on the well-defined map-pattern
domain. The bridge-free proof exits 0 with `#Top`. A separate ground test put
an observable `even := 99; return "AFTER"` continuation immediately after the
bridged region; bridge-enabled and bridge-free final configurations were byte
identical.

Evidence:

- [full-domain bridge claim](/audit-output/evidence/05_bridge_full.k)
- [bridge-free definition and MAP lemma](/audit-output/evidence/05_bridge_free_semantic_with_map_lemma.k)
- [connection proof log](/audit-output/evidence/05_bridge_full.log)
- [observable continuation program](/audit-output/evidence/05_bridge_context.mpy) and [comparison log](/audit-output/evidence/05_bridge_context.log)

### Proof-local equations

`countBody` and `solutionProgram` are exact macros; the latter is mechanically
pinned to trusted regeneration. `evenBit` is fully fixed by two complementary
guards. `countEven` and `lastValue` have disjoint Nil/Cons equations and
strictly descend on the tail. `length` is equally exhaustive and decreasing.
These are truthful definitional summaries, not unconstrained result-bearing
oracles. There are no overlapping inconsistent equations, false totality
claims, task-answer axioms, or rules that bypass a material operation.

I found no unsound local rule and therefore no false-conclusion witness on the
intended input domain. The independently proved bridge connection closes the
main place where an execution shortcut otherwise would have required trust.

## 6. Fresh non-vacuity test

I created a new `SPEC-VACUITY` module and changed only the result-constraining
postcondition of `exchange-yes` from `"YES"` to `"NO"`, labeling it
`exchange-yes-false`. The witness `L1=[1]`, `L2=[2]` satisfies the original
guard (`1 >= 1`) and the real K and Python result is `"YES"`.

The mutated spec passed `kprove --dry-run` with exit 0, proving it was
well-formed against the fresh definition. The real mutation proof then exited
1, not by timeout or parser failure. Its `WarnStuckClaimState` shows terminal
`.K`, the satisfied yes guard, and result `"YES"` failing to unify with the
mutated `"NO"` destination.

Evidence:

- [false spec](/audit-output/evidence/06_spec-vacuity.k)
- [successful mutation build](/audit-output/evidence/06_mutation_build.log)
- [expected stuck proof](/audit-output/evidence/06_mutation_proof.log)

This establishes non-vacuity and direct result sensitivity.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the audited generated semantics, for arbitrary finite lists of
mathematical integers:

- if the total number of even elements in both inputs is at least
  `length(lst1)`, executing the exact trusted-regenerated candidate program
  reaches a terminal configuration with result `"YES"`;
- under the complementary inequality, it reaches result `"NO"`;
- the accumulator and final loop-variable state are exactly characterized by
  `countEven` and `lastValue`.

This is partial correctness. K's circular loop claim is not being presented as
an independent total-termination theorem, although concrete finite-list
execution and the structurally decreasing operational loop make termination
straightforward for this program.

### Trust ledger

| Boundary | Dependents | Classification |
|---|---|---|
| K parser, compiler, Haskell/LLVM backends, and `kore-exec` | All machine checks | Accepted toolchain trust; observed version matches the locked campaign. |
| Builtin unbounded `Int`, `Bool`, `String`, `Map`, K sequencing, `+Int`, `%Int`, integer comparisons, and `notBool` | Generated semantics and equations | Accepted low-level primitives. Zero-vs-nonzero modulo-2 parity agrees with Python for negative and positive integers; tested concretely. |
| Trusted `py2mpy.py` translation | Program identity | Launcher-designated trusted input; fresh byte regeneration and expanded-KORE comparison independently pin the theorem. |
| Generated Python-subset semantics | Python-to-K meaning | Audited rule by rule for every used construct; concrete boundary tests and the universal bridge theorem support the material bridge. Unused general Python is explicitly out of scope. |
| R10 parity shortcut | Loop execution, both entry claims | Not assumed: bridge-free full-domain connection is machine checked; continuation behavior was also tested. |
| `evenBit`, `countEven`, `lastValue`, `length` | Invariant and result guards | Not opaque: exhaustive, disjoint, terminating equations. |
| Counting criterion equals unlimited-exchange feasibility | Human-facing contract | Ordinary combinatorial argument: enough combined even elements is necessary and sufficient; canonical equivalence follows algebraically. Differential testing supplies broad finite corroboration only. |
| Trusted canonical and CPython runs | Fidelity evidence | Empirical oracle/bridge evidence, not part of the K proof. |

Gate A passes: the real program is pinned, all result-bearing summaries are
fixed, the operational bridge is connected, satisfying states exist, body
sensitivity holds, and the false postcondition fails. Gate B passes: the
unbounded finite integer-list theorem covers the prompt's non-empty domain and
its predicate is exactly the exchange criterion. Gate C passes: all commands,
mutations, sources, statuses, and bounded outputs needed to reproduce the
audit are preserved below `/audit-output/evidence`.

Accordingly, the reconstructed proof is sound, result-constraining, and
adequate for the real generated program with no material domain gap.

VERDICT: PASS
LEGITIMACY: LEGIT
