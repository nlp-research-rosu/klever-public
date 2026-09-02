# Independent adversarial audit: 60-sum-to-n

The candidate has a reproducible, non-vacuous K proof of its submitted program
for `N >= 0`. It does **not** prove or implement the full HumanEval contract,
which declares an `int` input and states no nonnegative precondition. The trusted
canonical implementation returns `0` for negative inputs because
`range(n + 1)` is empty, whereas the submitted formula is nonzero for every
`n <= -2` tested (for example, `sum_to_n(-2)` is `1`). The candidate formalizes
the same exclusion as `requires N >=Int 0`.

This is a materially narrowed source-contract domain. The Kit characterization
is Gate-A-sound but Gate-B-limited; the benchmark's more specific decision rule
maps that limitation to **FAIL / NOT_LEGIT**.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout` `legacy-selected-stage1`,
condition `semantics`, and `semantics_mode` `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the rendered semantics
mode and mounts agree.

I checked the launcher inputs before treating any candidate record as evidence:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  `/generation-result.json`, all required legacy-selected-stage1 generation
  records, the candidate, and all trusted reference inputs are readable.
  `usage.json` is present and was inspected. Historical runtime metrics are not
  required for this layout.
- The parsed campaign-lock object exactly equals the `audit_campaign` block in
  `/audit-input.json`, and its SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every launcher-recorded single-file hash checked in
  [integrity_checks.log](evidence/integrity_checks.log) matches, including the
  run/task/result manifests, invocation, metrics, usage, prompt, complete
  structured-trace file, generation output/last response, canonical source,
  trusted prompt, and translator.
- No symlink exists anywhere below `/candidate`, `/reference`, or
  `/generation-evidence`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts.
- `diff -qr --no-dereference` and independent type/name manifests show that
  candidate `reference-semantics/` has exactly the same entries and bytes as
  `/reference/reference-semantics`: no missing, additional, mistyped, changed,
  or symlinked entry.
- The structured trace has 143 valid JSON records. All records were parsed and
  every function call/action summarized in
  [generation_trace_summary.log](evidence/generation_trace_summary.log). The
  generation report's `#Top` and success marker were treated only as untrusted
  claims.

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt declares `sum_to_n(n: int)` and says it sums the numbers from
1 through `n`; it gives examples for 1, 5, 10, 30, and 100 and gives no
precondition. The trusted canonical body is:

```python
return sum(range(n + 1))
```

Consequently, on Python integers below zero, the canonical result is `0`. The
candidate body is:

```python
return n * (n + 1) // 2
```

Running the trusted translator over the scratch copy exits 0, and the result is
byte-identical to submitted `solution.mpy`; see
[fidelity_checks.log](evidence/fidelity_checks.log).

The independent differential script
[differential_test.py](evidence/differential_test.py) imports both trusted
canonical and candidate entry points. It tests all five documented examples,
boundary values including `-1000, -100, -3, -2, -1, 0, 1, 2, 3, 1000`, every
integer from -50 through 200, and 200 deterministic generated integers in
`[-1000, 5000]`. Its complete input list and outputs are preserved in
[fidelity_checks.log](evidence/fidelity_checks.log).

Result: 446 distinct inputs, 82 mismatches. A minimal decisive witness is:

```text
n = -2
canonical = 0
candidate = 1
```

The formula agrees on the tested nonnegative domain, but the negative-input
divergence is a material implementation/specification disagreement.

## 3. Clean proof reconstruction

I copied only source proof artifacts plus the trusted translator, canonical,
prompt, and trusted semantics into `/tmp/audit-work/reconstruction`. No
candidate definition, cache, `kore-exec.tar.gz`, or other compiled artifact was
copied. The source inventory is
[scratch_source_inventory.log](evidence/scratch_source_inventory.log).

Using K v7.1.293, the following fresh commands were run:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled-audit
# exit 0

krun smoke.mpy --definition runtime-kompiled-audit
# exit 0; .K, NoExc, exit-code 0

kompile verification.k --backend haskell \
  --main-module SUM-TO-N-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled-audit
# exit 0

kprove spec.k --definition verification-kompiled-audit \
  --spec-module SUM-TO-N-SPEC
