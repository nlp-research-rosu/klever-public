# Independent adversarial review: 138-is-equal-to-sum-even

The candidate contains a legitimate partial-correctness proof for the intended
integer domain. I rebuilt the generated semantics and proof from source, ran
the six positive claims independently, checked the executed constructor term
against trusted regeneration, audited every local rule, and rejected two
fresh false mutations for the expected proof obligations.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: legacy-selected-stage1`,
condition `bare`, and `semantics_mode: GENERATED_SEMANTICS`. The mode boundary
is intact: `/reference/reference-semantics` does not exist, and the candidate
does not contain a `reference-semantics` tree. No hidden or inferred reference
semantics was used.

I read and parsed all records required for this layout:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- all 138 JSONL events in the structured trace, including all 25 recorded
  custom tool calls;
- the present legacy records `legacy-metrics.json` and
  `legacy-run-input.json`.

Historical `runtime-metrics.json` is absent, which is permitted for this
legacy-selected layout and was not reconstructed. The historical success
marker and old `#Top` outputs were not relied upon.

The campaign lock is byte-hashed to
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching `/audit-input.json`, and its parsed object exactly equals the embedded
`audit_campaign` block. Every declared regular-file hash matched, including
the canonical source, prompt, translator, run/task/result manifests,
invocation, metrics, usage, transcript, last message, prompt, and the sole
trace JSONL file. The candidate prompt and translator are byte-identical to
their trusted mounts. Required records and proof artifacts are real regular
files or real directories; there are no symlinks.

For clarity, the aggregate `candidate_tree_sha256` and
`generation_codex_trace_sha256` strings in `/audit-input.json` are not in the
same digest representation as the installed pipeline's `sha256_tree`
function. Independent pipeline digests are
`fd6a4ab61c74ce3e776a94b44475898037ecba786c9b70ce0f5d017d1b554ae7`
for `/candidate` and
`1964b9c43b785ee099356c884301429a1fad82a1dee39268b810da1ec3259395`
for the trace. Those values exactly match, respectively, the generation
invocation's retained workspace digest and `usage.json`'s source-trace
digest. Together with all matching constituent hashes and the symlink check,
this establishes mounted-byte integrity without assuming two differently
represented aggregate fields are interchangeable.

Evidence:
[provenance-check.log](evidence/provenance-check.log),
[generation-records-review.log](evidence/generation-records-review.log), and
[static-source-inventory.log](evidence/static-source-inventory.log).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks whether integer-valued `n` can be expressed as the sum
of exactly four positive even integers. Such a sum is necessarily even and at
least `2 + 2 + 2 + 2 = 8`. Conversely, every even `n >= 8` has the explicit
decomposition `(n - 6) + 2 + 2 + 2`. Thus the contract is exactly:

```text
n >= 8 and n is even
```

The trusted canonical implementation is `n % 2 == 0 and n >= 8`.
`solution.py` uses the equivalent order `n >= 8 and n % 2 == 0`. Both
operands are pure for the intended integer domain, so reordering does not
alter a result, state, exception, or control effect.

I regenerated `solution.mpy` with the trusted mounted translator in scratch.
The regenerated and submitted files are byte-identical, both with SHA-256
`4be6b3778909ca1c91506046bb2f1925cb4f689dad0162b5f8faa007e84eee8d`.

An independent differential script imported both entry points. It tested the
three documented examples, threshold and parity boundaries, negative and zero
values, 30- and 100-digit integers, and 500 deterministic generated integers:
520 distinct inputs, zero mismatches. A separate brute-force enumeration of
four positive even summands for every integer in `[-20, 80]` also had zero
mismatches against both implementations. There is no meaningful "empty"
integer case.

Evidence:
[regeneration.log](evidence/regeneration.log),
[differential_test.py](evidence/differential_test.py), and
[differential-test.log](evidence/differential-test.log).

## 3. Clean proof reconstruction

I copied source artifacts to `/tmp/audit-work/138-audit/scratch`, removed the
copied Python bytecode cache, and did not copy or use a candidate-built K
definition. K version 7.1.293 was used.

The generated semantics was freshly built with:

```text
kompile semantic.k --backend haskell --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-semantic-kompiled
```

It exited 0. Thirteen fresh `krun` executions covered negative values, zero,
`4`, `6`, both sides of the `8` threshold, odd/even values above it, ordinary
positive values, and 30-digit integers. Every run exited 0 and matched the
trusted canonical and generated Python implementations.

The proof definition was freshly built with:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
```

It exited 0. The unmodified original `spec.k` then printed `#Top` and exited
0. Because the six candidate claims are unlabeled, I mechanically made a copy
that only adds inert labels and changes the spec module name. I selected each
original claim separately with commands of this form:

