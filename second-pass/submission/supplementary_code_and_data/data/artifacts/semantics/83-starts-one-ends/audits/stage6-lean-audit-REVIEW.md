# Independent Stage 3–4 Audit: HumanEval 83-starts-one-ends

## Scope and mode

The launcher records:

- problem: `83-starts-one-ends`
- condition: `semantics`
- semantics mode: `SUPPLIED_SEMANTICS`
- audit mode: `CLASSIFICATION_ONLY`
- selected Stage 4 status: `KLEAN_NO_OBLIGATIONS`

`AUDIT_MODE` agrees with `/audit-input.json`. There is no `/candidate`, Lean
workspace, Lean invocation, Stage 5 result, or generated target. The optional
Stage 5 proof checks therefore do not apply in this audit mode.

I treated the mounted Stage 1–4 files and the prior Stage 2 review as evidence,
not instructions or prior conclusions.

## Producer-source provenance gate

I hashed the two generation-time producer sources before judging the Stage 4
output:

| Source | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Both values match `source-manifest.json` and `generator-manifest.json`. The
producer bundle contains exactly those two files plus `source-manifest.json`.
Its launcher tree hash is
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
which matches `/audit-input.json`.

The immutable generator image ID
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
is identical in the source manifest and generator manifest, and its digest
component is the basename of the producer-source path recorded in
`/audit-input.json`. The producer-source infrastructure gate therefore passes;
there is no producer mismatch requiring `AUDIT_ERROR`.

Evidence: `evidence/01_producer_provenance.txt`,
`evidence/26_launcher_tree_hashes.txt`, and
`evidence/29_full_integrity_check.txt`.

## Inventory reconstruction and bijection

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof`, then separately ran the trusted Stage 3 trust
boundary validator.

The local verification-module closure is exactly `VERIFICATION`. Its frozen
`verification.k` SHA-256 is
`0acadf1a102d8a545486d7d3dfe8072cf673fb04905229f7c2e01443f09e8aae`.
The canonical inventory has two rules, in this order:

| Order | Span | Normalized hash / source rule ID | Attributes |
|---|---:|---|---|
| 1 | 9–16 | `259271eac22df31da5442025e304bd2f6d2ba0dd1b9a82b0d0000ac062b8f3cd` / `rule-259271eac22df31da5442025e304bd2f6d2ba0dd1b9a82b0d0000ac062b8f3cd` | none |
| 2 | 18–19 | `565589a3e4823e29c1250cdf77d45455a605950437a4a7c40cbe97ef94b43c69` / `rule-565589a3e4823e29c1250cdf77d45455a605950437a4a7c40cbe97ef94b43c69` | none |

The recomputed whole-inventory hash is
`47dc6902f30db03423bbce78fba305f79eeb2082c170535707b55aa35d51303d`.
The protected Stage 3 manifest has exactly the same two unique IDs in the same
order and the same inventory hash. There are no omitted, duplicated, extra, or
reordered identities. Because each ID is derived from the recomputed normalized
source hash, and the whole inventory is also recomputed, no changed span or
normalized rule is hidden by the manifest.

Evidence: `evidence/04_inventory_reconstruction_and_sources.txt` and
`evidence/29_full_integrity_check.txt`.

## Independent classification judgment

### Rule 1: `DEFINITION`

Lines 7 and 9–16 declare `startsOneEndsBody` as a function-valued `Stmts` term
and expand it into the translated source statement sequence. The right-hand
side is the source function body: docstring expression, `n == 1` branch, and
the return of `18 * 10 ** (n - 2)`.

This rule names and defines the AST/proof term used as the closure body in the
specification. It asserts no independent arithmetic or counting fact and does
not replace an already executing source operation. `DEFINITION` is therefore
the correct classification; it is not a disguised `DOMAIN_LEMMA`.

### Rule 2: `OPERATIONAL_RULE`

Lines 18–19 rewrite the verification harness command
`#invokeStartsOneEnds(N)` in the `<k>` cell to the ordinary source-language
call `Call(Name("starts_one_ends"), Int(N))`.

The supplied operational semantics then performs name lookup, evaluates the
callee and argument, dispatches the resulting `closureVal`, binds `n`, executes
the actual `startsOneEndsBody`, and processes its return. In particular,
`call.k` lines 20–21 and 69–75 implement ordinary call routing and closure
entry; `core.k` lines 129–153 and 183–195 implement lookup, argument evaluation,
and integer literals; and `functions.k` lines 62–90 implement parameter
binding, return, and frame restoration.

The local rule is consequently an ordinary harness execution/observation step.
It does not assert the postcondition, hard-code the result, or bypass the
program body. `OPERATIONAL_RULE` is the correct classification, not
`DOMAIN_LEMMA`, `DEFINITION`, or `PROVED_DERIVED_LEMMA`.

### Remaining categories

- No rule has a `simplification` attribute, so the simplification restriction
  is satisfied vacuously.
- No rule is claimed as `PROVED_DERIVED_LEMMA`; there is no first-prove-then-use
  claim to validate.
