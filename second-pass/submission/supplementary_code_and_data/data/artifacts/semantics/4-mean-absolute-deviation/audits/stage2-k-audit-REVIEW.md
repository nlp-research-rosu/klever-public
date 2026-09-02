# Independent adversarial audit: 4-mean-absolute-deviation

The candidate's positive claim reconstructs and prints `#Top`, its Python
implementation agrees with the canonical implementation on the tested inputs,
and the claim is both result-constraining and sensitive to a mutation of the
executed program body. It is nevertheless not a legitimate proof. The
proof-local `#loop` rule is a materially unsound operational bridge: it skips
the real `for` target binding and is broad enough for a continuation to observe
the wrong value. A reviewer-authored claim using a one-element float list and
an immediate lookup of `number` closes with `#Top` under the candidate rule,
while the same claim under fixed supplied semantics fails and shows the correct
last element in both the result and local scope. This is a concrete false
conclusion enabled by a rule on which the target proof relies.

All execution and mutation work was performed below
`/tmp/audit-work/candidate`, copied from the read-only mounts. No
candidate-provided kompiled definition or cache was used. Reviewer-authored
artifacts and bounded logs are in [`evidence/`](evidence/).

## 1. Input and provenance integrity

Status: **PASS (audit infrastructure intact).**

I read `/audit-input.json` first. It declares:

- problem `4-mean-absolute-deviation`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

The required supplied-semantics mount `/reference/reference-semantics` is
present. This agrees with the rendered semantics mode, so there is no
mode/mount infrastructure contradiction.

The independent checker
[`provenance_check.py`](evidence/provenance_check.py) and its
[`provenance.log`](evidence/provenance.log) establish:

- `/audit-campaign-lock.json` is a real regular file, hashes to
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  and its JSON object exactly equals the `audit_campaign` block in
  `/audit-input.json`.
- The required legacy-selected-stage1 records are present and regular:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured `codex-trace/`.
  `usage.json` is present and was also inspected. The missing
  `runtime-metrics.json` is not required by this historical record layout.
- The independently computed SHA-256 values of the run manifest, task
  manifest, stage-one result, generation manifest, metrics, usage, prompt,
  last message, full output log, canonical source, trusted prompt, and trusted
  translator all equal the hashes recorded in `/audit-input.json`.
- The embedded task data, run identity, and stage identity are consistent.
- The complete structured trace was parsed: one JSONL file with 142 valid JSON
  records. Its pipeline tree digest is
  `c2711d119d50dadfa0a24a8103ce7c2b20e997b31185788d5ce33e98e98c78e6`,
  equal to `usage.json`'s recorded source trace digest. The individual trace
  file hash also equals the stage-one result record.
- The complete 339,345-byte `codex-output.log` was read and hashed. Generation
  records were treated only as historical claims, not proof evidence.
- The candidate prompt and translator are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- A type-sensitive recursive inventory of the two semantics trees found the
  same 25 entries, with identical file bytes and no symlink or unsupported
  entry. The independent pipeline tree digest of both trees is
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  equal to the recorded manifest-style trusted semantics hash.
- The mounted candidate's pipeline tree digest is
  `b69113e4e0d5899f794a133bc0e96f531d9c742f13ce109b3f81fd6cb01cdd2f`,
  equal to both `invocation.json`'s retained-workspace hash and
  `generation-result.json`'s workspace hash. The launcher also records
  alternate legacy digest fields; direct recursive comparison and the
  retained-workspace pipeline digest are the independent content checks used
  here.

The required candidate proof artifacts—`solution.py`, `solution.mpy`,
`verification.k`, `spec.k`, and `prove.sh`—are present. The candidate contains
no compiled K definition. Its Python bytecode cache was ignored and not used.

## 2. Program fidelity and candidate-versus-canonical checks

Status: **PASS for implementation fidelity.**

### Contract and implementation

The trusted prompt asks
`mean_absolute_deviation(numbers: List[float]) -> float` to return the average
absolute distance of the input elements from their arithmetic mean:

```text
mean = sum(numbers) / len(numbers)
result = sum(abs(x - mean) for x in numbers) / len(numbers)
```

The trusted canonical implementation is exactly that expression. Both it and
the prompt's mathematics presuppose a non-empty list for a normal return;
Python execution raises `ZeroDivisionError` on the empty list.

The candidate computes the same mean, initializes a float accumulator to
`0.0`, adds `abs(number - mean)` left-to-right in a `for` loop, then divides by
the length. It is a different surface algorithm but the same computation.

### Trusted translation

From the scratch copy I ran:

```text
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/candidate/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
cmp /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/candidate/solution.mpy
```

Both commands exited 0. Both MPY files hash to
`4d6a2ee19f9ee22100bdaa269b668999f402dd1abd83ee486c63d616d9f7954f`.
See [`translation.log`](evidence/translation.log).

### Independent differential testing

[`differential.py`](evidence/differential.py) independently imports the trusted
canonical entry point and the scratch candidate entry point. It compares exact
float hex encodings, treats two NaN returns as matching, and compares exception
types. The 213 cases include:

- the documented `[1.0, 2.0, 3.0, 4.0]` example;
- the empty boundary;
- singleton, two-element, duplicate, signed-zero, mixed-sign, subnormal,
  very-large, rounding-sensitive, infinity, and NaN cases;
- 200 deterministic generated lists of lengths 1 through 8.

The command exited 0 with `mismatch_count: 0`. The empty case raised
`ZeroDivisionError` in both implementations; the documented case returned
exactly `1.0` in both. Full inputs and outputs are in
[`differential-results.json`](evidence/differential-results.json), with the
exact invocation and status in
[`differential-command.log`](evidence/differential-command.log). These are
finite implementation-fidelity observations, not a universal proof.

## 3. Clean proof reconstruction

Status: **the positive proof closes, but only under the candidate's extended
theory.**

I copied source artifacts into `/tmp/audit-work/candidate` and created new
output definitions with distinct audit names. No candidate cache or compiled
definition was reused.

### Fresh concrete definition

Working directory: `/tmp/audit-work/candidate`.

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

Exit 0. See [`kompile-llvm.log`](evidence/kompile-llvm.log). The compiler
reported supplied-semantics exhaustiveness warnings for several helpers; none
prevented compilation.

I then ran:

```text
krun solution.mpy --definition runtime-audit-kompiled
krun smoke.mpy --definition runtime-audit-kompiled
```

Both exited 0. Loading `solution.mpy` left the expected bound closure and clean
control cells. The smoke module's four assertions—documented input, singleton,
symmetric pair, and equal triple—completed with `NoExc` and exit code 0. See
[`krun-solution.log`](evidence/krun-solution.log) and
[`krun-smoke.log`](evidence/krun-smoke.log).

### Fresh proof definition and every positive claim

```text
kompile verification.k --backend haskell \
  --main-module MAD-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

Exit 0; see [`kompile-haskell.log`](evidence/kompile-haskell.log).

`spec.k` contains one positive target claim. I ran it independently:

```text
kprove spec.k --definition verification-audit-kompiled \
  --spec-module MAD-SPEC
```

It printed `#Top` and exited 0. See
[`kprove-positive.log`](evidence/kprove-positive.log). This is a genuine
closure result under `MAD-VERIFICATION`; it is not, by itself, validation of
the added rules.

## 4. Adequacy and real-program pinning

Status: **program-pinned and result-constraining; body sensitivity passes.**

### Plain-language meaning of the claim

The sole entry claim quantifies over `VS:ValSeq`.

Its precondition `nonEmptyFloats(VS)` means:

- the sequence is non-empty; and
- every element is a K `Float`.

Its initial configuration has the normal module environment, an empty module
scope whose parent is the supplied builtins scope, an empty heap and stack,
`noRet`, `NoExc`, and exit code 0.

Its `<k>` cell executes:

```text
#runMad(list(VS))
```

The claimed terminal `<k>` value is:

```text
divFloatIntV(
  absDeviationFold(
    VS,
    divFloatIntV(sumFloatSeq(VS), vsLen(VS)),
    0.0),
  vsLen(VS))
```

In plain language this is the left-to-right absolute-deviation accumulator,
starting at `0.0`, divided by the input length, with its mean obtained from the
left-to-right float sum divided by that length. The destination also requires
the function binding to have been installed and all control/state cells to be
clean.

### Mechanical source-to-claim identity

`#runMad` rewrites to `#loadAll(madSolution)` followed by an ordinary
`Call(Name("mean_absolute_deviation"), V)`. It therefore loads and invokes the
bound function; it does not directly return the postcondition.

[`program_pinning.py`](evidence/program_pinning.py) extracts the balanced
`Module(...)` constructor term from the `madSolution` definition, normalizes
only whitespace outside string literals, and compares it to the regenerated
submitted `solution.mpy`. Both normalized terms have length 515 and SHA-256
`76796fc3be5879a017b43904c18a0b5cd99e40f8f65256e99b56e6647f478d31`.
The comparison exited 0; see
[`program-pinning.log`](evidence/program-pinning.log).

The closure body repeated in the destination is also the same body. The
ordinary supplied rules perform module loading, name lookup through the
builtins parent, closure invocation, parameter binding, return, and frame
popping. The typing-only import is handled as an inert unsupported import by
the fixed supplied semantics.

### Satisfiable precondition and concrete substitution

`VS = [1.0, 2.0, 3.0, 4.0]` satisfies `nonEmptyFloats`. Interpreting the formal
folds with the supplied primitives yields `1.0`; the trusted canonical and
candidate Python functions both yield `1.0`. The independent calculation,
command, and exit status are in
[`ground_witness.py`](evidence/ground_witness.py) and
[`ground-witness.log`](evidence/ground-witness.log).

### Body sensitivity

I made a separate reviewer mutation to the constructor term actually loaded by
`#runMad`: `total_deviation` starts at `1.0` instead of `0.0`. The destination
pins that mutated closure body, while retaining the original result formula.
The mutated definition compiled successfully, but its proof exited 1 with
`WarnStuckClaimState`; the residual result contains
`absDeviationFold(..., 1.0)` and cannot imply the required
`absDeviationFold(..., 0.0)`.

Artifacts:

- [`verification-body-mutated.k`](evidence/verification-body-mutated.k)
- [`spec-body-mutated.k`](evidence/spec-body-mutated.k)
- [`kompile-body-mutation.log`](evidence/kompile-body-mutation.log)
- [`body-sensitivity-kprove.log`](evidence/body-sensitivity-kprove.log)

Thus the theorem is mechanically sensitive to a material change in the program
term it executes. The duplication of the AST across files remains a
maintenance risk, not an immutable-candidate pinning failure.

## 5. Rule-by-rule static soundness review

Status: **FAIL. One proof-local operational bridge is concretely unsound and
can prove a false observable result.**

### Exhaustive inventory

[`rule-inventory.txt`](evidence/rule-inventory.txt) contains every module,
import, configuration, syntax declaration, context, rule, claim, and associated
multiline block from the copied supplied semantics, `verification.k`, and
`spec.k`. It records 1,232 declaration blocks, including:

- 695 supplied-semantics rules;
- 16 proof-local rules;
- one reachability claim;
- 227 supplied syntax declaration starts and four proof-local syntax
  declaration starts.

[`declaration-counts.log`](evidence/declaration-counts.log) separately records
45 supplied priority occurrences, two proof-local priority occurrences, all
`no-evaluators` declarations, and confirms there are no simplification rules
in either fixed or proof-local source.

[`rule-review.tsv`](evidence/rule-review.tsv) gives a disposition and reason
for every one of the 712 rule/claim rows:

- 411 supplied-baseline rules in modules reachable by the target language
  path;
- 284 supplied-baseline rules in modules/constructs not reached by this
  program;
