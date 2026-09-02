# Independent adversarial audit: 28-concatenate

## Outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof of the exact submitted generated program for finite lists of strings.
Both positive claims reconstruct from source and close, the loop lemma is
proved separately before being used modularly, and a fresh reachable
false-result mutation is rejected for the expected reason.

The verdict is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because the
candidate supplies a deliberately task-scoped generated semantics rather than
a machine-checked refinement of CPython. Its rules are sound for every
construct occurrence in this submitted program, but several rules are
over-broad as general Python rules. The finite differential evidence strongly
supports, but cannot universally prove, the remaining Python-to-K
interpretation bridge. These limitations do not enable a false conclusion for
the intended `List[str]` inputs to this exact program.

All candidate prose, logs, traces, caches, and prior proof results were treated
as untrusted. Candidate-built definitions were never used.

## 1. Input and provenance integrity

### Rendered semantics boundary

The rendered mode is `GENERATED_SEMANTICS`. Both
`/reference/reference-semantics` and a symlink at that path are absent. This is
the required mount state; there is no infrastructure breach and no hidden or
inferred reference semantics was used.

The candidate's untrusted `run-input.json` describes the `bare` condition with
no supplied semantics, which is consistent with the rendered mode. Its
`metrics.json` claims exit 0, 861 seconds, and no timeout. `codex-last.txt`,
`codex-output.log`, and the trace claim successful concrete runs and two
`#Top` proof stages. Those statements were not accepted as proof evidence.

The complete 259-line structured trace parsed as JSONL with zero malformed
records. The 11,935-line plain output log and trace were scanned for the
candidate's build/proof claims. The bounded summary, hashes, and excerpts are
in [stage1_integrity.log](evidence/stage1_integrity.log); the complete-trace
reader is [trace_summary.py](evidence/trace_summary.py).

### Trusted-file comparison and artifact types

The following byte comparisons succeeded:

| Comparison | SHA-256 | Result |
|---|---|---|
| `/candidate/prompt.py` vs `/reference/prompt.py` | `9481906207fb44fe66ec3a6b2bc82cf92b42739848b577fa9561de14375f807b` | identical |
| `/candidate/py2mpy.py` vs `/reference/py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | identical |

All required artifacts are present as regular, non-symlink files:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, the
structured trace, `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`,
`semantic.k`, `verification.k`, `spec.k`, and executable `prove.sh`. No
symlink exists anywhere under `/candidate`. There is no missing, changed,
mistyped, or symlinked required source artifact.

The candidate also contains extra generated material:
`semantic-kompiled/` and `__pycache__/solution.cpython-310.pyc`. These are
ordinary caches/build outputs, not source integrity failures. They were
explicitly ignored. No candidate `PROOF.md` or `spec-vacuity.k` exists; neither
was a generation deliverable, and fresh validation evidence was created
instead.

The source artifacts needed for execution were copied to
`/tmp/audit-work/fresh`. Their hashes remained:

- `semantic.k`: `2ddd2ef1b50f5757889d07381b11d779b92c66c21ee6aef1cd6`
- `verification.k`: `e93633b8a7730d721595849914379018046e25c0b0e6843968c3011a70a0b029`
- `spec.k`: `1b30b069c31527699f0eabea2b4448b89ea33b342a34be70f7b13f8b34cfed69`

Exact commands and exit status 0 are preserved in
[stage1_integrity.sh](evidence/stage1_integrity.sh) and
[stage1_integrity.log](evidence/stage1_integrity.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt requires:

> For a finite `List[str]`, return one string formed by concatenating the
> elements in list order. The empty list returns `""`.

The trusted canonical entry point is `return ''.join(strings)`. The candidate
entry point initializes `result = ""`, traverses `strings` left-to-right,
updates `result = result + string`, and returns `result`. This is a different
algorithm with the same value on the intended finite `List[str]` domain.

The trusted translator was run afresh:

```sh
python3 /reference/py2mpy.py /tmp/audit-work/fresh/solution.py \
  > /tmp/audit-work/fresh/solution.regenerated.mpy
