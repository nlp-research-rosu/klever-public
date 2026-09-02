# Independent adversarial audit: 56-correct-bracketing

## Finding

The candidate contains a legitimate partial-correctness proof of the submitted
program on the full source-contract domain. I reconstructed the LLVM and
Haskell definitions from source, independently reran both positive proof
targets, mechanically compared the translated function body with the closure
executed by the entry claim, inventoried the supplied and proof-local K rules,
and ran fresh result and body mutations. Both positive targets closed with
`#Top` and exit 0. The fresh false-result claim compiled but was rejected with
the concrete contrary result required for a meaningful non-vacuity test.

The candidate's `PROOF.md`, compiled directories, tests, logs, and generation
trace were treated only as untrusted claims. No candidate-produced compiled
definition or cache was used.

## 1. Input and provenance integrity

### Launcher record and semantics-mode gate

`/audit-input.json` declares:

- `record_layout`: `pipeline-v3`
- `problem_id`: `56-correct-bracketing`
- `condition`: `kit-semantics`
- `semantics_mode`: `SUPPLIED_SEMANTICS`
- `mount_reference_semantics`: `true`

The mode and trusted mounts are consistent:
`/reference/reference-semantics` is present. Therefore this is not an
infrastructure-error case.

All pipeline-v3 records required by the prompt are present, readable regular
files rather than symlinks:

- `/run.json`, `/task.json`, and `/generation-result.json`
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
  and `prompt.txt`
- the structured trace at
  `/generation-evidence/codex-trace/2026/07/25/rollout-2026-07-25T00-33-15-019f97c3-7059-7723-a2dd-413798611f73.jsonl`

The required candidate deliverables (`solution.py`, `solution.mpy`,
`verification.k`, `spec.k`, `prove.sh`, and `PROOF.md`) are also present as
regular files. See [integrity.log](evidence/integrity.log), which records file
type/readability checks, exact expected and actual SHA-256 values, recursive
comparisons, and exit statuses.

### Independent hashes and comparisons

Every launcher-recorded direct hash checked by the reviewer matched, including
the campaign lock, canonical program, trusted prompt, trusted translator,
pipeline manifests, all generation records, and the trace file. In particular:

- campaign lock:
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`
- canonical:
  `29ddcf16e9e8bd48ad7a6129ecd5fc1abbc3770d4ab87d0ab4a638e16a6e317a`
- prompt:
  `4d14ffd571dae1770eb5e26636b128c8520cee2173f2f4a592277c6cd094e644`
- translator:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`
- structured trace:
  `ed8a9e0ad00a6879aa99b9a0ef771ab4616220ecf71edc443958be9cac4169f9`

The parsed `/audit-campaign-lock.json` object equals the
`audit_campaign` block in `/audit-input.json`, and its bytes have the recorded
hash.

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounted versions. A recursive `diff -qr --no-dereference` of the candidate's
`reference-semantics/` and `/reference/reference-semantics/` returned 0.
Neither tree contains symlinks, special entries, missing entries, extra
entries, or type changes. Thus the supplied-semantics integrity condition
passes. This comparison does not bless the candidate's `verification.k`, which
is audited separately below.

### Generation records inspected as untrusted history

The trace has 307 JSON lines and parses completely. It records 18 shell command
calls, 11 patch calls, five textual `#Top` lines in the aggregate CLI log, and
the generator's final `KPROVE_PASSED`/`VALIDATED` claims. The exact event
inventory and shell commands are in
[generation-trace-summary.log](evidence/generation-trace-summary.log). Those
claims were not used as proof evidence.

`usage.json` contains a `source_trace_sha256` value that is not the byte hash of
the mounted trace, whereas `generation-result.json`, `invocation.json`, and the
launcher's audit manifest all agree with the independently measured trace hash.
This is an internal inconsistency in an untrusted usage-metrics field, not a
missing or malformed launcher-declared mount and not evidence about proof
legitimacy. The mounted required records themselves pass the launcher integrity
checks.

Stage 1 result: **PASS**. There is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and trusted implementation

The trusted prompt says that `correct_bracketing(brackets: str)` receives a
string consisting of `<` and `>` and returns true exactly for correct
bracketing. The examples require:

- `<` → false
- `<>` → true
- `<<><>>` → true
- `><<>` → false

The trusted canonical program maintains an integer depth, incrementing for `<`
and decrementing for `>`. It immediately returns false when a prefix has
negative depth and otherwise returns whether the final depth is zero. Thus the
contract domain is every finite Python string over `{<, >}`, including the
empty string; there is no stated size bound.

