# Independent Stage 3–5 audit: HumanEval 77-iscube

## Scope and conclusion

I independently audited condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`, in launcher mode `CLASSIFICATION_AND_PROOF`. I treated
the mounted workspaces, prior review, manifests, comments, logs, and candidate
source as untrusted evidence. I used the trusted inventory and gate code to
reconstruct facts, and made the classification, obligation-adequacy, and
operational-bridge judgments directly from the frozen K source and semantics.

The Stage 3 classification is complete and correct. Stage 4 authenticates to
the recorded immutable producer image and generates exactly the two true,
relevant domain-lemma obligations. The Stage 5 candidate clean-builds, proves
the unchanged generated target, has no forbidden trust declarations, and uses
only the standard Lean core axioms allowed by the trusted gate. Each supplied
target-parameter definition agrees with the frozen operational meaning on its
complete K-defined domain.

## Launcher and immutable-input integrity

`AUDIT_MODE` is `CLASSIFICATION_AND_PROOF`; the launcher JSON records the same
mode, problem `77-iscube`, condition `kit-semantics`, and
`SUPPLIED_SEMANTICS`. See
[00-audit-mode.log](evidence/00-audit-mode.log) and
[01-audit-input.log](evidence/01-audit-input.log).

I recomputed every mounted tree/file hash bound by `/audit-input.json`:

- Stage 1 pipeline tree:
  `ca615660f1c4cd43505ff84d74cec09aa2b7edc03ab95b99d8898f49ede4a33a`.
- Stage 1 deterministic-export tree:
  `4dc89c37310b7147d987d772fc889c48049a6a311bf406066afb7947619ad463`.
- Stage 3 discovery manifest:
  `95aca320c1794410f2809f3efc2b4c10c3cbb1f33330b65141db489b631d477a`.
- Selected Stage 2 audit tree:
  `3b1a1e94ea9cdfc095c4edb2ba6e5c6f04e0a600346b827b11ddcab059d137f9`.
- Selected Stage 4 generation tree:
  `2ede81f2af36f62dc5c519685786557319ba97f331dd97ec581966d643714cf2`.
- Producer-source tree:
  `1e5faff11bfada41bad76e5f42fbbbc6101a6155bd2f81524eca8cd7c87cdab1`.
- Generated Lean tree:
  `2eadc4fe5189bf683886248fb45281efdf3a9258bb7dcaba85bd885f79eb96aa`.
- Stage 5 candidate workspace:
  `900ed863c438d9d81fcdc306afccf368f77a767d7638cdf11d0a0fe1f64611ea`.

All 814 Stage 1 regular-file paths and contents match
`stage1_source_hashes` bijectively. The audit input's `lean_invocation_sha256`
describes a launcher-side invocation tree that is not one of the mounted audit
inputs; the mounted Lean workspace itself is fully matched above. Complete
results are in
[08-producer-and-recorded-hashes.log](evidence/08-producer-and-recorded-hashes.log).

## Stage 3 inventory reconstruction

Running the trusted `tools.k_rule_inventory.inventory_verification` against
the frozen Stage 1 workspace reconstructed the local verification closure as:

1. `VERIFICATION`
2. `CONNECTION-RULE`
3. `VERIFICATION-SYNTAX`
4. `VERIFICATION-BASE`

The closure contains exactly 10 rules. For every entry I recomputed the file,
module, start/end line, normalized source text, SHA-256, and
`source_rule_id`. Every ID is exactly `rule-` followed by its normalized hash.
There are no duplicated IDs or normalized hashes. The protected Stage 3 list
has exactly the same 10 IDs in the same order, with no omission or extra
entry. The recomputed whole inventory hash is
`8dd2336c6c649eb57c1eb6a0a7e1763c5685da701325c784841c45abce12edac`,
exactly the protected value. The full source text and spans are in
[06-reconstructed-rule-inventory.log](evidence/06-reconstructed-rule-inventory.log).

### Independent classification

The table uses abbreviated IDs; the evidence log above contains every full
identity.

| Rule | Frozen role | Classification | Judgment |
|---|---|---|---|
| `705397624556…` | Exact `#while`/return/frame transition to `cubeSearch(A,C)` | `PROVED_DERIVED_LEMMA` | Correct: Stage 1 first proves the identical complete reachability statement bridge-free, then installs and uses it. |
| `a125d094d701…` | `cubeOf(I) = I*I*I` | `DEFINITION` | Defines the fresh summary symbol `cubeOf`. |
| `19e878134276…` | equality base case of `cubeSearch` | `DEFINITION` | Defines a guarded base equation of the fresh summary. |
| `fb3d10bf0eb9…` | overshoot base case of `cubeSearch` | `DEFINITION` | Defines a guarded base equation of the fresh summary. |
| `bf30e24b2468…` | increment recurrence of `cubeSearch` | `DEFINITION` | Defines the recursive case of the fresh summary. |
| `050c02c309a5…` | loop-exit equality equals `cubeSearch` | `DOMAIN_LEMMA` | It relates existing integer operations to the summary, does not define its LHS, and was not separately proved before use. |
| `6a2681616cee…` | remove key 1 from singleton-plus-rest map | `DOMAIN_LEMMA` | It is a guarded mathematical fact about built-in map operations, not a definition or prior derived theorem. |
| `79867a7dea47…` | negative branch of `isCubeInt` | `DEFINITION` | Defines the fresh summary after sign normalization. |
| `9371ae3bb178…` | nonnegative branch of `isCubeInt` | `DEFINITION` | Defines the fresh summary through `cubeSearch`. |
| `e0a6a1010506…` | exact `iscubeClosure` term | `DEFINITION` | Names the proof term/closure produced by the source program. |

