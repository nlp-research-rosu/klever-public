# Adversarial proof audit: 56-correct-bracketing

## Executive decision

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied semantics. A clean Haskell definition built from
source proves the mutually recursive target set with exit status 0 and `#Top`.
The entry claim embeds the byte-identical trusted translation of
`solution.py`, returns a fully defined Boolean summary, and is rejected by both
a false-postcondition mutation and a real-body mutation.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, for three
evidence limitations:

1. all four named generation records and the structured generation trace are
   absent;
2. eight of nine proof-local operational shortcuts have fresh, bridge-free
   universal connection proofs, but the universal check for the ninth
   (`#pop`) stops at a symbolic Map-deletion equality. The rule is the ordinary
   valid Map law, and two ground fixed-semantics witnesses close, so this is an
   auditability gap rather than an unsoundness witness;
3. equivalence between the fully defined `bracketResult` recurrence and the
   natural-language/canonical bracket predicate is justified by direct
   induction plus finite differential evidence, not by a separate K theorem.

No candidate-provided compiled definition, cache, trace, prose report, or
claimed prior result was trusted.

## Audit environment and evidence convention

The mandated `using-kit` and `validating-proof` workflows were applied. The
rendered mode is `SUPPLIED_SEMANTICS`, so `writing-semantics` was correctly not
used. Tool versions were K v7.1.337 and Python 3.10.12
([`00-tool-versions.log`](/audit-output/evidence/00-tool-versions.log)).

All executable source was copied into `/tmp/audit-work`; concrete and proof
definitions there were rebuilt from source. Reviewer scripts, mutations,
inventories, inputs, and bounded logs are under
[`/audit-output/evidence`](/audit-output/evidence). The common logging wrapper
records working directory, shell-escaped command, output, and exit status
([`run_logged.sh`](/audit-output/evidence/run_logged.sh)).

## Stage 1 — Input and provenance integrity

### Mode and trusted-mount consistency

The trusted mount agrees with the rendered mode:

- `/reference/reference-semantics` exists as a real directory.
- `/reference/canonical.py`, `/reference/prompt.py`, and
  `/reference/py2mpy.py` exist as ordinary files.
- This is therefore not an infrastructure breach, and candidate verdict
  markers are appropriate.

### Candidate artifacts

The required executable proof sources `solution.py`, `solution.mpy`, `spec.k`,
`verification.k`, and `reference-semantics/` are ordinary files/directories;
none is symlinked. Candidate `prompt.py` and `py2mpy.py` are byte-identical to
their trusted versions:

