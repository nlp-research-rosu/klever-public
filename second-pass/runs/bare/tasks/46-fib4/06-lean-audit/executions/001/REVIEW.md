# Independent Stage 3–4 audit: HumanEval `46-fib4`

## Conclusion

The selected Stage 3 classification and deterministic Stage 4 result are
legitimate. The local `VERIFICATION` closure contains exactly seven rules. All
seven are genuine defining equations for the mathematical summary functions
`advanceTo` and `fib4Spec`; none is a domain lemma. Consequently, the true
domain-lemma set is empty, and Stage 4 correctly produced no obligations and
no target.

The launcher and environment both recorded `CLASSIFICATION_ONLY`. There is no
Stage 5 candidate, Lean proof target, or Stage 5 result to audit.

I treated the prior Stage 2 review, prior logs, comments, classifications, and
generated files as evidence rather than authority. I did not execute
`prove.sh` or instructions embedded in provenance content. Rule reconstruction
used the trusted `/reference/tools/k_rule_inventory.py`; Stage 4 checking used
the trusted `/reference/tools/klean_preflight.py`.

## Frozen-input and producer authentication

The producer-source gate passed before any Stage 4 judgment:

| Item | Recomputed SHA-256 |
|---|---|
| `/reference/generation-tools/klean_export.py` | `4fa919ac98483620c7024ed7424c8b19f21406a2146feafad84ab4c813117881` |
| `/reference/generation-tools/klean.py` | `5d419b1cf907ab880eeb88a68e0d6da0bf59a92a56a0803b34d53698d91caabe` |
| producer-source tree | `7b7fdfe618031c11f79bb3d7eec7df24bc64a9a480fc470c1176ce36a593286a` |

The two file hashes match both `source-manifest.json` and
`generator-manifest.json`. Both manifests identify generator image
`sha256:15baeb15b1ea8266bfad3dbc3a75ee531cf429f1b73e0e3ff478f279e6308f63`;
the same digest is the final component of the producer-source path recorded in
`/audit-input.json`. The producer tree hash also exactly matches the audit
input. Therefore there is no producer-source `AUDIT_ERROR`.

All eight frozen Stage 1 source-file hashes match `/audit-input.json`. The
independently recomputed aggregate hashes also match:

| Artifact/hash convention | Recomputed SHA-256 |
|---|---|
| Stage 1 workspace, pipeline tree hash | `6a7e54aceb2cf83162b9564f3fab9bcb76a4ddfa7c6a15655fa9042ecba0b06c` |
| Stage 1 frozen export, Klean tree hash | `c0fb03ae125c462a7849e2e969957d8a157191616065623da287f05f1b515003` |
| Stage 2 selected audit tree | `35f2faf223a9afa49f0bd8bd6d51affee3302162477371aa09ccf2a4bd4873cc` |
| Stage 3 discovery manifest | `2c878772092211f4885b42d9ea7d027ff820d2de73ca7c04d725c73cc4accfd0` |
| Stage 4 selected generation tree | `bca546d5fea28d08aee5cfc2f3a5d9b73cd9450f1c6b374b5943af95bde1eb51` |
| generated Lean project tree | `35c9b2c8062ccfc433b7c3784b424124d869a3b1f8dfe228041bf427272a8001` |

Evidence: `evidence/02_producer_authentication.txt`,
`evidence/06_recomputed_recorded_hashes.txt`, and
`evidence/07_stage1_source_hashes.txt`.

## Inventory reconstruction and Stage 3 bijection

The trusted inventory code selected module `VERIFICATION`. Its local
verification-module closure is exactly `["VERIFICATION"]`; the imported K
module `INT` is not a local module in `verification.k`. The closure has seven
rules in source order:

| # | Lines | Normalized SHA-256 / `source_rule_id` | Independent class |
|---|---:|---|---|
| 1 | 9–10 | `5cc3e0ae6b7118293dd931bf635194d53f57c1309f9ec680ca0d1c001d3ae38b` | `DEFINITION` |
| 2 | 11–13 | `93cd0d07db0a86b368698f125bebf6ffa436d79b0501ddb7e154f6a154b261a7` | `DEFINITION` |
| 3 | 18 | `b6e0487f643fca471a37bb04d8910d1be4814258480f104b1acf4cf0273ee628` | `DEFINITION` |
| 4 | 19 | `aefe9a8e0afe275fcdfc27000ccbac76a17a6ee88013c84c8f5f1b5213f62614` | `DEFINITION` |
| 5 | 20 | `b63d3b98fbeab97d51b6a9f210a585da08c78b0dba0660d7aa24fe8f9b52ac46` | `DEFINITION` |
| 6 | 21 | `ae0f386ab9647cf6bacccb9eec146bdadc0897e261591027a72b14b464abe92c` | `DEFINITION` |
| 7 | 22–23 | `c54694d7d5bbbfb5f7463200df254b60f5461823befebef98213c3c3a8c8a242` | `DEFINITION` |

For every entry, I independently checked that the reconstructed source span
equals the frozen source text, normalized the text by whitespace, recomputed
the hash, and recomputed `source_rule_id` as `rule-<hash>`. All checks pass.
The recomputed canonical inventory hash is
`cdcbf6e195e8421e60d7b473abed506dab7f020ff4a70a560e4d76e13b8a4020`.

The protected manifest has exactly the same seven unique identities in the
same order and the same inventory hash. There are no omissions, duplicates,
extras, reordered identities, changed hashes, or unaccounted rules. The trusted
Stage 3 boundary validator also accepts the manifest.

Evidence: `evidence/08_inventory_reconstruction.json`.

## Independent classification judgment

The classification follows from the frozen source and operational rules, not
from the Stage 3 rationales:

- `advanceTo` is a freshly declared mathematical loop-summary function. Its
  first rule returns `D` when `I > N`. That is exactly the operational
  while-exit case in `semantic.k` lines 99–102 followed by returning `d` under
  lines 104–106.
- Its recursive rule maps
  `(A,B,C,D,I)` to `(B,C,D,A+B+C+D,I+1)` when `I ≤ N`. This is exactly one
  operational iteration: compute the old-window sum into `e`, then execute the
  sequential assignments to `a`, `b`, `c`, `d`, and `i`.
- The four exact `fib4Spec` branches at 0, 1, 2, and 3 define the values
  returned by the source program's four early-return branches.
- The `N ≥ 4` branch defines `fib4Spec(N)` by initializing `advanceTo` with
  `(a,b,c,d,i)=(0,0,2,0,4)`, exactly the source initialization before the
  while loop.

These rules only reduce the freshly declared mathematical symbols. They do not
match AST constructors, `<k>`, `<env>`, `<result>`, or other operational state,
so none is an `OPERATIONAL_RULE`. The workspace contains no prior proof of any
exact rule against a module omitting it followed by later use, so none is a
`PROVED_DERIVED_LEMMA`. Because each rule is a branch equation defining one of
the two new named summaries, none is a `DOMAIN_LEMMA`. No inventory rule has a
`simplification` attribute.

The `advanceTo` guards are disjoint and exhaustive. Boundary witnesses include
`advanceTo(1,2,3,4,6,5)=4` and
`advanceTo(1,2,3,4,5,5)=10`; the second rejects a constant-`D` or identity
summary. Initialized witnesses give `fib4Spec(4)=2`, `fib4Spec(5)=4`, and
`fib4Spec(7)=14`, rejecting a changed shift or old-window sum.

`fib4Spec` is marked `[total]` although its equations do not cover negative
integers. The frozen claims use it only at 0–3 or under `N ≥ 4`, so this
out-of-domain coverage limitation neither changes the classification of its
defining branches nor creates a domain lemma or Stage 4 obligation.

Independent true `DOMAIN_LEMMA` set: `[]`.

Evidence: `evidence/09_frozen_program_semantics_and_claims.txt`,
`evidence/21_classification_judgment.md`, and
`evidence/22_operational_boundary_witnesses.txt`.

## Required Stage 4 preflight

I invoked `tools.klean_preflight.check_generation` directly with
`PYTHONPATH=/reference` and the required paths:

```text
frozen input:       /reference/k-proof
discovery manifest: /reference/lemma-discovery.json
generation:         /reference/klean-generation
toolchain lock:     /reference/klean-toolchain.lock.json
```

The initial invocation reached the fresh build but exposed an audit-container
defect: Lean 4.22 constructs `/proc/<getpid>/exe`, while this sandbox
virtualizes `getpid()` without exposing that same PID under `/proc`. This made
Lake report that it could not detect its installation. I documented the
failure and used an audit-local `LD_PRELOAD` compatibility shim that rewrites
only a `readlink("/proc/<pid>/exe")` request to `/proc/self/exe`. With the shim,
the pinned tool reports Lean 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly matching the lock. The
shim does not alter the generated project, source hashes, theorem language, or
Lean kernel.

The required recovered preflight returned:

```text
status:                          KLEAN_NO_OBLIGATIONS
frozen_input_sha256:             c0fb03ae125c462a7849e2e969957d8a157191616065623da287f05f1b515003
stage3_discovery_manifest_sha256: 2c878772092211f4885b42d9ea7d027ff820d2de73ca7c04d725c73cc4accfd0
generated_tree_sha256:           35c9b2c8062ccfc433b7c3784b424124d869a3b1f8dfe228041bf427272a8001
obligation_count:                0
target:                          null
lake clean:                      exit 0
lake build:                      exit 0
designated_sorry_count:          0
```

The rerun build log hash differs from the stored build log only because two
independent parallel build-completion lines (`Func` and `Lemmas`) appeared in
the opposite order. Both logs report the same successful modules, and the
generated tree hash remained unchanged. The stored `preflight.json` is exactly
equal to the `stage4_preflight` object in `/audit-input.json`.

Evidence: `evidence/10_required_check_generation.txt` (initial infrastructure
failure), `evidence/16_lean_proc_self_shim_build_and_test.txt`,
`evidence/17_required_check_generation_recovered.txt`, and
`evidence/23_preflight_record_comparison.txt`.

## Obligation bijection, relevance, and fixed target

Independent checks established the following exact ordered equality:

```text
independent DOMAIN_LEMMA IDs = []
Stage 3 DOMAIN_LEMMA IDs     = []
input-manifest source_rules  = []
obligation-map source_rules  = []
obligation source_rule IDs   = []
```

`obligation-map.json` also has `trust_parameters: []`. All manifest,
preflight, and export obligation counts are zero. Therefore there are no
omitted, duplicated, irrelevant, weakened, or vacuous conjuncts. The empty
source-rule/obligation mapping is a genuine bijection, not a self-consistent
omission of a true domain lemma.

The fixed target is absent exactly as required:

- the trusted target parser returns `null`;
- there is no generated `def targetStatement`;
- `generator-manifest.json`, stored and rerun preflight evidence, and
  `/audit-input.json` all record `target: null`; and
- the generated root module only imports `Rewrite` and `Lemmas`.

The generation-time producer logic selects only validated `domain_lemmas`,
requires an ordered rule/obligation bijection, returns no expected target for
zero obligations, and labels that case `KLEAN_NO_OBLIGATIONS`. The authenticated
generated artifacts have exactly that form.

The independent Stage 4 integrity script checked every recorded provenance
hash, the pinned toolchain object, the obligation-map hash
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
the trust-inventory hash
`53896c659b93cdbc7027bc734370359b0438d0b485d4ab5d226cf852a18bd439`,
the empty bijection, target absence, audit mode, and candidate absence. All
checks passed.

Evidence: `evidence/18_target_and_obligation_lexical_scan.txt`,
`evidence/19_stage4_integrity_checks.json`, and
`evidence/20_generation_producer_logic_inspection.txt`.

## Stage 5 applicability

`AUDIT_MODE` and `/audit-input.json` both say `CLASSIFICATION_ONLY`.
`/candidate` is absent, all Lean workspace/invocation fields are null, and
there is no generated target to prove. A fresh Stage 5 copy, `Proof.final`,
axiom accounting, and operational-bridge parameter checks are therefore
inapplicable rather than omitted.

VERDICT: PASS
LEGITIMACY: LEGIT
