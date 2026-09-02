# Independent adversarial review: 150-x-or-y

The candidate contains a legitimate, freshly reconstructable
partial-correctness proof of the submitted program. The proof is
result-constraining, uses a sound loop-summary connection claim, and executes
the exact trustedly regenerated constructor body. I found no proof-local
operational bridge, oracle, simplification, or false rule.

The remaining concern is at the Python intent/provenance boundary, not in the K
proof: the prompt gives no positivity precondition, yet the trusted canonical
returns `x` for `n <= 0` while the candidate and its theorem return `y`.
Ordinary mathematics supports the candidate—integers below 2 are not
prime—but the systematic disagreement with a trusted input prevents an
unqualified `PASS`.

All candidate records, prose, compiled definitions, and mutations were treated
as untrusted. Fresh work was done in `/tmp/audit-work/reconstruction`; reviewer
artifacts and bounded logs are under `/audit-output/evidence/`. Exact commands
and statuses are indexed in
[`evidence/COMMANDS.md`](evidence/COMMANDS.md).

## 1. Input and provenance integrity

The launcher declares `record_layout = pipeline-v3` and
`semantics_mode = SUPPLIED_SEMANTICS`. The required trusted
`/reference/reference-semantics` tree is present, so the mounts do not
contradict the rendered mode. I did not use `writing-semantics`, as required for
this mode.

The campaign object in `/audit-input.json` is structurally equal to
`/audit-campaign-lock.json`; the independent lock digest is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the recorded digest. The run, task, result, invocation, metrics,
runtime-metrics, usage, generation prompt, Codex output, Codex last message,
and trace file hashes all match their pipeline records. All required mounts are
real regular files/directories, not symlinks.

The complete structured trace contains one JSONL file, 303 valid JSON records,
and zero malformed records. The complete generation output has 22,361 lines.
These were parsed/read only as untrusted historical claims; no historical
`#Top` was accepted. See
[`stage1/inspect-provenance-final.log`](evidence/stage1/inspect-provenance-final.log)
and
[`stage1/generation-records-small.log`](evidence/stage1/generation-records-small.log).

Independent size-aware tree hashes match the pipeline-v3 manifest records:

- mounted candidate:
  `9dc5d71b32aa9db54f988e46797f812f3879d84047bdc42e96d2bc3448459e6d`,
  matching `generation-result.json`;
- structured trace:
  `77e8dcd3b8a45770ab044389226773405f8ef7a3117b0043a045bbbd54c0e45f`,
  matching `usage.json`;
- trusted semantics:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  matching the task/audit manifest.

`audit-input.json` also records generic tree digests whose byte encoding is not
specified in the mounted records. I did not assume an encoding for those
values; instead I checked the pipeline manifest hashes above and independently
hashed every mounted file. This leaves no unresolved mount-content mismatch.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounts. A recursive, no-dereference comparison of candidate
`reference-semantics/` against the trusted tree exits 0: entry sets, entry
types, and every byte agree, with no links, additions, omissions, or changes.
The required proof artifacts are present as regular files. Evidence:
[`stage1/hash-and-compare.log`](evidence/stage1/hash-and-compare.log) and the
reviewer checker
[`stage1/inspect_provenance.py`](evidence/stage1/inspect_provenance.py).

Conclusion: stage 1 passes. There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The written contract is: for integer `n`, return `x` when `n` is prime and
return `y` otherwise. The documented examples are `(7,34,12) -> 34` and
`(15,8,5) -> 5`.

The trusted canonical special-cases only `n == 1`, then uses
`for i in range(2,n)` with a `for`-`else`. It returns `y` on a found divisor
and `x` when the range completes without one. Consequently:

- for every positive integer, it implements the documented prime/composite
  split;
- for `n <= 0`, the range is empty and it returns `x`, even though such an
  integer is not prime under the ordinary definition.

The candidate uses an equivalent exhaustive scan for `n >= 2`: initialize the
result to `x`, scan every `i` from 2 through `n-1`, set the result to `y` on
each divisor, and return it. It explicitly returns `y` for `n < 2`. Continuing
after a divisor is semantically harmless because no later branch restores
`x`.

Running the trusted translator in scratch produces a 463-byte file
byte-identical to submitted `solution.mpy`, with SHA-256
`b3d33616b6a8cc55da56c1c5d890c618dd7d5cbf11d587b87bda3fc13d725bdd`.
See
[`stage2/translation-identity.log`](evidence/stage2/translation-identity.log).

