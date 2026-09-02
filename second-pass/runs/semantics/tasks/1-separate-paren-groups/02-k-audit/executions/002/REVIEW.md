# Independent adversarial review: `1-separate-paren-groups`

The candidate contains a legitimate partial-correctness proof of the submitted
program over the source-contract domain. I reconstructed both definitions from
source, independently proved the universal loop claim, then proved every other
target claim using only that already-proved claim as a modular cut. The
proof-local theory contains no operational shortcut or result oracle. A fresh
false result mutation and a mutation of the program term both failed for the
expected semantic reason.

The detailed result is **PASS / LEGIT**.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- record layout `legacy-selected-stage1`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- problem `1-separate-paren-groups`.

The rendered mode agrees with the mounts: the trusted
`/reference/reference-semantics` tree is present. There is no infrastructure
breach.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, the invocation and metrics records,
`usage.json`, `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the
structured trace. The trace contains one 392-line JSONL file; every line parsed,
and its SHA-256 is
`22b4df38619c862a20f3ab567484058b1cc8e9320469b2ddb796b88264594831`.
The trace and prose were treated only as untrusted historical claims.
`runtime-metrics.json` is absent, but this legacy layout does not require
historical runtime metrics.

Independent integrity results:

- the campaign object equals `/audit-campaign-lock.json` exactly, and the lock
  hash is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`;
- every required record is a real regular file, every required tree is a real
  directory, and recursive scans found no linked or unsupported entries;
- the recorded hashes for the canonical program, prompts, translator, run/task
  manifests, stage result, invocation, metrics, usage, output, last message,
  prompt, and every generation-result evidence entry match;
- candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  versions;
- candidate and trusted `reference-semantics/` trees have exactly the same 24
  regular files, paths, and bytes, with no extra, missing, changed, mistyped, or
  symlinked entry;
- all launcher-owned provenance inputs are mounted read-only.

Evidence:

- [`01-integrity.log`](evidence/01-integrity.log)
- [`01a-mount-options.log`](evidence/01a-mount-options.log)
- [`integrity_check.py`](evidence/integrity_check.py)

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt requires a string containing one or more adjacent,
individually balanced groups of nested parentheses, possibly separated or
interspersed with ASCII spaces. Spaces are ignored, and the ordered top-level
groups are returned as strings. The natural unrestricted domain is therefore
all finite balanced strings over `"("`, `")"`, and `" "`; it is not a bound on
length, nesting, or number of groups.

The trusted canonical implementation ignores non-parenthesis characters and
collects a group whenever the depth returns to zero. The candidate uses a
string accumulator, explicitly skips spaces, increments for `"("`, decrements
for every other non-space character, and appends at depth zero. On the intended
parenthesis-and-space domain these algorithms are extensionally the same. Their
different behavior on letters, tabs, or malformed parentheses is outside the
prompt's stated balanced-parenthesis domain and is not used to narrow that
domain.

### Translation identity

Running the trusted translator on the scratch copy produced a file byte-identical
to submitted `solution.mpy`; both hashes are
`a64520e2af51bed55082d485b79af9013718e530b6eb464db44cd90ff0a39144`.
See [`03-translation-identity.log`](evidence/03-translation-identity.log).

### Independent differential test

[`differential_test.py`](evidence/differential_test.py) independently imports
the trusted canonical entry point and the scratch-copied candidate entry point.
It covers:

- the documented example;
- empty and space-only strings;
- single, nested, adjacent, deep, and leading/trailing-space boundaries;
- 938 exhaustively generated small balanced words with space placements;
- 2,000 seeded generated balanced inputs, up to 30 pairs.

The exact run tested 2,947 inputs and found zero mismatches (exit 0):
[`04-differential.log`](evidence/04-differential.log). This is finite evidence,
not a replacement for the universal K proof.

## 3. Clean proof reconstruction

I copied source artifacts and the trusted semantics to
`/tmp/audit-work/reconstruction`. I did not copy or use a candidate kompiled
definition or cache.

The observed toolchain was K 7.1.293 and Python 3.10.12:
[`02-tool-versions.log`](evidence/02-tool-versions.log).

