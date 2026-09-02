# Independent adversarial audit: 69-search

## Executive decision

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted generated program under its freshly rebuilt Mini-Python
semantics. The proof is not vacuous, and its only proof-time operational bridge
is the exact conclusion of a separately reconstructed reachability proof
against the raw semantics.

The verdict is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because the
universal postcondition is equality to an executable recursive fold,
`searchSpec`. The fold is transparently consistent with the English
greatest-qualifying-value contract on non-empty positive lists, and it received
strong differential support, but no separate K theorem states and proves that
declarative maximum property. The formal entry claim is also broader than the
prompt in its input type: it covers every non-empty K integer sequence, while
the prompt promises positive integers. The equality theorem remains true on
that broader domain, but `searchSpec` should not be read as the prompt contract
there.

All candidate logs, traces, compiled definitions, caches, and prose were treated
only as untrusted claims. All executable evidence cited below was regenerated
from source in `/tmp/audit-work/69-search-audit`; candidate-provided compiled
definitions were never copied or used.

## 1. Input and provenance integrity

### Semantics-mode boundary

This audit was rendered in `GENERATED_SEMANTICS` mode. The trusted mount contains
exactly the expected top-level inputs:

- `/reference/canonical.py`
- `/reference/prompt.py`
- `/reference/py2mpy.py`

`/reference/reference-semantics` is absent. Thus the trusted mounts do not
contradict the rendered mode, and there is no infrastructure breach. I did not
search for, infer, or use any hidden reference semantics.

The complete check, including entry types, is in
`evidence/01-provenance.log` (exit 0).

### Required artifacts and identity checks

All inspected required candidate artifacts are regular files: `run-input.json`,
`metrics.json`, `codex-last.txt`, `codex-output.log`, `prompt.py`, `py2mpy.py`,
`solution.py`, `solution.mpy`, `semantic.k`, `verification-core.k`,
`verification.k`, `loop-lemma-spec.k`, `spec.k`, and `prove.sh`. The structured
trace is present at
`/candidate/codex-trace/2026/07/22/rollout-2026-07-22T05-32-21-019f8962-317a-7832-9db6-91fced374d7e.jsonl`.

No symlink occurs anywhere below `/candidate`. No required artifact is missing
or mistyped. The candidate's prompt and translator are byte-identical to the
trusted mounts:

| Artifact | Trusted and candidate SHA-256 | `cmp` |
|---|---|---|
| `prompt.py` | `62a5a2d0332d73a27da26ab1a46a7302d27bff719d9d354887d0a27a7cdc776a` | 0 |
| `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | 0 |

The candidate has additional helper source files
`verification-core.k` and `loop-lemma-spec.k`; both are legitimate parts of the
proof and are audited below. It also has extra generated/non-source entries:
`__pycache__/`, `semantic-kompiled/`, `verification-core-kompiled/`,
`verification-kompiled/`, and `kore-exec.tar.gz`. These are not source-integrity
failures, but none was trusted or reused.

### Untrusted generation reports

`run-input.json`, `metrics.json`, `codex-last.txt`, all 20,783 lines of
`codex-output.log`, and all 332 JSONL trace records were parsed or scanned as
untrusted generation evidence. They claim that the run was the bare condition,
did not time out, and ended with successful proof runs. Those claims were not
used to establish the verdict. A bounded full-file summary, hashes, marker
counts, and the final trace message are preserved in
`evidence/01-untrusted-generation-summary.log` (exit 0), produced by
`evidence/untrusted_generation_summary.py`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt requires `search(lst)` for a non-empty list of positive
integers. It must return the greatest integer `v > 0` whose frequency in `lst`
is at least `v`, or `-1` if no such value exists.

The trusted canonical implementation constructs a frequency array and scans
indices in increasing order. The submitted `solution.py` instead initializes
`answer = -1`, visits each list element, tests
`lst.count(value) >= value`, and retains the greatest passing element. On the
intended domain, every possible answer occurs in the list, so examining list
elements is sufficient; repeated examinations do not change the maximum. The
different asymptotic complexity is irrelevant to partial correctness.

### Trusted translation

The submitted Python was translated afresh with the trusted
`/reference/py2mpy.py`. The regenerated output and submitted `solution.mpy`
both have SHA-256
`d068f8ea064b79652859045ae46cf07357c5f05dc9619d1433f279b028fc92c6`,
and `cmp` exited 0. Exact command, status, and hashes are in
`evidence/02-translation-identity.log`.

### Independent differential execution

`evidence/differential_test.py` independently imports the trusted canonical
entry point and the scratch copy of the generated entry point. Its input set is
fully recorded in `evidence/02-differential-inputs.jsonl` and contains:

- the three documented examples;
- ten named boundary/branch cases, including frequency just below and exactly
  at a value, both outcomes of the inner maximum test, a single large value,
  and order permutations;
- every list over values `1..5` at lengths `1..6` (19,530 inputs);
- 2,000 deterministic random non-empty positive lists, with lengths `1..40`
  and values `1..100`.

There were 21,543 intended-domain cases and zero mismatches. The exact command
and summary are in `evidence/02-differential.log` (exit 0).

Three out-of-domain diagnostics were retained rather than silently folded into
the intended-domain result. Empty input differs: canonical Python raises
`ValueError`, while the candidate returns `-1`. Input `[0]` differs: canonical
returns `-1`, while the candidate returns `0`. These are not material
divergences because the trusted contract requires a non-empty list of positive
integers. They do, however, show why the intended-domain qualification matters.

Stage 2 result: **pass on the intended domain**.

## 3. Clean proof reconstruction

### Scratch isolation and concrete semantics

Only the source files and trusted inputs were copied to scratch. Output
definitions were newly created under
`/tmp/audit-work/69-search-audit/build`; no candidate `*-kompiled` directory or
cache entered the build.

The generated semantics was rebuilt from `semantic.k` with:

```text
/usr/bin/kompile semantic.k --backend llvm --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/69-search-audit/build/semantic-kompiled
```

It exited 0; see `evidence/03-build-semantic-llvm.log`.

The freshly compiled semantics then executed the exact submitted
`solution.mpy` on 13 intended-domain normal/boundary inputs and two
out-of-domain diagnostics. Every run exited 0, ended with `<k> .K </k>`, and
agreed with candidate Python. Every intended-domain run also agreed with
canonical Python. The input set is
`evidence/03-semantic-inputs.json`; all emitted `krun` commands and comparisons
are in `evidence/03-semantic-differential.log` (driver exit 0). This includes a
zero-iteration loop on empty input as a semantic boundary diagnostic.

### Proof definitions and every positive claim

The raw proof definition was freshly built with:

```text
/usr/bin/kompile verification-core.k --backend haskell --main-module VERIFICATION-CORE --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/69-search-audit/build/verification-core-kompiled
```

It exited 0 (`evidence/03-build-verification-core.log`). The raw loop invariant
was then proved without importing the later summary rule:

```text
/usr/bin/kprove loop-lemma-spec.k --definition /tmp/audit-work/69-search-audit/build/verification-core-kompiled --spec-module LOOP-LEMMA-SPEC
```

It printed `#Top` and exited 0
(`evidence/03-kprove-loop-invariant.log`).

The final proof definition was freshly built with:

```text
/usr/bin/kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/69-search-audit/build/verification-kompiled
```

It exited 0 (`evidence/03-build-verification.log`). Each entry claim was then
run in its own `kprove` process:

| Claim | Selection | Result | Evidence |
|---|---|---|---|
| example one | `--claims SPEC.example-one` | `#Top`, exit 0 | `evidence/03-kprove-example-one.log` |
| example two | `--claims SPEC.example-two` | `#Top`, exit 0 | `evidence/03-kprove-example-two.log` |
| example three | `--claims SPEC.example-three` | `#Top`, exit 0 | `evidence/03-kprove-example-three.log` |
| universal entry | `--claims SPEC.functional-correctness` | `#Top`, exit 0 | `evidence/03-kprove-functional-correctness.log` |

Stage 3 result: **pass**. All positive targets closed under fresh definitions.

## 4. Adequacy and real-program pinning

### Plain-language meaning of the claims

The three example claims each start from `boot`, the exact `searchProgram`,
their respective concrete list, an empty environment, and `noResult`. They
require termination at `.K`, an empty environment, and respectively results
`2`, `3`, and `-1`.

The universal entry claim starts from the same control/program/environment/result
state with input `VList(cons(H,T))`. Its only formal input precondition is that
the K list is non-empty; `H` and all elements of `T` are arbitrary mathematical
integers. It requires final result
`VInt(searchSpec(cons(H,T)))`.

The loop claim starts at the actual loop head after a `value` binding exists.
It accepts arbitrary full list `L`, remaining list `IS`, answer `A`, and
previous value. With the exact final-return continuation and exact three-binding
environment, it requires final result `scan(L,IS,A)`.

