# Independent adversarial audit: 36-fizz-buzz

The candidate is **not a legitimate proof of the full HumanEval contract**. It
does contain freshly reproducible, non-vacuous K proofs of one universal inner
digit loop and six concrete entry executions. It mechanically pins those
executions to the regenerated submitted program. It never states or proves a
universal entry-point theorem, however: the only entry claims fix `n` to
`-5, 0, 50, 78, 79, 100`. The declared `fizzBuzzSpec`/`fizzBuzzAcc` outer
summary is not used by any claim. That materially narrows the unrestricted
`int` source-contract domain. Under the benchmark-specific decision rule, this
Kit-style `SOUND-BUT-LIMITED` result is `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

The launcher record says:

- `record_layout = legacy-selected-stage1`
- `semantics_mode = SUPPLIED_SEMANTICS`
- `condition = semantics`
- `problem_id = 36-fizz-buzz`

The mode and mounts are consistent: `/reference/reference-semantics` exists.
There is no infrastructure breach.

Independent checks found:

- `/audit-campaign-lock.json` is byte-hashed to
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the hash declared in `/audit-input.json`, and its parsed JSON value
  equals the complete `audit_campaign` block.
- Every record required by `legacy-selected-stage1` is a readable regular file
  (or, for `codex-trace`, a readable directory): `/run.json`, `/task.json`,
  `/generation-result.json`, `invocation.json`, `metrics.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
  Present `usage.json`, `legacy-metrics.json`, and `legacy-run-input.json` were
  also inspected.
- All launcher-declared file hashes checked in
  [01-integrity.log](evidence/01-integrity.log) match the independently hashed
  mounts. The single trace file has SHA-256
  `8c78224a1851042ee1a13dcdbe20d2af5b0d850fc8f9c9aadf9ff9f611b1ce2e`,
  matching both generation manifests.
- Every one of the 933 structured-trace lines parses as JSON; there are zero
  parse errors. The trace contains 233 tool calls and 233 corresponding tool
  outputs. The complete untrusted generation claim, including its seven-claim
  `KPROVE_PASSED` assertion, was inspected but not relied upon.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts.
- Recursive, no-dereference comparison of the supplied semantics found 25
  entries in each tree (one directory and 24 regular files), with no missing,
  additional, changed, mistyped, or symlinked entry:
  `semantics_trees_exact=True`.
- All candidate and reference source-file hashes and entry types are recorded
  in [01-integrity.log](evidence/01-integrity.log). Reviewer scripts are
  [check_integrity.py](evidence/check_integrity.py),
  [summarize_trace.py](evidence/summarize_trace.py), and
  [01-integrity.sh](evidence/01-integrity.sh).

The candidate proof deliverables are all present. Candidate-provided bytecode
and all generation prose/logs were treated only as untrusted evidence.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks `fizz_buzz(n: int)` to return the total number of digit
`7` occurrences in all integers strictly less than `n` that are divisible by
11 or 13. The prompt supplies no numerical bound. For nonpositive `n`, the
canonical `range(n)` is empty and the result is zero.

The candidate implementation uses an outer integer loop and decimal
division/modulo rather than strings. For every selected nonnegative `i`, its
inner loop counts each base-10 digit equal to 7. This is a different but
appropriate algorithm.

The trusted translator was run in clean scratch:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

It exited 0. `cmp -l solution.mpy regenerated-solution.mpy` exited 0, and both
files have SHA-256
`890b9c5ceba7377100824db98d3879fbd209c6592d93c8ba35179692b7b88328`.

The independent differential test imports the trusted canonical entry point
and submitted generated entry point from separate modules. It covers:

- all integers from `-20` through `500`;
- prompt examples and explicit negative/empty cases;
- thresholds around 11, 13, 22, 26, 50, 77, 78, 79, 117, 176, 770, and other
  divisibility/digit boundaries;
- larger values through 20,000; and
- 1,000 deterministic random draws in `[-1000, 20000]`.

There were 1,488 distinct cases and zero mismatches. Selected results include
`78 -> 2`, `79 -> 3`, `118 -> 4`, `1000 -> 47`, and `20000 -> 1280`. This
supports implementation fidelity on tested values but is finite evidence, not
a universal proof. Exact inputs, results, commands, and statuses are in
[02-program-fidelity.log](evidence/02-program-fidelity.log); the independent
oracle driver is [differential_test.py](evidence/differential_test.py).