| Artifact | SHA-256 | Result |
|---|---|---|
| `prompt.py` | `4d14ffd571dae1770eb5e26636b128c8520cee2173f2f4a592277c6cd094e644` | exact |
| `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | exact |

The candidate `reference-semantics/` tree recursively has exactly the same 24
files plus one subdirectory, with the same bytes as the trusted tree and no
missing, additional, mistyped, changed, or symlinked entry. This verifies integrity only; it does
not bless `verification.k`.

The complete type/byte/tree check and hashes are in
[`integrity_check.py`](/audit-output/evidence/integrity_check.py) and
[`01-integrity.log`](/audit-output/evidence/01-integrity.log), exit 0.

### Missing and extra evidence

The following named generation records are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured trace filename is present. They could not be read and provide no
provenance support. This is a documented evidence concern, not a substitute
for or contradiction of the reconstructed proof.

The candidate additionally contains `prove.sh`, `concrete_tests.py`,
`concrete_tests.mpy`, and a Python `__pycache__` entry. They are outside the
supplied-semantics integrity tree and were treated only as untrusted support
artifacts. No candidate K compiled definition was copied or reused. The
scratch-copy manifest and exact copy command are in
[`02-prepare-scratch.log`](/audit-output/evidence/02-prepare-scratch.log).

## Stage 2 — Program fidelity and candidate-versus-canonical checks

### Natural-language and canonical contract

On the documented domain, `brackets` is a finite string containing only `<`
and `>`. The required result is true exactly when:

1. scanning left to right, the number of closes never exceeds the number of
   opens in any prefix; and
2. the final numbers of opens and closes are equal.

This restatement follows `/reference/prompt.py` and the actual trusted
canonical implementation. The canonical code increments for `<`, decrements
for every other character, rejects immediately when depth becomes negative,
and accepts exactly at final depth zero. The intended domain restriction makes
“every other character” precisely `>`.

The submitted `solution.py` uses the same algorithm. Its differences are a
renamed loop variable, a harmless initialization `bracket = ""`, and a
different docstring. All branches and return behavior otherwise match the
canonical code.

### Trusted translation

Running the copied trusted translator on the scratch copy of `solution.py`
produced a file byte-identical to submitted `solution.mpy`; both SHA-256 values
are:

```text
a4f95cf18ab5c87487831f7940e0e2ba6ba4e0368af55487e4c57abcebf74132
```

The exact command, `cmp`, hashes, and exit 0 are in
[`03-regenerate-solution.log`](/audit-output/evidence/03-regenerate-solution.log).
Thus the K entry claim is checked against the trusted translation of the real
submitted Python, not against a candidate-selected transliteration.

### Independent differential testing

[`differential_test.py`](/audit-output/evidence/differential_test.py) imports
the trusted and submitted entry points under distinct module names. It tested:

- all four documented examples;
- 12 explicit empty/one-character/branch-boundary cases;
- every `<`/`>` string of lengths 0 through 12 (8,191 cases);
- 500 seeded cases at lengths 13, 14, 15, 16, 31, 32, 63, 64, 127, and 128;
- 10 long balanced or immediate-negative cases, reaching length 512.

There were 8,717 comparisons and zero mismatches. The command and summary are
in [`04-differential.log`](/audit-output/evidence/04-differential.log), exit 0.
Every exact input is preserved in
[`differential-inputs.txt`](/audit-output/evidence/differential-inputs.txt),
whose recorded SHA-256 is
`bc6e2dbd5622f089f9f2bfe234fd03f843a207294c0b1916b8f76fe51e887563`.
This is finite intent-bridge evidence, not the K proof.

## Stage 3 — Clean proof reconstruction

### Fresh definitions

The concrete definition was built from the copied trusted supplied semantics:

```text
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled
```

It exited 0
([`05-build-concrete.log`](/audit-output/evidence/05-build-concrete.log)).
The compiler warned about non-exhaustive total functions in `builtins.k`,
`float.k`, `methods.k`, and `subscript.k`. None of those functions is reachable
from this program; they are accounted for in Stages 5 and 7.

As supplementary concrete evidence, the candidate assertion harness was first
regenerated with the trusted translator and required to be byte-identical
([`06-regenerate-concrete-harness.log`](/audit-output/evidence/06-regenerate-concrete-harness.log),
exit 0). Fresh `krun` execution terminated with `.K`, `NoExc`, and exit code 0
([`07-run-concrete-harness.log`](/audit-output/evidence/07-run-concrete-harness.log),
exit 0). This untrusted candidate test harness is not used as proof evidence.

The proof definition was independently built by:

```text
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled
```

It exited 0
([`08-build-proof.log`](/audit-output/evidence/08-build-proof.log)). It imports
`MPY`, not the concrete-only `MPY-CONCRETE` module.

### Positive targets

The target consists of the mutually recursive pair of loop circularities and
the entry claim. A fresh run explicitly selecting all three was:

```text
timeout --signal=INT --kill-after=30s 1800 kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.loop-zero,SPEC.loop-positive,SPEC.correct-bracketing --output pretty
```

It exited 0 and printed `#Top`
([`10-prove-all-positive.log`](/audit-output/evidence/10-prove-all-positive.log)).
The mutually recursive loop pair also independently exited 0 with `#Top`
([`22-prove-loop-claim-pair.log`](/audit-output/evidence/22-prove-loop-claim-pair.log)).