### Exact program identity

The `searchProgram`, `searchBody`, and `searchLoopBody` macros expand to the
same constructor tree as `solution.mpy`:

1. initialize `answer` to unary-minus `1`;
2. iterate `value` over `lst`;
3. test `lst.count(value) >= value`;
4. if true, test `value > answer`;
5. assign `answer = value` only on the inner true branch;
6. return `answer`.

The match is visible side-by-side in
`evidence/04-05-static-inventory.log`, and the constructor file was independently
regenerated byte-for-byte in Stage 2. Thus the macro is an abbreviation for the
submitted generated program, not a substituted algorithm.

At entry, the proof executes the real raw semantics through `boot`, assignment,
loop setup, and the first loop iteration. The loop summary cannot match before
that first iteration because its exact environment requires a `"value"`
binding. After the first real iteration, it summarizes the remaining actual
loop and exact return continuation using the separately proved loop theorem.

### Result constraint and satisfying states

The postcondition fixes `<result>` to a concrete `VInt(...)`; it contains no
free result variable, tautology, implication escape, or omitted result cell.
The bridge likewise fixes the result to `scan(L,IS,A)` and clears the exact
environment in the same way as raw return execution.

A concrete satisfying universal-entry state is:

```text
<k> boot </k>
<program> searchProgram </program>
<input> VList(cons(1, cons(2, cons(2, .Ints)))) </input>
<env> .Map </env>
<result> noResult </result>
```

Substitution `H = 1`, `T = cons(2,cons(2,.Ints))` reduces the claimed result to
`searchSpec([1,2,2]) = 2`. The candidate and canonical Python implementations
both return `2`, and fresh K execution returns `VInt(2)`. Additional satisfying
substitutions `[1]`, the first prompt example, and the no-answer example all
agree. Exact states and values are in
`evidence/04-claim-witnesses.log` (exit 0).

Stage 4 result: **pass**, with the domain/intent limitation discussed in
Stages 2 and 7.

## 5. Rule-by-rule static soundness review

The complete numbered source and declaration extraction is preserved in
`evidence/04-05-static-inventory.log`. The following inventory is exhaustive
for local syntax, functions, rules, claims, and special attributes in
`semantic.k`, `verification-core.k`, `verification.k`,
`loop-lemma-spec.k`, and `spec.k`.

### Syntax, configuration, and declaration inventory

`MPY-SYNTAX` declares:

- `Module(Module(Stmts))`;
- `Stmts` as a zero-separator list of `Stmt`;
- `Params(Strings)` and comma-separated `Strings`;
- statement constructors `FuncDef`, `Assign`, `For`, `If`, and `Return`;
- expression constructors `Int`, `Name`, `UnaryOp`, `Attribute`, `Call`, and
  `Compare`;
- `Exprs`, `CmpOp`, and `CmpOps`.

`MPY` declares:

- `IntSeq` as `.Ints` or `cons(Int,IntSeq)`;
- values `VInt`, `VBool`, and `VList`;
- result `noResult` or a `Value`;
- control item `boot`;
- partial K functions `eval`, `negate`, `asInt`, and `asInts`;
- total K function `count`;
- control items `exec`, `execStmt`, `choose`, and `loop`.

Its sole configuration has exactly the state required by the submitted
program: `<k>`, `<program>`, `<input>`, `<env>`, and `<result>`. There is no
heap, allocation state, call stack, I/O, or exception cell because the target
program uses none of those effects.

`VERIFICATION-CORE` declares three macros (`searchProgram`, `searchBody`,
`searchLoopBody`) and four proof-side functions. `promote`, `scan`,
`searchSpec`, and the unused `positive` function are all declared
`[function,total]`.

There are no declarations marked `[functional]`, no opaque symbols, no
`[simplification]`, `[anywhere]`, `[owise]`, or `[trusted]` rules, and no local
axioms. The only explicit priority is `[priority(40)]` on the derived loop
bridge.

### Mapping from every used constructor to behavior