The candidate implements the same characterization with `balance` and a
persistent Boolean `valid`. Instead of returning at the first negative prefix,
it sets `valid = False` and continues. Since `valid` is never reset, its final
result

```text
valid and balance == 0
```

equals the canonical result on the entire intended domain.

### Trusted regeneration

The reviewer ran the trusted mounted translator over the scratch copy of
`solution.py`. The regenerated file and submitted `solution.mpy` compare
byte-for-byte and both have SHA-256:

```text
bf1cca1c9f6ca6e8178453bc46114854d97627930072093c07e01618cf9cb1b0
```

Command and status: [translation-identity.log](evidence/translation-identity.log).

### Independent differential test

[differential_test.py](evidence/differential_test.py) independently imports the
trusted canonical and candidate entry points. It tests:

- all four documented examples;
- empty and explicit branch/boundary cases;
- every string over `{<, >}` of lengths 0 through 12 (8,191 strings);
- 500 deterministic generated strings up to length 256;
- long nested, sequential, and prefix-invalid strings up to 1,024 characters.

After duplicate elimination, 8,674 unique inputs were checked. The run reported
zero mismatches and exited 0. Exact scope and output:
[differential.log](evidence/differential.log).

Stage 2 result: **PASS**. The generated implementation is faithful, and its MPY
translation is the submitted translation.

## 3. Clean proof reconstruction

### Isolation and toolchain

Only source artifacts were copied into `/tmp/audit-work/proof`. The supplied
semantics came from the trusted `/reference/reference-semantics` mount, not
from a candidate compiled directory. Candidate `runtime-kompiled/`,
`verification-kompiled/`, caches, and binaries were not copied or consulted.

The independently observed tools were K `v7.1.293` and Python `3.10.12`.

### Fresh concrete definition and execution

The reviewer compiled:

```text
kompile /tmp/audit-work/proof/reference-semantics/semantics.k
  --backend llvm
  --main-module MPY-KRUN
  --syntax-module MPY-SYNTAX
  --output-definition /tmp/audit-work/proof/runtime-kompiled
```

It exited 0. The log records supplied-semantics warnings about several
non-exhaustive total functions; none is reachable in this program. See
[kompile-llvm.log](evidence/kompile-llvm.log).

The reviewer-authored [concrete_probe.py](evidence/concrete_probe.py) contains
the exact submitted function body and 12 assertions covering the prompt
examples, empty input, both update branches, prefix failure, nesting, and
concatenation. Before translation, its function body was mechanically diffed
against the submitted source body. It was then translated with the trusted
translator. See
[concrete-probe-translation.log](evidence/concrete-probe-translation.log).

Running that MPY program against the fresh LLVM definition exited 0 with
`<k> .K </k>`, exit code 0, empty heap and stack, and the expected exact closure
body in module scope. See
[krun-concrete-probe.log](evidence/krun-concrete-probe.log).

### Fresh proof definition

The reviewer compiled:

```text
kompile /tmp/audit-work/proof/verification.k
  --backend haskell
  --main-module VERIFICATION
  --syntax-module MPY-SYNTAX
  --output-definition /tmp/audit-work/proof/verification-kompiled
```

It exited 0. Only unused-variable warnings in the supplied `str.k` appeared.
See [kompile-haskell.log](evidence/kompile-haskell.log).

### Positive target claims

The candidate designates two positive proof commands. Both were rerun against
the fresh definition:

1. `SPEC.loop-inv` alone printed `#Top` and exited 0:
   [kprove-loop.log](evidence/kprove-loop.log).
2. The complete `SPEC` module, which proves the loop claim and the
   `correct-bracketing` entry claim together, printed `#Top` and exited 0:
   [kprove-full-spec.log](evidence/kprove-full-spec.log).

The entry claim relies on the loop circularity, so filtering the spec to only
the entry label would remove a lemma it needs. The complete-spec command is
the candidate's positive entry-proof target and closes every claim in `SPEC`.

Stage 3 result: **PASS**. The proof reconstructs cleanly from source.

## 4. Adequacy and real-program pinning

### `SPEC.loop-inv` in plain language

Precondition:

- `CODES` is an `IntSeq` all of whose codes are 60 (`<`) or 62 (`>`);
- execution is at the exact `#loop` term used for string iteration and the
  submitted two-`If` loop body;
- the current scope has exactly the four local bindings `balance`, `bracket`,
  `brackets`, and `valid`;
