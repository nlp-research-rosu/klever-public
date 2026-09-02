# Independent adversarial audit — HumanEval 49 `modp`

The candidate's `#Top` is reproducible and non-vacuous, and its main claim
mechanically pins the submitted constructor term. It nevertheless is not a
legitimate proof of the full trusted task: the generated implementation differs
from the trusted canonical program at a boundary inside its own claimed domain,
the claim materially restricts the unqualified integer source domain, and the
generated semantics contains an unguarded Python-`pow` bridge with a concrete
false-result witness.

## 1. Input and provenance integrity

Status: **PASS**.

`/audit-input.json` declares `legacy-selected-stage1`,
`GENERATED_SEMANTICS`, condition `bare`, and problem `49-modp`. The mounted
inputs are consistent with that declaration:

- `/reference/reference-semantics` is absent, as generated-semantics mode
  requires.
- `/audit-campaign-lock.json` is a real file, is JSON-equal to the
  `audit_campaign` block, and independently hashes to the recorded
  `ad5dfc...d745`.
- The required legacy-selected records are real, readable files:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace. `usage.json`
  is present and was inspected. The absent `runtime-metrics.json` is expressly
  exempt for this legacy layout.
- All recorded per-file hashes checked by
  [stage1_integrity.py](evidence/stage1_integrity.py) match. Candidate
  `prompt.py` and `py2mpy.py` are byte-identical to their trusted mounts.
  The trusted canonical hash is the recorded
  `3fe6e1...8faf`.
- Recursive `lstat` inspection found only real directories and regular files
  in the candidate and generation-evidence trees—no symlinks or mistyped
  entries.
- The independently reimplemented pipeline tree digest of the mounted
  candidate is `bcc951...8770`, equal to both the invocation's retained
  workspace hash and the generation result's workspace hash. The trace's sole
  JSONL file hashes to `127d11...3971`, matching both generation records; its
  tree digest `8692d5...fb9f` matches `usage.json`.
- All 174 structured trace records parse as JSON. The trace and the 415,587
  byte console log were inspected as untrusted generation history; their
  historical `#Top` was not reused.

The complete check and bounded trace inventory are in
[stage1_integrity.log](evidence/stage1_integrity.log) and
[trace_summary.log](evidence/trace_summary.log). There is no infrastructure
breach.

## 2. Program fidelity and candidate-versus-canonical checks

Status: **FAIL**.

The prompt asks `modp(n: int, p: int)` to return `2^n` modulo `p` and gives
five examples, including the zero-exponent example `(0,101) -> 1`. It states no
input precondition. The trusted canonical starts at `ret = 1`, performs
`ret = (2 * ret) % p` for each element of `range(n)`, and returns `ret`.
Consequently its zero/negative-iteration behavior is part of the executable
trusted reference.

The candidate instead implements:

```python
def modp(n: int, p: int):
    return pow(2, n, p)
```

Using the trusted translator in scratch regenerated `solution.mpy`
byte-for-byte; both files hash to
`a825c9...cf1` ([mpy_regeneration.log](evidence/mpy_regeneration.log)).

The independent differential oracle imported the trusted and generated entry
points separately. It tested all documented examples; loop boundaries around
negative, zero, one, and two iterations; modulus boundaries; all 156 pairs
`0 <= n <= 12, 1 <= p <= 12`; 468 small signed-integer pairs; and 399 unique
deterministic generated pairs (seed 49). Results:

| Scope | Cases | Mismatches |
|---|---:|---:|
| Documented examples | 5 | 0 |
| Branch/boundary cases | 12 | 6 |
| Candidate formal domain grid | 156 | 1 |
| Small annotated-integer grid | 468 | 113 |
| Generated signed-integer inputs | 399 | 26 |

Most importantly, `(n=0,p=1)` satisfies the candidate's own
`N >= 0, P > 0` precondition, yet canonical returns `1` and candidate returns
`0`. Modulus one is not excluded by the prompt. Even granting the candidate's
informal natural-number interpretation, this is a positive-modulus,
nonnegative-exponent boundary divergence. Negative exponents and zero/negative
moduli expose many further result and exception divergences. Full inputs and
outcomes are preserved in
[differential_test.py](evidence/differential_test.py) and
[differential_test.log](evidence/differential_test.log); exit 1 records the
detected mismatch, not a test-infrastructure failure.

## 3. Clean proof reconstruction

Status: **PASS for reconstruction**, but proof closure does not cure Stages 2,
4, and 5.

Only source artifacts were copied to `/tmp/audit-work/fresh`; no candidate
definition or cache was copied. The independently installed toolchain reports K
`v7.1.293`. Fresh commands were:

```text
kompile --backend llvm semantic.k --main-module MODP-SEMANTIC \
  --syntax-module MODP-SYNTAX --output-definition semantic-llvm-kompiled
# exit 0

kompile --backend haskell verification.k --main-module MODP-VERIFICATION \
  --syntax-module MODP-SYNTAX \
  --output-definition verification-haskell-kompiled
# exit 0

kprove spec.k --definition verification-haskell-kompiled \
  --spec-module MODP-SPEC
# #Top, exit 0
```