There are no ordinary `OPERATIONAL_RULE` entries in this local closure. Both
rules marked `[simplification]` are `DOMAIN_LEMMA`, satisfying the required
restriction.

For the derived lemma, `connection-spec.k` requires only
`verification-base.k`, which does not contain the installed bridge. After
removing the claim label and the installed rule's operational priority
attribute, the complete K term, continuation, bindings, all cell transitions,
and variable set are byte-for-byte equal after whitespace normalization. In
the frozen `prove.sh`, the connection proof precedes compilation of
`connection-rule.k`, which precedes compilation and proof of the final
verification module. The authenticated Stage 1 log contains six `#Top`
results and no unexpected mutation success. See
[28-derived-lemma-order-and-identity.log](evidence/28-derived-lemma-order-and-identity.log)
and [29-stage1-proof-result-markers.log](evidence/29-stage1-proof-result-markers.log).

### Mathematical relevance and truth

The source program normalizes a negative input to its magnitude, increments a
candidate from zero until its cube is no longer below that magnitude, and
returns whether the terminating cube is equal. The first domain lemma is
exactly the loop-exit observation: under `¬(I³ < A)`, `I³ == A` and
`cubeSearch(A,I)` are both true in the equality case and both false in the
overshoot case. It is load-bearing for the requested cube postcondition.

The second domain lemma is the function-frame cleanup used by the frozen
operational semantics. The `#pop` rule updates scopes with
`SC[L <- undef]`; when the callee frame at key 1 is represented by a singleton
map disjoint from `REST`, removing key 1 returns exactly `REST`. It is
load-bearing for completing the source call with the restored caller state.
Neither domain lemma is irrelevant or a disguised assertion of an unrelated
property.

## Stage 4 producer authentication and deterministic generation

Before judging generation, I directly hashed the mounted producer sources:

| Source | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `74842302afea69a17a4815cf1213f080da4ac56d53b80d181f27196ec4112d63` |
| `klean.py` | `659c1d1c627ff2ca101ab8f9b5a1f1d73968e019e2a305f4ec1d1afa2d8c5a91` |

Both match `source-manifest.json` and `generator-manifest.json`. The immutable
image ID is consistently
`sha256:21e4151b8f48811e6c31994b3719c3e8a4a787856e1d3911ca9700e54a39c910`
in the generator manifest, source manifest, and the image-keyed producer path
recorded by `/audit-input.json`. Thus there is no producer-source
infrastructure error.

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and the required frozen workspace, protected classification, selected
generation, and trusted lock file. The audit sandbox hides
`/proc/<current-pid>/exe` while allowing the equivalent `/proc/self/exe`;
Lean 4.22's runtime reads the former and initially failed before any build.
The first failure is preserved in
[09-rerun-check-generation.log](evidence/09-rerun-check-generation.log).
I used an audit-only `LD_PRELOAD` shim that redirects only that exact
same-process readlink to `/proc/self/exe`; it does not alter Lean, the project,
or any mounted input. The probe and shim source/results are in
[31c-procfs-probe-without-shim.log](evidence/31c-procfs-probe-without-shim.log),
[31d-procfs-probe-with-shim.log](evidence/31d-procfs-probe-with-shim.log), and
[procself_readlink_shim.c](evidence/procself_readlink_shim.c).

