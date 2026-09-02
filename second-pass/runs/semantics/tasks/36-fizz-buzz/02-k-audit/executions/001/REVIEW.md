# Independent adversarial review: 36-fizz-buzz

The candidate is **not a legitimate partial-correctness proof of the real
generated program**. Fresh reconstruction does confirm that all seven submitted
K claims close and that their literal results are non-vacuous. The decisive
failures are different:

1. the entry claims execute a manually declared `FIZZ-BUZZ-CLOSURE`, not the
   submitted `solution.mpy` module or a closure obtained by loading it; and
2. the entry theorem is only six ground examples, not a theorem over the
   prompt's integer input domain.

The supplied closure currently duplicates the submitted function body, but
there is no proof dependency connecting the two. A source-body mutation
demonstrates that the proof is insensitive to `solution.mpy`.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted
`/reference/reference-semantics` mount is present. There is therefore no
infrastructure contradiction and no reason to suppress candidate verdict
markers.

I enumerated both semantics trees with `lstat`-style, no-follow traversal. The
candidate tree has 25 entries and is identical to the 25-entry trusted tree in
entry names, entry types, and regular-file SHA-256 content. It has no symlink,
missing entry, additional entry, mistyped entry, or changed entry. See
[stage1-semantics-integrity.log](evidence/stage1-semantics-integrity.log) and the
reviewer script
[check_tree_integrity.py](evidence/check_tree_integrity.py).

The candidate prompt and translator are byte-identical to their trusted
versions:

- prompt SHA-256:
  `9ca3d814d8f4c88fc35c6286cf046f39b0903222b094a800926eead370bcf4bb`;
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The hashes and successful `cmp` statuses are in
[stage1-prompt-translator-integrity.log](evidence/stage1-prompt-translator-integrity.log).

### Missing provenance artifacts

The candidate does not contain `run-input.json`, `metrics.json`,
`codex-last.txt`, or `codex-output.log`. No structured generation-trace
artifact is present in the enumerated candidate tree either. These are
provenance/integrity deficiencies, recorded in
[stage1-provenance-artifacts.log](evidence/stage1-provenance-artifacts.log).
They do not prevent reconstruction from the available trusted and candidate
source files, but no generation narrative or reported metrics can be audited.

No candidate-produced compiled definition or cache was used.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

From `/reference/prompt.py` and `/reference/canonical.py`, `fizz_buzz(n)` must
return the total number of occurrences of the decimal digit `7` among all
integers `i` in Python's `range(n)` for which `i` is divisible by 11 or 13.
The documented examples are:

- `fizz_buzz(50) == 0`;
- `fizz_buzz(78) == 2`;
- `fizz_buzz(79) == 3`.

For integer `n <= 0`, `range(n)` is empty and the result is 0.

### Implementation inspection

`/candidate/solution.py` uses a different but appropriate algorithm. It scans
`i = 0, ..., n-1`; for selected `i`, it repeatedly examines `i % 10` and
replaces `i`'s local copy by `i // 10`. Since every scanned `i` is
non-negative, this counts exactly the decimal `7` digits. The special selected
integer 0 contains no `7`, so skipping its empty digit loop preserves the
canonical result. The source-level algorithm difference is preserved in
[stage2-solution-canonical-diff.log](evidence/stage2-solution-canonical-diff.log).

The trusted translator regenerated `solution.mpy` byte-for-byte. Both files
have SHA-256
`890b9c5ceba7377100824db98d3879fbd209c6592d93c8ba35179692b7b88328`;
`cmp` exited 0. See
[stage2-regenerate-mpy.log](evidence/stage2-regenerate-mpy.log).

### Independent differential test

The reviewer-authored
[differential_test.py](evidence/differential_test.py) imports the trusted
canonical entry point and the generated Python entry point independently. It
tested:

- every integer from -20 through 300;
- explicit negative, empty, loop-entry, divisor-11, divisor-13, `11*13`,
  selected-digit-7, multiple-7, and large boundaries;
- all three documented examples; and
- 128 deterministic random integers in `[-100, 5000]`, seed `360036`.

There were 446 unique inputs and zero value or result-type mismatches. Exact
inputs, representative results, command, and exit 0 are in
[stage2-differential.log](evidence/stage2-differential.log). This is finite
evidence for source-to-canonical fidelity, not a universal proof.

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied into
`/tmp/audit-work/fizz-buzz-audit`. A pre-build search confirmed that no
`*-kompiled` directory existed
([stage3-prebuild-cache-check.log](evidence/stage3-prebuild-cache-check.log)).