The builds are recorded in
[build_semantic_llvm.log](evidence/build_semantic_llvm.log) and
[build_verification_haskell.log](evidence/build_verification_haskell.log).
The original six-claim module printed `#Top`. Auditor-created one-claim modules
then ran the general claim and each of the five ground claims separately; every
command printed `#Top` and exited 0
([positive_claims.log](evidence/positive_claims.log)).

Fresh LLVM execution matched generated Python on eight normal/boundary inputs
within `N >= 0, P > 0`, including `(0,1)`: both K and generated Python return
`0`, while canonical returns `1`. Outside the proof guard, the semantics is not
a faithful Python model: at `(2,-5)`, generated and canonical Python both
return `-1`, but K returns `4`; modulus zero did not produce Python's modeled
exception and was bounded at six seconds. See
[concrete_semantics.log](evidence/concrete_semantics.log). That bounded
out-of-domain probe is a semantics finding, not a proof/toolchain failure.

## 4. Adequacy and real-program pinning

Status: **FAIL for source-contract adequacy; PASS for immutable-artifact
pinning and result constraint**.

The general claim says:

- Initial state: the exact constructor program is in `<k>`; `<n>` is arbitrary
  `N`, `<p>` arbitrary `P`, formals/result are uninitialized; and
  `N >= 0`, `P > 0`.
- Final state: `<k>` is empty, formals are `("n","p")`, and the result is
  `expectedModp(N,P)`, defined as K's `2 ^%Int N P`.

The other five entry claims have fixed inputs from the prompt and fixed numeric
results. There are no loop/helper/circularity claims.

The trusted regeneration and a constructor-level parser comparison establish
program identity. `kast` parsed both `solution.mpy` and the first claim's
extracted `<k>` LHS to identical JSON KAST, with equal canonical digest
`f2d2aa...5dde`
([pinning_check.log](evidence/pinning_check.log)). The claim therefore executes
the submitted body, not a separately named summary.

Satisfying states exist. For example, `N=3,P=5` reaches result `3` in K and
both Python implementations. `N=0,P=1` also satisfies the precondition and
reaches K/generated result `0`, but trusted canonical result `1`. Thus the
formal result is constrained but is not the trusted canonical result
throughout the claimed domain.

Body sensitivity also passed: changing the executed constructor from base
`Int(2)` to `Int(3)` at the ground witness `(1,5)`, while retaining expected
result `2`, produced `WarnStuckClaimState` with actual `result(3)`. The
mutation and log are
[spec-body-mutation.k](evidence/spec-body-mutation.k) and
[body_mutation.log](evidence/body_mutation.log).

The formal precondition also materially narrows the source signature, which
only says `int, int`; the canonical has defined return behavior for negative
`n`, negative `p`, and some `p=0` cases. The prompt does not state the
candidate's exclusions. Under the benchmark's mapping, materially narrowing
the HumanEval source-contract domain is not a non-fatal limitation.

## 5. Rule-by-rule static soundness review

Status: **FAIL**.

The exhaustive declaration/rule inventory is preserved in
[rule_inventory.md](evidence/rule_inventory.md), with a mechanical source scan
in [static_inventory_check.log](evidence/static_inventory_check.log).
There are no helper K files. The complete local inventory is:

- Syntax: `Int(Expr)`, `Name(Expr)`, four-field `Call`; two-name `Params`;
  `Return`; `FuncDef`; `Module`; `noFormals`/`formals`; and
  `noResult`/`result`.
- Configuration: `<k>`, integer `<n>` and `<p>`, `<formals>`, and `<result>`
  inside `<modp>`. There is no heap, environment, stack, exception, allocation,
  or I/O cell.
- Functions: `evalInt` and `expectedModp`, both `[function]` and neither
  `[total]`.
- Local rules: four `evalInt` equations, one module/function-entry operational
  rule, one exact-context return rule, and one `expectedModp` equation.
- Claims: one symbolic entry goal and five ground entry goals.
- There are no local `total`, `functional`, opaque, priority, simplification,
  concrete, strict/seqstrict, macro, or anywhere declarations.

Rule assessments:

1. `evalInt(Int(I),...) => I` is a true literal equation.
2. First-formal `Name` lookup is correct for the submitted `"n"`.
3. Second-formal lookup is guarded by distinct formal names, so it does not
   overlap rule 2; it is correct for `"n" != "p"`.
4. `Call(Name("pow"),BASE,EXP,MOD)` recursively evaluates operands and replaces
   the call by K `^%Int`. This is the decisive false bridge. Its rule has no
   `P > 0` guard and no binding/exception guard. Concrete false-conclusion
   witness on the unqualified integer source domain:

   ```text
   input n=2, p=-5
   real generated Python pow(2,2,-5) = -1
   trusted canonical                 = -1
   generated K rule/result           = 4
   ```

   The installed K documentation explains the cause: `^%Int` uses K integer
   remainder semantics, while Python chooses the sign of a negative modulus.
   The documentation and hash are in
   [k_powmod_trust_boundary.log](evidence/k_powmod_trust_boundary.log).
   The rule can therefore enable a false returned result for the actual
   submitted body and an input not excluded by the prompt. Modulus zero is a
   second unmodeled behavior. Textually selecting `"pow"` without an
   environment is also over-broad for shadowing programs, although no such
   shadowing occurs in this submitted body.
