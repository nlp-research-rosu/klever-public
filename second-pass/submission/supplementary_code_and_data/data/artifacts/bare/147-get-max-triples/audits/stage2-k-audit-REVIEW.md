# Independent adversarial audit: 147-get-max-triples

The candidate contains a legitimate, result-constraining partial-correctness
proof of its actual generated program over the full positive-integer contract
domain. The proof and generated semantics reconstruct cleanly, the claim pins
the trusted-regenerated constructor program, and independent body and
postcondition mutations are rejected for the expected semantic reason.

The remaining concerns are non-fatal trust-boundary limitations: the K theorem
uses a deliberately small single-function entry convention rather than a
general Python call semantics, and the equivalence between its closed-form
postcondition and the English triple-enumeration contract is established by a
correct informal residue argument plus finite differential evidence, not by a
second K theorem.

## 1. Input and provenance integrity

`/audit-input.json` declares `legacy-selected-stage1`,
`GENERATED_SEMANTICS`, problem `147-get-max-triples`, and condition `bare`.
`/reference/reference-semantics` is absent, as this mode requires. I did not
seek or use any hidden reference semantics.

The independent checker
[`stage1_integrity.py`](evidence/stage1_integrity.py) read and validated:

- `/audit-input.json` and `/audit-campaign-lock.json`;
- `/run.json`, `/task.json`, and `/generation-result.json`;
- `invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and both historical legacy records;
- all 339 JSON objects in the structured trace.

Every required mount and record is a real regular file or real directory. No
candidate or generation-trace entry is a symlink or unsupported type. Historical
`runtime-metrics.json` is absent, but it is not required for this declared
legacy layout. `usage.json` is present and was inspected.

The campaign lock is byte-hashed to
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`
and its parsed object exactly equals the `audit_campaign` block. All declared
regular-file hashes match. Both independently reconstructed tree-hash schemes
also match:

| Tree | Launcher digest | Generation/pipeline digest |
|---|---|---|
| `/candidate` | `315450951708b6a7603a090898a4ed672139a44b2490a636ab9486d8e86ab252` | `bc9e219af0d5c41f16de070cfc336c56298f6b4d3878fee3950176add79e79c5` |
| structured trace | `645be3d82537fc43078fa0c341cac3a0caad1414927250befd4face3224e9c88` | `e9708461ce994b937f68c748d739e2cc34716e4a970382ad3f30318297781966` |

The candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
mounts. The candidate contains all required proof artifacts. Full output and
exit 0 are in [`stage1_integrity.log`](evidence/stage1_integrity.log). The
preserved `stage1_integrity_attempt1.log` records a reviewer-script indexing
mistake: it initially expected selected trace line 338 to be a response item;
inspection showed it is the recorded `token_count` event. I corrected only the
reviewer script and reran it successfully. This was not a mount, provenance, or
candidate failure.

The generation transcript claimed `#Top`, but no audit conclusion below relies
on that claim or on candidate-built caches.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says: for positive integer `n`, form
`a[i] = i*i-i+1` for indices `1..n`, and count index triples `i<j<k` whose
three values sum to a multiple of 3. The documented `n=5` result is 1. The
trusted canonical implementation constructs this array and directly enumerates
all triples.

The candidate instead computes a closed form. With
`q = floor((n+1)/3)`, it returns

`q(q-1)(q-2)/6 + (n-q)(n-q-1)(n-q-2)/6`.

Trusted regeneration used:

```text
python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/generated-tests/solution-regenerated.mpy
cmp /tmp/audit-work/generated-tests/solution-regenerated.mpy /candidate/solution.mpy
```

Both commands exited 0. Both files have SHA-256
`023c86c0f1ad0b464ed905d669b2ffba7ab4a37cbe097cd5c374bbd2089415c0`;
see [`translator_identity.log`](evidence/translator_identity.log).

The independent
[`differential_test.py`](evidence/differential_test.py) imports the trusted
canonical and candidate entry points separately. It checked:

- the documented `n=5` example;
- the empty-array robustness case `n=0` (outside the positive formal domain);
- every `n` from 0 through 80, repeatedly crossing every residue-class and
  first-triple boundary;
- 26 distinct seeded generated values from 84 through 175;
- a separately written direct contract enumerator on all 107 canonical cases;
- a separate residue-count oracle at `181`, `999`, `10^6`, `10^18`, and
  `10^30`.

There were zero mismatches; command `python3
/audit-output/evidence/differential_test.py` exited 0. Inputs, seed, counts, and
results are preserved in
[`differential_test.log`](evidence/differential_test.log). These tests are
finite evidence, not the universal proof.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/rebuild`; no
candidate-provided compiled definition or cache was copied. K tool versions
were independently confirmed as 7.1.293 for `kompile`, `krun`, and `kprove`;
see [`toolchain_versions.log`](evidence/toolchain_versions.log).

Fresh source builds used:

```text
kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition audit-runtime-evidence-kompiled