```

The regenerated file is byte-identical to both the scratch copy and submitted
`/candidate/solution.mpy`; all have SHA-256
`6a7ae3bc549d9525bebb62f6f7779f4b9a28a4436c1518942ce3a5adfbc65f89`.

### Independent differential

[differential.py](evidence/differential.py) independently imports
`/reference/canonical.py` and the scratch copy of the generated
`solution.py`. It records the complete input corpus in
[differential-cases.jsonl](evidence/differential-cases.jsonl), whose SHA-256
is `e3989974bdfc2c5dc61ed222da48ceb21345a2db1987188413d22ac06ee3ad89`.

The 401 distinct cases comprise:

- both documented examples;
- explicit zero-iteration, one-iteration, empty-element, Unicode, control
  character, long-list, and long-element boundaries;
- every list of lengths 0 through 3 over five representative string atoms;
- 256 deterministic generated attempts with seed 28028, after duplicate
  inputs were removed.

Every case compared type, value, length, and result digest. Result:
`case_count=401`, `mismatch_count=0`. The exact command exited 0; see
[stage2_program_fidelity.sh](evidence/stage2_program_fidelity.sh) and
[stage2_program_fidelity.log](evidence/stage2_program_fidelity.log).

The loop has only its empty/nonempty list branch boundary, and both are covered.
No divergence was found on the intended domain. Inputs outside `List[str]` are
not part of the prompt contract.

## 3. Clean proof reconstruction

### Fresh builds

K version v7.1.293 was used. From the scratch source, two separate definitions
were built:

```sh
kompile /tmp/audit-work/fresh/semantic.k \
  --backend llvm \
  --main-module MPY-SEMANTICS \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/fresh/concrete-kompiled

kompile /tmp/audit-work/fresh/semantic.k \
  --backend haskell \
  --main-module MPY-SEMANTICS \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/fresh/proof-kompiled
```

Both builds exited 0. The resulting `backend.txt` files say `llvm` and
`haskell`, respectively. Commands, hashes, and outputs are in
[stage3_build.sh](evidence/stage3_build.sh) and
[stage3_build.log](evidence/stage3_build.log).

### Fresh generated-semantics executions

[compare_krun.py](evidence/compare_krun.py) issued and recorded seven direct
`krun` commands against only the fresh LLVM definition. Cases were empty,
singleton empty, singleton nonempty, the `abc` example, interspersed empty
strings, a prefix/empty/suffix case, and Unicode. Every run:

- exited 0;
- ended with `<k> .K </k>`;
- produced the same result as both trusted canonical Python and generated
  Python.

The summary is `cases=7`, `failures=0`; see
[stage3_concrete.log](evidence/stage3_concrete.log). Two earlier logs named
`stage3_concrete_attempt*` preserve reviewer-harness parsing mistakes: the
underlying `krun` commands already exited 0 and printed the expected states,
but the first parser did not accept multiline K formatting and the second did
not decode K's `\xHH` UTF-8 rendering. Those reviewer issues were corrected
before the successful recorded comparison and are not candidate failures.

### Positive target claims

The loop invariant was selected and proved independently:

```sh
kprove /tmp/audit-work/fresh/spec.k \
  --definition /tmp/audit-work/fresh/proof-kompiled \
  --claims SPEC.concatenate-loop
```

It exited 0 and printed `#Top`; see
[stage3_prove_loop.log](evidence/stage3_prove_loop.log).

The exact second positive target recorded by the candidate was then run:

```sh
kprove /tmp/audit-work/fresh/spec.k \
  --definition /tmp/audit-work/fresh/proof-kompiled \
  --trusted SPEC.concatenate-loop
```

Because the only other claim is `SPEC.concatenate-correct`, this marks the
already discharged invariant as the modular lemma and proves the end-to-end
claim. It exited 0 and printed `#Top`; see
[stage3_prove_entry.sh](evidence/stage3_prove_entry.sh) and
[stage3_prove_entry.log](evidence/stage3_prove_entry.log). The trusted claim is
not an unproved assumption in the audit: it is the byte-identical claim proved
by the immediately preceding independent command against the same fresh
definition.