A diagnostic run selecting `loop-zero` alone was auditor-interrupted after
approximately 11 minutes (status 130), because that selection excludes the
`loop-positive` companion circularity needed after an open bracket
([`09-prove-loop-zero.log`](/audit-output/evidence/09-prove-loop-zero.log)).
It emitted neither a residual nor a candidate failure. The declared positive
target is the three-claim mutually recursive set, and that complete set closes
cleanly.

No prior `#Top`, compiled directory, log, or candidate final report contributed
to these results.

## Stage 4 — Adequacy and real-program pinning

### Plain-language claim meanings

| Claim | Precondition | Postcondition | Satisfiable witness |
|---|---|---|---|
| `loop-zero` | Execution is at the real `#loop` over suffix `S`; current local `depth` is 0; the current function frame, caller continuation, stack, and fresh frame location have the shown forms. | The rest of the real loop and final return pop the frame and deliver `bracketResult(S,0)` to the saved continuation. | `L=1`, caller 0, saved location 1, empty continuation, `S=""`, exact local map, and an outer map without key 1. |
| `loop-positive` | Same real loop/frame state, but integer `D > 0`. | It pops and delivers `bracketResult(S,D)` to the saved continuation. | The reachable state after processing prefix `<`: `D=1`, suffix `>`, `L=1`, and the same frame cells. |
| `correct-bracketing` | Exact initial MPY configuration and any `S:IntSeq`; it loads the submitted module and calls `correct_bracketing(str(S))`. | Exact final module state with returned Boolean `bracketResult(S,0)` and unchanged empty heap, empty stack, no return/exception, and exit code 0. | `S=.IntSeq`, or any listed concrete code sequence. |

The unused `INPUT`, `OLD`, and parent variables in loop claims are a deliberate
generalization, not vacuity: the active suffix and current depth determine the
remaining computation. The freshness guard makes frame deletion well-defined.

### Actual program and constrained result

The entry claim's `Module(FuncDef(...))` body is syntactically identical to the
regenerated submitted `solution.mpy`, including docstring expression,
initializations, both loop conditionals, both augmented assignments, the early
false return, and the final equality return. It performs normal module loading,
name lookup, call dispatch, frame creation, parameter binding, and body
execution. No rule replaces the whole call or function body with
`bracketResult`.

The right-hand `<k>` result is the Boolean term `bracketResult(S,0)`, not a free
variable, unconstrained oracle, implication, or tautology. The eight equations
in `verification.k` fully determine it for every `IntSeq` and integer depth.

[`claim_witnesses.py`](/audit-output/evidence/claim_witnesses.py) substitutes
empty, balanced, leading-close, and positive-depth reachable states into all
three claims. Every formal result agrees with both Python implementations;
[`17-claim-witnesses.log`](/audit-output/evidence/17-claim-witnesses.log)
records zero mismatches and the complete satisfying state schemas.

## Stage 5 — Rule-by-rule static soundness review

### Exhaustive inventory

[`rule-inventory.tsv`](/audit-output/evidence/rule-inventory.tsv) is the
source-located exhaustive inventory produced by
[`rule_inventory.py`](/audit-output/evidence/rule_inventory.py). It covers all
24 supplied K files plus `verification.k` and `spec.k`:

| Kind | Count |
|---|---:|
| Configuration | 1 |
| Syntax declarations | 228 |
| Contexts | 5 |
| Rules | 712 |
| Claims | 3 |
| Total | 949 |

Attributes inventoried include 147 `function`, 108 `total`, 25 `symbol`, 22
`no-evaluators`, 54 `priority`, 35 `concrete`, 26 `owise`, 6
`simplification`, 5 macro forms, and strictness attributes. There are no
`functional` declarations. Each record has one of these audit dispositions:

- 104 trusted-supplied records on the submitted program path, reviewed below;
- 824 trusted-supplied records unreachable from this solution;
- 1 proof-local summary declaration and 8 summary equations;
- 9 proof-local operational bridges;
- 3 target claims reviewed in Stage 4.