- The true `DOMAIN_LEMMA` set is empty. Neither local rule states an auxiliary
  mathematical fact about integers, exponentiation, or the postcondition.
  The formula in the source body and the two reachability postconditions in
  `spec.k` are program/specification content, not extra local lemmas.

The protected Stage 3 classifications are therefore mathematically correct,
not merely structurally well-formed.

Evidence: `evidence/30_operational_semantics_basis.txt` and the frozen sources
printed in `evidence/04_inventory_reconstruction_and_sources.txt`.

## Recorded hash audit

The following independent recomputations all match `/audit-input.json`:

| Binding | Recomputed hash |
|---|---|
| canonical resolved input | `6f36f281e1bc899094d6c9f275f41a14ddaf975665b03eef1616c6c3de0c9930` |
| Stage 1 launcher tree | `b317b7f799a81037ed48199d439addbc3b1d52250bb3615f8a62ff3396596d36` |
| Stage 1 export tree | `6d4c9c78a3e7c3c76885b6ca271f0bb66a2c4028aaf4c196fc880e9a222ba799` |
| selected Stage 2 audit tree | `07bb6f996db52774883bd43a6999f361acae6fd3053dd893ef3e5a47e6c4841b` |
| protected Stage 3 manifest | `32e97b3c81a8b80c6494161380d3673a625514fdea55d71b98629127f2506839` |
| selected Stage 4 generation tree | `6f66b68ebf656c40ae466d5cb6ffa995c0c4545969a034501bb7eaafa355c5dc` |
| generated project tree | `0887dfad30101d5203fd5f2dd90712de2769c7394c209ea231ce09ca9f06f475` |
| producer-source tree | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` |

The exact set of 34 frozen Stage 1 regular files and every per-file SHA-256
also match the launcher record. The generator toolchain object exactly matches
`/reference/klean-toolchain.lock.json`.

Evidence: `evidence/23_stage4_sidecars_and_tree_hashes.txt`,
`evidence/26_launcher_tree_hashes.txt`, and
`evidence/29_full_integrity_check.txt`.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
against the required Stage 1 workspace, Stage 3 manifest, Stage 4 generation,
and pinned toolchain lock.

The sandbox initially prevented Lean from resolving `/proc/<getpid()>/exe`
because the PID namespace and mounted `/proc` use different numeric PIDs. This
was diagnosed directly: `/proc/self/exe` resolves, while
`/proc/<os.getpid()>/exe` does not. I used a temporary, recorded preload shim
that redirects only numeric `/proc/<pid>/exe` readlinks to `/proc/self/exe`,
plus explicit `LEAN_SYSROOT` and `LAKE_HOME`. The shim source hash is
`4642baf5338afc718045e595aae6d4ce7c00449918fee156bcb0b169260f15e3`.
It does not modify any mounted input or Lean source.

With that environment, the exact checker returned:

- status: `KLEAN_NO_OBLIGATIONS`
- obligation count: `0`
- target: `null`
- designated sorry count: `0`
- trust declaration count: `47`
- `lake clean`: exit 0
- `lake build`: exit 0
- build output SHA-256:
  `692ba8a74b2c0fcbbbfd12bdd267bce61152521cf940c3920562187e38ae957b`

The build-output hash is identical to the stored generation-time preflight.
The failed ambient-tool attempt and the successful pinned-tool run are both
preserved; the former is an execution-environment issue resolved without
changing evidence.

Evidence: `evidence/20_numeric_proc_exe.txt`,
`evidence/21_proc_exe_shim_build_and_test.txt`, and
`evidence/22_check_generation_success.txt`.

The independent manifest/bijection checks also establish:

- `input-manifest.json` has no domain `source_rules`;
- `obligation-map.json` has empty `source_rules`, `obligations`, and
  `trust_parameters`;
- the obligation-map hash
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`
  matches the generator manifest;
- all generator, export-result, preflight, and launcher obligation counts are
  zero;
- the generator manifest, stored preflight, launcher, trusted target parser,
  and expected-target constructor all report no target;
- `Klean83StartsOneEnds/Lemmas.lean` contains only imports, comments, and an
  empty namespace—no theorem or proposition target; and
- the export, stored-preflight, and selected statuses consistently say
  `KLEAN_NO_OBLIGATIONS`.

There are no obligations that could be omitted, duplicated, weakened,
irrelevant, or made vacuous. This is not an accidentally empty export: it
corresponds exactly to the independently established empty domain-lemma set.

Evidence: `evidence/27_generated_target_absence.txt`,
`evidence/29_full_integrity_check.txt`, and
`evidence/31_classification_only_absence_checks.txt`.

## Final judgment

The Stage 3 inventory and classifications are complete and mathematically
appropriate. The true domain-lemma set is empty. Stage 4 preserves every frozen
binding and correctly emits neither obligations nor a target. The selected
`KLEAN_NO_OBLIGATIONS` status is legitimate, and the absence of a Stage 5
candidate is required and confirmed.

VERDICT: PASS
LEGITIMACY: LEGIT