## 3. Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/reviewer-002/scratch`. The semantics copy came from the trusted
reference mount. No candidate-built definition or cache was copied or reused.
K reports version `v7.1.293`.

Fresh concrete reconstruction used:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
krun reviewer-concrete-tests.mpy \
  --definition reviewer-runtime-kompiled --output pretty
```

Both commands exited 0. The concrete test translation was byte-identical to the
submitted `concrete-tests.mpy`. `krun` ended with `.K`, `NoExc`, and exit code
0 after the five assertions.

Fresh proof reconstruction used:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled
```

It exited 0. To select claims independently, the reviewer copied `spec.k` to a
scratch-only `spec-labeled.k` and added only inert labels. Each claim was then
run by a separate command of this form:

```text
kprove spec-labeled.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC --claims SPEC.<label> --output pretty
```

Every positive target claim independently exited 0 and printed `#Top`:

| Claim | Formal input/result | Exit | Output |
|---|---|---:|---|
| `inner-loop` | symbolic `X >= 0` | 0 | `#Top` |
| `entry-neg5` | `fizz_buzz(-5) = 0` | 0 | `#Top` |
| `entry-0` | `fizz_buzz(0) = 0` | 0 | `#Top` |
| `entry-50` | `fizz_buzz(50) = 0` | 0 | `#Top` |
| `entry-78` | `fizz_buzz(78) = 2` | 0 | `#Top` |
| `entry-79` | `fizz_buzz(79) = 3` | 0 | `#Top` |
| `entry-100` | `fizz_buzz(100) = 3` | 0 | `#Top` |

The complete commands, statuses, bounded outputs, and individual unabridged
proof logs are indexed by
[03-clean-reconstruction.log](evidence/03-clean-reconstruction.log). Compiler
warnings concern unused variables or nonexhaustive behavior of unrelated
supplied functions; none prevented either clean build or any selected claim.

## 4. Adequacy and real-program pinning

### Formal preconditions and postconditions

The inner-loop claim in `/candidate/spec.k:8` has this plain-language meaning:

- Precondition: `<k>` begins with the actual translated inner `while` followed
  by an arbitrary continuation; the current scope has `n=N`, `count=A`, `i=I`,
  and `x=X`; other listed cells are arbitrary but fixed; and `X >= 0`.
- Postcondition: the continuation remains, `n` and `i` are unchanged, `x=0`,
  and `count=countSevensAcc(A,X)`. All other cells are preserved.

It is satisfiable. For example, take scope location 1, parent 0,
`N=78, A=5, I=0, X=177`, empty heap/stack, `noRet`, `NoExc`, and any matching
continuation. The stated summary gives final `count=7` and `x=0`.

Each entry claim has no symbolic input precondition. It pins an explicit
pristine module configuration and one concrete closure argument. Those six
states are plainly realizable. Extraction and substitution against both Python
implementations gives:

| `n` | Claimed | Canonical | Submitted |
|---:|---:|---:|---:|
| -5 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |
| 50 | 0 | 0 | 0 |
| 78 | 2 | 2 | 2 |
| 79 | 3 | 3 | 3 |
| 100 | 3 | 3 | 3 |

The extraction script and output are
[claim_substitution.py](evidence/claim_substitution.py) and
[04-adequacy-pinning.log](evidence/04-adequacy-pinning.log).

### Mechanical program pinning

The claims do not read `solution.mpy`; they invoke a constructor macro. The
allowed constructor-level identity check succeeds:

1. Trusted regeneration establishes the submitted `solution.mpy`.
2. `kast --expand-macros` parsed both `solution.mpy` and
   `Module(FIZZ-BUZZ-DEF)` under the fresh proof definition.
3. The emitted KORE files are byte-identical (`cmp` exit 0), each with SHA-256
   `677d737b3f1778adbaca11fbddf5aaa67483dc4eed7edcf0db9c820003b5e7f5`.
4. A bridge-free reviewer claim using only fixed semantics proves that loading
   that exact module in environment 0 binds `"fizz_buzz"` to
   `FIZZ-BUZZ-CLOSURE`. It exits 0 with `#Top`.

Thus every fixed entry claim executes the actual submitted function body; this
is not a substituted-program failure. Evidence and exact commands are in
[04-adequacy-pinning.log](evidence/04-adequacy-pinning.log).

### Fatal adequacy gap