With that environment compatibility correction, the exact trusted checker
returned `PASS`, rebuilt the generated project after `lake clean`, found two
obligations, zero sorries, and the expected target. Its full commands, build
output, and returned evidence are in
[11-rerun-check-generation-with-proc-shim.log](evidence/11-rerun-check-generation-with-proc-shim.log).

### Obligation bijection and adequacy

My independently classified domain set has exactly the two IDs
`050c02c…` and `6a268161…`. The `source_rules` and `obligations` arrays contain
those same IDs once each in the same order. Every source text, span, normalized
hash, conjunct hash, discovery hash, and inventory hash matches. No definition
or proved derived lemma is exported as an obligation, and no domain lemma is
omitted or duplicated.

The generated conjuncts preserve the K rules exactly:

- For all integers `A,I`, if `not (I³ < A) = true`, then
  `(I³ == A) = cubeSearch(A,I)`.
- For all maps `REST` and scopes `S`, if key 1 is absent from `REST`, then
  removing key 1 from `(1 ↦ S) REST` equals `REST`.

The hypotheses are not vacuous. `A=8,I=2` realizes the equality/true branch;
`A=9,I=3` realizes the overshoot/false branch; and `REST=.Map` realizes the
map guard for every `S`. The result is therefore discriminating and not a
tautological conjunction. Full structural comparisons are in
[14-obligation-bijection-and-target.log](evidence/14-obligation-bijection-and-target.log).

### Fixed target identity

The generated project contains exactly one target declaration,
`Klean77Iscube.Lemmas.targetStatement`, in
`Klean77Iscube/Lemmas.lean`. Recomputed values are:

- statement SHA-256:
  `d5996a478c905ca7b2321227fced05556a5e59a0428eab8b73a73cf7027a0107`;
- declaration-definition SHA-256:
  `6a16918a27f38836cd81a135dba59dc749e52fd1937891b6223d99d9fad14f67`.

The declaration, file, parameter list and bindings, statement, and both hashes
match `generator-manifest.json`, the trusted preflight result, and
`/audit-input.json` exactly.

## Stage 5 clean build, theorem identity, and trust

I created the fresh workspace
`/tmp/audit-work/lean-proof-audit-77-001`, copied the immutable generated
project into it as `Base`, and copied only the candidate project sources and
metadata. The copied Base tree hash remains
`2eadc4fe5189bf683886248fb45281efdf3a9258bb7dcaba85bd885f79eb96aa`,
and every copied candidate source hash equals its mounted original.

In that fresh project:

- `lake clean` exited 0 with no output;
- `lake build` exited 0 and rebuilt the generated modules and `Proof` from
  source; the only messages were two harmless generated unused-variable
  warnings.

The complete outputs are
[16-lake-clean-fresh-proof.log](evidence/16-lake-clean-fresh-proof.log) and
[17-lake-build-fresh-proof.log](evidence/17-lake-build-fresh-proof.log).

Static inspection found exactly one candidate definition for each of the nine
fixed target bindings, exactly one `theorem final`, and no `sorry`, `admit`,
`unsafe`, new `axiom`, or new `opaque`. The candidate neither declares the
`Klean77Iscube` namespace nor defines/shadows `targetStatement`.
`Proof.final`'s normalized type is exactly the fixed generated statement, not
a duplicate or weakened theorem. See
[19-static-target-and-candidate-gate.log](evidence/19-static-target-and-candidate-gate.log).

Running Lean with `#print axioms Proof.final` produced exactly:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The exact command/output is in
[18-print-axioms-proof-final.log](evidence/18-print-axioms-proof-final.log).
The trusted final gate's allowance consists of those three standard Lean core
axioms plus declarations listed in `trust-inventory.json`. There is no
`sorryAx`, no unrecorded or non-core axiom, and none of the 41 generated
collection-hook axioms is a dependency of `Proof.final`. The reconciliation is
in [32-axiom-reconciliation.log](evidence/32-axiom-reconciliation.log).
I also reran the trusted `check_proof_candidate`, which independently copied,
clean-built, type-checked, and axiom-checked the mounted candidate and returned
`PASS`; see
[30-rerun-trusted-proof-candidate-gate.log](evidence/30-rerun-trusted-proof-candidate-gate.log).

## Operational-bridge audit of every target parameter

The two source rules bind nine Lean parameters. I located the one exact
candidate `def` for each and compared it with its KORE hook/symbol, the bound
source IDs, the frozen rules, the source loop, and the K operational model.