5. The module rule treats the sole function definition as the selected entry
   invocation, writes its two formal names, and exposes its body. It matches
   the entire `<k>` cell, not an arbitrary continuation. This bespoke runner is
   adequate for the exact one-function artifact, though it is not ordinary
   Python module-definition behavior.
6. The return rule also matches the entire `<k>` cell, consumes the only
   statement, reads both inputs/formals, and writes the only result. It neither
   discards an admitted continuation nor abstracts other state. It is sound for
   the submitted body conditional on `evalInt`.
7. `expectedModp(N,P) => 2 ^%Int N P` truthfully defines the K-side expected
   value; it does not independently establish Python/canonical meaning.

All syntactic constructs in the regenerated program map to these declarations
and rules. `evalInt` equations are constructor-disjoint; the two name rules are
guard-disjoint; recursion descends through the finite expression tree.
Arguments in this minimal syntax have no state effects, so unspecified
equational order is harmless for this body. No other local rule is labeled
unsound.

The main claim closes because actual execution and the postcondition reduce to
the same hooked `^%Int` symbol. This is a conditional external-primitive
identity, not an independent derivation of that primitive's Python meaning.

## 6. Fresh non-vacuity test

Status: **PASS**.

The fresh mutation retained the exact submitted body and satisfying ground
input `(3,5)`, but changed the result obligation from `3` to `4`.

```text
kprove --dry-run spec-vacuity-audit.k \
  --definition verification-haskell-kompiled \
  --spec-module AUDIT-SPEC-VACUITY --output none
# exit 0

kprove spec-vacuity-audit.k \
  --definition verification-haskell-kompiled \
  --spec-module AUDIT-SPEC-VACUITY
# exit 1, WarnStuckClaimState
```

The residual is a completed configuration with `result(3)`, which cannot
unify with required `result(4)`. Thus the mutation built, reached the relevant
obligation, and failed for the intended semantic reason. Artifacts:
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k),
[nonvacuity_dry_run.log](evidence/nonvacuity_dry_run.log), and
[nonvacuity_proof.log](evidence/nonvacuity_proof.log).

## 7. Proven-versus-assumed accounting

The successful reachability proof establishes precisely this conditional
statement:

> Under the candidate's generated semantics, for all K integers `N >= 0` and
> `P > 0`, running the exact regenerated constructor term for the submitted
> `pow(2,n,p)` body from the configured entry state reaches empty computation,
> records formals `"n","p"`, and records K value `2 ^%Int N P`.

It also establishes the five fixed examples. It does not prove equivalence to
the canonical loop, behavior outside the precondition, Python exception
behavior, or the universal equivalence of K `^%Int` and Python three-argument
`pow`.

Trust ledger:

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted `py2mpy.py` translation | Program identity | Acceptable and mechanically checked byte-for-byte and constructor-for-constructor. |
| K parser, reachability engine, unbounded integers, Boolean/string comparisons | All claims | Ordinary accepted toolchain trust; freshly rebuilt under recorded K 7.1.293. |
| Hooked `INT.powmod` | Call rule, `expectedModp`, every result | Acceptable only as a named external primitive on the guarded positive-modulus/nonnegative-exponent domain. The proof is interpretation-parametric because both sides use the same symbol. Finite execution supports but does not universally prove the Python bridge. |
| Unguarded mapping of Python `pow` to `^%Int` | Generated semantics for all integer configurations | Illegitimate as written: concrete `(2,-5)` false-result witness and missing modulus-zero exception behavior. |
| Bespoke “load sole definition and invoke it with `<n>/<p>`” runner | Entry interpretation | Informal but non-fatal for this immutable artifact because the exact function, parameters, body, and state transition are pinned and body-sensitive. |
| Assumption that source inputs satisfy `n >= 0, p > 0` | General theorem scope | Illegitimate narrowing: not stated in the prompt, excludes canonical-defined integer behavior, and still fails canonical fidelity at `(0,1)` within the restriction. |
| Differential and concrete tests | Python/K/canonical bridge | Finite empirical evidence only; reproducible and useful for finding counterexamples, not a substitute for the K proof. |

Gate summary: reconstruction, immutable-program pinning, and non-vacuity pass.
Real-language soundness fails on the unguarded `pow` bridge, and intent
adequacy fails on canonical behavior and input scope. The benchmark therefore
requires `FAIL / NOT_LEGIT` despite the genuine reconstructed `#Top`.

Exact commands, exit statuses, and evidence-file mapping are collected in
[COMMANDS.md](evidence/COMMANDS.md).

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
