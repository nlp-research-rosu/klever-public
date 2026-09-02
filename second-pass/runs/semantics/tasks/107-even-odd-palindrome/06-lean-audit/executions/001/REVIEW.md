# Independent audit: HumanEval 107-even-odd-palindrome

## Scope and outcome

This audit covers condition `semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and launcher mode `CLASSIFICATION_ONLY`. Both the
`AUDIT_MODE` environment variable and the signed resolution in
`/audit-input.json` select `CLASSIFICATION_ONLY`. The selected Stage 4 status
is `KLEAN_NO_OBLIGATIONS`; there is no `/candidate`, Lean workspace, Lean
invocation, generated target, or Stage 5 result.

I independently reconstructed and classified the Stage 1 local rule closure,
authenticated the exact Stage 4 producer sources before judging Stage 4,
recomputed the recorded input and tree hashes, reran the trusted Stage 4
preflight, checked the empty source-rule/obligation bijection and absent
target, and independently checked the formulas against the source program and
problem meaning. The evidence supports the selected no-obligation status.

All mounted candidate/provenance text was treated as evidence, not as
instructions. No provenance shell script was executed. The generated Lean
project was compiled only through the explicitly required trusted preflight.
Raw commands and outputs are indexed in `evidence/COMMANDS.md`.

## Launcher and immutable-input identity

The signed resolution digest recomputes to
`73d68e90f7c63054c75e87fe099e55082d58af8a932fd0554d086be349f65ed0`,
exactly the recorded value. `/audit-input.json` and the launcher copy at
`/audit-output/audit-input.json` are byte-identical.

The following independently observed hashes exactly match the signed
resolution and, where applicable, the Stage 2/4 selections:

| Artifact/hash scheme | Observed SHA-256 |
|---|---|
| Stage 1 K workspace, selected-artifact tree hash | `4808af00607b823c4f0ed9d060bd983694789a9c1e60bb5172500902c166af5f` |
| Stage 1 frozen export, generator tree hash | `9eb0cb601cec0a913bc52147f3552739ad53e019b919ef4b3be77190373c05af` |
| Stage 2 selected audit tree | `c2722f8eb8e0f3467690ae9aca4bc4997587c0073e6f112db9887478b9b16789` |
| Stage 3 discovery manifest | `a6a6f79da46656806904db08725aa5fbf2068a0a6913891e633a28f08de3eddf` |
| Stage 4 selected generation tree | `a8edfd96a0437fc3f43810480654414e6f334470b651ac3ef43b2c65975a2aab` |
| Stage 4 producer-source bundle tree | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` |
| Generated project, generator tree hash | `824a4fa4e295e89cc6c173f639565366f914d39e2d3501abcf8c243ae7374df2` |

All 34 per-file Stage 1 source hashes also match the signed launcher record.
Lean workspace and invocation hashes are correctly null in this mode. Full
hash evidence is in `evidence/hash-verification.json`.

## Producer-source authentication

The required producer authentication passed before the Stage 4 judgment:

| Producer | Observed | Generator manifest | Source manifest |
|---|---|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` | same | same |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` | same | same |