```text
kprove spec-audit-labeled.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC-AUDIT-LABELED \
  --claims SPEC-AUDIT-LABELED.audit-claim-N
```

For every `N` from 1 through 6, the command printed `#Top` and exited 0.

Evidence:
[semantic-build.log](evidence/semantic-build.log),
[concrete-semantics.log](evidence/concrete-semantics.log),
[verification-build.log](evidence/verification-build.log),
[positive-original-spec.log](evidence/positive-original-spec.log),
[spec-audit-labeled.k](evidence/spec-audit-labeled.k), and
`positive-claim-1.log` through `positive-claim-6.log` in
[evidence](evidence/).

## 4. Adequacy and real-program pinning

The claims state the following:

1. With no additional precondition, for every K `Int N`, executing the
   submitted body returns
   `BoolValue(sumFourPositiveEvens(N))`.
2. If `A`, `B`, `C`, and `D` are arbitrary positive even K integers, executing
   the submitted body at their sum returns `BoolValue(true)`.
3. If `sumFourPositiveEvens(N)` is true, the proof-local checker establishes
   that `(N - 6, 2, 2, 2)` are positive even integers whose sum is `N`.
4. The three remaining claims prove the documented results at `4`, `6`, and
   `8`.

The third claim is an arithmetic intent lemma, not a purported source helper
or substituted program. The other five claims execute a complete `Module`
term. A quote-aware layout normalization mechanically compared every one of
those five terms with trusted-regenerated `solution.mpy`; all five constructor
trees are identical. The semantics' entry rule matches the exact function
name, binds its actual parameter name, and recursively evaluates the matched
body `E`; the result is not fresh or unconstrained.

The entry harness models calling the named HumanEval entry point with the
integer in `<input>`. This is a small, explicit call harness rather than a
model of Python module import side effects. It is adequate here because the
submitted module contains exactly that one function, the binding is pinned by
name and shape, and the rule evaluates rather than summarizes its body.

Body sensitivity was checked independently of postcondition non-vacuity. I
changed `Int(8)` to `Int(10)` in the program term actually executed by a copy
of the universal claim while retaining the original threshold-8 obligation.
The mutated spec dry-ran successfully, but `kprove` exited 1 with
`WarnStuckClaimState` on the false equivalence between the threshold-8 and
threshold-10 results. `N = 8` is a concrete counterexample.

All preconditions are satisfiable. Examples include `N = 8` for the universal
and witness claims, and `A = B = C = D = 2` for the four-summand claim. At
`N = 8`, `10`, and `20`, the explicit witnesses are valid and both Python
implementations return true. Fresh K execution agrees at the same relevant
inputs.

Evidence:
[pinning-check.log](evidence/pinning-check.log),
[precondition-witnesses.log](evidence/precondition-witnesses.log),
[spec-body-mutation.k](evidence/spec-body-mutation.k),
[body-mutation-dry-run.log](evidence/body-mutation-dry-run.log), and
[body-mutation-proof.log](evidence/body-mutation-proof.log).

## 5. Rule-by-rule static soundness review

The complete local inventory is preserved in
[rule-inventory.md](evidence/rule-inventory.md). There are no additional
candidate helper K files.

### Syntax, configuration, and used-construct coverage

`semantic.k` locally declares:

- `Program`: `Module(Stmt)`;
- `Stmt`: `FuncDef(String, Params, Stmt)` and `Return(Expr)`;
- `Params`: one `String`;
- `Expr`: `Name`, `Int`, binary operation, Boolean operation, and comparison;
- `CmpOp`: an operator string and right expression;
- values `IntValue` and `BoolValue`, plus `noResult`;
- `<k>`, `<input>`, and `<result>` cells inside `<mpy>`.

Every constructor in submitted `solution.mpy` maps to one of these
declarations: `Module`, `FuncDef`, `Params`, `Return`, `BoolOp("and",...)`,
two `Compare` terms, `Name`, `Int`, `BinOp("%",...)`, and `CmpOp` with
`">="` or `"=="`.

### The ten local semantic rules

1. The entry rule consumes the exact named one-function module, reads
   `<input>`, evaluates its matched return expression, and writes only
   `<result>`.
2. A matching parameter `Name(X)` evaluates to the input `N`.
3. `Int(I)` evaluates to `IntValue(I)`.
4. `BinOp` recursively evaluates both operands and delegates by operator.
5. `%` on two integer values delegates to `%Int` when the divisor is nonzero.
6. `Compare` recursively evaluates both sides and delegates by operator.
7. Integer `>=` delegates to `>=Int`.
8. Integer equality delegates to `==Int`.
9. `BoolOp` recursively evaluates both operands and delegates by operator.
10. Boolean `and` delegates to `andBool`.