| Used generated construct | Declaration | Behavior |
|---|---|---|
| `Module`, `FuncDef`, `Params` | `semantic.k:5,7,10` | exact `boot` rule at lines 85–88 |
| statement list | `semantic.k:6` | empty/sequence rules at lines 90–91 |
| `Assign(Name(...),...)` | lines 11, 17 | environment update at lines 93–94 |
| `For(Name(...),...)` | lines 12, 17 | loop setup/iteration at lines 101–105 |
| `If` | line 13 | boolean dispatch at lines 96–99 |
| `Return` | line 14 | result/return control at lines 107–109 |
| `Int` | line 16 | `eval` at line 58 |
| `Name` | line 17 | guarded environment lookup at lines 59–60 |
| unary `"-"` | line 18 | lines 61 and 69 |
| `Attribute(...,"count")` and one-argument `Call` | lines 19–20 | lines 62–63 plus recursive `count` |
| single `Compare` with `">="` | lines 21, 23–24 | lines 64–65 |
| single `Compare` with `">"` | lines 21, 23–24 | lines 66–67 |

Every constructor in `solution.mpy` therefore has both syntax and applicable
behavior. The single-element subsorts supplied by K list syntax make the call
and comparison equations intentionally match the one argument and one
comparison emitted by this program. Unsupported call shapes, operators, or
types do not silently fabricate a value; the partial functions become stuck.

### Exhaustive semantic-rule decisions

| ID | Rule | Decision and justification |
|---|---|---|
| S1 | `eval(Int(I),_) => VInt(I)` | Sound literal interpretation. |
| S2 | guarded `eval(Name(X),RHO)` | Sound lookup when the key exists; missing names remain visibly unmodeled. |
| S3 | unary-minus evaluation | Sound for the only used operator and integer operand. |
| S4 | `Call(Attribute(E,"count"),ARG)` | Sound for the target's pure integer-list count call; it delegates to fully defined `count`. |
| S5 | `Compare(...,">=",...)` | Sound integer comparison for the target's outer guard. |
| S6 | `Compare(...,">",...)` | Sound integer comparison for the target's inner guard. |
| S7 | `negate(VInt(I))` | Sound mathematical-integer negation. |
| S8 | `asInt(VInt(I))` | Sound type projection; other values are intentionally stuck. |
| S9 | `asInts(VList(IS))` | Sound list projection; other values are intentionally stuck. |
| S10 | `count(_, .Ints) => 0` | Sound base case. |
| S11 | equal-head count step | Soundly adds one and structurally descends. |
| S12 | unequal-head count step | Soundly skips the head under `I =/=Int J` and descends. |
| S13 | exact `boot` rule | Soundly binds the supplied input to parameter `lst` for the exact top-level `search` definition. |
| S14 | `exec(.Stmts) => .K` | Sound sequence base case. |
| S15 | statement-sequence decomposition | Preserves left-to-right statement order. |
| S16 | assignment rule | Evaluates against the old environment and then updates the named binding, matching the target. |
| S17 | `If` setup | Evaluates the pure guard against the current environment before branch selection. |
| S18 | `choose(true,...)` | Selects exactly the then branch. |
| S19 | `choose(false,...)` | Selects exactly the else branch. |
| S20 | `For` setup | Evaluates the target list once and initializes the explicit iterator. This is faithful because the body never mutates the list. |
| S21 | empty-loop rule | Sound zero-iteration termination. |
| S22 | non-empty-loop rule | Binds the next integer before executing the body, then returns to the remaining list; this matches Python iteration for this immutable target. |
| S23 | return rule | Evaluates the return expression, clears local bindings, and discards the active function continuation. This is faithful for the top-level function and for any return location expressible in this stack-free subset. |

The `eval` equations have disjoint constructor/operator heads on all used
terms. `count`'s cons rules are disjoint (`I == J` versus `I =/=Int J`),
collectively cover integer heads, and recurse on a strictly shorter `IntSeq`.
The partial projections are applied only to values of their matching
constructors along every target path.

Expression evaluation is encoded by pure K functions rather than explicit
evaluation frames. The target expressions contain only immutable integer/list
lookups, count, and comparisons, so no observable order, state, exception, or
allocation effect is lost. Python's arbitrary-precision integer behavior is
matched by K's mathematical integers for all used operations.

### Exhaustive helper/proof-rule decisions