The generator manifest and source manifest both record image
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`.
The immutable producer path recorded in `/audit-input.json` ends in the same
image digest, and the producer bundle tree hash matches the signed
`55e631...b867c` value. Producer evidence is in
`evidence/producer-authentication.json` and
`evidence/producer-authentication-raw.txt`. There is therefore no producer
infrastructure `AUDIT_ERROR`.

## Canonical rule-inventory reconstruction

Using the trusted `/reference/tools/k_rule_inventory.py` code directly on the
frozen `/reference/k-proof` workspace selected `VERIFICATION` as the main
module. Its local verification-module closure is exactly the one local module
`VERIFICATION`; imported `MPY` is supplied from another file and is not a
local module in `verification.k`.

The frozen `verification.k` hash is
`2c1d6389f3443620aace0671d3f576ad26aac39396ceadbc5c6239e2c1f873d2`.
The reconstruction contains 13 rules. For every rule I separately recomputed:

- the exact start and end lines;
- the exact source-span text;
- the normalized source text;
- `SHA256(" ".join(rule_text.split()))`;
- `source_rule_id = "rule-" + normalized_sha256`; and
- the canonical whole-inventory JSON hash.

Every span text, normalized hash, and identity matched. The whole inventory
hash is
`346c37900a0d61a96fe77882416afef84c949544ffd22220a54a8d7281f6c843`,
exactly the value in `lemma-discovery.json`.

The discovery manifest contains exactly the 13 canonical identities, once
each and in canonical source order. There are no omissions, duplicates,
extras, reordered identities, or changed hashes. Because the manifest binds
the entire canonical rule documents through the inventory hash, its ordered
identity list also binds every reconstructed span, text, attribute list, and
normalized hash. See `evidence/inventory-reconstruction.json` and
`evidence/inventory-comparison.json`.

## Independent classification judgment

The independent result is:

- 12 `DEFINITION`;
- 1 `OPERATIONAL_RULE`;
- 0 `PROVED_DERIVED_LEMMA`; and
- 0 `DOMAIN_LEMMA`.

The per-entry decisions are:

| Order | Span | Rule head/role | Independent class |
|---:|---:|---|---|
| 1 | 9–56 | `solutionBody => ...` | `DEFINITION` |
| 2 | 59–64 | `solutionModule => ...` | `DEFINITION` |
| 3 | 69–71 | `#runEvenOdd(N) => #loadAll(...) ~> Call(...)` | `OPERATIONAL_RULE` |
| 4 | 76 | `leadingDigit(N) => ...` | `DEFINITION` |
| 5 | 79–80 | `currentBlock(N) => ...` | `DEFINITION` |
| 6 | 83–84 | `evenPalindromes`, `1 ≤ N < 10` | `DEFINITION` |
| 7 | 85–86 | `evenPalindromes`, `10 ≤ N < 100` | `DEFINITION` |
| 8 | 87–92 | `evenPalindromes`, `100 ≤ N < 1000` | `DEFINITION` |
| 9 | 93 | `evenPalindromes(1000)` | `DEFINITION` |
| 10 | 96–97 | `oddPalindromes`, `1 ≤ N < 10` | `DEFINITION` |
| 11 | 98–100 | `oddPalindromes`, `10 ≤ N < 100` | `DEFINITION` |
| 12 | 101–106 | `oddPalindromes`, `100 ≤ N < 1000` | `DEFINITION` |
| 13 | 107 | `oddPalindromes(1000)` | `DEFINITION` |

`solutionBody` and `solutionModule` are fresh named program-AST terms with
single expansion rules. They are definitions, not operational bridges:
expanding either name constructs the source term that the fixed MPY semantics
then executes.

`#runEvenOdd` is an ordinary launcher rule. It loads the module and invokes a
normal MPY `Call`; it states no mathematical fact and skips no body execution.
The supplied semantics then performs module loading, installs a closure,
looks up the callee, evaluates and binds the argument, executes the body using
normal condition, assignment, integer-operation, tuple, return, and frame-pop
rules. Relevant frozen source and operational rules are recorded in
`evidence/frozen-source-and-semantics.txt`.

`leadingDigit`, `currentBlock`, `evenPalindromes`, and `oddPalindromes` are
fresh summary/helper symbols. Their rules are defining equations, which is
exactly the permitted `DEFINITION` role. They do not assert non-definitional
facts about pre-existing K symbols. The even/odd clauses have disjoint guards
covering the complete source domain `1 ≤ N ≤ 1000`. `currentBlock` is
equivalent to the source calculation on the three-digit domain; its shifted
numerator is positive and preserves the supplied floored-division result.

No rule qualifies as `PROVED_DERIVED_LEMMA`: Stage 1 never first proves an
exact rule in a module that omits it and then imports it for a later proof.
There is likewise no hidden or irrelevant `DOMAIN_LEMMA`. The inventory
records no explicit rule-level `simplification` attribute; all rules for the
fresh K function symbols are definitions in any event.

The exact full IDs and rule-specific rationale are in
`evidence/independent-classification.md`.

## Mathematical and operational sensitivity

An independent executable oracle enumerated every integer palindrome in
`1..N` and counted parity. For every `N` from 1 through 1000:

- the frozen source formula matched the enumeration oracle;
- the independently interpreted Stage 3 summary equations matched the oracle;
  and