- 14 accepted proof-local definitional/orchestration rules;
- one proof-local evidence gap;
- one rejected unsound proof-local rule;
- the target claim.

The supplied rules are byte-identical to the launcher-selected trusted tree.
The fixed baseline does not justify proof-specific rules, and none of the two
candidate priority rules appears in that baseline.

### Construct-to-semantics map

| Program construct | Declaration and execution rules |
|---|---|
| `Module`, `ImportFrom`, `FuncDef`, `Params`, statements/expressions | `semantics/syntax.k` |
| module load and statement sequencing | `core.k`: `#loadAll`, statement-list rules |
| typing-only import | `controls.k`: non-math `ImportFrom` owise no-op |
| function binding, call frame, parameter, return/pop | `functions.k`, `call.k` |
| `Name` lookup and builtins binding | `core.k`: `#look`, `builtinsScope` |
| left-to-right call arguments | `core.k`: `#evalArgs`; `call.k`: call routing |
| `sum(numbers)` | fixed `call.k`/`builtins.k`/`float.k`, preempted by the candidate sum bridge |
| `len(numbers)` | `builtins.k`: `applyBuiltin("len")`, `seqLen`; `core.k`: `vsLen` |
| float literal and `/`, `+`, `-`, `abs` | `float.k`: `divFloatIntV`, `addF`, `subF`, `absF`, `intToF` |
| `For` and target binding | `controls.k`: `#loop`; `tuple.k`: `#bindTgt`; preempted by candidate loop bridge |
| `AugAssign` | `controls.k`, plus float `applyBin` rules; skipped by the candidate loop bridge and represented by its fold |

The initial binding chain fixes `sum`, `len`, and `abs` to the supplied
builtins: the function frame contains its parameters/locals, its parent module
scope contains only the submitted function binding, and the module parent is
`builtinsScope`. Evaluation order in the ordinary path is left-to-right.

The fresh compiler warned about non-exhaustive supplied total functions such as
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. Those
helpers are not reached by this program. The target's `vsLen` is structurally
total on `ValSeq`; its float operations use the explicitly opaque primitives
listed in stage 7.

### Proof-local declarations and ordinary rules

1. `madSolution [function,total]` has one nullary, exhaustive equation. Its RHS
   is the exact submitted module. Accepted as a definitional name.
2. `#runMad(Val)` expands to exact module loading and an ordinary named call.
   It preserves the active continuation and does not synthesize a result.
   Accepted as entry orchestration.
3. `allFloats` and `nonEmptyFloats` each have empty, Float-head, and owise
   non-Float-head cases. The cases are disjoint after `owise`, cover `ValSeq`,
   and recurse on a strict tail. Accepted.
4. `sumFloatSeq`, `sumFloatTail`, and `absDeviationFold` have base/Float-head
   equations and recurse on a strict tail. On every use allowed by
   `nonEmptyFloats`, they cover the input and fix an exact structural value in
   terms of supplied float primitives. They are not free oracles. Accepted as
   definitional summaries.

There are no proof-local simplification rules, lemmas, or auxiliary claims.

### Candidate sum operational bridge: evidence gap, not labeled unsound

The priority-40 sum rule rewrites:

```text
#applyK(toCall(builtinV("sum")), (list(VS), .Vals))
  => sumFloatSeq(VS)
requires nonEmptyFloats(VS)
```

It matches the selected builtin value, an exact one-argument list call, and an
arbitrary continuation while framing every other cell. Fixed semantics would
route to `#sumAcc(list(VS), 0)`, switch on the first Float to
`#sumAccF`, then use `addF` left-to-right. The candidate equations visibly
mirror that fixed fold and preserve the other cells. I found no false
conclusion witness for this rule, so I do **not** call it unsound.

However, it is an operational acceleration of program execution, and the
candidate contains no bridge-free universal connection theorem over its full
match domain. Finite differential tests are not that theorem. Under the Kit
validation contract this remains an evidence gap.

### Candidate loop operational bridge: rejected with false-conclusion witness

The second priority-40 rule matches the exact submitted loop:

```text
#loop(list(VS), Name("number"),
  AugAssign(Name("total_deviation"), "+",
    Call(Name("abs"), BinOp("-", Name("number"), Name("mean")))))
  => .K ...
```

It requires a non-empty all-Float sequence and Float-valued `mean` and
`total_deviation`. It replaces the loop by a single map update setting
`total_deviation` to `absDeviationFold`. It frames:

- the arbitrary trailing `<k>` continuation admitted by `...`;
- the environment and all other scope entries;
- the scope parent and all other scopes;
- heap, allocation counters, stack, return state, exception state, and exit
  code.

The accumulator summary is structurally faithful, but the state footprint is
not. Fixed `for` execution calls `#bindTgt(Name("number"), element)` before
each body execution. After a non-empty loop, Python and fixed semantics retain
`number` bound to the final element. The bridge never writes `number`; it
either leaves an old binding unchanged or leaves the name absent.

This difference is reachable and observable. The strongest reviewer witness
starts with a one-element Float list `F`, an old binding
`"number" |-> G`, and the immediate continuation `Name("number")`. The
candidate bridge preserves `G`, then the continuation returns `G`. Fixed
execution overwrites the binding with `F`, then returns `F`. Taking the
satisfiable ground interpretation `F = 1.0`, `G = 2.0`, the candidate rule
therefore proves the false conclusion `2.0` where real/fixed execution returns
`1.0`.

Machine evidence:

- [`loop-context-witness.k`](evidence/loop-context-witness.k) under the
  candidate definition prints `#Top` and exits 0:
  [`loop-context-with-bridge.log`](evidence/loop-context-with-bridge.log).
- [`verification-no-loop.k`](evidence/verification-no-loop.k) is the same
  proof-local theory with only this loop bridge removed.
- [`loop-context-witness-no-bridge.k`](evidence/loop-context-witness-no-bridge.k)
  under that bridge-free definition exits 1 with `WarnStuckClaimState`. Its
  residual `<k>` result is `F`, its scope has `"number" |-> F`, and the unmet
  condition is `#Not(F #Equals G)`:
  [`loop-context-without-bridge.log`](evidence/loop-context-without-bridge.log).

A second state-only witness reaches the same conclusion: with the bridge, K
proves a post-loop map without the target binding; without it, the residual
contains `"number" |-> F`. See
[`loop-unsound-witness.k`](evidence/loop-unsound-witness.k),
[`loop-unsound-with-bridge.log`](evidence/loop-unsound-with-bridge.log),
[`loop-unsound-witness-no-bridge.k`](evidence/loop-unsound-witness-no-bridge.k),
and
[`loop-unsound-without-bridge.log`](evidence/loop-unsound-without-bridge.log).

The failure is not an exception-model or value-only subtlety. It is an
ordinary reachable scope write and, because the rule admits arbitrary
continuations, can directly change a returned value. Rule priority only makes
the bad bridge preempt fixed execution; it does not justify it. There is no
bridge-free theorem proving preservation of this broader state/control
context.

The target execution reaches exactly this `#loop` term, the guards follow from
the entry precondition and prior assignments, and no auxiliary loop claim is
present. The successful target proof therefore uses this rejected shortcut.

## 6. Fresh non-vacuity test

Status: **PASS. The target claim discriminates a meaningful false result.**

The candidate supplied no `spec-vacuity.k`; no candidate mutation record was
trusted. I created
[`spec-false-result.k`](evidence/spec-false-result.k). It leaves the
precondition, executed program, destination cells, and closure body unchanged,
but replaces the actual result `R` by `subF(R, R)`.

For the satisfying input `[1.0, 2.0, 3.0, 4.0]`, the true result is `1.0`;
under the supplied concrete float primitive, the mutation denotes `0.0`.

First:

```text
kprove spec-false-result.k \
  --definition verification-audit-kompiled \
  --spec-module MAD-SPEC-FALSE-RESULT --dry-run
```

This built the spec successfully and exited 0; see
[`false-mutation-dry-run.log`](evidence/false-mutation-dry-run.log).