For independent claim selection, I added labels to the scratch copy of
`spec.k`. No claim term, cell, precondition, or postcondition was changed. The
complete diff is
[stage3-claim-labeling-diff.log](evidence/stage3-claim-labeling-diff.log).

Using K v7.1.337:

- the concrete LLVM definition rebuilt from
  `reference-semantics/semantics.k`, exit 0
  ([stage3-build-concrete.log](evidence/stage3-build-concrete.log));
- the Haskell proof definition rebuilt from `verification.k`, exit 0
  ([stage3-build-proof.log](evidence/stage3-build-proof.log)).

The LLVM build emitted baseline exhaustiveness warnings for helpers such as
`mapStrVS`, several float helpers, `joinCodes`, and `valSeqAt`. None is on this
integer-only program path, and these files are byte-identical to the trusted
supplied semantics. The Haskell build emitted only unused-variable warnings in
the trusted string helper.

Each positive target was then selected and run independently:

| Claim | Result |
|---|---|
| universal inner loop | exit 0, `#Top` |
| entry `n=-5` | exit 0, `#Top` |
| entry `n=0` | exit 0, `#Top` |
| entry `n=50` | exit 0, `#Top` |
| entry `n=78` | exit 0, `#Top` |
| entry `n=79` | exit 0, `#Top` |
| entry `n=100` | exit 0, `#Top` |

The authoritative log check is
[stage3-positive-proof-summary.log](evidence/stage3-positive-proof-summary.log);
it points to the seven individual bounded proof logs.

An earlier reviewer attempt ran six ground proofs concurrently and caused
backend code-137 kills. That audit-induced resource event is not used against
the candidate. Every affected target was rerun sequentially and succeeded; the
sequential logs listed by the summary above are the verdict evidence.

## 4. Adequacy and real-program pinning

### Plain-language claims and satisfiable preconditions

The inner-loop claim in `/candidate/spec.k:7` says:

- start with the exact `#while(x > 0, INNER-BODY)` computation followed by any
  continuation `CONT`;
- in current scope `L`, bind `n=N`, `count=A`, `i=I`, and `x=X`;
- require `X >= 0`;
- after the loop, continue with `CONT`, preserve `n` and `i`, set `x=0`, and
  set `count=countSevensAcc(A,X)`;
- frame the scope allocator, heap, heap allocator, stack, return state,
  exception state, and exit code.

A concrete satisfying state uses `L=1`, `A=4`, `X=707`, `N=1000`, `I=12`,
`CONT=.K`, `scopeLoc=2`, empty heap/stack, `noRet`, `NoExc`, and exit code 0.
The loop ends with count 6 and `x=0`.

Each of the six entry claims has no symbolic `requires`: its precondition is the
displayed ground `Call(FIZZ-BUZZ-CLOSURE,N)` in the pristine module cell state.
Its postcondition is a literal integer, respectively
`0, 0, 0, 2, 3, 3` for `N=-5,0,50,78,79,100`. Thus these claims are
result-constraining, not free-variable or implication tautologies.

[adequacy_witness.py](evidence/adequacy_witness.py) exhibits the inner state and
checks every ground entry result against both Python implementations. All
comparisons match; the command exits 0 in
[stage4-ground-witnesses.log](evidence/stage4-ground-witnesses.log).

### Current body duplication is not program pinning

The `FIZZ-BUZZ-CLOSURE` macro in `/candidate/verification.k:70` contains a
manually repeated function body. After expanding `OUTER-BODY` and `INNER-BODY`
and normalizing explicit empty `.Stmts` units, that body is currently identical
to the body in submitted `solution.mpy`. The independent comparison and equal
hashes are in
[stage4-current-closure-identity.log](evidence/stage4-current-closure-identity.log).

That equality is reviewer evidence only. Neither `verification.k` nor `spec.k`
requires, loads, parses, or executes `solution.mpy`. The entry `<k>` cell calls
the macro closure directly. `FIZZ-BUZZ-DEF`, which at least represents a
function definition, is itself unused.

The body-sensitivity experiment makes this gap observable:

1. in a separate scratch copy, I changed only `solution.mpy` from
   `Return(Name("count"))` to `Return(Int(999))`;
2. dependency search found only a comment mentioning `solution.py`, and no
   source dependency on either solution file
   ([stage4-pinning-mutation-diff.log](evidence/stage4-pinning-mutation-diff.log));
3. I freshly rebuilt `verification.k`, exit 0
   ([stage4-pinning-rebuild.log](evidence/stage4-pinning-rebuild.log));
4. the proof still closed `n=0 => 0` with exit 0 and `#Top`
   ([stage4-pinning-mutated-proof.log](evidence/stage4-pinning-mutated-proof.log)).