The inventory command, source hashes, counts, and complete opaque-symbol list
are in [`18-rule-inventory.log`](/audit-output/evidence/18-rule-inventory.log).

The 824 unreachable records remain part of the selected, byte-identical trusted
supplied semantics, but no LHS is generated by this program's constructs.
Notably, every one of the 25 opaque/symbol declarations is in float, sort, or
MD5 functionality absent from `solution.mpy`; none can affect a branch, state,
result, or postcondition here.

### Used syntax and fixed-semantics path

| Submitted construct | Declaration and fixed behavior |
|---|---|
| `Module`, `FuncDef`, `Params`, statement lists | `syntax.k`; `core.k` loads/sequences; `functions.k` installs the exact closure. |
| `Call(Name(...), str(S))` | `core.k` local/global lookup and left-to-right argument machinery; `call.k` evaluates the callee, pushes a fresh frame, and binds the argument. |
| `Expr(Str(docstring))` | `str.k` ASCII literal conversion; `controls.k` discards the resulting expression value. |
| `Assign(Name, Int/Str)` | strict RHS evaluation in `syntax.k`; integer/string literal rules; `controls.k` updates the current scope. |
| `For(Name, Name, body)` | `controls.k` evaluates the iterable once and uses `#loop`; `str.k`'s iterator yields one-character strings left to right; target binding and `#loopLbl` resume the suffix. |
| `If(Compare(...))` | `operators.k` evaluates left then right; string equality or integer comparison computes a Boolean; `controls.k` selects exactly one branch. |
| `AugAssign` `+`/`-` | strict literal evaluation and `int.k` arithmetic update the integer local. |
| `Return(Bool(false))` and final return | `functions.k` records the value, discards the function continuation as Python return requires, pops the frame, restores the caller, and emits the value. |

The configuration cells are `k`, `env`, `scopes`, `scopeLoc`, `heap`,
`heapLoc`, `stack`, `ret`, `exc`, and `exit-code`. The entry claim pins them
all. The program allocates a scope frame but no heap object. On the intended
well-sorted string domain, there is no exceptional operation. Argument and
operand order, local binding, early-return control, saved continuation, frame
removal, and scope-location restoration all match the real flow.

The LLVM warnings concern `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`,
and `valSeqAt`; none occurs in the mapping above. The `strLt` unused-variable
warnings concern string ordering, whereas this program uses string equality.
Consequently those supplied-library limitations have no dependent proof claim.

### `bracketResult`: declaration and all eight equations

`bracketResult(IntSeq,Int)` is `[function,total]`, but not opaque. Its equations
partition the complete domain:

1. empty suffix at depth 0 gives true;
2. empty suffix at positive or negative depth gives false;
3. code 60 (`<`) at depth 0 or positive depth recurses with depth plus one;
4. any non-60 code at depth 0 gives false;
5. any non-60 code at positive depth recurses with depth minus one;
6. every nonempty suffix at negative depth gives false.

Empty/cons sequence forms, zero/positive/negative integers, and code
equal/not-equal to 60 are exhaustive and pairwise disjoint. Every recursive
case structurally shortens the suffix. The rules agree on no overlap, and the
six simplification attributes only orient truthful equations. This definition
exactly mirrors the submitted program on all `IntSeq` values; on the intended
domain the only non-60 code is 62 (`>`).

### All nine proof-local operational bridges

| Lines in `verification.k` | Effect and complete-context review | Decision |
|---|---|---|
| 41–43 | Evaluates `Return(Bool(B))`, sets `retV(B)`, and performs the same abrupt `#pop` transition as fixed `Return`. The wildcard continuation is intentionally discarded by both rules. | Sound exact composition. |
| 45–59 | Looks up integer local `depth`, evaluates `== 0`, records that Boolean, and returns. The active environment and exact plain local frame pin the binding. | Sound exact composition. |
| 61–93 | Two guarded rules evaluate one-character local `bracket == "<"` for code 60 versus non-60 and preserve the arbitrary continuation. Guards are disjoint and exhaustive. | Sound exact composition. |
| 95–119 | Two rules evaluate literal 1 and perform the fixed integer `depth` update for `+` or `-`. Only the current plain local frame changes. | Sound exact composition. |
| 121–153 | Two rules evaluate integer `depth < 0` and preserve the arbitrary continuation. Guards `< 0` and `>= 0` are disjoint and exhaustive. | Sound exact composition. |
| 159–168 | Normalizes fixed `#pop`: consumes `retV`, removes the head frame, restores environment/location, and deletes fresh key `L` from the scope map. | Mathematically sound Map normalization; universal mechanized connection gap documented below. |