| Candidate definition | Bound operational meaning | Independent judgment |
|---|---|---|
| `_Map_` | `MAP.concat` | It appends the two generated map representations. The K hook is defined for disjoint maps; on the source rule's complete domain, the left map is the singleton key 1 and the guard says key 1 is absent from `REST`, so this is exactly the successful branch of the generated disjoint-map model. Collision cases have no K result and are outside this rule's match domain. |
| `_in_keys(_)_MAP_Bool_KItem_Map` | `MAP.in_keys` | Recursive structural key membership over the generated map representation; true exactly when the key occurs. |
| `_<Int_` | integer less-than | `decide (left < right)` over unbounded Lean integers, exactly K `Int` ordering. |
| `_==Int_` | integer equality | `decide (left = right)`, exactly K integer equality. |
| `_[_<-undef]` | `MAP.remove` | Deletes every entry with the selected key. K maps have unique keys; on every valid K map, and specifically on singleton-plus-absent-rest, this is exactly key removal. |
| `_|->_` | `MAP.element` | Produces exactly the singleton key/value map representation. |
| `_*Int_` | integer multiplication | Direct unbounded integer multiplication, exactly K `Int` multiplication. |
| `cubeSearch` | the three frozen summary equations | Uses the frozen base behavior when `candidate³ ≥ a`; otherwise it searches exactly the bounded interval that can contain an integer cube root, restricted to roots at or above the start. This is extensionally equal to the recurrence for all integers. |
| `notBool_` | Boolean negation | Direct Boolean negation. |

For `cubeSearch`, let `f(a,i)` be the frozen K recurrence. Integer cubing is
strictly increasing because `(i+1)³-i³ = 3i²+3i+1 > 0`. Thus `f(a,i)` returns
true exactly when some integer `j ≥ i` has `j³=a`; otherwise it reaches the
first overshoot and returns false. The candidate uses radius `|a|+1` and scans
all integers from `-(|a|+1)` through `|a|+1`, retaining `j ≥ i`. Every integral
cube root `r` of `a` satisfies `|r| ≤ |a|+1`, so the scan includes every and
only possible qualifying root. When `i³ ≥ a`, its direct equality branch is
exactly the two K base cases. This establishes universal equivalence; the
finite tests below are corroboration rather than its justification.

Adversarial Lean evaluations covered exact cubes, non-cubes, overshoot,
negative targets, a distant negative start, and zero, producing respectively
`true, false, true, false, false, true`. A separate finite existential oracle
checked 8,241 pairs with `a∈[-100,100]` and `i∈[-20,20]`: there were zero
semantic mismatches and zero violations of any of the three K recurrence
equations. See
[20-operational-bridge-examples.log](evidence/20-operational-bridge-examples.log)
and
[25-cube-summary-differential-and-recurrence-fixed2.log](evidence/25-cube-summary-differential-and-recurrence-fixed2.log).
The map constructors were universally checked to preserve both inputs, and a
concrete disjoint union has two entries; see
[22-operational-bridge-universal-constructor-checks.log](evidence/22-operational-bridge-universal-constructor-checks.log).

Counterfactual mutations confirm why this independent check matters:

- Replacing the recurrence/search branch by constant `false` still allows the
  fixed exit obligation to build, but the operational witness
  `cubeSearch(8,0)` becomes false instead of the frozen result true. See
  [26c-build-recurrence-mutation.log](evidence/26c-build-recurrence-mutation.log)
  and
  [26d-recurrence-mutation-operational-witness.log](evidence/26d-recurrence-mutation-operational-witness.log).
  The actual candidate is not this convenient implementation; its definition
  passes the universal argument and the adversarial comparisons above.
- Replacing the guarded exit/equality branch by constant `false` makes the
  proof fail with the residual goal `¬ I*I*I = A`, showing that the generated
  obligation constrains the load-bearing exit result. See
  [27c-build-exit-mutation-expected-failure.log](evidence/27c-build-exit-mutation-expected-failure.log).

The actual definitions are therefore neither constant, identity, hard-coded,
nor vacuous operational conveniences. They implement the frozen meanings on
the complete operational domains used by the two source rules.

## Final judgment

There is a genuine nonempty two-lemma domain set, so the selected `PASS` Stage
4 status and proof-bearing mode are appropriate; `KLEAN_NO_OBLIGATIONS` would
have been illegitimate. No inventory, classification, generation, target,
proof-identity, axiom, or operational-bridge defect remains.

VERDICT: PASS
LEGITIMACY: LEGIT