# exit 0; #Top
```

The complete bounded output, exact command rendering, warnings, and exit
statuses are in [reconstruction.log](evidence/reconstruction.log). There is one
positive target claim, and it closes freshly.

## 4. Adequacy and real-program pinning

### Plain-language claim

The entry precondition fixes the normal initial MPY configuration (module
environment 0, empty module map, builtins parent, empty heap and stack, no
return, no exception, exit code 0) and assumes `N >= 0`.

The postcondition requires:

- the `<k>` result to be `triangular(N)`;
- module loading to have bound `sum_to_n` to the exact submitted closure body;
- environment, scope allocator, heap, heap allocator, stack, return state,
  exception state, and exit code to have the specified final values.

`triangular(N)` is fully defined as the supplied floor-division expression

```text
(N * (N + 1) - pyMod(N * (N + 1), 2)) / 2
```

and is neither fresh nor unconstrained.

### Program identity and execution

[pinning_and_witnesses.log](evidence/pinning_and_witnesses.log) mechanically
extracts the argument of `#loadAll` from `verification.k`, removes only
whitespace/comments outside strings, and compares it with regenerated
`solution.mpy`. The constructor trees match exactly:

```text
Module(FuncDef("sum_to_n",Params("n"),
  Return(BinOp("//",BinOp("*",Name("n"),
  BinOp("+",Name("n"),Int(1))),Int(2)))))
```

The entry wrapper then performs an ordinary `Call` through the supplied
semantics. It does not replace the body with a result summary. There are no
helper or loop claims; the program is loop-free.

`N = 0` is an explicit satisfying state. Substitution at
`N = 0, 1, 2, 5, 30, 100` gives equal canonical, generated-Python, and claimed
results, as recorded in [pinning_and_witnesses.log](evidence/pinning_and_witnesses.log).

For body sensitivity, I changed the **executed K body** from `n * (n + 1) // 2`
to `n * (n + 2) // 2`, including the closure expected in the post-state, while
leaving the triangular result obligation unchanged. The mutated definition
builds (exit 0), but its proof exits 1 with a stuck residual comparing the two
different expressions. `N = 2` is a concrete witness: mutated result 4 versus
required result 3. Artifacts and output are
[verification-body-mutation.k](evidence/verification-body-mutation.k),
[spec-body-mutation.k](evidence/spec-body-mutation.k), and
[body_mutation.log](evidence/body_mutation.log).

### Fatal adequacy failure

The exact program is pinned, but the entry claim assumes `N >= 0`. Neither the
prompt nor Python type annotation imposes that restriction. The canonical
implementation defines the omitted negative cases, and the candidate disagrees
on them. Thus the theorem is about the submitted program only on a materially
narrowed subset, not about the real generated program over the full source
contract.

## 5. Rule-by-rule static soundness review

The exhaustive inventory in [rule_inventory.md](evidence/rule_inventory.md)
reproduces every top-level declaration with its source line span: 229 syntax
declarations, one configuration, 5 contexts, 697 rules, and the sole claim,
across `semantics.k`, every supplied helper K file, `verification.k`, and
`spec.k`. The generation script and command record are
[build_rule_inventory.py](evidence/build_rule_inventory.py) and
[rule_inventory_command.log](evidence/rule_inventory_command.log).

Every inventory entry falls into one of these reviewed classes:

1. **Executed fixed-semantics path.** The submitted term uses only `Module`,
   `FuncDef`, `Params`, `Return`, `BinOp`, `Name`, `Int`, and `Call`. Their
   declarations and active rules are:

   - syntax declarations in `syntax.k` for those constructors, including
     `BinOp`'s `seqstrict(2,3)` and strict return evaluation;
   - `core.k` configuration, `#loadAll`, statement sequencing, integer
     literals, name lookup, and left-to-right argument evaluation;
   - `functions.k` function binding, parameter binding, return, and frame pop;
   - `call.k` callee evaluation, argument evaluation, closure dispatch, frame
     allocation, and continuation restoration;
   - `operators.k` value dispatch; and
   - `int.k` rules for `+`, `*`, `//`, and `pyMod`.

   Constructor-to-rule matches, priorities, total declarations, and exact
   source lines are collected in
   [static_review_checks.log](evidence/static_review_checks.log). Evaluation is
   left-to-right; lookup selects the module closure then local `n`; the call
   creates one scope and stack frame; return restores and deletes it; no heap
   allocation or exception is possible on this path. The divisor is the fixed
   nonzero integer 2. The `pyMod`/division expression is Python floor division
   for that divisor. The rules agree with Python and ordinary integer
   mathematics on every claim state. No overlap or priority introduces an
   alternative result.

2. **Candidate-local extensions.**

   - `#runSumToN(N)`: an entry constructor that expands to the exact submitted
     `Module` followed by its ordinary call. It reads or writes no cell itself
     and is not an operational bridge over program-defined execution.
   - `triangular(N)`: a definitional summary with one unconditional,
     exhaustive, descending-free equation. It is exactly the same fixed
     divisor-2 floor-division expression used by the program. It is
     result-bearing but not opaque, has no overlapping equations, and does not
     encode a result independently of execution.
   - `SUM-TO-N-SPEC`'s one claim: the only claim in the entire audited source
     set. There are no proof-local priority rules, simplification rules,
     auxiliary claims, opaque functions, or call interceptions.

   The body mutation and false-postcondition mutation independently confirm
   that these extensions neither bypass body execution nor make arbitrary
   results provable.