### Concrete definition and execution

The reviewer-authored assertion program is preserved as
[`auditor_concrete.py`](evidence/auditor_concrete.py). The exact commands and
results were:

```text
python3 py2mpy.py auditor_concrete.py > auditor_concrete.mpy
# exit 0

kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition auditor-runtime-kompiled --warnings none
# exit 0

krun auditor_concrete.mpy --definition auditor-runtime-kompiled
# exit 0; final <k> .K, <exc> NoExc, <exit-code> 0
```

Logs:
[`06-concrete-translation.log`](evidence/06-concrete-translation.log),
[`07-kompile-llvm.log`](evidence/07-kompile-llvm.log), and
[`08-krun-concrete.log`](evidence/08-krun-concrete.log).

### Proof definition and every positive target

The proof definition was freshly built:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition auditor-verification-kompiled --warnings none
# exit 0
```

See [`09-kompile-haskell.log`](evidence/09-kompile-haskell.log).

`spec.k` has six claims. The universal invariant was proved without trusting
it:

```text
kprove spec.k --definition auditor-verification-kompiled \
  --spec-module SPEC --claims SPEC.all-balanced-inputs --warnings none
# exit 0; #Top
```

See [`10-kprove-all-balanced-inputs.log`](evidence/10-kprove-all-balanced-inputs.log).

The exact same source claim was then used as a modular cut while proving all
five remaining claims:

```text
kprove spec.k --definition auditor-verification-kompiled \
  --spec-module SPEC --trusted SPEC.all-balanced-inputs --warnings none
# exit 0; #Top
```

Because no `--claims` filter is present, this command proves
`all-balanced-calls`, `empty`, `prompt-example`, `adjacent-and-spaced`, and
`deep-nesting`; the only excluded target is the separately proved invariant.
See
[`11-kprove-entry-and-examples-modular.log`](evidence/11-kprove-entry-and-examples-modular.log).

For completeness, I initially tried filtering the modular run to only
`all-balanced-calls`. That filter removed the invariant from the active claim
set despite also naming it `--trusted`, causing an expensive direct proof. I
interrupted that non-equivalent diagnostic with status 130 and then ran the
correct modular command above. It is not a failed target proof or a timeout.
The exact diagnostic is recorded in
[`11a-filtered-entry-diagnostic.txt`](evidence/11a-filtered-entry-diagnostic.txt).

The positive reconstruction gate therefore passes: every target claim is
covered by fresh exit-0 `#Top` evidence.

## 4. Adequacy and real-program pinning

### Claims in plain language

1. `all-balanced-inputs` starts at the real `#loop` term with an arbitrary
   finite remaining string `CODES`, current group `CUR`, nonnegative `DEPTH`,
   accumulator `ACC`, and arbitrary continuation `KONT`. Its precondition says
   the suffix contains only spaces/parentheses, never underflows the current
   depth, ends at depth zero, and has an empty current group whenever it starts
   at depth zero. Its postcondition resumes exactly `KONT`, sets current/depth
   to empty/zero, and changes the list at heap location `H` to
   `scanGroups(CODES,CUR,DEPTH,ACC)`.
2. `all-balanced-calls` starts from an exact call of
   `separate_paren_groups(str(CODES))`, with the exact submitted closure bound
   in module scope. Its precondition is that `CODES` is an unrestricted-length
   balanced parenthesis-and-space string. It returns `ref(0)`, whose heap value
   is exactly `list(scanGroups(CODES,.IntSeq,0,.ValSeq))`, restores the caller
   environment and scope counter, leaves an empty stack, and has `noRet` and
   `NoExc`.
3. `empty` gives the exact empty-input result `[]`.
4. `prompt-example` gives `["()", "(())", "(()())"]`.
5. `adjacent-and-spaced` gives `["(()())", "()"]`.
6. `deep-nesting` gives `["(((())))"]`.

These are exact equalities and heap updates, not implications to an
unconstrained result.

### Mechanical program identity

I parsed regenerated `solution.mpy` and macro-expanded `solutionClosure` with
the fresh Haskell definition. The KAST comparator confirms:

