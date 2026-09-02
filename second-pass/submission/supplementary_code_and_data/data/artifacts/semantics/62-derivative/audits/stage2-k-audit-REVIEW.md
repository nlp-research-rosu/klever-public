# Independent adversarial review: 62-derivative

The candidate's positive `kprove` runs reconstruct successfully, the theorem is
result-constraining, and its closure body is mechanically identical to the
trustedly regenerated program. It is nevertheless not a legitimate proof. The
entry proof depends on a global `[simplification]` rule that is false under the
supplied semantics. A fresh machine-checked witness proves a symbolic statement
with that rule whose empty-list ground instance is false, and removing the rule
makes the candidate entry proof fail.

## 1. Input and provenance integrity

I read `/audit-input.json` first and used only its `container_paths` mounts.
It declares:

- problem `62-derivative`;
- condition `semantics`;
- `semantics_mode: SUPPLIED_SEMANTICS`;
- `record_layout: legacy-selected-stage1`.

The trusted `/reference/reference-semantics` mount is present, so the mounts do
not contradict the rendered mode. `/audit-campaign-lock.json` is regular and
readable, its JSON is exactly equal to the `audit_campaign` block, and its
SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.

For the declared legacy-selected-stage1 layout, I inspected `/run.json`,
`/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the structured trace. I also inspected
the optional `usage.json`. Every required record is a readable regular file,
and every independently computed digest matches `/audit-input.json` and, where
applicable, `/generation-result.json`.

The single structured trace file has SHA-256
`811b5dd869d2a322fb925a378b342cb189c5552483543da52c8ee2aa479c0724`.
All 835 JSONL records parse. They span 2026-07-23T05:53:05.979Z through
2026-07-23T06:30:55.853Z and contain 75 `exec` and 42 `apply_patch` tool calls.
The trace, prose report, old logs, and old `#Top` results were treated only as
untrusted generation history.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
mounts, with SHA-256 values respectively
`2ed91ee79d7a7ff2cac9f9699c62f64df5f2e38d86c9bcac80d028bb32933331`
and
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
The canonical hash is
`1ffae87f75c744800fc0334d747f4d7e4e3a8ff46a26bbcc9a2e1541c545096e`.

I recursively compared candidate and trusted supplied semantics by relative
path, entry type, and file digest. All 25 entries are identical. There are no
missing, additional, changed, mistyped, or symlinked entries. The five required
candidate proof artifacts are readable regular files. Thus there is no audit
infrastructure breach.

Evidence: `evidence/check_integrity.py` and
`evidence/01-integrity.log` (command exit 0).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract represents a polynomial as
`xs[0] + xs[1] * x + xs[2] * x^2 + ...` and asks for its derivative
coefficients in the same representation. For a finite coefficient list, this
means dropping the constant coefficient and returning
`[1 * xs[1], 2 * xs[2], ..., (n-1) * xs[n-1]]`. Empty and singleton lists
produce an empty list. The trusted canonical implementation constructs
`i * x` for every enumerated coefficient and slices away index zero.

The candidate uses a different but equivalent source algorithm: it enumerates
the input, appends `i * x` only when `i > 0`, and returns the accumulator.

I regenerated the submitted constructor program with the trusted translator:

```text
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/reconstruction/solution.py \
  > /tmp/audit-work/reconstruction/solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both files have SHA-256
`2bcf05dc954c38635670b7d9f29e97af284ef97a270195c950960bb4d7b4d042`;
the command exited 0. See `evidence/02-translation-identity.log`.

The independent differential test imports the trusted and candidate Python
entry points separately. It covers both documented examples, empty and
singleton cases, the `i == 0`/`i == 1` boundary, zeros and negatives, huge
integers, a 201-element list, every list of length 0 through 5 over
`(-3,-1,0,1,2,7)`, and three additional numeric probes. The deterministic
scope is 9,346 calls, with zero mismatches. The test algorithm and complete
generated-input definition are preserved in
`evidence/differential_test.py`; the exit-0 result is in
`evidence/02-differential.log`.

The differential run is finite evidence, not a universal proof.

## 3. Clean proof reconstruction

I copied sources to `/tmp/audit-work/reconstruction`, which contained no
candidate-built `*-kompiled` directory, and built new definitions under unique
reviewer names.

The concrete definition was rebuilt with:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
```