The candidate has no symbolic entry claim. `fizzBuzzAcc` and `fizzBuzzSpec`
occur only in `/candidate/verification.k`; neither occurs in any claim in
`/candidate/spec.k`. There is no universal outer-loop invariant or auxiliary
outer-loop execution claim. The six fixed entry proofs close even when selected
alone, without the universal inner-loop claim, by concrete unrolling.

The inner theorem proves only how the digit loop transforms `count` for one
already-selected integer. It does not prove, for an arbitrary `n`, which outer
iterations are selected or that their digit counts accumulate to the requested
total. For example, intended-domain input `n=118` has result 4 in both Python
implementations, but no entry theorem covers it.

Accordingly, the formal entry domain is a finite set of six values, not the
unrestricted HumanEval `int` domain. This is a material domain narrowing and is
the decisive failure.

## 5. Rule-by-rule static soundness review

The exhaustive machine-generated inventory is
[05-rule-inventory.md](evidence/05-rule-inventory.md), produced by
[build_rule_inventory.py](evidence/build_rule_inventory.py). It contains one
line-addressable row for every local declaration/rule block in
`semantics.k`, all 23 supplied helper K files, and `verification.k`:

- 1,111 total blocks;
- 707 rules;
- 235 syntax declarations;
- 1 configuration and 5 contexts;
- 152 function-bearing blocks and 113 total-bearing blocks;
- all 52 priority-bearing, 30 `owise`, 58 concrete, 3 simplification, 8 macro,
  and 1 recursive-macro blocks;
- no `functional` or `smtlib` declaration; and
- 22 actual `no-evaluators` opaque declarations (29 inventory blocks mention
  an opaque boundary when attached comments/rules are included).

Each row records its attributes, used-path status, and assessment. The full
attribute search and submitted-constructor map are preserved in
[05-static-review.log](evidence/05-static-review.log).

### Used construct-to-rule map

| Submitted construct | Declaration/evaluation path |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; `core.k:124-127`; `functions.k:14` |
| `Call` of closure | `call.k:20-21,69`; `core.k:189-191`; `functions.k:63-64,80,85` |
| `Assign`, `AugAssign` | `syntax.k`; `controls.k:9,20` |
| `Name`, `Int` | `core.k:130-132,194` |
| statement order | `core.k:126-127` |
| `%`, `//`, `+` | strict/seqstrict syntax; `operators.k:12`; `int.k:9,15-16,19-20` |
| `<`, `>`, `==` | compare contexts and dispatch in `operators.k:15-17`; `int.k:22,24,26` |
| short-circuit `or` | `bool.k:16-17,22,24` |
| `If` | strict condition and `controls.k:51-54` |
| `While` | `controls.k:65,77-81,85` |
| `Return` | strict expression and `functions.k:78,85` |

These rules evaluate operands left-to-right where required, preserve Python
short-circuiting, and use unbounded K integers. Calls create one fresh local
scope and stack frame, bind `n`, execute the real body, restore the caller
environment, and remove the local scope. The submitted program never allocates
heap objects; heap, exception, and exit-code cells remain unchanged. The
pristine entry claims pin all observable cells.

No material ref-dereference priority rule can fire because every program value
here is an integer or Boolean. The generic call rule's `owise` attribute does
not bypass callee/argument evaluation. Return's abrupt continuation removal is
the fixed semantics' intended function-return control effect and is paired with
the saved call frame.

### Proof-local extension inventory

| Extension | Class and review | Claim dependency |
|---|---|---|
| `divisibleBy11Or13` | Truthful total definition using positive divisors 11 and 13. | None |
| `countSevensAcc` | Definitional summary. Base/last-digit guards are disjoint; for `I>0` they cover both digit cases and recurse to a smaller nonnegative integer. The three simplification rules are true over the inner claim's `X>=0` domain. | Inner-loop postcondition only |
| `fizzBuzzAcc` | Truthful recursive mathematical accumulator over `[I,N)` on its defined uses. It is not an operational bridge. | None |
| `fizzBuzzSpec` | Names `fizzBuzzAcc(0,0,N)`; total for integer `N` through the guarded recursion/base. | None |
| `INNER-BODY`, `OUTER-BODY`, `FIZZ-BUZZ-DEF`, `FIZZ-BUZZ-CLOSURE` | Constructor macros, not runtime oracles. Exact expansion and module-load binding were mechanically checked. | Program term in helper/fixed entry claims |