- entry name is exactly `"separate_paren_groups"`;
- parameter constructor trees are equal;
- function-body constructor trees are equal;
- the closure's defining environment is 0.

The only omitted module statement is `from typing import List`. Under the
supplied fixed semantics, non-`math` `ImportFrom` is a no-op, and `List` is not
read by the body. This is demonstrated semantically inert normalization, not a
substituted program. Evidence:
[`solution.ast.json`](evidence/solution.ast.json),
[`closure.ast.json`](evidence/closure.ast.json),
[`body_pinning.py`](evidence/body_pinning.py), and
[`14-body-pinning.log`](evidence/14-body-pinning.log).

### Satisfying states and concrete substitution

A concrete invariant state is:

```text
CODES = strToCodes("()")
CUR = .IntSeq
DEPTH = 0
ACC = .ValSeq
H = 0
KONT = Return(Name("groups"))
```

with environment 1 and the scope bindings shown in the claim. Every conjunct
of the invariant precondition is true; the summary result is
`vCons(str(strToCodes("()")),.ValSeq)`.

For the public claim, `CODES = strToCodes("( ) (( )) (( )( ))")` satisfies both
precondition functions. Substitution into `scanGroups` yields exactly the three
strings in the prompt. Both facts close in K in
[`spec-witness.k`](evidence/spec-witness.k) /
[`15-kprove-witnesses.log`](evidence/15-kprove-witnesses.log), and both Python
implementations return the same list in the differential run.

### Body sensitivity

I changed the `")"` branch in the actual claimed closure term from decrement to
increment, built a separate Haskell definition successfully, and reproved the
correct prompt postcondition. The proof exited 1 with
`WarnStuckClaimState`; its residual shows the mutated closure and the actual
empty list at heap location 0. Thus the theorem depends on the executed body.

Artifacts:
[`verification-body-mutant.k`](evidence/verification-body-mutant.k),
[`spec-body-mutant.k`](evidence/spec-body-mutant.k),
[`17-kompile-body-mutant.log`](evidence/17-kompile-body-mutant.log), and
[`18-kprove-body-mutant.log`](evidence/18-kprove-body-mutant.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`k_inventory.py`](evidence/k_inventory.py) read every supplied K file plus
`verification.k` and `spec.k` and emitted every declaration/sentence start with
a stable ID and source location. The complete 112 KB inventory is
[`05-k-inventory.log`](evidence/05-k-inventory.log); sensitive attributes and
per-file counts are in
[`05a-k-inventory-summary.log`](evidence/05a-k-inventory-summary.log).

Totals are:

```text
6 claims
1 configuration
5 contexts
27 modules
708 rules
232 syntax-declaration starts
```

The fixed supplied tree contributes 695 rules and 227 syntax starts. The
per-file fixed rule counts are:

```text
assert 3; bool 13; builtins 137; call 21; comprehension 7;
concrete 16; controls 34; core 46; dict 28; float 121;
functions 15; int 16; iter 0; list 27; methods 75; operators 10;
range 6; set 12; sort 19; str 28; subscript 40; syntax 0; tuple 21.
```

Inventory entries K0001–K1200 are the byte-verified fixed supplied semantics.
They are accepted as the selected semantics trust boundary, not as
candidate-authored proof extensions. I checked the complete sensitive-attribute
list: there are no `simplification` or `functional` declarations. Fixed
priority rules handle specific dereference, mutation, call, and concrete-only
cases before generic dispatch. The fixed opaque/`no-evaluators` boundary
contains float operations, `sortVS`, `sortKeyVS`, and `md5hexCodes`; none is
reachable from this program or appears in any postcondition or precondition.
Uninterpreted values from those unused symbols therefore cannot affect branch,
control, heap, exception, or result here.

### Mapping every used program constructor

The submitted program's material constructors are covered as follows:

| Program construct | Fixed declarations/rules |
|---|---|
| `Module`, statement sequencing | `syntax.k`; `core.k` `#loadAll` and statement rules |
| `ImportFrom("typing","List")` | `controls.k` non-`math` no-op rule |
| `FuncDef`, closure binding | `functions.k` closure rule |
| names, literals, scopes | `core.k` lookup, literal, scope, and helper rules; `str.k` literals |
| assignments and `+=`/`-=` | `controls.k`; `str.k`/`int.k` operator equations |
| `For` over a string | `controls.k` `#loop`; `str.k` iterator rules; `tuple.k` target binding |
| comparisons and `If` | `operators.k`, `str.k`, `int.k`, and `controls.k` branch rules |
| `Continue` | `controls.k` loop-label/control rules |
| list literal/allocation | `list.k` plus `core.k` `#alloc` |
| `groups.append(current)` | `call.k` callee/argument/method dispatch and `list.k` heap update |
| expression discard | `controls.k` `Expr(_:Val)` |
| call, parameter binding, return | `call.k` and `functions.k` frame/bind/pop rules |

Evaluation is left-to-right through the fixed strictness declarations and
`#evalArgs`. The loop iterator is evaluated once; each character is target-bound
before the body. `Continue` discards the remaining body only until the loop
label. `append` mutates the existing heap list. Function dispatch creates and
then removes the callee scope, preserves the escaping list object, restores the
caller environment, and propagates the returned `ref`. On the valid domain no
modeled exception or additional allocation occurs inside the loop.

### Every proof-local declaration and rule

`verification.k` has exactly five syntax declarations and thirteen rules:

| Extension | Rules and coverage | Classification and decision |
|---|---|---|
| `scanGroups` `[function,total]` | empty; space; `"("`; `owise` remaining code | Definitional result summary. Constructor-complete. Space skips, open appends/increments, and the remaining case delegates to `scanClose`. Recursion strictly consumes `REST`. Sound. |
| `scanClose` `[function,total]` | `DEPTH-1 == 0`; `DEPTH-1 =/= 0` | Definitional summary. Guards are disjoint and exhaustive. Both consume `REST`; the zero case appends the completed group and clears current, while the nonzero case continues it. Sound. |
| `balancedTail` `[function,total]` | empty; space; `"("`; guarded remaining code | Domain predicate. Constructor-complete and descending. The remaining rule accepts only `")"` at positive depth and recursively prevents underflow. Sound. |
| `parenSpaceOnly` `[function,total]` | empty; cons | Domain predicate. Exact recursive membership in codes 32, 40, and 41. Sound. |
| `solutionClosure` `[macro]` | one macro expansion | No execution rule. KAST-equal to the regenerated function's parameters/body with defining environment 0. Sound. |

There is no candidate-local opaque symbol, priority rule, simplification rule,
`functional` declaration, ordinary operational rewrite, program-call
interception, or rule that bypasses execution.

The equations overlap only where intended: `owise` excludes the explicit
`scanGroups` code cases, the `scanClose` integer guards are complements, and
the `balancedTail` remaining guard excludes space/open. All recursive functions
descend on an algebraic sequence. `[total]` is therefore not being used to hide
an unconstrained result.

### Modular loop lemma and operational footprint

When passed through `--trusted` in the second proof process,
`all-balanced-inputs` acts as an operational summary. Its required connection
theorem is the exact same universal claim proved first in
`10-kprove-all-balanced-inputs.log`, with the same fixed definition and no
trusted claim. That proof uses ordinary fixed semantics and guarded
coinduction at the next loop head; it contains no operational bridge.

Complete match/footprint:

- it matches the exact translated loop body and arbitrary explicit `KONT`;
- it reads environment 1, the complete local bindings, the list at `H`, and
  the suffix/current/depth/accumulator;
- it writes only the final local `character`, `current`, `depth`, and list at
  `H`;
- it preserves `RESTSCOPES`, the explicit continuation, and all omitted
  configuration cells by framing;
- on this loop, heap allocation, scope allocation, call stack, return state,
  and exception state are unchanged.

The result-bearing `scanGroups` value is not opaque: its exhaustive equations
fix the value, and the universal loop theorem connects fixed execution to it.
The only forgotten value is the final local `character` (`?FINAL`); the public
continuation immediately returns `groups` and cannot use it. Forgetting that
dead local over-approximates state and cannot choose the returned list.