It exited 0. Running

```text
krun concrete_tests.mpy --definition reviewer-runtime-kompiled
```

also exited 0; the final configuration has `.K`, `NoExc`, and exit code 0.
See `evidence/03-kompile-llvm.log` and `03-krun-concrete.log`.

The proof definition was rebuilt with:

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition reviewer-verification-kompiled
```

It exited 0. I then ran every target independently:

```text
kprove spec.k --definition reviewer-verification-kompiled \
  --claims loop-invariant

kprove spec.k --definition reviewer-verification-kompiled \
  --claims loop-invariant,entry-empty --trusted loop-invariant

kprove spec.k --definition reviewer-verification-kompiled \
  --claims loop-invariant,entry-cons --trusted loop-invariant
```

Each command printed `#Top` and exited 0. The candidate's combined second
invocation, selecting both entries and trusting the separately proved loop
claim, also printed `#Top` and exited 0. Exact outputs are in
`evidence/03-kompile-haskell.log`, `03-kprove-loop.log`,
`03-kprove-entry-empty.log`, `03-kprove-entry-cons.log`, and
`03-kprove-entry-all.log`.

These results establish closure under the candidate's extended theory. They do
not establish that the extension is valid; Stage 5 shows it is not.

## 4. Adequacy and real-program pinning

### Plain-language claims

`loop-invariant` applies when `N > 0`. Its precondition has a loop over the
remaining represented coefficients `INPUT`, starting at index `N`, a local
scope containing `xs`, the stable result reference, and prior `i`/`x` values,
and a result heap object containing prefix `ACC`. Its postcondition consumes
the loop, resumes the arbitrary continuation `CONT`, preserves the framed
heap, environment, parent scope, input, and result reference, allows the final
dead `i`/`x` bindings to be existential, and changes the result contents to
`derivativeAcc(ACC, INPUT, N)`.

`entry-empty` starts an actual call to the derivative binding with the empty
represented integer list, the builtins parent, empty heap and stack, no return
state, and no exception. It requires termination with a returned reference
whose heap object is `derivativeSeq(.IntVals)`, namely the empty list.

`entry-cons` has the same concrete function binding and machine state but
accepts any integer `HEAD` followed by any finite recursive `TAIL`. It requires
the returned reference to point to
`derivativeSeq(ivCons(HEAD, TAIL))`. Empty and cons constructors are exhaustive
over all finite `IntVals`; this is not a fixed-size or bounded-unrolling
theorem.

The entry postconditions are not tautologies. `?RESULT` is existential, but
the returned `ref(?RESULT)` is tied to the same heap address containing the
specific derivative summary.

### Mechanical pinning

I parsed the trustedly regenerated `solution.mpy` and `derivativeClosure` with
the fresh definition using `kast --expand-macros --output json`. The
constructor-level check found one module statement named `derivative`, exactly
identical parameter constructors, exactly identical body constructors, and
the expected defining environment 0. This mechanically accounts for the
omitted module-loading wrapper: the claim directly supplies the same function
binding and body. See `evidence/check_pinning.py` and
`evidence/04-program-pinning.log` (exit 0).

The claim uses a bare read-only `list(ValSeq)` argument rather than allocating a
source list literal. The supplied semantics explicitly permits bare list
values as read-only claim inputs, and this program never mutates `xs`; this
input representation is semantically inert for the submitted body.

### Satisfying witnesses and body sensitivity