An additional reviewer-only form combining `--claims
SPEC.concatenate-correct` and `--trusted SPEC.concatenate-loop` was interrupted
after more than five minutes without output. It is not a candidate target and
is not used for the verdict. The exact candidate target then completed
immediately. The command, status 130, and process observation are disclosed in
[stage3_optional_filtered_interrupted.md](evidence/stage3_optional_filtered_interrupted.md).

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.concatenate-loop` has no explicit `requires` clause. Its sorted
precondition says:

- control is at the exact real loop body
  `result = result + string`;
- the continuation is the real final `return result`, the `PyStmts` unit, and
  `cleanup`;
- remaining items are an arbitrary finite `StrList`;
- the accumulator holds arbitrary string `ACC`;
- argument/current/function cells hold well-sorted values;
- no result has yet been published.

Its postcondition consumes the entire continuation, resets the modeled call
cells, and requires the result to be exactly `concatAcc(ACC, ITEMS)`.

`SPEC.concatenate-correct` also has no explicit `requires`. Its sorted
precondition starts from the exact six-cell initial configuration and executes:

```text
load(<the submitted solution.mpy Module term>)
~> invoke("concatenate", lVal(INPUT))
```

for an arbitrary finite `INPUT:StrList`. Its postcondition consumes `<k>`,
resets the modeled call cells, and requires the result to be exactly
`concatAcc("", INPUT)`.

### Exact pinning and result constraint

[stage4_pinning_and_witness.py](evidence/stage4_pinning_and_witness.py)
whitespace-normalizes the submitted MPY and the claim, then checks that the
whole submitted `Module(...)` term occurs under `load`, immediately followed
by the exact invocation and `=> .K`. It also checks that the loop claim contains
the real loop body and exact post-loop suffix. All five pinning/result checks
are true; see
[stage4_pinning_and_witness.log](evidence/stage4_pinning_and_witness.log).

The result is not a fresh variable, tautology, or one-way property. It is an
equality enforced by the destination `<result>` cell. `concatAcc` has exhaustive
base/cons equations over `StrList`; no RHS-only existential can choose the
answer.

### Satisfying witnesses

Both claim preconditions are satisfiable:

1. Entry witness: `INPUT = "a" :: "b" :: "c" :: .StrList` with the exact
   initial configuration. The claimed result reduces to `"abc"`; trusted
   canonical Python and generated Python both return `"abc"`.
2. Loop witness reachable after the first iteration of that entry:
   `ACC="a"`, `ITEMS="b" :: "c" :: .StrList`, `_CURRENT="a"`,
   `_ALL="a" :: "b" :: "c" :: .StrList`, and `_FUN` equal to the loaded
   function. The claimed result reduces to `"abc"`; both Python entries return
   `"abc"` on the complete input.

The witness script exited 0. This also shows the invariant is tied to real
control flow rather than an unreachable helper state.

## 5. Rule-by-rule static soundness review

The complete numbered sources and declaration search are preserved in
[stage5_static_source_inventory.log](evidence/stage5_static_source_inventory.log).
There are exactly three local K source files: `semantic.k`, `verification.k`,
and `spec.k`.

### Local syntax, attributes, configuration, and claims

`MPY-SYNTAX` has these local declarations:

| Declaration | Productions | Audit decision |
|---|---|---|
| `Pgm` | `PyProgram` | Correct parser start sort. |
| `PyProgram` | `Module(PyStmts)` | Matches the submitted translator root. |
| `PyStmts` | delimiter-free `List{PyStmt,""}` | Matches juxtaposed translated statements and explicit `.PyStmts` unit. |
| `Params` | `Params(String)` | Covers the one submitted parameter. |
| `PyStmt` | `ImportFrom`, `FuncDef`, `Assign`, `For`, `Return` | Exactly the statement constructors used by `solution.mpy`; no used statement is missing. |
| `PyExpr` | `Name`, `Str`, `BinOp` | Exactly the expression constructors used. |
| `StrList` | `.StrList`, `String :: StrList` | Finite list-of-string input domain. |
| `PyVal` | `sVal(String)`, `lVal(StrList)` | Separates scalar strings from string lists. |
| `Function` | `noFunction`, `function(name,param,body)` | Sufficient single-function control representation. |
| `Result` | `noResult`, `PyVal` | Sufficient unpublished/published result representation. |
| `KItem` | `load`, `moduleLoaded`, `invoke`, `assignTo`, `addLeft`, `addRight`, `startFor`, `loop`, `bindLoop`, `finishReturn`, `cleanup` | All are explicit control continuations; none is opaque. |

The configuration has one top `<py>` cell and six child cells: `<k>`,
`<function>`, `<argument>`, `<accumulator>`, `<iterationItem>`, and `<result>`.
Every non-`<k>` cell is read or written by an operational rule. There is no
heap, allocation, output, exception, or general environment cell; none is
needed for the observable result of this exact first-order function.

`verification.k` adds one declaration,
`concatAcc(String, StrList):String [function]`. There is no local `[total]`,
`[functional]`, `[simplification]`, `[priority]`, `[owise]`, `[anywhere]`, or
`[concrete]` declaration or rule. There are no local opaque symbols. The
`[function]` attribute is not treated as proof of truth; the two equations were
audited below.

`spec.k` has exactly two reachability claims, inventoried in Stage 4. The loop
claim is a progressing circularity: the nonempty case executes a real loop
iteration before returning to the invariant with the structural tail. The
entry claim uses that exact separately proved claim as its only modular lemma.

### Construct-to-rule map

| Submitted construct | Declaration/rules |
|---|---|
| `Module` and `PyStmts` | semantic lines 60-62 |
| `ImportFrom("typing","List")` | line 63 |
| `FuncDef` and `Params("strings")` | lines 64-71 |
| `Assign(Name("result"), ...)` | lines 81-83 |
| `For(Name("string"), Name("strings"), body)` | lines 90-96 |
| `Return(Name("result"))` | lines 100-102 |
| `Name("strings")`, `Name("result")`, `Name("string")` | lines 75-80 |
| `Str("")` | line 74 |
| `BinOp("+", left, right)` | lines 84-86 |

Thus every syntactic construct actually used is declared and has a complete
execution path for the well-sorted submitted program.

### All 24 operational rules

| # | Source rule | Static decision |
|---:|---|---|
| 1 | `load(Module(STMTS))` | Soundly places the exact module statement list before `moduleLoaded`; continuation is preserved. |
| 2 | `.PyStmts => .K` | Correct empty statement-list identity. |
| 3 | `S REST => S ~> REST` | Correct left-to-right statement sequencing. Empty/nonempty list rules are disjoint. |
| 4 | `ImportFrom(_,_) => .K` | Sound for the exact `typing.List` import because the translated body never reads that binding and intended execution has `typing`; over-broad for arbitrary imports, documented below. |
| 5 | `FuncDef(F,Params(P),BODY)` | Correctly records name, parameter, and exact untranslated body in the sole function slot. There is one definition. |
| 6 | `moduleLoaded => .K` | Correct staging-marker removal. |
| 7 | `invoke(F,ARG)` | Requires a stored function with the same `F` and exact parameter `"strings"`, writes the argument, and schedules the exact body before cleanup. Binding is pinned; it is not selected by an unconstrained oracle. |
| 8 | `Str(S) => sVal(S)` | Faithful string-literal injection. |
| 9 | `Name("strings")` | Reads the argument cell; faithful for the parameter occurrence. |
| 10 | `Name("result")` | Reads the accumulator cell; faithful for both loop and return occurrences. |
| 11 | `Name("string")` | Reads the current iteration item; faithful for the loop body. The three name rules are disjoint. |
| 12 | `Assign(Name(X),E)` | Evaluates the RHS before the store continuation, matching Python assignment order for the used target. |
| 13 | `V ~> assignTo("result")` | Stores the evaluated value in the accumulator. Only the actually used target is completed; unsupported targets would remain visibly stuck. |
| 14 | `BinOp("+",LEFT,RIGHT)` | Schedules the left operand first. |
| 15 | `V ~> addLeft(RIGHT)` | After the left value, schedules the right and preserves the left value. |
| 16 | `sVal(S2) ~> addRight(sVal(S1))` | Returns `S1 +String S2`; operand order and string typing match the submitted `str + str`. |
| 17 | `For(Name(X),ITER,BODY)` | Evaluates the iterable before starting the loop, preserving body and target. |
| 18 | `lVal(ITEMS) ~> startFor(...)` | Admits exactly the formal finite string-list domain and starts its structural loop. |
| 19 | `loop(_, .StrList, _)` | Correct zero-iteration exit. It is disjoint from the cons rule. |
| 20 | `loop(X,S::REST,BODY)` | Binds the head, executes the body once, then loops on the structural tail; this is left-to-right and strictly descending. |
| 21 | `bindLoop("string",V)` | Updates the exact submitted loop variable before the body. Other targets fail visibly. |
| 22 | `Return(E)` | Evaluates the returned expression before publication. It does not implement general abrupt unwinding, but the submitted return is the final statement and its only suffix is `.PyStmts ~> cleanup`, so the accepted context is sound for this program. |
| 23 | `V ~> finishReturn` | Publishes exactly the evaluated return value without inventing or abstracting it. |
| 24 | `cleanup` | Resets the task's transient control cells after the sole call. No later submitted continuation observes them. This is a projection for the one-call theorem, not a model of persistent Python globals. |

Control continuations preserve the framed `<k>` suffix; cell updates touch only
the state components each operation requires. Evaluation is deterministic on
the submitted sorted terms. Potential overlap checks are clean:
empty/nonempty `PyStmts`, empty/cons `StrList`, the three literal `Name`
patterns, and the two `concatAcc` patterns are pairwise disjoint. Other rule
heads or continuation constructors differ. No priority is needed.

### Verification equations and proof-extension classification

| Rule | Class | Decision |
|---|---|---|
| `concatAcc(ACC,.StrList) => ACC` | Definitional summary | True base equation. |
| `concatAcc(ACC,S::REST) => concatAcc(ACC +String S,REST)` | Definitional summary | True left-fold step; strictly descends on `REST`. |

The equations cover every `StrList` constructor, do not overlap, and terminate.
Although the declaration lacks `[total]`, it is mathematically total on its
declared structural domain. Crucially, no operational semantic rule calls
`concatAcc`; it does not replace or bypass program execution. The universally
quantified loop reachability claim is the connection from the real operational
loop to this summary. There is no same-symbol circular oracle.

There are no operational bridges, fresh result-bearing abstractions, trusted
program helpers, simplification lemmas, or task-answer rewrites. `+String` is a
K builtin primitive, not a local proof shortcut.

### Scope limitations, not intended-domain unsoundness

No local rule was judged materially unsound for any intended finite
`List[str]` input to this exact submitted program, so there is no
intended-domain false-conclusion witness to report.

The definition is nevertheless not a reusable Python semantics:

- A hypothetical body `return "a"; return "b"` would finish with `"b"` here,
  while Python returns `"a"`, because rule 22 preserves arbitrary suffixes.
- `ImportFrom("nonexistent","X")` would be skipped here while Python raises
  `ImportError`.
- A second invocation after cleanup would not find the function slot, while a
  Python module retains its function binding.

These are concrete witnesses to out-of-scope over-breadth, not witnesses on the
submitted program or its input domain. The generated-semantics boundary allows
minimal coverage for the submitted program, but this lack of general-language
containment is one reason for the `CONCERNS` verdict rather than `PASS`.

## 6. Fresh non-vacuity test

No candidate mutation was relied upon. The reviewer created
[spec-vacuity.k](evidence/spec-vacuity.k) in scratch and preserved an identical
copy as evidence. It executes the exact submitted program on the satisfying
empty input but changes the required final result from the true `sVal("")` to
the false `sVal("!")`.

First, a dry run successfully built the mutation:

```sh
kprove /tmp/audit-work/fresh/spec-vacuity.k \
  --definition /tmp/audit-work/fresh/proof-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.concatenate-false-empty \
  --dry-run