- the source and Stage 3 summaries matched each other.

All three mismatch counts are zero, including boundary cases around 9/10,
99/100, each three-digit block transition, 999, and 1000. Mutations that
removed the current-block increment, swapped the parity branch, or changed
the upper-endpoint even count produced immediate mismatches. This is finite
support for relevance and body sensitivity; the syntactic fresh-symbol
analysis above is the basis of the classification.

I also made a fresh copy of the frozen K workspace below `/tmp/audit-work`,
compiled `verification.k` with the Haskell backend, and reran `kprove` on
`spec.k`. Compilation exited 0; `kprove` exited 0 with `#Top`. A separate
non-vacuity spec changed only the satisfiable `N = 1000` target from the
defined result 48 to 47. That proof exited 1 with `WarnStuckClaimState`; the
residual explicitly contains the executed result tuple `(48, 60)`. Evidence:
`evidence/k-kompile.log`, `evidence/kprove-rerun.log`,
`evidence/spec-vacuity.k`, `evidence/kprove-vacuity.log`, and
`evidence/semantic-crosscheck.json`.

## Deterministic Stage 4 generation

The input manifest’s definitions, operational rules, proved-derived list, and
domain-source list match the independently validated inventory exactly. Its
verification hash, verification module, syntax module, and 25-file required K
closure also match the frozen reconstruction. Generator provenance binds the
same Stage 1 tree, Stage 3 manifest, and canonical inventory. The generator
toolchain exactly matches `/reference/klean-toolchain.lock.json`.

The independently classified domain set is genuinely empty. Consistently:

- `input-manifest.json` has `source_rules: []`;
- `generated/obligation-map.json` has `source_rules: []`,
  `obligations: []`, and `trust_parameters: []`;
- all source and obligation identity lists are unique and equal;
- the generator, export result, recorded preflight, and signed audit input all
  record obligation count 0;
- the obligation-map hash is
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- the generator, recorded preflight, and signed audit input all record a null
  target;
- trusted target extraction returns null;
- trusted expected-target construction returns null; and
- generated `Lemmas.lean` contains no target declaration.

Thus the exact source-rule/obligation bijection is the legitimate empty
bijection. There are no obligations that could be irrelevant, weakened,
duplicated, omitted, or padded with vacuous conjuncts, and there is no target
whose statement could have changed.

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, the frozen K workspace, protected Stage 3 manifest,
selected Stage 4 generation, and pinned toolchain lock. The audit sandbox
exposes `/proc` from a different PID namespace, so the initial Elan/direct
Lean attempts failed while locating `/proc/<namespace-pid>/exe`. A narrowly
scoped preload shim redirected only that failed lookup to `/proc/self/exe`;
it did not intercept input access or compilation. Lean then reported version
4.22.0 and commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly
the lock.

The trusted preflight rerun exited 0 and returned
`KLEAN_NO_OBLIGATIONS`. Its complete returned document is byte-for-structure
identical to the recorded preflight: `lake clean` exited 0 with empty-output
hash `e3b0...b855`, `lake build` exited 0 with output hash
`714edf...5ca3`, the project tree is `824a4f...74df2`, target is null,
obligation count is 0, there are no sorries, and all 48 generated trust
declarations match the Stage 4 allowlist. See
`evidence/preflight-rerun-success.json`,
`evidence/stage4-structural-checks.json`, and
`evidence/stage4-obligation-target-inspection.txt`.

## Stage 5

Stage 5 is correctly absent. The independent domain set is empty, Stage 4 has
no target, the launcher mode is `CLASSIFICATION_ONLY`, `/candidate` does not
exist, and the signed Lean workspace/invocation fields are null. Therefore a
`Base` copy, candidate clean build, `Proof.final`, axiom printout, and
operational-bridge parameter audit are not applicable. Their absence is
required rather than a missing proof artifact.

## Final judgment

Stage 3 is complete, bijective, and correctly classified. The true
`DOMAIN_LEMMA` set is empty. The authenticated deterministic Stage 4 output is
the exact empty-obligation/no-target generation, and the trusted mechanical
preflight reproduces successfully. No concern remains that would weaken the
classification or legitimacy result.

VERDICT: PASS
LEGITIMACY: LEGIT