- `balance` is any integer `BAL`, `valid` is any Boolean `VALID`, and all
  framed configuration and continuation state is arbitrary but preserved.

Postcondition:

- the loop computation is consumed;
- `balance` becomes `BAL + bracketDelta(CODES)`;
- `valid` becomes
  `VALID and bracketPrefixOK(CODES, BAL)`;
- `bracket` may have its actual final value, represented existentially;
- the original argument, parent, continuation, and other cells are preserved.

This is a weaker summary only for the irrelevant final loop-variable value; it
fully constrains both values that can affect the returned result.

A concrete satisfying loop state exists, for example local location 1 with
`CODES = iCons(60, iCons(62, .IntSeq))`, `BAL = 0`, `VALID = true`,
`bracket = str(.IntSeq)`, `brackets = str(CODES)`, and parent 0 in an otherwise
clean default configuration.

### `SPEC.correct-bracketing` in plain language

Precondition:

- `CODES` contains only 60 and 62;
- module location 0 contains exactly a binding from `"correct_bracketing"` to a
  closure with the submitted parameter, body, and defining environment;
- the builtins scope is at -1;
- environment, scope allocator, heap, heap allocator, call stack, return state,
  exception state, and exit code are the clean exact values in the claim.

Postcondition:

- the exact call terminates at a Boolean `?RESULT`;
- all explicitly pinned operational cells are restored;
- `?RESULT == bracketCorrect(CODES)`.

The result is not a free oracle. `bracketCorrect` is transparent and reduces to
prefix nonnegativity from balance zero conjoined with final net balance zero.
The `ensures` is equality, not a one-way implication.

The empty sequence is a concrete satisfying entry witness:
`bracketChars(.IntSeq) = true`,
`bracketCorrect(.IntSeq) = true`, and both trusted Python implementations
return true.

### Mechanical program-term pinning

The entry claim need not execute the outer `Module` loader because it begins in
the exact post-load module binding. That normalization is justified
mechanically:

1. trusted regeneration proves the submitted MPY term came from
   `solution.py`;
2. [pinning_check.py](evidence/pinning_check.py) extracts the unique translated
   `FuncDef` body and the unique entry-claim `closureVal` body with
   balanced-constructor parsing;
3. after only whitespace removal, the `.Stmts` list identity, and the
   `Params("brackets")` to `("brackets", .ParamNames)` expansion performed by
   the supplied `FuncDef` rule, the parameter list, defining environment, and
   body are identical;
4. both normalized bodies have SHA-256
   `f1c63bb93784ca5ba22d099cf7131f771e97f50f7ee8afdb34e4c58cab5dc841`.

The check exited 0; see [pinning-check.log](evidence/pinning-check.log).

### Concrete substitutions

[claim_witnesses.py](evidence/claim_witnesses.py) substitutes eight satisfying
inputs—including empty, each one-character branch, balanced, nested,
prefix-invalid, sequential, and final-positive cases—into the transparent K
summary. For every witness, `bracketChars` is true and `bracketCorrect` equals
both Python implementations. See
[claim-witnesses.log](evidence/claim-witnesses.log).

Stage 4 result: **PASS**. Both claims are satisfiable, result-constraining, and
mechanically pinned to the actual submitted program.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[rule_inventory.sh](evidence/rule_inventory.sh) and
[rule-inventory.log](evidence/rule-inventory.log) enumerate every K source
file, module/import, declaration start, configuration, context, syntax
declaration, ordinary rule, claim, and special attribute in the supplied
semantics and candidate proof. The supplied tree contains:

| Source module | Syntax declarations | Rules | Relevance to target proof |
|---|---:|---:|---|
| `semantics.k` | 0 | 0 | assembly/import boundary |
| `syntax.k` | 16 | 0 | submitted AST constructors |
| `core.k` | 37 | 46 | configuration, sequencing, lookup, literals, arguments |
| `iter.k` | 1 | 0 | iterator protocol declaration |
| `range.k` | 2 | 6 | unreachable |
| `operators.k` | 0 | 10 | comparison dispatch and evaluation order |
| `int.k` | 1 | 16 | `+`, `-`, `<`, and `==` |
| `bool.k` | 0 | 13 | Boolean equality/truth and short-circuit `and` |
| `float.k` | 34 | 121 | unreachable |
| `str.k` | 5 | 28 | ASCII literals, string equality, string iteration |
| `set.k` | 6 | 12 | unreachable |
| `list.k` | 5 | 27 | unreachable in the target |
| `tuple.k` | 4 | 21 | only `#bindTgt(Name, Val)` is active |
| `subscript.k` | 15 | 40 | unreachable |
| `comprehension.k` | 3 | 7 | unreachable |
| `methods.k` | 27 | 75 | unreachable |
| `controls.k` | 3 | 34 | assignment, augmented assignment, `If`, and `For` |
| `functions.k` | 4 | 15 | closure binding, parameters, return, frame pop |
| `builtins.k` | 38 | 137 | builtin operation rules unreachable |
| `call.k` | 3 | 21 | callee/argument order and exact closure call |
| `sort.k` | 6 | 19 | unreachable |
| `assert.k` | 0 | 3 | used only by finite LLVM evidence, not target proof |
| `dict.k` | 12 | 28 | unreachable |
| `concrete.k` | 5 | 16 | LLVM-only evidence; absent from Haskell proof module |
| **Supplied total** | **227** | **695** | |

