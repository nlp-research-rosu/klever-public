# Independent adversarial audit: `31-is-prime`

## Headline

**FAIL / NOT_LEGIT.** The candidate's claims do reconstruct to `#Top` under its
own freshly compiled K theory, the result is non-vacuously constrained, and the
claim term matches the submitted MPY term. However, that theory is materially
unsound as a semantics of the real generated Python program over the claim's
universal integer domain. Its return-call rule implements unbounded,
stack-free tail-call optimization. CPython does not. For two satisfying inputs,
the real submitted `solution.py` raises `RecursionError`, while the rebuilt
proof-free K semantics fabricates normal Boolean returns. This is a concrete
wrong-control/wrong-exception witness, not a timeout, infrastructure
uncertainty, or merely thin evidence.

The audit used K v7.1.293 and Python 3.10.12. All executable sources were copied
to `/tmp/audit-work/candidate-src`; trusted Python inputs were copied to
`/tmp/audit-work/trusted`. Candidate compiled definitions and caches were never
used.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent (including as a symlink), exactly as
required. The trusted mount contains only the three expected regular files:
`canonical.py`, `prompt.py`, and `py2mpy.py`. There is no mode/mount
contradiction and hence no infrastructure breach. See
[`01_mode_and_inventory.log`](evidence/01_mode_and_inventory.log).

### Candidate artifacts and untrusted claims

The following required candidate artifacts are present as regular, non-symlink
files: `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`,
`semantic.k`, `verification.k`, `spec.k`, and `prove.sh`. One structured JSONL
trace is present as a regular file. Hashes, sizes, and type checks are recorded
in [`03_provenance_integrity.log`](evidence/03_provenance_integrity.log).
There are no missing, mistyped, or symlinked required artifacts.

The candidate also contains `semantic-kompiled/`,
`verification-kompiled/`, and `__pycache__/`. These are extra derived/cache
artifacts, not integrity failures; they were deliberately excluded from the
scratch copy and never trusted. No candidate `PROOF.md` or `spec-vacuity.k` is
present, but neither was a required generation deliverable.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`; both
`cmp` checks exited 0. The untrusted run metadata identifies problem
`31-is-prime`, condition `bare`, and the same prompt/translator hashes. The
candidate's final report claims that its tests passed and its proof printed
`#Top`. Those statements were treated only as claims. The bounded initial
inspection is in [`04_untrusted_claims.log`](evidence/04_untrusted_claims.log);
the full generation log and structured trace were searched end-to-end for
commands, proof results, and errors in
[`23_full_untrusted_log_review.log`](evidence/23_full_untrusted_log_review.log).