All have priority 40, so priority was checked as preemption rather than treated
as justification. Their guards and exact local-frame patterns narrow them to
states where the fixed steps have the displayed outcomes. They do not touch
heap, heap location, exception, or exit cells. The return bridges have the
same abrupt-control domain as fixed return; the branch/update bridges preserve
the arbitrary continuation admitted by their ellipses. No fresh or opaque
result is introduced.

A fresh definition importing only fixed `MPY`, with no candidate proof rules,
was built successfully
([`12-build-fixed-proof.log`](/audit-output/evidence/12-build-fixed-proof.log)).
The bridge-free universal claims in
[`bridge-check.k`](/audit-output/evidence/bridge-check.k) quantify over the same
continuations, bindings, values, and framed cells as the candidate rules.
All eight expression/control bridges prove with exit 0 and `#Top`
([`14-prove-fixed-expression-bridges.log`](/audit-output/evidence/14-prove-fixed-expression-bridges.log)).

Including `#pop` in that fixed-only check exits 1 because the backend leaves:

```text
(L |-> FRAME SC)[L <- undef] == SC
```

under `notBool L in_keys(SC)` rather than normalizing it
([`13-prove-fixed-bridges.log`](/audit-output/evidence/13-prove-fixed-bridges.log)).
That residual is the exact valid finite-Map deletion law used by the candidate,
not a differing control/result/state witness. Two concrete fixed-semantics
claims—one with no remainder and one preserving two other frames—both exit 0
with `#Top`
([`pop-ground.k`](/audit-output/evidence/pop-ground.k),
[`16-prove-fixed-pop-ground.log`](/audit-output/evidence/16-prove-fixed-pop-ground.log)).
The LHS map decomposition and freshness guard exclude a duplicate `L`, so
deleting `L` necessarily leaves `SC`. I found no false conclusion witness and
therefore do not label this rule unsound; the absence of a backend-closed
universal connection theorem is retained as a concern.

### Static soundness conclusion

No local rule encodes the final answer while bypassing the program, replaces a
program-derived computation with an unconstrained oracle, fabricates semantics
for an unmodeled used construct, or permits a false result on the intended
domain. No unsoundness is claimed, so there is no missing false-conclusion
witness.

## Stage 6 — Fresh non-vacuity test

The candidate supplies no `spec-vacuity.k`; no candidate mutation evidence was
trusted. The fresh
[`spec-vacuity.k`](/audit-output/evidence/spec-vacuity.k) retains both genuine
loop claims and changes only the entry result to:

```text
notBool bracketResult(S, 0)
```

This is demonstrably false at the satisfying input `S=.IntSeq`: the original
summary is true and the mutation requires false. The mutation parsed and
reached the prover, then exited 1 with `WarnStuckClaimState`. The residual is
the expected unmet result obligation:

```text
bracketResult(S, 0) == notBool bracketResult(S, 0)
```

The exact command, status, and bounded residual are in
[`21-false-postcondition.log`](/audit-output/evidence/21-false-postcondition.log).
This is a meaningful proof rejection, not a parser error, missing import,
timeout, unrelated crash, or unreachable mutation.