The independent differential script imports the trusted and generated entry
points under distinct module names. It covers both examples, explicit branch
boundaries, six different `x`/`y` payload pairs (including strings and lists),
and every `n` from -25 through 500: 624 calls, zero exceptions, and 50 reported
mismatches. The duplicate boundary/range cases account for the count; every
mismatch has `n <= 0`, with canonical result `x` and candidate result `y`.
There are no mismatches for tested `n >= 1`. Script and full bounded output:
[`stage2/differential.py`](evidence/stage2/differential.py) and
[`stage2/differential.log`](evidence/stage2/differential.log).

Judgment: this does not show a substituted or incorrectly translated program.
It is an intent ambiguity between two trusted sources. The prompt's
“otherwise” language and standard primality definition support the candidate,
while the canonical supplies contrary executable evidence at the unqualified
lower boundary. I treat that as a non-fatal concern rather than proof
illegitimacy.

## 3. Clean proof reconstruction

I copied only source artifacts to scratch and used the trusted semantics tree.
Candidate `runtime-kompiled`, `verification-kompiled`, caches, bytecode, and
logs were not copied or used. The observed live tools are K v7.1.293 and Python
3.10.12
([`stage3/toolchain-and-scratch.log`](evidence/stage3/toolchain-and-scratch.log)).

Fresh proof build:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-audit-kompiled
```

This exits 0. The only warnings are unused variables in supplied `str.k`.
The focused helper proof exits 0 and prints `#Top`:

```text
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC --claims SPEC.trial-loop
```

The complete positive specification, which includes both the loop circularity
and the entry target, also exits 0 and prints `#Top`:

```text
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC
```

Logs:
[`stage3/kompile-verification.log`](evidence/stage3/kompile-verification.log),
[`stage3/kprove-trial-loop.log`](evidence/stage3/kprove-trial-loop.log), and
[`stage3/kprove-complete-spec.log`](evidence/stage3/kprove-complete-spec.log).

Selecting the entry claim alone excludes its helper circularity and begins
symbolically unrolling an unbounded loop; I interrupted that diagnostic with
exit 130. It is not a failed positive target. The submitted positive workflow
is the complete-spec run, where the helper and its dependent entry claim close
together.

I also freshly built the concrete definition from the trusted semantics with
LLVM/`MPY-KRUN`. A reviewer-authored ten-case program using the exact function
body covers negative, zero, one, prime, and composite inputs. Translation and
`krun` exit 0; the final configuration has `.K`, `NoExc`, and modeled exit code
0. Evidence:
[`stage3/kompile-runtime.log`](evidence/stage3/kompile-runtime.log),
[`stage3/concrete_probe.py`](evidence/stage3/concrete_probe.py), and
[`stage3/krun-concrete-probe.log`](evidence/stage3/krun-concrete-probe.log).

Conclusion: stage 3 passes; both required positive targets reconstruct.

## 4. Adequacy and real-program pinning

### Formal claims in plain language

`[trial-loop]` starts at the exact submitted `#while` with locals
`n=N`, `x=X`, `y=Y`, `i=I`, and `result=R`; an exact saved call frame; and
normal return/exception state. Its precondition is `2 <= I <= N`. It proves
that the loop finishes, leaves `i=N`, and leaves `result` equal to
`trialChoice(N,I,R,Y)`, while preserving the arbitrary trailing continuation,
other scopes, heap, heap counter, and exit cell.

`[x-or-y]` has no `requires` clause. For every `N:Int` and modeled
`X,Y:Val`, it loads the submitted function binding, looks it up by name,
evaluates and binds its three arguments, executes its body, returns through the
real frame machinery, and constrains the final value `?V` by
`?V ==K xOrYSpec(N,X,Y)`. It also pins the final environment, scope, heap,
allocation counters, stack, return state, exception state, and exit status.
This is equality, not a one-way implication or a free result.

### Mechanical program identity

The reviewer script extracts the `Module(...)` inside the entry claim's
`#loadAll`, removes only six explicit `.Stmts` list identities, parses both it
and regenerated `solution.mpy` using fresh `kast`, and compares the complete
JSON constructor trees. Both parses exit 0; the trees are equal, with canonical
tree digest
`8be106732caecfcf1b9cc8782a2badbd792e1bd69fe1e5728356882640f600b4`.
Evidence:
[`stage4/pinning_check.py`](evidence/stage4/pinning_check.py) and
[`stage4/pinning-check-v2.log`](evidence/stage4/pinning-check-v2.log).

Binding is also pinned operationally: module load stores that body in scope 0;
`Name("x_or_y")` resolves the stored closure; call dispatch allocates scope 1
and binds the arguments; return pops exactly that frame. No rule selects a
function merely from its textual name.

### Satisfiable witnesses and concrete substitution