| ID | Rule | Class | Decision and justification |
|---|---|---|---|
| V1 | `searchProgram` macro | syntactic definition | Exact abbreviation for the submitted module/function constructor. |
| V2 | `searchBody` macro | syntactic definition | Exact abbreviation for initialization, loop, and return in `solution.mpy`. |
| V3 | `searchLoopBody` macro | syntactic definition | Exact abbreviation for both nested guards and assignment. |
| V4 | true-guard `promote` equation | definitional summary | Returns `I` exactly when frequency and strict-maximum tests both hold. |
| V5 | complemented `promote` equation | definitional summary | Returns `A` under the exact Boolean complement of V4. The guards are disjoint and exhaustive. |
| V6 | `scan(_, .Ints, A) => A` | definitional summary | Sound fold base case. |
| V7 | non-empty `scan` step | definitional summary | Applies the same `promote` operation as one loop iteration and structurally descends. |
| V8 | `searchSpec(L) => scan(L,L,-1)` | definitional summary | Names the loop fold from the program's initial answer. |
| V9 | `positive(.Ints) => true` | definitional summary | Mathematically sound base case, though unused by every claim. |
| V10 | recursive `positive` step | definitional summary | Sound conjunction of head positivity and tail positivity; structurally terminating and unused. |
| B1 | priority-40 exact loop/return rule | derived operational bridge | Sound because its entire transition is exactly the separately proved raw loop reachability claim. |

All five total functions have complete constructor/guard coverage and structural
descent where recursive. No totality attribute is being used to hide an
undefined result. In particular, the `promote` equations are exact Boolean
complements and cannot disagree on an overlap.

### Operational bridge audit

B1 matches:

- exactly `loop("value",IS,searchLoopBody)` followed by exactly
  `exec(Return(Name("answer")) .Stmts)`;
- exactly `searchProgram`;
- input `VList(L)`;
- exactly the three local bindings `answer`, `lst`, and `value`, with no map
  remainder;
- exactly `noResult`;
- every cell in the configuration.

Its `<k>` pattern has no ellipsis or arbitrary suffix, so it does not accept a
broader continuation than the raw lemma. It writes exactly `.K`, `.Map`, and
`VInt(scan(L,IS,A))`, which are the raw lemma's complete destination. `L`, `IS`,
and `A` need no reachability relation: the raw lemma itself proves the result
universally for those variables. The previous value is correctly irrelevant
because a non-empty next step overwrites it, and the empty case returns `A`.

Priority 40 makes B1 preempt the default loop step only in this exact proved
context. Priority is not used as a justification; the raw lemma is.

The result-bearing value `scan` is not opaque and is not an oracle. The raw
lemma is the universal connection theorem from actual loop execution to that
value. `scan`'s equations are independently visible, total, and terminating.

As a distinct body-sensitivity check, I changed only the real macro loop guard
from `>=` to `>` while leaving `promote` unchanged. The mutated raw definition
built successfully, but the loop proof exited 1 with
`WarnStuckClaimState`; its residual exposed the unmet equality between scanning
with `promote(L,I,A)` and scanning with unchanged `A`. For the concrete boundary
`L = [1], I = 1, A = -1`, the original body promotes to `1`, while the mutation
does not. The mutation, diff, build, and failure are preserved in:

- `evidence/04-body-mutation-verification-core.k`
- `evidence/04-body-mutation-diff.log`
- `evidence/04-body-mutation-build.log`
- `evidence/04-body-mutation-kprove.log`

### Language-model limits

This is intentionally a minimal generated semantics, not full CPython. It does
not model arbitrary objects, mutation during iteration, dynamic dispatch,
general calls, exceptions, heaps, or unsupported AST nodes. None is exercised
by `solution.mpy` on a positive integer list. Missing behavior for unused
constructs is therefore not a defect in `GENERATED_SEMANTICS` mode.

No inventoried rule is labeled unsound, so there is no unsound-rule
false-conclusion witness to report. The narrower evidence gap is instead the
unformalized declarative interpretation of `searchSpec`, accounted for in
Stage 7.

Stage 5 result: **pass for real-program soundness**.

## 6. Fresh non-vacuity test

The candidate did not supply `spec-vacuity.k`; no candidate mutation was
trusted. I created the fresh, separately named
`evidence/06-spec-vacuity.k`. It uses the satisfiable initial input `[1]` but
changes the result obligation from the true `VInt(1)` to false `VInt(2)`.

First, a `kprove --dry-run` compiled the mutated specification to KORE and
exited 0. The command wrapper, exact inner command, byte count, and status are
in `evidence/06-vacuity-dry-run.log`; the generated claim is
`evidence/06-vacuity-dry-run.kore`.

The actual proof command was:

```text
/usr/bin/kprove spec-vacuity.k --definition /tmp/audit-work/69-search-audit/build/verification-kompiled --spec-module SPEC-VACUITY
```