As a separate operational-sensitivity test,
[`body-mutation.k`](/audit-output/evidence/body-mutation.k) changes the real
open-bracket update from increment to decrement while retaining expected result
true on input `"<>"`. Ground execution reaches `false`, cannot unify with
`true`, and exits 1 with `WarnStuckClaimState`
([`20-body-mutation.log`](/audit-output/evidence/20-body-mutation.log)). Thus
the proof is sensitive to the submitted function body; the local bridges do
not bypass it.

## Stage 7 — Proven versus assumed accounting

### Precisely what is proved

Conditional on the K toolchain and selected supplied semantics, for every
finite `S:IntSeq`, the exact translated submitted module, started in the exact
initial configuration and called as `correct_bracketing(str(S))`, reaches a
final configuration whose returned `<k>` value is
`bracketResult(S,0)`. The module closure is the exact submitted body; the
environment, scopes, location counters, empty heap, empty stack, return state,
exception state, and exit code satisfy the entry postcondition.

The two loop claims additionally establish, for every satisfiable generalized
loop state at depth 0 or positive depth, that execution of the real remaining
loop and final return yields `bracketResult` of the remaining suffix and
current depth while correctly popping the frame.

This is a partial-correctness reachability result. It is not a proof about
arbitrary Python features, arbitrary argument types, concurrency, I/O, or
strings outside the formal `str(IntSeq)` model.

### Trust and assumption ledger

| Boundary | Influence and dependents | Assessment/evidence |
|---|---|---|
| Trusted supplied semantics | Defines all execution, state, calls, arithmetic, strings, loops, and returns used by every claim. | Required trust boundary for this mode; candidate tree is recursively exact. The used path was statically reviewed and freshly executed/compiled. |
| K v7.1.337 compiler, Haskell/LLVM backends, solver, and builtin Int/Bool/String/Map/List theories | Establish parsing, rewriting, reachability closure, and builtin algebra. | Ordinary machine-checking trust boundary. Exact versions and commands are preserved. |
| Trusted `py2mpy.py` | Bridges submitted Python AST syntax to the `.mpy` term embedded by the claim. | Candidate translator is exact; trusted regeneration is byte-identical. The translator is syntactic, not a correctness oracle. |
| Proof-local `bracketResult` | Determines every final Boolean and loop summary. | Not opaque: complete, disjoint, descending equations were reviewed. It depends on ordinary integer/sequence mathematics. |
| Eight expression/control bridges | Accelerate real fixed-semantics steps and affect control/result/local state. | Fresh fixed-only universal connection claims close with `#Top`; no circular dependency on `bracketResult`. |
| `#pop` Map normalization | Affects return control, scope deallocation, stack, environment, and final result delivery. | Valid Map deletion law; fixed ground witnesses close. Universal fixed-only check stops only at symbolic Map equality, so auditability remains a concern. |
| Opaque/symbol library operations and non-exhaustive-total compiler warnings | Could affect results if called. | No dependent construct or claim in this program; excluded from the execution path. |
| Natural-language/canonical intent bridge | Interprets `bracketResult(S,0)` as correct balancing for `<`/`>` strings. | Direct structural induction is straightforward but not separately machine-checked. The trusted canonical differential has zero mismatches on 8,717 comparisons; finite evidence is not a universal theorem. |
| Termination | Partial correctness does not assume or establish general Python termination. | Here each recursive summary and concrete string loop consumes one constructor, but the reported status remains partial correctness. |

### Final gate assessment

- Fresh verification: pass—clean build, exit 0, and `#Top` for the complete
  positive target.
- Real-program soundness: pass with the documented universal Map-connection
  evidence gap; no false-conclusion witness exists, eight other bridges are
  universally connected, body sensitivity succeeds, and non-vacuity succeeds.
- Intent adequacy: pass on the documented `<`/`>` string domain; the exact
  implementation matches the trusted canonical in independent testing.
- Evidence auditability: concern because generation records are absent, the
  `#pop` connection is not universally backend-closed, and the final
  summary-to-English bridge is informal plus finite testing.

These limitations do not permit a false result, substitute a different
program, weaken the result to a free variable, or make the proof vacuous. They
therefore warrant `CONCERNS / LEGIT`, not `FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