The clean source-copy command and copied-file sizes are in
[`02_scratch_copy.log`](evidence/02_scratch_copy.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language and canonical contract

The trusted prompt says that `is_prime(n)` must return true when the given
number is prime and false otherwise. Its examples cover composites, primes,
and `1`. The trusted canonical implementation has this behavior for integer
inputs:

1. return `False` for `n < 2`;
2. test every integer `k` in `range(2, n - 1)`;
3. return `False` upon a divisor and `True` if none is found.

For integers, any composite `n >= 2` has a proper divisor in that tested range,
so this implements the stated primality predicate. The intended domain is the
integer domain exercised by the canonical use of `range`, and the formal K
entry claim is even broader syntactically: it has no precondition beyond
`N:Int`.

The submitted implementation uses a different, ordinarily valid algorithm:
`no_divisor(n,d)` tests divisors from 2 through the square-root boundary by
recursion. If it returns normally, this agrees with the canonical algorithm.
The operational fact that CPython recursion is bounded is material below.

### Translation identity

I regenerated `solution.mpy` from the scratch copy of `solution.py` with the
trusted translator:

```text
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/candidate-src/solution.regenerated.mpy
```

`cmp` exited 0, and both MPY files have SHA-256
`00b29828350d9010ed35873d1f9bea77917fb78d7e196128343103f6806c7bff`.
See [`05_translation_identity.log`](evidence/05_translation_identity.log).

### Independent differential test

[`differential_test.py`](evidence/differential_test.py) independently imports
the scratch copy of the trusted canonical entry point and the scratch copy of
the submitted generated entry point. Its final scope is:

- all integers from -250 through 2000;
- every documented example;
- explicit boundaries around `n < 2`, perfect squares, divisor and no-divisor
  branches;
- 512 deterministic pseudorandom integers in [-5000, 20000], seed 310031;
- the empty argument list as an arity-boundary case;
- two recursion/control boundaries: 1,000,003 and 1,022,117.

After deduplication it exercised 2,708 integer inputs. The empty call produced
`TypeError` in both implementations. The integer run found exactly two
mismatches and exited 1:

| Input | Trusted canonical | Submitted `solution.py` |
|---:|---|---|
| 1,000,003 | returns `True` | raises `RecursionError` |
| 1,022,117 = 1009 × 1013 | returns `False` | raises `RecursionError` |

The complete generated input list, outcomes, and exact command are in
[`15_differential_with_recursion_boundary.log`](evidence/15_differential_with_recursion_boundary.log).
A concise reproduction, including the runtime recursion limit of 1000, is in
[`recursion_witness.py`](evidence/recursion_witness.py) and
[`22_recursion_witness_python.log`](evidence/22_recursion_witness_python.log).
This is a material intended-domain divergence: the submitted function does not
return the required Boolean at those inputs.

## 3. Clean proof reconstruction

### Fresh builds

Only copied source files were used. The following definitions were created
under new scratch names:

| Action | Evidence | Result |
|---|---|---|
| Compile `semantic.k` with LLVM as `semantic-kompiled-clean` | [`07_compile_semantic_llvm.log`](evidence/07_compile_semantic_llvm.log) | exit 0 |
| Compile `verification.k` with Haskell as `verification-kompiled-clean` | [`09_compile_verification_haskell.log`](evidence/09_compile_verification_haskell.log) | exit 0 |

The toolchain/version record is
[`00_toolchain.log`](evidence/00_toolchain.log). No candidate-provided compiled
definition, cache, `allRules.txt`, or backend binary was reused.

### Concrete generated-semantics execution

[`concrete_compare.sh`](evidence/concrete_compare.sh) ran the submitted MPY
file with the proof-free LLVM definition and compared each result with both
Python implementations. Inputs were
`-1,0,1,2,3,4,6,8,9,15,16,25,31,49,101,13441`. All 16 normal and branch
boundary cases matched and every `krun` exited 0; see
[`08_concrete_compare.log`](evidence/08_concrete_compare.log).

The same proof-free definition was then run on the two recursion witnesses. It
exited 0 and produced:

```text
N=1000003  -> Bool(true)
N=1022117  -> Bool(false)
```

See [`16_k_recursion_gap.log`](evidence/16_k_recursion_gap.log). Juxtaposed
with the real-Python exceptions in stage 2, these are direct semantic
counterexamples.

### Positive claims

The submitted spec has two positive claims. Fresh runs produced:

| Invocation | Result |
|---|---|
| `kprove ... --claims helper-correct` | `#Top`, exit 0 ([`10_kprove_helper.log`](evidence/10_kprove_helper.log)) |
| unfiltered `kprove spec.k ... --spec-module SPEC` | `#Top`, exit 0; both submitted claims are proved together ([`12_kprove_all.log`](evidence/12_kprove_all.log)) |

For completeness I also ran an entry-only claim filter. It exited 1 after
symbolically unrolling to `d=17` because selecting only the entry claim removes
the helper circularity on which it depends; the backend then cannot decide the
ever-growing symbolic remainder condition. That diagnostic is preserved in
[`11_kprove_entry.log`](evidence/11_kprove_entry.log). It is not the
dependency-preserving submitted proof: the unfiltered proof set closes both
claims. Thus the clean K reconstruction succeeds as a statement *within the
candidate's theory*. It does not validate that theory as Python semantics.

## 4. Adequacy and real-program pinning

### Claims in plain language

`helper-correct` has precondition `N >= 2` and `D >= 2`. The function map must
contain the exact stored `no_divisor` body, but may contain other entries; the
initial environment and result are arbitrary. It claims that invoking the
helper consumes the computation and leaves result
`Bool(noDivisor(N,D))`. The final environment is existential and therefore
unconstrained.

`is-prime-correct` has no `requires` clause, so it covers every K integer. It
starts with the exact program term followed by an invocation of
`is_prime(N)`, empty function/environment maps, and initial
`Bool(false)`. It claims that computation is consumed, the exact two function
definitions are installed, and the final result is `Bool(prime(N))`. Only the
final environment is existential.

These are result-constraining claims. `prime(N)` is not a free variable:
`verification.k` exhaustively defines it as false below 2 and as
`noDivisor(N,2)` otherwise. Likewise, `noDivisor` is fixed by three disjoint
equations.

### Satisfying states and concrete substitution

An entry state with `N=31`, empty maps, empty environment, and initial
`Bool(false)` satisfies the universal entry precondition. A helper state with
`N=31`, `D=2`, the exact helper binding, empty environment, and any initial
result satisfies both helper inequalities. An independently authored ground
spec also checks the composite entry state `N=4`.

All three ground claims closed with `#Top`:

- `is_prime(31)` reaches `Bool(true)`;
- `is_prime(4)` reaches `Bool(false)`;
- `no_divisor(31,2)` reaches `Bool(true)`.

The spec is [`ground-witness.k`](evidence/ground-witness.k), and the result is
[`14_ground_witness_proof.log`](evidence/14_ground_witness_proof.log). Both
Python implementations return the same values for 31 and 4.

At `N=1,000,003`, however, formal substitution gives
`Bool(prime(1000003)) = Bool(true)`, and the rebuilt K semantics indeed returns
that value. The trusted canonical returns `True`; the actual submitted
implementation raises `RecursionError`. This state also satisfies the entry
precondition. It is the concrete adequacy failure.

### Program pinning

The `<k>` cell uses `solutionProgram()`, whose defining equation expands to the
same constructor tree as the regenerated, byte-identical submitted
`solution.mpy`. The two function-summary equations likewise contain the exact
parameter lists and bodies. The proof therefore does not substitute a
different source body, and the operational rules execute those bodies. The
numbered sources supporting this constructor-by-constructor check are in
[`17_numbered_sources.log`](evidence/17_numbered_sources.log).

This current-file identity does not cure the semantics error. It proves the
right syntax tree under the wrong recursive-call model.

## 5. Rule-by-rule static soundness review

The exhaustive declaration/rule inventory is
[`rule_inventory.md`](evidence/rule_inventory.md). It enumerates:

- every syntax production in `MPY-SYNTAX` and `SEMANTIC`;
- the complete four-cell configuration;
- all 27 local semantic rules;
- every local `[function]` declaration;
- the sole priority rule;
- every declaration and all eight equations in `verification.k`;
- both reachability claims;
- construct-to-declaration/rule coverage for every constructor in
  `solution.mpy`.

There are no local `[total]`, `[functional]`, `[simplification]`, or
`[concrete]` declarations and no opaque symbols. Every used constructor has
syntax and an operational path. Missing behavior for unused Python constructs
was not treated as a defect.

Most of the intentionally small semantics is sound on the submitted flow:
module/function loading is ordered; maps bind the exact unique parameters;
guards select the correct branches; positive-divisor `%Int` agrees with
Python; arbitrary-precision integer arithmetic agrees with Python integers;
and all actual expressions are pure, making the functional evaluation scheme
observationally harmless. The K definition of `D dividesInt N` is exactly
`(N %Int D) ==Int 0`; the relevant installed built-in source is captured in
[`18_builtin_integer_contract.log`](evidence/18_builtin_integer_contract.log).

The proof-local equations are also not answer-smuggling shortcuts.
`solutionProgram()` and the two function names only expand concrete syntax.
`noDivisor` and `prime` are result-bearing mathematical summaries, but program
execution is connected to them by the recursive helper claim rather than by an
operational oracle. Their guards are pairwise disjoint and exhaustive over
their uses, and the helper recursion strictly advances `D` on its formal
domain.

### Materially unsound operational rule and false-conclusion witness

The unsound rule is `semantic.k:73–74`, together with the stackless
configuration and invocation rule:

```text
<k> Return(Call(Name(F), ES)) ~> KREST </k>
<env> RHO </env>
  =>
<k> #invoke(F, #evalArgs(ES,RHO)) </k>
```

It has priority 40 over the general return rule. Its complete matched context
accepts any remaining K continuation, reads the current environment, evaluates
the pure submitted arguments, discards the entire continuation, selects the
function-map binding through `#invoke`, overwrites the environment with the
callee binding, and has no stack/depth/exception cell. For a mathematical
tail-call language that would be a valid tail jump. It is not CPython call
behavior: CPython creates a frame even in syntactic tail position and raises
`RecursionError` when the configured depth is exceeded.

Concrete false-conclusion witnesses on the intended and formal domains:

1. `N=1,000,003` is accepted by the entry claim. The repeated rule concludes a
   normal `Bool(true)` final state. The submitted Python instead raises
   `RecursionError`; the trusted canonical returns `True`.
2. `N=1,022,117` is accepted by the entry claim. The repeated rule concludes a
   normal `Bool(false)` final state. The submitted Python instead raises
   `RecursionError`; the trusted canonical returns `False`.

Thus the rule enables normal result conclusions that the real program cannot
reach and suppresses a reachable observable exception. This directly violates
call, control, and exception fidelity. It cannot be excused as an unreachable
case because the entry claim is universal and both witnesses satisfy it. It
also cannot be downgraded to a mere termination omission: the audit contract
requires observable exceptions to be preserved, and the K theory affirmatively
rewrites each call to a normal Boolean completion.

No other local rule was labeled unsound. Narrower limitations—such as only
covering one/two-argument calls and omitting general non-tail calls—stop on
unused constructs and do not fabricate a result for this submitted term.

## 6. Fresh non-vacuity test

No candidate mutation artifact was available or trusted. I authored
[`spec-vacuity.k`](evidence/spec-vacuity.k), fixing the satisfying input
`N=31` but changing the correct final `Bool(true)` obligation to
`Bool(false)`.

The dry run parsed and built the mutation successfully and exited 0; see
[`20_vacuity_dry_run.log`](evidence/20_vacuity_dry_run.log). The actual proof
then exited 1 with `WarnStuckClaimState`. Its residual is a completed
configuration with `.K` and `Bool(true)`, which does not unify with the mutated
`Bool(false)` destination. See
[`21_vacuity_expected_failure.log`](evidence/21_vacuity_expected_failure.log).

This is the expected unmet result obligation, not a parser error, timeout,
missing import, unrelated crash, or unreachable mutation. The K claim is
therefore non-vacuous and discriminating. This stage passes; it does not repair
the stage-5 semantics failure.

## 7. Proven-versus-assumed accounting

### What the successful reachability proof actually establishes

Under the freshly compiled candidate theory—not under real CPython semantics—
the successful unfiltered `kprove` run establishes:

- for all K integers `N >= 2` and `D >= 2`, the modeled invocation of the
  exact helper body reaches `Bool(noDivisor(N,D))`;
- for every K integer `N`, the modeled execution of the exact submitted MPY
  constructor term reaches `Bool(prime(N))`;
- `prime` is the candidate's recursively defined finite-divisor predicate.

The proof is result-constraining and non-vacuous. It proves neither faithful
Python call/exception behavior nor the absence of CPython recursion failure.

### Trust and assumption ledger

| Boundary | Dependents | Status |
|---|---|---|
| K parser, reachability engine, LLVM/Haskell backends | all build/run/proof evidence | Ordinary low-level trusted toolchain boundary; versions and clean commands recorded. |
| Imported K `Int`, `Bool`, `Map`, arithmetic, comparisons, `%Int`, and `dividesInt` | semantic evaluation and mathematical summaries | Acceptable fixed primitive boundary; relevant installed definitions inspected. |
| Trusted CPython-AST translator | source-to-MPY identity | Acceptable trusted input; candidate copy and trusted mount match byte-for-byte, and regeneration matches. |
| Manual equality of `solutionProgram()` and submitted MPY constructors | real-term pinning | Statically checked and supported by direct proof-free execution; no alternate body found. |
| Candidate's generated language semantics as a Python model | every reachability conclusion about `solution.py` | **Illegitimate.** The stack-free tail-call rule suppresses real `RecursionError`, with two concrete satisfying witnesses. |
| `noDivisor`/`prime` as ordinary primality mathematics | natural-language intent | The standard square-root divisor argument is sound but informal rather than separately machine-proved. Finite differential evidence supports only tested inputs. |
| Differential and concrete tests | source/semantic bridge on enumerated values | Empirical only. They expose the counterexample and do not substitute for the K proof or a universal semantics connection theorem. |

There are no opaque or unconstrained result-bearing symbols. The existential
final environment is internal and does not influence the specified return
value. The material trust failure is control/exception semantics, not an oracle
or tautological postcondition.

### Gate and decision summary

- **Real-program soundness (Gate A): FAIL.** Wrong normal-result and exception
  behavior is witnessed at two satisfying inputs.
- **Intent adequacy (Gate B): FAIL.** The submitted Python fails to return the
  required Boolean for those intended integer inputs, and the formal model
  hides that behavior.
- **Trust/evidence auditability (Gate C): PASS.** Commands, statuses, bounded
  outputs, scripts, inputs, mutation, and rule inventory are preserved.
- **Positive K reconstruction:** PASS within the candidate theory.
- **Non-vacuity:** PASS.

The decision boundary requires `FAIL / NOT_LEGIT` when proof success relies on
materially unsound semantics. The concrete witnesses establish exactly that
case.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
