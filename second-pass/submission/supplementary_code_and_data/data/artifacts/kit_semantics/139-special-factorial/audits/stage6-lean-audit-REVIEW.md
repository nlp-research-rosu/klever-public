# Independent audit: 139-special-factorial / kit-semantics

## Scope and outcome

The launcher-selected mode is `CLASSIFICATION_ONLY`, matching both
`AUDIT_MODE` and `/audit-input.json`. The semantics mode is
`SUPPLIED_SEMANTICS`. I independently audited Stage 3 classification and Stage
4 deterministic generation. Stage 5 proof review is inapplicable: the true
domain-lemma set is empty, the generated target is absent, `/candidate` is
absent, and the signed resolution has no Stage 5 result.

The Stage 3 classification is correct, `KLEAN_NO_OBLIGATIONS` is genuine, and
the generated output has neither an omitted obligation nor a vacuous target.

## Producer provenance gate

I hashed the mounted generation-time producer sources before judging Stage 4:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`

Both hashes exactly match `generator-manifest.json` and
`source-manifest.json`. The generator image ID is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in both manifests, and the same digest is the bundle-name component of the
generation-producer path signed into `/audit-input.json`. The bundle contains
exactly the two producer files and its source manifest. Its canonical pipeline
tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
also exactly matching the audit input.

The initial exploratory transcript `01-producer-provenance.txt` records that
`jq` is unavailable and also prints a Klean-project tree digest that is not the
pipeline bundle digest used by the signed resolution. The canonical pipeline
calculation is recorded in `03-producer-tree-identity.txt` and fully reconciled
in `06-recorded-hash-verification.txt`; there is no provenance mismatch.

## Frozen-input and recorded-hash reconciliation

The signed audit-input envelope digest recomputes to
`b609703037574eab15f5665a1788da13b45e00dc828d0f19a02af20c7d385cb8`.
The independent hash script performed 41 checks with zero failures, including:

- all 788 Stage 1 paths and per-file SHA-256 values, with no missing, extra, or
  changed files;
- the pipeline Stage 1 workspace tree, Stage 2 audit tree, selected Stage 4
  tree, and producer-source tree hashes;
- the Klean Stage 1 export and generated-project tree hashes;
- the Stage 3 manifest, `verification.k`, obligation-map, trust-inventory, and
  Stage 4 sidecar bindings;
- both selected-artifact hashes and the generator toolchain's exact equality
  with `/reference/klean-toolchain.lock.json`; and
- the signed null Lean-workspace, Lean-invocation, target, and Stage 5 fields.

The generated-project tree hash is
`c6456e96db012253da3a7816edb9733ec31057aa24e6e6196aac6866ccc42a92`.
No mounted input changed during either fresh preflight run.

## Canonical rule inventory

`prove.sh` selects `VERIFICATION` as the verification main module. The trusted
inventory code reconstructed the local module closure as exactly
`["VERIFICATION"]`. The fixed `MPY` and `INT` imports come from the supplied
semantics rather than from another proof-local module in `verification.k`.

The reconstructed inventory has exactly four ordered entries. For each entry I
recomputed the normalized source hash and the `rule-<hash>` identity. I also
recomputed the canonical whole-inventory hash. The result is:

| Span | Normalized SHA-256 / source rule ID | Independent class |
|---|---|---|
| 11–12 | `76c9fee7d31c7b9af2772f9513ebc29daf766162032c70206947d10685c8ab71` / `rule-76c9fee7d31c7b9af2772f9513ebc29daf766162032c70206947d10685c8ab71` | `DEFINITION` |
| 13–15 | `56984dfdcdf0ba8c027875164046db3a50319cd8bde210cf5869ac4eb5483d0b` / `rule-56984dfdcdf0ba8c027875164046db3a50319cd8bde210cf5869ac4eb5483d0b` | `DEFINITION` |
| 18–19 | `7e43f2e0797b8ac08b474026ab65d98ed66d18b24b058dc65450b65246cf00b5` / `rule-7e43f2e0797b8ac08b474026ab65d98ed66d18b24b058dc65450b65246cf00b5` | `DEFINITION` |
| 20–22 | `110b740de92d5388806b355cf84cbe138a0ae279db89595139a60295681df25c` / `rule-110b740de92d5388806b355cf84cbe138a0ae279db89595139a60295681df25c` | `DEFINITION` |

The whole-inventory hash is
`1993002e3c6d8018cd5a567c10250d952113f008862ec1beac606f480a035d82`.
It exactly matches `/reference/lemma-discovery.json`. The manifest has the same
four identities in the same order, all are unique, and there are no omitted,
extra, duplicated, reordered, or unaccounted entries. Because each identity
contains its normalized hash and the manifest binds the whole inventory hash,
there is also no changed rule text or source span hidden behind an identity.

## Independent classification judgment

All four rules are definitional equations for two named summaries:

1. `factorialAfter(I,N,F) = F` when `I > N` is the base equation for the
   final factorial accumulator.
2. When `I <= N`, `factorialAfter` advances to `I+1` with accumulator `F*I`.
3. `productAfter(I,N,F,R) = R` when `I > N` is the base equation for the
   final result accumulator.
4. When `I <= N`, `productAfter` advances to `I+1` with the new factorial
   `F*I` and the new result `R*(F*I)`.

The fourth equation's use of `F*I` in both new accumulators is material. The
supplied operational semantics evaluates statement sequences in order,
evaluates assignment right-hand sides before writing them, and implements
integer `*`, `+`, and `<=` with the corresponding K integer operations. Thus it
matches the source order `factorial = factorial * i` followed by
`result = result * factorial`, rather than multiplying the result by the stale
factorial.

These equations rewrite only the freshly named `factorialAfter` and
`productAfter` symbols. They do not match an MPY execution configuration,
observe an ordinary execution term, bypass a program body, assert the desired
postcondition as an independent fact, or purport to be previously proved
derived lemmas. They therefore satisfy the requested `DEFINITION` category.
The `I > N` and `I <= N` guards are disjoint and exhaustive over `Int`; the
recursive branch advances `I`, so the equations truthfully and totally define
the finite summary. All evaluative/simplification rules in the inventory are
therefore classified as `DEFINITION`, satisfying the simplification-policy
constraint.

The summaries are directly relevant to the fixed invariant and postcondition.
Starting from `I=1`, `F=1`, and `R=1`, after iteration `j`, the recurrence gives
`F=j!` and `R=1! * 2! * ... * j!`, exactly the HumanEval contract. Independent
checks covered contract inputs 1 through 8 and nonstandard accumulator states,
including the base boundary and negative/zero intermediate values. Identity,
constant-zero, and stale-factorial counterfactual definitions all disagreed at
`n=4` (correct result 288), so the equations are operationally discriminating.

There is no separate mathematical proposition or domain fact among the four
rules. Accordingly:

- `DOMAIN_LEMMA = {}`
- `OPERATIONAL_RULE = {}`
- `PROVED_DERIVED_LEMMA = {}`
- `DEFINITION` contains all four rules.

No relevant domain lemma has been hidden under another category, and there is
no irrelevant claimed domain lemma.

## Stage 4 obligation bijection and target identity

Given the independently empty domain set, the deterministic Stage 4 mapping is
exact:

- `input-manifest.json.source_rules = []`;
- `obligation-map.json.source_rules = []`;
- `obligation-map.json.obligations = []`;
- `obligation-map.json.trust_parameters = []`; and
- both generator and export obligation counts are zero.

The generator's expected-target constructor returns `null`, the trusted target
parser observes `null`, and the generator manifest and signed audit input both
record a null target. `Lemmas.lean` contains only imports and an empty namespace;
there is no `KleanTarget`, theorem, proposition definition, empty conjunction,
or `True` substitute. Consequently there are no irrelevant, weakened,
duplicated, omitted, or vacuous conjuncts, and no target change.

## Fresh preflight and mechanical gate

I invoked `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and exactly these inputs:

```text
/reference/k-proof
/reference/lemma-discovery.json
/reference/klean-generation
/reference/klean-toolchain.lock.json
```

The audit sandbox exposes `/proc/self/exe` but not Lean's namespace-local
`/proc/<getpid()>/exe`, so the first clean-build attempt failed while Lean tried
to locate its installation. I preserved that failure. I then used the small,
source-preserved shim in `proc_exe_readlink_shim.c`, which redirects only the
unavailable `/proc/<digits>/exe` readlink shape to `/proc/self/exe`, plus a Lake
installation-layout shim under `/tmp/audit-work`. This changes neither the
generated sources nor Lean logic. `lean --version` then reported the pinned
Lean 4.22.0 commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

The fresh trusted preflight returned:

```text
status: KLEAN_NO_OBLIGATIONS
obligation_count: 0
target: null
designated_sorry_count: 0
lake clean: exit 0, empty output
lake build: exit 0, Build completed successfully.
```

The fresh build-output SHA-256 is
`d5eb4147211a1d23bc3d864380d1505e64d582f543d796d2a929297edce00c15`,
identical to the previously recorded preflight hash. A subsequent trusted
classification-only final gate also returned `PASS`, bound the complete signed
input hash set, reported no candidate and no used axioms, and repeated the
successful fresh preflight. The mechanical tool deliberately reports semantic
classification as not evaluated; the rule-by-rule semantic judgment above is
this audit's independent evaluation.

The generated project contains 45 allowlisted executable hook declarations and
zero proof holes; the trusted preflight independently rejects proposition
trust. With no generated proposition and no Stage 5 proof, `Proof.final`,
`#print axioms`, proof identity, and candidate operational-bridge checks do not
exist in this mode and were correctly not fabricated.

## Evidence index

- Producer hashes and image binding: `evidence/02-producer-manifests.txt`,
  `evidence/03-producer-tree-identity.txt`
- Canonical inventory and Stage 3 contract comparison:
  `evidence/05-canonical-rule-inventory.txt`
- All recorded hashes and all Stage 1 per-file hashes:
  `evidence/06-recorded-hash-verification.txt`
- Initial preflight/toolchain diagnosis and transparent recovery:
  `evidence/07-fresh-klean-preflight.txt` through
  `evidence/10-lean-proc-shim-test.txt`
- Successful fresh required preflight:
  `evidence/11-fresh-klean-preflight-with-shim.txt`
- Frozen operational-semantics rules:
  `evidence/12-operational-semantics-excerpts.txt`
- Summary, adversarial-state, and counterfactual checks:
  `evidence/13-summary-recurrence-checks.txt`
- Independent inventory/obligation/target bijection:
  `evidence/14-inventory-bijection-target.txt`
- Signed classification-only mechanical gate:
  `evidence/15-classification-only-mechanical-gate.txt`
- HumanEval contract, source solution, and fixed K claim:
  `evidence/16-problem-contract-and-fixed-claim.txt`

The audit helper sources are preserved beside the transcripts as
`verify_recorded_hashes.py`, `audit_inventory_and_bijection.py`,
`check_summary_recurrences.py`, and `proc_exe_readlink_shim.c`.

VERDICT: PASS
LEGITIMACY: LEGIT