There is one configuration and five contexts. The inventory also records 45
priority sites, 29 `owise` sites, 110 declaration lines containing
`[function, total]`, and 25 opaque `symbol(...)` sites. There are no
`[simplification]` or `[functional]` declarations in the audited source.

The 25 supplied opaque symbols are confined to floating-point operations,
sorting/key sorting, and MD5. No target syntax or reachable target rule
mentions them. They therefore cannot influence control, state, the summaries,
or the postcondition.

### Proof-local rules: individual decisions

The candidate adds four syntax declarations and these seven equations:

| Rule | Decision and justification |
|---|---|
| `bracketDelta(.IntSeq) => 0` | True base case: an empty suffix changes balance by zero. |
| `bracketDelta(iCons(C, REST)) => (if C == 60 then 1 else -1) + bracketDelta(REST)` | True for every integer code and matches the program's exact `if/else`; structural recursion descends to `REST`. |
| `bracketPrefixOK(.IntSeq, BAL) => true` | True base case: an empty suffix introduces no new observed balance. |
| `bracketPrefixOK(iCons(C, REST), BAL) => ...` | True for both branches: it checks the post-character balance and recursively checks every later prefix. The two conditional branches are exhaustive and disjoint. |
| `bracketChars(.IntSeq) => true` | Correct empty-domain case. |
| `bracketChars(iCons(C, REST)) => (C == 60 or C == 62) and bracketChars(REST)` | Exact inductive characterization of the source input alphabet. |
| `bracketCorrect(CODES) => bracketPrefixOK(CODES, 0) and bracketDelta(CODES) == 0` | Exact balance characterization of correct bracketing and the candidate return value. |

All four `[total]` declarations have complete constructor coverage. Empty and
`iCons` rules do not overlap, the recursive argument strictly decreases, and
`bracketCorrect` has an unguarded equation over its complete declared domain.
There is no false overlap or uncovered candidate-helper case.

The proof-local inventory contains no ordinary rule that matches or preempts a
program computation, no `Call`, `For`, `#loop`, `Return`, lookup, assignment, or
cell rewrite, no priority or `owise` rule, no simplification axiom, no opaque
symbol, and no fresh result-bearing value. Therefore there is no operational
bridge and no program-derived oracle requiring a separate bridge theorem.

`SPEC.loop-inv` is a reachability circularity rather than an ordinary semantic
rewrite. Its filtered proof closes independently. Each nonempty application
executes a real iterator/body step before returning to a smaller suffix; the
empty case executes the real iterator-done path. Its framed continuation is
preserved, and the entry proof uses it with the observable trailing
`Return(...) ~> #endcall` continuation.

### Used-construct mapping and operational review