The four evaluator symbols are `[function]` but deliberately not `[total]`.
Unsupported syntax, wrong types, unbound names, unknown operator strings, and
zero divisors therefore remain stuck instead of receiving fabricated
behavior. The submitted program exercises none of those gaps: its only divisor
is the constant `2`, every name is the sole parameter, and every operator has
an exact rule.

The evaluator is eager while Python `and` is short-circuiting. For this exact
body, the right operand is a pure integer modulo/equality expression with a
nonzero constant divisor. It cannot mutate state, allocate, return abruptly,
or raise on any K `Int`. Even if `%Int` and Python choose different signed
remainders on a negative odd integer, equality to zero agrees; moreover, the
left comparison is false there. Thus eagerness has no observable semantic
effect on the submitted program. No broader Python-semantics claim is made.

### The three verification extensions

1. `sumFourPositiveEvens(Int) [function,total]` has one unconditional,
   exhaustive, nonrecursive equation to
   `N >= 8 and N % 2 == 0`.
2. `canonicalWitnessesAreValid(Int) [function,total]` has one unconditional,
   exhaustive, nonrecursive equation spelling out positivity, evenness, and
   sum equality for `(N - 6, 2, 2, 2)`.
3. `checkCanonicalWitnesses(Int)` has one proof-local operational rule that
   evaluates the preceding defined predicate into `<result>`. It does not
   match or preempt any submitted-program term and changes no other state.

The two total functions have complete coverage and no overlapping equations.
The checker does not return `true` unconditionally; the prover must establish
the explicit arithmetic predicate from the claim's characterization
precondition. These are definitions and a proof-local arithmetic checker, not
opaque oracles or operational bridges over source execution.

There are no local simplification rules, priorities, `owise` equations,
`functional` declarations, opaque symbols, fresh result values, recursive
equations, loop circularities, or overlaps. No local rule was found unsound,
so there is no asserted unsoundness requiring a false-conclusion witness.

## 6. Fresh non-vacuity test

I created a fresh result mutation, independent of the body-sensitivity test.
It executes the exact submitted constructor term for arbitrary `N:Int` but
demands `BoolValue(true)` for every input. `N = 4` satisfies the initial
pattern and is a concrete false case: fresh K execution and both Python
implementations return false.

The mutated artifact built successfully under `kprove --dry-run` with exit 0.
The actual proof exited 1 with `WarnStuckClaimState`; the residual is the unmet
condition that `N >= 8` and `N % 2 == 0` would have to be true universally.
This is the expected result-constraining failure, not a parser error, timeout,
missing import, or unrelated crash.

Evidence:
[spec-vacuity.k](evidence/spec-vacuity.k),
[vacuity-dry-run.log](evidence/vacuity-dry-run.log), and
[vacuity-proof.log](evidence/vacuity-proof.log).

## 7. Proven versus assumed accounting

The reconstructed K proof formally establishes, under the submitted generated
semantics:

- for every unbounded K integer `N`, the exact submitted function body returns
  true exactly when `N >= 8` and `N` is divisible by `2`;
- any sum of four arbitrary positive even integers is accepted;
- whenever the characterization is true, the explicit four values
  `(N - 6, 2, 2, 2)` are positive, even, and sum to `N`;
- the documented examples return false, false, and true.

Together, those facts prove the source contract over the intended integer
domain. This is a partial-correctness result in the Kit sense.

The trust and evidence boundary is:

- The prompt, canonical implementation, and translator mounts are trusted
  inputs fixed by the benchmark. Their mounted hashes and candidate copies
  were independently checked.
- The K 7.1.293 parser, Haskell backend, reachability prover, and imported
  `INT`, `BOOL`, and `STRING` primitives are trusted. The proof relies on
  ordinary unbounded-integer arithmetic and Boolean operations from those
  domains.
- The entry harness and ten generated semantic rules are part of the audited
  theory, not silently trusted proof facts. Their complete target-program
  coverage, state footprint, binding, control behavior, and body sensitivity
  were checked above.
- There are no opaque symbols or unconstrained empirical bridges.
  `sumFourPositiveEvens` and `canonicalWitnessesAreValid` are fully defined by
  exhaustive equations.
- Differential and concrete tests are finite supporting evidence for the
  Python-to-generated-semantics bridge only. They are not treated as the
  universal proof.
- Non-integer Python objects and unused Python constructs are outside the
  theorem. This does not materially narrow the stated contract: parity,
  positivity, and sums of positive even numbers define an integer problem, and
  K `Int` is unbounded like Python integers.

The proof is result-constraining, body-sensitive, pins the real regenerated
program, covers the material source-contract domain, and uses no materially
unsound local semantic or proof rule.

VERDICT: PASS
LEGITIMACY: LEGIT