kompile verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition audit-verification-evidence-kompiled
```

Both exited 0. Exact command traces and statuses are in
[`kompile_runtime_command.log`](evidence/kompile_runtime_command.log) and
[`kompile_verification_command.log`](evidence/kompile_verification_command.log).

Fresh generated-semantics execution was compared against both Python
implementations for `n = 0,1,2,3,4,5,6,10,11,100`. Every `krun` exited 0 and
returned the same integer. Representative results were `0`, `1`, `4`, `36`,
`39`, and `53361` for `n=1,5,6,10,11,100`, respectively. The script prints
each exact `krun` command, exit status, K configuration, and comparison in
[`concrete_semantics_compare.log`](evidence/concrete_semantics_compare.log).

There is exactly one positive claim. It was run independently:

```text
kprove spec.k --definition audit-verification-evidence-kompiled \
  --spec-module SPEC
```

It printed `#Top` and exited 0. See
[`kprove_positive_second_clean_definition.log`](evidence/kprove_positive_second_clean_definition.log).

## 4. Adequacy and real-program pinning

In plain language, the sole entry claim says:

- precondition: `N` is any mathematical integer at least 1;
- initial state: execute the explicitly embedded
  `get_max_triples(n)` module term with input `N`, empty environment, and no
  result;
- final state: computation is consumed, the environment contains exactly
  `"n" |-> N`, and the returned integer is exactly
  `validTripleCount(N)`.

This is equality through the rewritten `<result>` cell, not a free result,
tautology, implication-only postcondition, or existential escape. There are no
helper or loop claims to check.

[`program_pinning.py`](evidence/program_pinning.py) parses constructor syntax
into trees rather than relying on prose. The candidate `solution.mpy`, trusted
regeneration, and the term between `<k>` and `=> .K` in `spec.k` are identical
constructor trees. The function binding is exactly `get_max_triples`; its
parameter and body are exact. The check exited 0. It also exhibits satisfying
states at `N=1,5,10,100`. Substitution gives claimed/candidate/canonical values
`0`, `1`, `36`, and `53361`, respectively; see
[`program_pinning.log`](evidence/program_pinning.log).

I separately changed the executed body's outer addition to subtraction,
translated that changed source with the trusted translator, and embedded that
changed constructor term in
[`spec-body-mutated.k`](evidence/spec-body-mutated.k). The generated changed
term and claim term differ from the submitted term at exactly that operator.
At satisfying input `N=5`, the original returns 1 and the mutation returns -1.
The exact command

```text
kprove spec-body-mutated.k --definition audit-verification-kompiled \
  --spec-module SPEC-BODY-MUTATED
```

exited 1 with `WarnStuckClaimState` at the failed result implication. See
[`body_mutation_precheck.log`](evidence/body_mutation_precheck.log) and
[`body_mutation_kprove_command.log`](evidence/body_mutation_kprove_command.log).
This demonstrates sensitivity of the program term actually executed by the
claim.

The formal domain is every `N >= 1`, exactly the unrestricted positive-integer
source domain. There is no fixed-size unrolling, example-only claim, or narrowed
precondition.

## 5. Rule-by-rule static soundness review

The exhaustive source-level inventory is
[`rule_inventory.md`](evidence/rule_inventory.md). It enumerates every local
sort and syntax production, configuration cell, strictness declaration,
ordinary operational rule, function/total declaration, defining equation, and
claim. There are no generated helper K files.

The used construct map is complete:

| Program constructor | Declaration/effect |
|---|---|
| `Module`, `FuncDef`, `Params` | sole-function entry rule binds the exact parameter to `<input>` and then executes the body |
| `Return` | strict evaluation, consumes the computation, writes exact `<result>` |
| `Name` | reads the exact integer binding from `<env>` |
| `BinOp` | `seqstrict(2,3)` enforces Python left-to-right operand evaluation |
| `+`, `-`, `*` | exact unbounded integer operations |
| `//` | guarded integer division; every submitted divisor is positive 3 or 6 |
| `Int` | the only modeled value and local `KResult` |

For `N >= 1`, every dividend reaching `//` is nonnegative: a class size is
nonnegative and `x(x-1)(x-2)` is zero at `x=0,1,2` and positive thereafter.
Thus the modeled division agrees with Python floor division throughout the
claim domain. All syntax and every ordinary semantic rule are exercised by the
concrete runs.