Fresh ground K claims instantiate the two entry domains with `[]` and
`[3,1,2,4,5]`. They require exact outputs `[]` and `[1,4,12,20]`.
Together they printed `#Top` and exited 0 without trusting the symbolic loop
claim. Both Python implementations return the same values. The artifact and
log are `evidence/witness-spec.k` and `evidence/04-ground-witnesses.log`.

For a body-sensitivity test, I changed the constructor actually executed by
the closure from `BinOp("*",...)` to `BinOp("+",...)`, rebuilt a separate
Haskell definition successfully, and retained the correct expected output.
The proof exited 1 with `WarnStuckClaimState`; the final heap contains
`[2,4,7,9]`, not `[1,4,12,20]`. See
`evidence/verification-body-mutant.k`,
`evidence/body-mutation-spec.k`,
`evidence/04-body-mutation-build.log`, and
`evidence/04-body-mutation-proof.log`.

The formal entries cover finite integer coefficient lists. The trusted prompt
uses the broad annotation `list` and does not spell out an element type, while
the examples are integer-valued. Non-integer numeric behavior is source-level
only in this candidate; it is not covered by the K theorem. This is a scope
limitation, but the final failure does not depend on whether that ambiguity is
judged material.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/inventory_k.py` scanned `semantics.k`, every supplied helper K file,
`verification.k`, and `spec.k`. The complete flattened inventory is
`evidence/05-rule-inventory.log` (exit 0):

- 950 inventoried entries;
- 707 rules, 234 syntax declarations, 5 contexts, 1 configuration, and 3
  claims;
- 148 entries declaring/mentioning `function`, 108 `total`, no `functional`;
- 25 `symbol`, 22 `no-evaluators`, 29 priority, 1 simplification, 32 concrete,
  26 owise, 7 macro, and 1 macro-rec entries.

Inventory rows K0001-K0928 are the fixed supplied semantics: 695 rules, 227
syntax declarations, all five contexts, and the configuration. I reviewed
their guards, overlaps, priorities, recursive descent, cells, allocation,
scope and stack changes, and evaluation order. Rows for unused constructs are
inert for this theorem; I found no concrete false-conclusion witness in the
used fixed fragment and do not allege an additional fixed-semantics defect.

The material constructor-to-rule map is:

- `Call`, `Name`, and the derivative binding: lookup, callee evaluation,
  left-to-right argument evaluation, closure dispatch, parameter binding,
  frame push/pop, and return in `core.k`, `call.k`, and `functions.k`;
- the docstring and expression statement: `Str` and `Expr` rules in `str.k`
  and `controls.k`;
- result initialization: `ListExpr`, `#alloc`, and assignment rules in
  `list.k`, `core.k`, and `controls.k`;
- `enumerate(xs)`: the builtins lookup, argument dereference, allocation, and
  fixed `enumVS` equations at `builtins.k:124-129`;
- `For`: one-time iterable dereference, `#loop`, `#iterNext`,
  `#loopStep`, and loop labels in `controls.k` and `list.k`;
- tuple target binding: `#bindTgt`/`#unpackSeq` in `tuple.k`;
- `i > 0`: strict comparison dispatch and integer `>Int` in
  `operators.k` and `int.k`;
- `result.append(i * x)`: attribute/call routing, integer multiplication,
  mutator priority, and in-place heap update in `call.k`, `operators.k`,
  `int.k`, and `list.k`.

The priority rules used here correctly make heap dereferences and the append
mutator preempt generic dispatch. The function frame restores the caller
environment and stack; list construction allocates the result object;
`enumerate` allocates a temporary list; append mutates only the result heap
entry. The entry postcondition frames the temporary heap allocation.

The fixed opaque symbols are `sortVS`, `sortKeyVS`, the float/conversion family
(`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`), and `md5hexCodes`. None occurs in the program, summaries,
preconditions, branch conditions, or postconditions, so none influences this
result.

### Proof-local extensions