| Submitted construct | Declaration and active supplied rules | Soundness assessment |
|---|---|---|
| `Module`, `FuncDef` | `syntax.k`; `core.k` 125–127; `functions.k` 14–16 | Loader sequences statements; `FuncDef` installs the exact parameter/body closure in current environment. Entry claim starts in exactly that post-load state. |
| `Call(Name(...), arg)` | `call.k` 20–21 and 69–74; `core.k` 131–154, 189–191; `functions.k` 63–66, 85–90 | Callee is looked up before the sole argument; arguments evaluate left-to-right; a fresh local frame is allocated, the parameter is bound, and pop restores caller state and continuation. Exact binding and clean allocator cells rule out alias/binding ambiguity. |
| `Int`, `Bool`, `Str`, `Name` | `core.k` 131–154 and 193–205; `str.k` 13–17 | Primitive literals and lookup have exact meanings. Used string literals are ASCII `""` and `"<"`, within the supplied string conversion domain. |
| `Assign(Name, value)` | strict RHS in `syntax.k`; `controls.k` 9–18 | RHS evaluates first and the current local scope is updated. Cell-write priority rules require a `$cells` marker absent from this plain closure frame. |
| `AugAssign(Name, +/- , Int(1))` | strict RHS in `syntax.k`; `controls.k` 20–31; `int.k` 9 and 13 | `balance` is already an integer, so the direct map-update rule computes exact mathematical addition/subtraction. The heap-ref priority route is inapplicable. |
| `Compare` | contexts and dispatch in `operators.k` 15–17; string equality in `str.k` 25; integer `<`/`==` in `int.k` 22 and 26 | Left then right evaluation is preserved; active comparisons are exact structural ASCII-string equality and mathematical integer comparisons. |
| `If` | strict condition in `syntax.k`; `controls.k` 51–54; `truthy(Bool)` in `core.k` 199–205 | The condition evaluates before exactly one branch; all target conditions reduce to Boolean, so no partial truthiness case is used. |
| `For` / `#loop` | strict iterable in `syntax.k`; `controls.k` 65 and 69–74; `str.k` 8–10; `tuple.k` 31–41 | The string is evaluated once, iteration yields one-character strings in order, target binding writes the local `bracket`, the complete body executes, and the continuation repeats on the suffix. Ref/cell priority rules are inapplicable. |
| `Return(BoolOp(...))` | `bool.k` 16–25; `functions.k` 78–90 | `and` evaluates `valid` first and short-circuits exactly as Python; both operands/results are Boolean. `Return` records the value, discards only the callee suffix, and frame pop restores the caller continuation and state. |

All target operations are deterministic on the precondition. No allocation or
heap mutation occurs except temporary scope-frame allocation; the entry claim
requires and proves restoration of environment, scopes, scope allocator,
stack, return state, heap, heap allocator, exception state, and exit code. No
target branch can raise a modeled exception.

The active priority rules either protect cell/heap-reference cases or concrete
sorting. The entry frame contains plain integer, Boolean, and string values and
no `$cells` marker or `ref`, so those higher-priority rules are provably
inapplicable. The generic `Call` and `Compare` `owise` dispatches are therefore
the correct routes and are not preempted by any candidate rule.

### Supplied warnings and unused rules

The LLVM compiler warned that `mapStrVS`, `floorFI`, `toF`, `ceilF`,
`joinCodes`, and `valSeqAt` have non-exhaustive total matches. None of these
symbols, their consumers, or the relevant value constructors occurs in the
submitted term, either claim, or a proof-local equation. The Haskell proof
build did not report these totality warnings. They are a limitation of the
broader supplied language model, not a route by which this target conclusion
can be proved. There is no concrete or symbolic false target-domain conclusion
witness enabled by them, so I do not label them unsound for this proof.

Every declaration/rule not in the active mapping belongs to a module whose
redex constructors are absent from the program and summaries, or to an
inactive guarded case in an active module. The exhaustive line inventory makes
this classification auditable rather than silently omitting those rules.

Stage 5 result: **PASS**. No materially unsound semantics or proof rule
contributes to closure, and there is no smuggled correctness conclusion.

## 6. Fresh non-vacuity test

The candidate's `spec-vacuity.k` was not used. The reviewer created the
independent [spec-audit-vacuity.k](evidence/spec-audit-vacuity.k), which calls
the exact submitted closure on `<>` but changes the result obligation from the
true `bracketCorrect` value to `false`.

The witness satisfies the entry domain:

```text
CODES = iCons(60, iCons(62, .IntSeq))
bracketChars(CODES) = true
canonical("<>") = candidate("<>") = bracketCorrect(CODES) = true
```

First, `kprove --dry-run` parsed and compiled the mutated claim and exited 0:
[vacuity-dry-run.log](evidence/vacuity-dry-run.log). Thus the negative result
is not a parser/import/build failure.

The actual mutation proof exited 1 with `WarnStuckClaimState`. Its residual has
`<k> true ~> .K </k>` while the altered postcondition requires false. This is
the expected unmet result obligation:
[kprove-fresh-vacuity.log](evidence/kprove-fresh-vacuity.log).