The mutated submitted program would return 999, while the theorem remains
unchanged. This is a concrete body-insensitivity witness: the proof is about a
substituted AST, not the actual submitted MPY artifact.

### Missing universal entry theorem

Even for the duplicated closure, there is no claim of the form
`Call(..., N) => fizzBuzzSpec(N)` for arbitrary integer `N`, and there is no
outer-loop invariant. `divisibleBy11Or13`, `fizzBuzzAcc`, and `fizzBuzzSpec`
are never referenced by any submitted claim. The universal inner-loop theorem
does not connect the full outer execution to the prompt property.

Consequently, successful reconstruction establishes six examples, not partial
correctness over the intended integer input domain. Both the program-pinning
failure and this domain-coverage failure independently cross the stated
`FAIL / NOT_LEGIT` boundary.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored [inventory_k.py](evidence/inventory_k.py) inventories
every `syntax`, `rule`, `context`, `configuration`, and `claim` in the complete
supplied semantics tree, `verification.k`, and the original unlabeled
`spec.k`. The generated
[rule-inventory.tsv](evidence/rule-inventory.tsv) has one source-located,
normalized row and an audit decision for each item:

- 955 total items;
- 707 rules;
- 235 syntax declarations;
- 5 contexts;
- 1 configuration;
- 7 claims.

Of these, 928 items (695 rules and 233 other declarations) are from the
byte-identical trusted supplied semantics, 20 items (12 rules and 8 syntax
declarations) are candidate proof extensions, and 7 are candidate claims.
There are no `[functional]` declarations. The ledger records 45 priority rules,
three simplification rules, all function/total declarations, concrete rules,
macros, and every opaque/symbol declaration. Generation and classification
counts are in
[stage5-inventory-generation.log](evidence/stage5-inventory-generation.log)
and [stage5-inventory-summary.log](evidence/stage5-inventory-summary.log).

Every trusted-semantics row is classified as the selected supplied baseline,
not as a candidate proof extension. Every candidate row has a separate
decision. The detailed ledger, rather than a sampled list, is the exhaustive
rule-by-rule record.

### Candidate proof-extension decisions

`divisibleBy11Or13` (`verification.k:8-10`) is a total mathematical predicate.
Its one equation is valid for all K integers because both divisors are nonzero.
It is unused by all claims.

`countSevensAcc` (`verification.k:12-24`) has three simplification equations:

- `I=0` returns the accumulator;
- positive `I` ending in 7 increments it and recurses on `I // 10`;
- positive `I` not ending in 7 recurses without increment.

The positive guards are disjoint and exhaustive, and the recursive argument
strictly decreases for positive integers. The symbol is deliberately partial
for negative `I`, but its only claim use requires `X>=0`. These equations are
ordinary base-10 mathematics and do not bypass execution; they summarize the
post-state of the separately executed inner loop.

`fizzBuzzAcc` (`verification.k:26-34`) has three disjoint equations:
`I>=N`, `I<N` and selected, and `I<N` and not selected. Its recursive cases
increase `I` by one and are mathematically sound. `fizzBuzzSpec`
(`verification.k:36-37`) delegates to that accumulator. All four rules and
their declarations are unused by every submitted claim, so they contribute no
theorem about the entry point.

`INNER-BODY`, `OUTER-BODY`, `FIZZ-BUZZ-DEF`, and `FIZZ-BUZZ-CLOSURE`
(`verification.k:41-79`) are compile-time AST macros. Their equations are
truthful syntactic definitions; no false mathematical conclusion witness was
found. `FIZZ-BUZZ-DEF` is unused. The other three execute the duplicated entry
body. Their defect is not a false rewrite rule: it is the unjustified use of an
unlinked duplicate as though it were the submitted program.

The candidate adds no opaque symbol, no priority rule, and no operational
bridge rule that preempts fixed semantics. I therefore do **not** label any
candidate rule unsound and do not invent a false-conclusion witness for one.
The separate source-body mutation is evidence of theorem/program
non-identity, not evidence that a macro equation is mathematically false.

### Used-construct map and operational behavior

The duplicated closure uses only this subset of the supplied baseline:

| Program construct | Declaration and rules | Operational effect |
|---|---|---|
| `Call` and `closureVal` | `syntax.k`, `call.k`, `functions.k` | evaluate callee/argument, allocate a call scope, bind `n`, push/pop a frame, restore caller state |
| statement sequence and names | `core.k` | left-to-right statement sequencing and lexical scope lookup |
| `Assign`, `AugAssign` | `controls.k` plus integer `applyBin` | update `count`, `i`, and `x` in the current scope |
| `While` and `If` | `controls.k`, `truthy` in `core.k` | re-evaluate guards, sequence body and loop continuation, select exactly one branch |
| `%`, `//`, `+` | `operators.k`, `int.k` | evaluate operands left-to-right; `pyMod` and floored division agree with Python for the positive divisors 10, 11, and 13 |
| `<`, `>`, `==` | `operators.k`, `int.k` | integer comparison |
| short-circuit `or` | `bool.k` | evaluate the 13-divisibility comparison only when the 11 comparison is false |
| `Return` | `functions.k` | place the returned integer in `ret`, discard the callee continuation, then restore the caller frame |