Rows K0929-K0947 comprise every declaration and rule in `verification.k`:

| Inventory rows | Classification | Review |
|---|---|---|
| K0929 | structural representation | `IntVals` has exactly empty/cons constructors and represents every finite integer list. |
| K0930-K0932 | definitional summary | `asValSeq` is total, constructor-exhaustive, disjoint, and structurally descending. |
| K0933-K0937 | definitional summary | `derivativeSeq`/`derivativeAcc` skip index 0 and append `N * I` for `N > 0`. Guards are disjoint on all uses and recursion descends. The undefined negative-`N` case is never claimed total and is unreachable from the entries. |
| K0938 | representation constructor | `enumIntSeq` introduces an alternate `ValSeq` representation. It is not itself an equation. |
| K0939 | operational bridge and simplification | **Unsound and proof-critical.** Detailed witness below. |
| K0940-K0941 | operational iterator rules | Empty/cons iterator steps emit the same next pair and next index as fixed eager enumeration and preserve all framed cells. They are valid only for the alternate representation; they do not justify K0939 in arbitrary contexts. |
| K0942-K0947 | syntax macros | `derivativeTarget`, `derivativeLoopStep`, and `derivativeClosure` expand exactly to the regenerated target, body, parameters, binding, and environment. |

The three inventory claims K0948-K0950 are the loop, empty entry, and cons
entry described in Stage 4. Their mathematical summaries and control-flow
shapes are adequate conditional on a valid enumeration connection.

### False simplification witness

The offending rule is:

```text
rule enumVS(asValSeq(VS:IntVals), N:Int)
  => enumIntSeq(VS, N)
  [simplification]
```

It has no guard, cell constraint, continuation constraint, or iterator-context
constraint. It therefore matches the pure fixed-semantics function in every
context. The proposed justification covers only
`#iterNext(list(enumIntSeq(...)))`; the matched domain also permits length,
truthiness, equality, slicing, and arbitrary continuations. There is no
bridge-free universal connection theorem over that complete match domain.

The equation also overlaps the fixed constructor equations in a
non-substitutionally valid way. For `VS = .IntVals`, fixed semantics reduces:

```text
asValSeq(.IntVals)                 => .ValSeq
enumVS(.ValSeq, 0)                 => .ValSeq
truthy(list(.ValSeq))              => false
```

The symbolic candidate simplifier instead produces
`enumIntSeq(VS,0)`. Because that constructor is distinct from `.ValSeq`,
`truthy(list(enumIntSeq(VS,0)))` simplifies to true.

I machine-checked all sides:

1. A Haskell definition importing only fixed `MPY` plus the structural
   `IntVals`/`asValSeq` definitions built successfully.
2. Under that fixed definition, the ground claim that empty enumeration is
   false printed `#Top` and exited 0.
3. Under the candidate definition, the symbolic claim that the same
   enumeration is true for every `VS:IntVals` printed `#Top` and exited 0.
   Its empty-list substitution is therefore a false conclusion admitted by
   the extended theory.
4. Confirming the contradiction operationally, the explicit empty ground
   instance under the candidate definition, with expected `true`, exited 1
   and got stuck at `false`.

The reviewer sources are `evidence/bridge-fixed.k`,
`bridge-fixed-spec.k`, `bridge-extended-spec.k`, and
`bridge-extended-ground-spec.k`. Exact results are in
`evidence/05-bridge-fixed-build.log` (0),
`05-bridge-fixed-proof.log` (`#Top`, 0),
`05-bridge-extended-proof.log` (`#Top`, 0), and
`05-bridge-extended-ground-proof.log` (`WarnStuckClaimState`, 1).