`verification.k` defines no opaque symbol, priority rule, SMT axiom, ordinary
operational shortcut, or rule that intercepts `Call`, `While`, arithmetic, or
return. In particular, it does not replace program execution with
`fizzBuzzSpec`. There is no result-bearing oracle or circular abstraction.

The supplied fixed semantics has opaque boundaries for
`sortVS`, `sortKeyVS`, `md5hexCodes`, and the float primitives
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`,
`mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, and `sqrtF`. None appears in the submitted AST, any proof
claim, any proof-local summary, or the reconstructed proof path. They therefore
cannot affect these results.

No rule is classified as materially unsound for the submitted theorem, so
there is no unsoundness allegation requiring a false-conclusion witness. The
verdict does not rely on semantic unsoundness; it relies on the objectively
finite theorem domain.

## 6. Fresh non-vacuity test

The reviewer-authored
[spec-vacuity.k](evidence/spec-vacuity.k) changes the true `n=78` result
obligation from 2 to 3 while leaving the executed closure and pristine state
unchanged.

- Independent witness: canonical and submitted Python both return 2.
- Mutation dry-run/compilation: exit 0.
- Mutation proof: exit 1 with `WarnStuckClaimState`.
- The residual terminal configuration contains `<k> 2 ~> .K </k>`, which
  fails to unify with destination 3.

This is an expected unmet result obligation, not a parse error, missing import,
timeout, or unrelated crash.

As a separate body-sensitivity check,
[spec-body-sensitivity.k](evidence/spec-body-sensitivity.k) changes the
actually invoked closure's `count += 1` to `count += 2` and keeps the original
`n=78 -> 2` postcondition.

- Body-mutation dry-run/compilation: exit 0.
- Body-mutation proof: exit 1 with `WarnStuckClaimState`.
- The residual terminal result is 4.

Thus the fixed claims are non-vacuous and depend on both their result and the
program term. Commands, exit statuses, and bounded residuals are in
[06-non-vacuity.log](evidence/06-non-vacuity.log).

## 7. Proven versus assumed accounting

### What successful reachability establishes

Conditional on the trusted K toolchain and supplied semantics:

1. For every matching inner-loop state with `X>=0`, if the translated inner
   loop reaches its continuation, it preserves the framed state, sets `x=0`,
   and changes `count` to the recursively defined decimal-seven count.
2. From the exact pristine configurations, the real submitted closure returns
   0 at `n=-5,0,50`, 2 at `n=78`, and 3 at `n=79,100`.
3. The reviewer connection check establishes that the hardcoded constructor
   macro in those claims is exactly the trusted-regenerated submitted function
   body and binding.

It does **not** establish:

- `fizz_buzz(N) = fizzBuzzSpec(N)` for arbitrary `N`;
- the correctness of the outer loop for arbitrary `N`;
- equivalence to the canonical implementation over the full `int` domain; or
- a general source-contract theorem inferred from finite differential tests.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K `v7.1.293`, Haskell backend, `kore-exec`, SMT/builtin integer/Boolean/map/list theory | All machine-checked results | Necessary foundational trust |
| Supplied reference semantics | Binding, evaluation, control, state, calls/returns | Required benchmark boundary; integrity exact; material used path statically reviewed |
| Trusted `py2mpy.py` | Source-to-constructor translation | Byte-identity regeneration plus constructor-level pinning |
| `countSevensAcc` equations | Inner helper postcondition | Defined and reviewed, not opaque |
| Unused supplied opaque float/sort/MD5 symbols | None | Explicit but inert for this program/proof |
| Python differential test | Implementation/canonical bridge on 1,488 values | Finite empirical support only |
| Human interpretation of decimal digit counting | Meaning of the recursive summary | Supported by truthful equations and tests for the inner loop; no universal outer theorem |
| Termination | Reachability interpretation | The requested result is partial correctness; no independent total-correctness claim is credited |

Gate A passes for the limited formal claims: they reconstruct, execute the real
program term, constrain results, and reject false/body mutations. Gate B fails:
the entry theorem materially narrows an unrestricted contract to six constants.
The evidence is reproducible, but Gate C evidence cannot turn finite examples
into the missing universal theorem.

The candidate therefore represents sound partial progress, not the requested
partial-correctness proof of the full generated program contract. The benchmark
explicitly maps this material `SOUND-BUT-LIMITED` domain narrowing to
`FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