State and control are explicit. The entry rule reads `<input>`, requires an
empty environment, and installs the one parameter. Name lookup only reads the
map. Arithmetic has no state footprint. The return rule requires an evaluated
integer, no trailing continuation, and `noResult`, then writes that exact
integer. No rule discards a continuation, fabricates allocation/state, or
short-circuits the submitted body.

`choose3` and `validTripleCount` are the only local `[function,total]` symbols.
Each has one unconditional, terminating, nonoverlapping equation. They occur
only in the destination postcondition and never rewrite a program term, so
they are definitional summaries rather than operational bridges or oracles.
There are no local opaque/fresh symbols, priorities, simplification rules,
`[functional]` declarations, `owise` rules, or derived lemmas.

The entry rule intentionally ignores the function-name metavariable and treats
the sole definition as the selected entry point. That would not model ordinary
module import for an alternate module, but its complete matched context and
binding behavior are explicit, and the fixed claim contains exactly one
capture-free one-argument function with the required name and exact body. It
does not enable a false result for this submitted program on any intended
input. Missing behavior for unused Python constructs and unused division by
zero is permitted in generated-semantics mode.

No candidate-local rule was found unsound on the intended domain, so there is
no false-conclusion witness to report for an unsound rule.

## 6. Fresh non-vacuity test

The fresh mutation
[`spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k) keeps the exact
submitted program and changes only the result obligation from
`validTripleCount(N)` to `validTripleCount(N) +Int 1`.

The satisfying witness `N=5` has actual and canonical result 1 while the
mutated target is 2; see
[`vacuity_witness.py`](evidence/vacuity_witness.py) and
[`vacuity_witness.log`](evidence/vacuity_witness.log).

The mutation first built successfully:

```text
kprove spec-vacuity-audit.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
```

Exit was 0; see [`vacuity_dry_run.log`](evidence/vacuity_dry_run.log). The live
proof command without `--dry-run` exited 1, printed `WarnStuckClaimState`, and
showed the unmet implication equating the computed result with that result plus
one. See
[`vacuity_kprove_command.log`](evidence/vacuity_kprove_command.log). This is a
reachable, semantic rejection, not a parser error, timeout, missing import, or
unrelated crash.

## 7. Proven versus assumed accounting

### Precisely proven

Under modules `MPY` and `VERIFICATION`, for every mathematical integer
`N >= 1`, execution of the exact trusted-regenerated constructor program from
the stated initial cells reaches the exact return

`C3(q) + C3(N-q)`,

where `q = (N+1) div 3` and `C3(x) = x(x-1)(x-2) div 6`. The computation is
consumed, the input is preserved, and the only environment binding is
`"n" |-> N`. This theorem is universal over positive integers and is sensitive
to both the program body and result obligation.

### Trust and assumption ledger

| Boundary | Dependents | Disposition |
|---|---|---|
| K 7.1.293 compiler, Haskell/LLVM backends, reachability engine | All builds and proof closure | Ordinary low-level trusted computing base; acceptable. |
| Imported K `INT`, `STRING`, and `MAP` modules | Values, arithmetic, bindings | Fixed upstream primitives; acceptable. Only unbounded integers and simple finite maps/strings are used. |
| Trusted `/reference/py2mpy.py` | Python-source to constructor identity | Launcher-trusted input; byte identity was independently regenerated. |
| Candidate's `MPY` semantics | Meaning of every executed constructor | Not assumed wholesale: rebuilt, concretely exercised, and exhaustively reviewed. Its sole-function entry convention is narrower than general Python semantics but preserves every material operation and control effect of this exact program. This is a non-fatal concern, not an execution bypass. |
| Residue/counting bridge from `validTripleCount` to the English contract | Intent adequacy | Correct informal mathematics: `i*i-i+1` has residue 0 only for `i ≡ 2 (mod 3)`, otherwise residue 1; a three-term sum is divisible by 3 iff all three residues are 0 or all are 1. It is not separately machine-checked in K. This is the principal non-fatal concern. |
| Trusted canonical and independent differential tests | Empirical support for source-intent bridge | 107 canonical cases plus boundary and large residue-oracle cases, all reproducible with zero mismatches. Finite support only; it is not substituted for the K theorem or universal mathematical argument. |

There is no opaque result-bearing symbol, unconstrained oracle, empirical
execution bridge, hidden lemma, or candidate-supplied compiled artifact in the
proof dependency chain. The candidate's `PROOF.md` is absent and its generation
reports were not used as proof.

Gate A (real-program soundness and non-vacuity) passes. The formal domain and
postcondition materially match the source contract, with no narrowing. Evidence
is reproducible and honestly finite. The proof is therefore legitimate. The
benchmark-level `CONCERNS` status records the non-machine-checked
summary-to-English-contract bridge and the minimal generated entry convention;
neither can make a false conclusion about the fixed program on a positive
integer input provable.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