The entry precondition is simply true. Ground substitutions
`N=2,X=10,Y=20`, `N=4,X=10,Y=20`, and both documented examples agree among
the formal summary, candidate Python, and canonical Python. The state
`N=2,I=2,R=10,Y=20` satisfies the loop precondition and has
`trialChoice=10`; composite and prime loop witnesses are recorded as well.
For `N=0,X=10,Y=20`, the summary and candidate are 20 while the canonical is
10, exposing rather than hiding the stage-2 concern. See
[`stage4/ground_witnesses.py`](evidence/stage4/ground_witnesses.py) and
[`stage4/ground-witnesses.log`](evidence/stage4/ground-witnesses.log).

Finally, a reviewer mutation changed both occurrences of the body inside the
claim from `result = x` to `result = y` while retaining the original demanded
prime result. It dry-builds with exit 0, then fails with
`WarnStuckClaimState` at actual residual value 20. The mutation changes the
program term actually executed; it does not merely change an external source
file. Evidence:
[`stage4/make_body_mutation.py`](evidence/stage4/make_body_mutation.py),
[`stage4/spec-audit-body-mutation.k`](evidence/stage4/spec-audit-body-mutation.k),
and
[`stage4/body-mutation-kprove.log`](evidence/stage4/body-mutation-kprove.log).

Conclusion: stage 4 passes. The proof executes and constrains the real submitted
program.

## 5. Rule-by-rule static soundness review

The exhaustive lexical inventory covers 26 source files and 1,052 outer K
sentences: 25 `requires`, 91 imports, 228 syntax declarations, one
configuration, five contexts, 700 rules, and two claims. Overlapping attribute
counts include 146 function declarations, 108 total declarations, 45 priority
rules, 36 `[concrete]` rules, 29 `owise` rules, three macros, one recursive
macro, and 22 `no-evaluators` declarations. There is no local `functional` or
`simplification` declaration/rule.

Every sentence is enumerated with source span, module, class, attributes, exact
normalized text, source text, and SHA-256 in
[`stage5/inventory.json`](evidence/stage5/inventory.json) and
[`stage5/inventory.md`](evidence/stage5/inventory.md). Every one of those 1,052
records has an explicit disposition in
[`stage5/dispositions.csv`](evidence/stage5/dispositions.csv). The generated
counts and hashes are in
[`stage5/inventory-and-dispositions-v3.log`](evidence/stage5/inventory-and-dispositions-v3.log).

### Proof-local rules

`verification.k` adds exactly two syntax alternatives and five equations:

- `trialChoice` base: when `I >= N` and `I >= 2`, return the carried result;
- divisor step: when `2 <= I < N` and `pyMod(N,I) == 0`, advance to `I+1`
  carrying `Y`;
- non-divisor step: the same range with `pyMod(N,I) != 0`, advance carrying
  the current result;
- `xOrYSpec` returns `Y` when `N < 2`;
- otherwise (`N >= 2`) it starts `trialChoice(N,2,X,Y)`.

The base and recursive ranges are disjoint. The recursive equality/inequality
guards are disjoint and exhaustive for integers. Every used divisor is at
least 2, so modulo has a nonzero denominator. Recursive ground instances
strictly approach the base. `xOrYSpec`'s two guards are disjoint and exhaustive,
justifying its `total` attribute. `trialChoice` is partial outside `I >= 2`,
but neither claim nor any defining equation produces such an occurrence.

These functions rewrite only summary terms; they do not match `Call`, `While`,
assignment, return, scopes, or any configuration cell. The loop claim is the
machine-checked universal connection theorem from fixed execution to
`trialChoice`. There are no proof-local priority, simplification, concrete,
symbolic, anywhere, owise, hook, or opaque rules
([`stage5/attribute-absence.log`](evidence/stage5/attribute-absence.log)).

### Fixed-semantics path

The exact construct/rule/cell map is
[`stage5/used-construct-map.md`](evidence/stage5/used-construct-map.md).
The material findings are:

- statement sequencing and explicit call argument machinery impose
  left-to-right evaluation;
- strict/context rules evaluate `If`, assignment RHSs, binary operands, and
  comparison operands before dispatch;
- lookup resolves the actual scope-0 closure, then ordinary scope-1 locals;
- closure call, binding, return, and pop preserve the saved continuation and
  restore/delete the correct call state;
- `While` reevaluates its guard and resumes only after the full body;
- integer `<`, `==`, `%`, and `+` use K's unbounded integer operations;
- ordinary assignment changes only `i` and `result`; heap, allocation,
  exception, and exit cells are untouched.