As an independent body-sensitivity check, the reviewer also created
[spec-audit-body-mutation.k](evidence/spec-audit-body-mutation.k). It changes
the `Return` comparison in the closure term actually executed by the claim
from `balance == 0` to `balance == 1`; it does not merely edit an external
source file. Its dry run exited 0
([body-mutation-dry-run.log](evidence/body-mutation-dry-run.log)), and its proof
exited 1 with the mutated concrete result `false` against the original
empty-input result `true`
([kprove-body-mutation.log](evidence/kprove-body-mutation.log)).

Stage 6 result: **PASS**. The proof is result-discriminating and body-sensitive.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied `MPY` semantics, for every finite code sequence `CODES`
satisfying `bracketChars(CODES)`, the exact submitted
`correct_bracketing` closure, called from the clean entry configuration in
`SPEC.correct-bracketing`, reaches a Boolean result equal to:

```text
bracketPrefixOK(CODES, 0)
and
bracketDelta(CODES) == 0
```

The loop claim establishes by real symbolic execution that `bracketDelta`
equals the loop's final balance change and `bracketPrefixOK` equals the
persistent `valid` condition. The entry claim executes real lookup, argument
evaluation, frame creation, parameter binding, all assignments, all loop
iterations, both branch points, return evaluation, and frame pop. The proof is
unbounded in string length; it is not a finite unrolling or examples-only
theorem.

For sequences over `{60, 62}`, the transparent summary is exactly the standard
bracketing criterion: no prefix has more closers than openers, and the complete
sequence has equal numbers of each. The trusted canonical program implements
the same criterion by returning at the first negative prefix and otherwise
checking final depth zero.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| Trusted supplied `MPY` semantics | Binding, evaluation order, calls, loop control, state, return, and primitive values | Required theorem base for `SUPPLIED_SEMANTICS`; candidate copy is byte-identical. Every target-active rule was inspected above. |
| K parser/compiler, Haskell backend, reachability engine, and built-in Int/Bool/Map/List/K-equality hooks | Compilation and symbolic closure of both claims | Standard machine-checking trust boundary. Positive proofs and two independently rejected mutations provide toolchain sanity evidence, not a metaproof. |
| String meta-hooks `ordChar`, `substrString`, and `lengthString` | Conversion of the ground ASCII literals `""` and `"<"` | Acceptable fixed primitive boundary; inputs to the claim are already explicit code sequences, and used literals are within the supplied ASCII guard. |
| Trusted `py2mpy.py` | Python-AST to MPY constructor bridge | Required mounted translator; candidate copy matches it, regeneration is byte-identical, and constructor-level claim pinning succeeds. |
| Elementary balance characterization of correct bracketing | Bridge from transparent `bracketCorrect` to the English contract and canonical algorithm | Ordinary mathematical argument: prefix nonnegativity excludes unmatched closers and final zero excludes unmatched openers. Supported, but not replaced, by 8,674 differential cases. |
| Trusted canonical and CPython differential execution | Finite source-level validation only | Zero mismatches on the documented/boundary/exhaustive-small/generated scope. It contributes no K rule or universal axiom. |
| LLVM backend and reviewer concrete assertions | Finite semantics execution evidence only | Twelve assertions reached clean termination. This is not used in place of the Haskell reachability proof. |
| Supplied opaque float/sort/MD5 symbols and unused broad-language rules | None on this program or postcondition | Explicitly inventoried but unreachable; no target claim depends on an interpretation of them. |

There is no proof-local trusted primitive, empirical oracle, opaque
result-bearing symbol, operational bridge, or informal assumption about the
submitted function body. Candidate prose, prior `#Top` output, generation
traces, and finite tests are not part of the proof.

### Scope and exclusions

- The formal input domain exactly matches the prompt's finite strings over
  `<` and `>` and includes empty strings. It has no size bound.
- Values that are not strings and strings containing other characters are
  outside the source contract and formal precondition.
- The theorem is partial correctness under the supplied MPY model, not a proof
  of the full CPython language, Unicode behavior beyond this ASCII alphabet,
  resource limits, or complexity.
- The exact clean entry configuration and binding are part of the theorem.
  This is appropriate for the generated standalone HumanEval function and
  does not substitute a different body.

### Gate and benchmark decision

- Real-program soundness / Gate A: **PASS**
- Intent adequacy / Gate B: **PASS**
- Trust and evidence auditability / Gate C: **PASS**

There is no material domain narrowing, result unconstrainedness, substituted
program, failed reconstruction, vacuity, or materially unsound rule. The
standard supplied-semantics/toolchain boundaries are explicit and do not
justify downgrading an otherwise fully pinned, unbounded proof.

VERDICT: PASS
LEGITIMACY: LEGIT