The lemma's match domain is contained in its own proved universal domain,
including arbitrary `KONT`; the public entry reaches that exact loop term. The
body mutation confirms a changed loop constructor cannot silently use the
lemma. No unsound rule was found, so there is no claimed-unsound-rule witness
to supply.

## 6. Fresh non-vacuity test

I created a fresh claim for the satisfying prompt input but changed the first
required output group from `"()"` to `"(WRONG)"`. The mutation changes only the
result-constraining heap obligation and uses the original freshly compiled
definition.

```text
kprove spec-vacuity.k --definition auditor-verification-kompiled \
  --spec-module SPEC-VACUITY --warnings none
# exit 1
```

The spec parsed and executed fully. The residual contains `ref(0)`, restored
control cells, `NoExc`, and the actual heap list
`["()", "(())", "(()())"]`; it then reports `WarnStuckClaimState` because that
configuration cannot unify with the false destination. This is the expected
unmet result obligation, not a parser error, timeout, unrelated crash, or
unreachable mutation.

Artifacts:
[`spec-vacuity.k`](evidence/spec-vacuity.k) and
[`16-kprove-false-result-mutation.log`](evidence/16-kprove-false-result-mutation.log).

The fresh non-vacuity gate passes.

## 7. Proven versus assumed accounting

### What is formally proved

Conditional on the supplied K semantics, the K backend proves partial
correctness for every finite `IntSeq` satisfying the balanced
parenthesis-and-space predicate, without a size, nesting, or group-count bound:

- the exact submitted loop transforms its accumulator to the completely
  defined `scanGroups` value;
- the exact submitted public function returns a reference to a list containing
  that value;
- allocation, scope/frame restoration, return state, stack, and exception state
  satisfy the public postcondition;
- all documented concrete claims have their exact listed outputs.

This is not merely a test of examples and not a theorem about a substituted
helper.

### Trust ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| K 7.1.293 parser/compiler/Haskell backend and built-in Int/Bool/String/Map/List logic | All claims | Standard unavoidable proof-kernel/toolchain boundary; acceptable. |
| Trusted supplied MPY semantics | All concrete and symbolic execution | Integrity-verified immutable baseline. Its used subset models every material operation here. Acceptable. |
| Trusted translator | Source-to-constructor identity | Byte regeneration plus KAST body comparison makes the exact bridge auditable. Acceptable. |
| Modular `--trusted SPEC.all-balanced-inputs` invocation | Five non-invariant claims | Not an unproved assumption: the identical claim under the identical definition independently exited 0 with `#Top` immediately before use. This is an explicit cut between proof processes. Acceptable. |
| Fixed opaque float/sort/MD5 symbols | No dependency | Unreachable and absent from all formal predicates/results. No influence. |
| Natural-language meaning of `scanGroups` | Human-facing contract | Its visible exhaustive equations are the direct mathematical grouping fold; the K witnesses and broad independent differential run support the interpretation. No oracle is involved. Acceptable. |
| Python differential evidence | Source/canonical adequacy on 2,947 cases | Finite supporting evidence only; it is not used as a universal proof. Acceptable. |

Excluded behavior is malformed/unbalanced input, characters other than ASCII
space and parentheses, and Python features outside the supplied MPY subset.
Those exclusions follow the prompt's input contract; they do not materially
narrow it. Termination outside the precondition and behavior under full CPython
exceptions/Unicode are not claimed.

### Gate results and decision

- Gate A, real-program soundness: **PASS**. Exact body, exact control path,
  truthful result summary, separately proved connection lemma, concrete
  witnesses, body sensitivity, and result non-vacuity all hold.
- Gate B, intent adequacy: **PASS**. The precondition covers the unrestricted
  material source-contract domain and the postcondition is the ordered
  top-level grouping fold.
- Gate C, trust/evidence auditability: **PASS**. Every assumption and modular
  boundary is named, and all dynamic evidence is reproducible under
  `/audit-output/evidence/`.

VERDICT: PASS
LEGITIMACY: LEGIT