The only potentially overlapping priority rules on this path are closure-cell
lookup/assignment rules. They require a `"$cells"` binding, absent from the
unannotated function frame. Specialized call, comparison, reference, float,
container, sorting, and method rules have disjoint constructor/operator shapes.
The generic rules therefore neither skip nor misroute task computation.

### Remaining supplied rules and opaque boundaries

The other supplied modules define floats, strings, sets, lists, tuples,
subscripts, comprehensions, methods, builtins, ranges, sorting, assertions, and
dicts. Their constructors never occur in the executed body or summaries.
`MPY-CONCRETE` is imported only by the fresh LLVM main module, not by
`VERIFICATION`. The 22 symbolic opaque declarations (float operations,
`sortVS`, `sortKeyVS`, and `md5hexCodes`) and supplied non-exhaustive total
helpers are listed in
[`stage7/trust-ledger.md`](evidence/stage7/trust-ledger.md). None can influence
a task branch, result, state change, or postcondition.

Some of those broad MPY facilities are intentionally partial approximations of
full Python—for example symbolic float/sort values and total-but-unevaluated
out-of-bounds helpers. I do not label an unused rule unsound merely from that
model limitation: there is no reachable task-domain term and hence no false
task conclusion witness for those rules. Conversely, no task-relevant rule
replaces a property-bearing computation with such a symbol.

Conclusion: stage 5 passes. No material unsound rule or overlap contributes to
claim closure.

## 6. Fresh non-vacuity test

I inspected the candidate's `spec-vacuity.k` and body mutation only as untrusted
evidence
([`stage6/candidate-mutations-untrusted.log`](evidence/stage6/candidate-mutations-untrusted.log)).
I then wrote the distinct reviewer mutation
[`stage6/spec-audit-vacuity.k`](evidence/stage6/spec-audit-vacuity.k).

It executes the unchanged, fully pinned body at the satisfiable ground input
`n=2,x=10,y=20` but deliberately requires returned value 20. A `--dry-run`
build exits 0, proving that the mutation parses and compiles. Actual `kprove`
exits 1 with `WarnStuckClaimState`; the terminal configuration has `<k> 10 ~>
.K </k>`, so failure is exactly the unmet false result, not a parser error,
missing import, timeout, or unrelated crash. Logs:
[`stage6/mutation-dry-run.log`](evidence/stage6/mutation-dry-run.log) and
[`stage6/mutation-kprove.log`](evidence/stage6/mutation-kprove.log).

Conclusion: stage 6 passes. The positive theorem discriminates a meaningful
false result.

## 7. Proven versus assumed accounting

The successful reachability proof establishes the following conditional
partial-correctness theorem under the supplied MPY semantics:

> For every K integer `N` and modeled values `X` and `Y`, if the exact submitted
> `x_or_y` execution terminates from the pinned initial configuration, it
> returns `Y` when `N < 2` or some integer in `2 .. N-1` divides `N`; otherwise
> it returns `X`. It finishes with the pinned normal environment, scope, heap,
> stack, allocation, return, exception, and exit state.

For `N >= 2`, “no divisor in `2 .. N-1`” is the standard characterization of
primality. Thus the theorem proves the written prime/otherwise behavior for
the modeled integer domain. The K proof does not rely on candidate prose,
generation traces, differential tests, or prior compiled artifacts.

The actual dependency-path assumptions are the supplied MPY rules for the used
constructs; K's Int/Bool/Map/List primitives; generated strictness; and K
v7.1.293's kompiler/Haskell/Kore proof implementation. The translator is
trusted only for the source-to-constructor bridge, which is independently
checked by byte regeneration and parsed-tree equality. The full ledger,
including every imported-but-unused opaque symbol and each empirical/informal
bridge, is
[`stage7/trust-ledger.md`](evidence/stage7/trust-ledger.md).

Gate accounting:

- Real-program soundness: **PASS**. Exact body, exact binding, real fixed
  execution, sound summaries, a proved loop connection, a satisfying state,
  result equality, false-result rejection, and body sensitivity are all
  established.
- Intent adequacy: **PASS for the written prime/otherwise contract**, with a
  documented canonical boundary conflict at `n <= 0`. The theorem does not
  narrow the prompt to finite sizes or examples; it covers every K `Int`.
- Trust/evidence auditability: **PASS**. Commands, exit codes, positive
  `#Top`s, mutation residuals, source inventory, scripts, and finite-test scope
  are preserved and separated from the formal theorem.

The canonical disagreement is real and systematic, but it does not make the K
theorem false, vacuous, substituted, or domain-bounded. Because the written
contract supports the candidate's lower-bound behavior and no explicit
positive-`n` precondition exists, the appropriate benchmark mapping is a
legitimate proof with concerns, not `FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