It exited 1 for the expected semantic reason, not a parser/build/import failure.
`WarnStuckClaimState` shows a fully terminated configuration with
`<result> VInt(1) </result>`, which cannot match the mutated `VInt(2)`
destination. See `evidence/06-vacuity-kprove.log`.

Stage 6 result: **pass**. The proof discriminates a false result.

## 7. Proven versus assumed accounting

### What the machine-checked proof establishes

Conditional on the audited K definition and K's built-ins, the successful
reachability proof establishes:

1. The exact loop body, from the exact loop-head/return-continuation
   configuration, reaches result `scan(L,IS,A)` for all finite K integer
   sequences `L` and `IS` and all integer answers `A`.
2. From the exact entry state, the exact submitted constructor program on every
   non-empty K integer sequence reaches an empty computation and result
   `searchSpec(input)`.
3. The three prompt examples reach results `2`, `3`, and `-1`.

This is a partial-correctness statement. I do not upgrade it to a separate
formal termination theorem, even though all modeled recursion and iteration
structurally descend on finite `IntSeq` values.

It does not machine-prove full CPython semantics, asymptotic complexity,
behavior on empty/non-positive inputs under the English contract, or a
quantified declarative “greatest qualifying positive integer” predicate.

### Trust and assumption ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K parser/compiler/Haskell and LLVM backends | Underlie every build, run, and proof | Standard unavoidable proof-tool trust boundary; independently rebuilt and cross-checked concretely. |
| K built-in `Int`, `Bool`, `Map`, generated list, and K-sequence operations | Arithmetic, comparisons, guard logic, lookup/update, syntax lists, and control sequencing | Acceptable low-level language primitives. No task answer is hidden in them. |
| Generated `semantic.k` | Defines the individually generated Mini-Python subset | Audited rule by rule and concretely compared with both Python implementations on normal/boundary cases. This is a custom semantics, so its Python correspondence is a model argument rather than a theorem about CPython. |
| Trusted translator `/reference/py2mpy.py` | Connects `solution.py` to `solution.mpy` | Trusted input; byte-identity regeneration establishes the submitted constructor artifact. |
| `searchProgram` macros | Connect the proved program term to `solution.mpy` | Exact constructor-tree identity, not an assumption or alternate implementation. |
| Raw loop reachability claim | Justifies operational bridge B1 | Machine-checked from raw semantics in a definition that does not import B1. Body-sensitivity mutation confirms dependence on the real guard. |
| `count`, `promote`, `scan`, `searchSpec` | Carry all result-bearing computation in the semantics/spec | Fully defined by guarded, terminating equations; none is opaque. `scan` is connected universally to raw loop execution by the loop proof. |
| `positive` | No dependent claim | Sound but dead proof helper; it supplies no hidden precondition and contributes nothing to closure. |
| Python interpreter and trusted canonical implementation | Differential oracle for implementation/intent and finite K/Python checks | Empirical support only, not part of or a substitute for the K proof. |
| Informal fold-to-English argument | Connects `searchSpec` to “greatest positive value with frequency at least itself” on positive lists | Plausible and straightforward: `promote` preserves the greatest qualifying element seen so far, and `scan` visits every list occurrence. Nevertheless, no separate declarative K invariant/theorem formalizes this bridge. This is the principal concern. |

The differential corpus is comparatively broad, not thin: 21,543
intended-domain Python comparisons with no mismatches. The fresh semantics
received 13 intended-domain normal/boundary comparisons. These data support
only the tested bridges. They do not replace the universal raw loop proof or
turn the informal intent bridge into a theorem.

### Gate accounting and final rationale

- **Fresh reconstruction:** pass.
- **Real-program soundness:** pass. The exact program executes, the sole bridge
  has a universal raw-semantics connection proof, all state/control context is
  contained, and the result is constrained and non-vacuous.
- **Intent adequacy:** the theorem covers the intended non-empty positive-list
  domain and the implementation matches the trusted canonical implementation
  throughout the recorded corpus. Concern remains because the English
  maximum property is represented by an executable fold rather than a separate
  declarative K theorem, and because the formal claim itself does not state the
  prompt's positivity restriction.
- **Evidence auditability:** pass. Scripts, complete input corpus, exact
  commands, exit statuses, bounded logs, mutations, and residuals are preserved
  under `/audit-output/evidence/`.

The concern does not allow a false result under the intended domain, does not
make the proof vacuous, and does not replace execution with an oracle. It is
therefore a limitation of the formal intent bridge, not a reason to reject the
proof as illegitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