Then:

```text
kprove spec-false-result.k \
  --definition verification-audit-kompiled \
  --spec-module MAD-SPEC-FALSE-RESULT
```

This exited 1 with `WarnStuckClaimState`. The configuration unifies with the
destination, but the implication fails on the unmet equality
`R #Equals subF(R,R)`. This is the expected result obligation, not a parser
error, missing import, timeout, or unrelated backend failure. See
[`false-mutation-kprove.log`](evidence/false-mutation-kprove.log).

This successful non-vacuity gate does not repair the unsound theory used by the
positive proof.

## 7. Proven versus assumed accounting

Status: **the reconstructed reachability statement is precise, but its
connection to real execution is invalidated by the loop bridge.**

### What `#Top` establishes

Under the union of the supplied `MPY` semantics and every rule in
`MAD-VERIFICATION`, the successful reachability proof says:

> For every finite non-empty K `ValSeq` whose elements are K Floats, starting
> from the pinned clean configuration, `#runMad(list(VS))` can reach the exact
> structural mean-absolute-deviation fold term shown in the postcondition,
> while installing the exact submitted function binding and restoring the
> other specified cells.

The returned term is constrained, and the false-result test confirms it cannot
be replaced by an arbitrary different structural term. The constructor
comparison and body mutation confirm that the claim is about the submitted
body, not a substituted source program.

That statement is a theorem of the extended rewrite theory. It is not a sound
theorem of real program execution because the extended theory includes the
false loop transition demonstrated above.

### Trust and assumption ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K parser, kompilers, Haskell/LLVM backends, builtin integer/map/list theories | All builds, executions, and proofs | Ordinary machine-checking trust boundary; versions independently observed as K 7.1.293 |
| Byte-identical supplied MPY semantics (695 rules) | Defines Python-subset loading, binding, calls, loops, state, and values | Required fixed baseline; integrity passed. It is intentionally incomplete outside its modeled subset |
| `intToF`, `addF`, `subF`, `absF`, `divFloatIntV` | Determine every numeric component of the final postcondition | Supplied `[no-evaluators]` symbolic primitives with concrete LLVM equations/hooks. The K proof is structural/conditional on these intended float meanings; smoke and differential results provide finite evidence only |
| `sumFloatSeq`, `sumFloatTail`, `absDeviationFold` equations | Name the result-bearing structural folds | Truthful terminating equations on the claimed all-Float domain; not unconstrained oracles |
| Candidate sum priority bridge | Replaces fixed builtin-sum execution | No false witness found, but no bridge-free universal candidate connection theorem; concerning evidence gap |
| Candidate loop priority bridge | Replaces fixed target binding and every loop-body step | Illegitimate: machine-checked false-result and false-state witnesses; the target proof depends on it |
| Trusted translator plus constructor comparison | Connects `solution.py`, `solution.mpy`, and `madSolution` | Byte identity and constructor identity established mechanically |
| Canonical/candidate differential suite | Supports implementation equivalence and concrete primitive interpretation on 213 cases | Finite empirical evidence; not a universal proof or repair for an unsound rule |
| Partial-correctness/termination boundary | Claim reasons about normal reachability on finite non-empty sequences | Empty input is excluded and both Python implementations raise there. No theorem about exception behavior is supplied |

The formal domain is universal in sequence length; it is not a finite-size
unrolling. It is limited to non-empty K Float sequences. That matches the
declared `List[float]` normal-return cases, but it does not prove behavior for
empty input or Python's permissive mixed numeric inputs.

### Decision

The implementation is faithful, the submitted AST is pinned, the fresh
positive proof closes, and the result/non-vacuity checks are meaningful. Those
facts cannot make an unsound operational bridge legitimate. The bridge admits
an observable continuation and proves `G` where fixed execution returns `F`;
`F=1.0, G=2.0` is the required concrete false-conclusion witness on a
non-empty float input. The candidate therefore relies on a materially unsound
proof rule and fails the benchmark's legitimacy boundary.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