```

This exited 0; see
[stage6_mutation_build.log](evidence/stage6_mutation_build.log).

The real proof command then exited 1. `kore-exec` emitted
`WarnStuckClaimState`, showing a fully terminated configuration with
`<k> .K </k>` and actual `<result> sVal("") </result>`, which does not unify
with the mutated destination `sVal("!")`. This is the expected unmet
result-bearing obligation, not a parser error, missing import, timeout,
unreachable mutation, or unrelated crash. The wrapper records
`MUTATION_KPROVE_EXIT_STATUS=1` and itself exits 0 after confirming the expected
failure; see [stage6_mutation_prove.sh](evidence/stage6_mutation_prove.sh) and
[stage6_mutation_prove.log](evidence/stage6_mutation_prove.log).

The proof is therefore non-vacuous and discriminates a reachable false result.

## 7. Proven versus assumed accounting

### What is machine-proved

Under the fresh K definition, the proof establishes this partial-correctness
statement:

> For every finite `INPUT:StrList`, if the exact submitted `solution.mpy` term
> starts in the stated six-cell initial configuration and its modeled
> execution terminates, the final computation is consumed and its result is
> exactly `sVal(concatAcc("", INPUT))`.

It also independently establishes the universally quantified loop invariant:
from any matching exact loop-head state, the real loop body and real return
suffix produce `concatAcc(ACC, ITEMS)`. The proof is about the real submitted
constructor tree, not a substituted helper program.

This is partial correctness. The report does not inflate the circular
reachability proof into a separate machine-checked termination theorem.

### Trust and evidence ledger

| Boundary | Influence | Basis and assessment |
|---|---|---|
| K v7.1.293 parser/compiler/Haskell prover and reachability-logic implementation | All machine-checking | Ordinary unavoidable toolchain trust; acceptable. |
| K builtin `String` representation and `+String` | Every accumulated value and final result | Fixed primitive outside the program-defined theorem. Seven K/Python boundary runs, including Unicode, support it; acceptable but not re-proved here. |
| `StrList` as finite Python `List[str]` | Formal input domain | Direct structural encoding aligned with the prompt annotation; informal representation bridge. |
| Trusted `py2mpy.py` | Program identity from Python AST to constructor tree | Problem-designated trusted input; byte regeneration pins the submitted tree. The translator's semantic adequacy is not itself formally verified. |
| Generated operational rules as a model of the used Python constructs | Control, binding, state, and result | Exhaustively reviewed rule-by-rule and dynamically compared on seven K cases; sound for every occurrence in this program, but not a universal CPython refinement. |
| `concatAcc` equations | Formal postcondition value | Truthful, exhaustive, disjoint structural equations; connected to real execution by the machine-proved loop claim. Not an assumption or opaque oracle. |
| `SPEC.concatenate-loop` used with `--trusted` in the entry proof | End-to-end claim closure | Separately proved with exit 0 and `#Top` against the identical source/definition immediately before use; discharged modular lemma, not residual trust. |
| CPython canonical-vs-generated differential | Implementation-to-intent bridge | 401 reproducible cases, zero mismatches. Strong finite evidence only; not a universal theorem. |
| Concrete K-vs-both-Python comparison | Generated-semantics bridge | Seven normal/boundary cases, zero failures. Finite evidence only. |

There is no local opaque symbol. There is no proof rule that fabricates a
result, replaces a program-defined computation with an oracle, or encodes the
desired answer into operational execution.

The remaining informal argument is the conventional one: on a finite
`List[str]`, Python's `for` traverses elements in order, Python string `+`
concatenates its operands, and the task-scoped K rules implement the same fold.
The static rule audit makes that bridge precise for this source; finite
differentials support it but do not make it machine-universal. This is an
evidence limitation, not a false-proof mechanism.

Excluded behavior includes non-`List[str]` inputs, import failure, exceptions
and finite-memory allocation failure, arbitrary programs using the declared
syntax, code after `return`, repeated calls in one K configuration, and
observations of Python global state after the call. None is requested by the
HumanEval contract.

Validation gates:

- Gate A, real-program soundness: pass.
- Gate B, intent adequacy for finite `List[str]`: pass, with the documented
  task-scoped-language limitation.
- Gate C, trust/evidence auditability: pass; all empirical evidence is
  reproducible and explicitly labeled finite.

The candidate is legitimate. The concerns are limited to the informal,
task-scoped generated-semantics bridge and do not create a material adequacy
gap for the stated program and domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