All relevant bindings resolve in the freshly created call scope. The program
does not allocate heap objects, mutate the heap, perform output, or use
exceptions. The literal nonzero divisors eliminate division-by-zero paths.
Call setup/pop accounts for `env`, `scopes`, `scopeLoc`, `stack`, and `ret`;
the claims pin or frame the remaining cells.

The supplied baseline contains 25 symbol declarations, 22 of which explicitly
use `no-evaluators`, in the MD5, float, and sorting subsystems. It also contains
all 45 priority rules. None of those opaque values or priority-specific object,
float, list, dict, subscript, method, or sorting paths is reachable in this
integer-only closure. The full list is
[stage7-opaque-priority-ledger.log](evidence/stage7-opaque-priority-ledger.log).

## 6. Fresh non-vacuity test

The fresh mutation
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k) keeps the satisfiable
pristine `n=0` entry state but changes the result obligation from 0 to 1. Both
Python implementations return 0 for this witness.

The mutation successfully parsed and generated its backend command under
`--dry-run`, exit 0:
[stage6-vacuity-dry-run.log](evidence/stage6-vacuity-dry-run.log).

The actual proof then exited 1 with `WarnStuckClaimState`. The residual
configuration has `<k> 0 ~> .K </k>` while the destination requires 1, followed
by the expected “cannot be rewritten further” prover error:
[stage6-vacuity-proof.log](evidence/stage6-vacuity-proof.log).

This is meaningful non-vacuity evidence for the duplicated ground entry
theorem. It is not a parser failure, missing import, timeout, or unreachable
mutation. It does not repair the real-program pinning or universal-adequacy
failures.

## 7. Proven versus assumed accounting

### What the successful K runs establish

Conditional on the trusted supplied MPY semantics and K toolchain:

1. the manually declared inner-loop AST transforms any displayed scope with
   `X>=0` according to `countSevensAcc(A,X)`, sets `x=0`, and resumes the framed
   continuation; and
2. the manually declared full closure returns the literal expected values for
   the six ground inputs `-5, 0, 50, 78, 79, 100`.

The successful runs do not establish:

- execution of the submitted `solution.mpy` module;
- sensitivity to changes in that module;
- a result for arbitrary `n`;
- equivalence of `fizzBuzzSpec` to a full entry execution; or
- total correctness/termination beyond what the concrete runs and informal
  loop descent make evident.

### Trust and evidence ledger

- **Trusted prompt, canonical implementation, and translator.** These are
  mounted authority inputs. They define intent and the translation oracle.
- **Trusted supplied semantics.** Candidate and trusted trees are exactly
  identical. K built-in integer, Boolean, string, map/list, rewriting, and
  backend correctness remain the low-level trust boundary. This is acceptable
  under `SUPPLIED_SEMANTICS`.
- **Proof-local digit-count equations.** These are independently reviewed,
  guarded, terminating mathematics. They affect only the inner claim and are
  acceptable.
- **Unused proof-local specification functions.** `divisibleBy11Or13`,
  `fizzBuzzAcc`, and `fizzBuzzSpec` are sound definitions but prove nothing
  merely by being declared.
- **Manual closure-to-program bridge.** Static normalization shows current AST
  equality, and differential testing supports behavioral equality on 446
  inputs. Neither creates a dependency on `solution.mpy`. The mutation admits
  the opposite real-program behavior while the proof still closes. This bridge
  is illegitimate for a theorem claimed about the submitted program.
- **Differential testing.** It supports the tested source/canonical bridge only.
  It is finite empirical evidence and cannot substitute for the missing K
  connection or universal entry theorem.
- **Opaque supplied symbols.** MD5, float, and sorting opaque symbols are
  baseline trust boundaries but are unreachable here and influence no branch,
  state, or postcondition in these claims.
- **Missing provenance.** No generation trace, run input, metrics, or Codex
  report is available. No candidate narrative is relied upon.

### Decision

Fresh proof closure and a good false-result rejection do not overcome theorem
identity and adequacy. The body mutation proves that the K theorem is
insensitive to the real MPY artifact, and the theorem covers only six entry
values. Under the stated decision boundary, this is a proof of a substituted,
under-specified program and must be rejected.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