This is not merely an unused broad rule. The symbolic entry proof needs K0939
to turn the fixed tail
`enumVS(asValSeq(TAIL),1)` into the constructor matched by the loop claim. I
removed only K0939 in a scratch definition. The definition built, but the
entry proof exited 1 with a residual containing exactly
`enumVS(asValSeq(TAIL),1)` and ten unexplored branches. See
`evidence/verification-no-bridge.k`, `spec-no-bridge.k`,
`05-no-bridge-build.log`, and `05-no-bridge-entry-proof.log`.

Thus K0939 makes a false symbolic conclusion provable on the empty satisfying
input and is materially responsible for closing the claimed universal entry
proof. The fresh `#Top` results cannot be accepted as a proof of the fixed
semantics or real program.

## 6. Fresh non-vacuity test

I did not rely on any candidate vacuity artifact. The fresh
`evidence/spec-vacuity.k` invokes the actual closure on the satisfying input
`[3,1,2,4,5]` and changes only the final result obligation from
`[1,4,12,20]` to the demonstrably false `[1,4,12,21]`.

The parser/proof build check:

```text
kprove spec-vacuity.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run
```

exited 0. The actual proof command without `--dry-run` exited 1 with
`WarnStuckClaimState`. Its final heap visibly contains the correct
`[1,4,12,20]`, so failure is the expected unmet result obligation rather than
a parser error, missing import, timeout, or unrelated crash. Exact logs are
`evidence/06-vacuity-dry-run.log` and `06-vacuity-proof.log`.

The theorem is therefore non-vacuous and discriminates this ground wrong
answer. Non-vacuity does not make the symbolic simplification sound.

## 7. Proven versus assumed accounting

What the successful candidate reachability runs establish is narrowly this:
under `MPY` plus all rules in `verification.k`, including K0939, the structural
loop claim closes, and after trusting that separately closed claim, both
structural entry cases reach a reference whose heap value is the
`derivativeSeq` summary. Because K0939 is false and essential, that statement
cannot be transferred to execution under the fixed supplied semantics.

Trust and assumption ledger:

| Boundary | Influence | Assessment |
|---|---|---|
| K toolchain v7.1.293, Haskell/LLVM backends, K integer/Boolean/map/list hooks | Parsing, rewriting, proof search, concrete execution | Ordinary low-level tool trust. |
| Byte-identical supplied `MPY` tree | All program execution | Required fixed semantics boundary; intact. Its task-used fragment was reviewed. |
| Trusted translator | Source-to-constructor program identity | Byte identity and independent expanded-AST body comparison support this bridge. |
| Direct bare-list claim input | Initial argument representation | Acceptable for this read-only `xs` body under the supplied semantics. |
| `derivativeSeq`/`derivativeAcc` | Final result meaning | Truthful structural equations for integer inputs; no opaque result oracle. |
| Loop invariant used via `--trusted` in entry phase | Universal remaining-loop summary | It was separately proved `#Top`, but under the same bad theory. Chaining does not repair K0939. |
| `enumIntSeq` iterator rules | Loop control and yielded `(i,x)` pairs | Pointwise iterator behavior is plausible, but its global connection to fixed `enumVS` is not proved. |
| K0939 symbolic simplification | Binding the fixed enumeration tail to the loop invariant and therefore the final result | Illegitimate. It is false under ground substitution, over-broad in context, and proof-critical. |
| Fixed float, sort, and MD5 opaque symbols | None for this program | Inert and not a reason for the verdict. |
| Python differential testing | Candidate/canonical source equivalence on 9,346 inputs | Finite empirical support only; not a replacement for K proof. |
| Integer-only formal input sort | The theorem excludes other coefficient values accepted by the Python code | Documented scope limitation; not needed for the decisive failure. |

Validation Gate A fails: the real-program soundness theory contains a
proof-critical false operational bridge. Gate A5 non-vacuity passes, and the
body and result are pinned, but those later facts cannot override Gate A.
Intent and evidence were reviewed, yet no legitimate candidate theorem remains
to receive a successful Gate B/C status.

Under the benchmark decision boundary, reliance on a materially unsound proof
rule is `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