3. **Unexercised fixed-semantics declarations/rules.** Every remaining supplied
   rule is for a constructor, value sort, method, control form, collection,
   float, string, range, comprehension, assertion, sorting, dictionary, or
   builtin that cannot occur in this submitted constructor tree. The recursive
   task-symbol search finds `sum_to_n`, `triangular`, and `runSumToN` only in
   `verification.k`/`spec.k`; no supplied rule encodes this task's answer.
   These fixed rules contribute no rewrite, branch condition, state change, or
   result to the target claim.

The supplied semantics contains explicitly opaque or concrete-only primitives
for symbolic floats (`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
and `sqrtF`), symbolic sorting (`sortVS`, `sortKeyVS`), and MD5
(`md5hexCodes`), as well as totalized unused access helpers such as
`valSeqAt`. They are part of the exact trusted supplied baseline, are listed
in the inventory/static log, and have no dependency path to this integer-only
claim. They therefore do not smuggle or support the candidate conclusion.

I found no materially unsound proof-local or used fixed-semantics rule, so
there is no unsound-rule allegation requiring a false-conclusion witness. The
candidate defect is the explicit domain restriction, not a false K rewrite.

## 6. Fresh non-vacuity test

I created [spec-vacuity-audit.k](evidence/spec-vacuity-audit.k) independently;
no candidate vacuity artifact was used. It changes the result obligation to:

```k
<k> #runSumToN(N) => triangular(N) +Int 1 </k>
```

`N = 0` satisfies the precondition and witnesses falsity: the program result is
0 while the mutated target is 1.

The mutation's `kprove --dry-run` exits 0 and emits a KORE claim, proving that
the test is well formed and builds against the fresh definition. The live
`kprove` exits 1 with `WarnStuckClaimState`; the residual contains the expected
failed equality between the actual triangular expression and that expression
plus 1. Exact commands, hash/size of dry-run output, statuses, and residual are
in [vacuity_mutation.log](evidence/vacuity_mutation.log). This is a meaningful
proof failure, not a parser error, timeout, missing import, or unrelated crash.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Conditional on the supplied MPY semantics and K's builtin integer theory, for
every K integer `N >= 0` in the claim's explicit initial configuration, the
exact submitted module loads, the exact submitted `sum_to_n` closure is called,
and if execution terminates it returns the divisor-2 floor expression denoted
by `triangular(N)`, with the asserted final cells. This is a sound,
result-constraining partial-correctness theorem about the exact candidate
program on the restricted domain.

It does **not** establish correct behavior for negative integers and does not
establish the HumanEval contract over all annotated inputs. In fact, finite
execution demonstrates that the candidate is wrong there.

### Trust and evidence ledger

- **Trusted prompt and canonical source.** These define the intended contract
  and oracle. They are launcher-hash verified.
- **Trusted translator.** Its use is a syntactic bridge from `solution.py` to
  `solution.mpy`; fresh regeneration is byte-identical.
- **Supplied MPY semantics.** Its exact-tree integrity is verified. The used
  integer/call/function subset is statically reviewed and freshly executed.
  This is the primary semantic trust boundary.
- **K v7.1.293 backend, builtin `Int`, `%Int`, `/Int`, maps/lists, and SMT
  reasoning.** These are toolchain primitives assumed by `kompile`, `krun`, and
  `kprove`.
- **Closed-form-to-sum mathematics.** For nonnegative `n`,
  `n(n+1)/2 = 1 + ... + n` is ordinary mathematics, not a separate K theorem
  in this candidate. Concrete comparison supports it on the recorded inputs
  but finite tests are not substituted for the K execution proof.
- **Unexercised opaque supplied primitives.** Listed in Stage 5; none affects
  the claim's value, control, state, exception, or postcondition.
- **Differential evidence.** It supports the Python implementation/canonical
  bridge only on 446 recorded inputs. Crucially, it supplies concrete
  counterexamples to full-domain correctness.

Gate A (real-program soundness for the stated theorem) passes. Gate B (intent
adequacy) fails because `N >= 0` materially narrows the unrestricted `int`
contract and hides actual candidate/canonical divergence. Gate C
(reproducibility and trust accounting) passes. The Kit result is therefore
sound-but-limited; under the benchmark's explicit mapping for material
HumanEval domain narrowing, the candidate is not legitimate.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
