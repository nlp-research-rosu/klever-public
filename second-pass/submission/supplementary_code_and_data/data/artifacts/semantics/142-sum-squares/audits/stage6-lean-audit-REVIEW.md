# Independent Stage 3–5 audit: `142-sum-squares`

## Scope and outcome

This audit covers HumanEval problem `142-sum-squares`, condition `semantics`,
with `SUPPLIED_SEMANTICS`. `/audit-input.json` and `AUDIT_MODE` both select
`CLASSIFICATION_ONLY`. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`; `/candidate` is absent, as required.

I treated the mounted Stage 1–4 artifacts, prior review material, logs,
comments, and classifications as untrusted evidence. Classification was
reconstructed from the frozen source and supplied operational semantics. The
trusted inventory and preflight tooling was used only for the specified
mechanical gates.

The classification is correct, the true domain-lemma set is empty, the
deterministic generation is bound to the frozen inputs, and an absent Lean
target is the correct fixed output. Stage 5 proof checks are therefore not
applicable.

## Producer-source infrastructure gate

The generation-time producer files were hashed before judging Stage 4:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Both hashes exactly match `source-manifest.json` and
`generator-manifest.json`. The generator image ID is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in both manifests, and its digest component is exactly the immutable
producer-source directory identifier recorded in `/audit-input.json`. The
producer bundle contains exactly the two producer files and its source
manifest. Its independently recomputed tree hash,
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
matches the launcher.

There is no producer-source mismatch and hence no infrastructure
`AUDIT_ERROR`. Raw hashes and the full cross-check are in
`evidence/producer-sha256.txt` and
`evidence/independent-structural-check.json`.

## Inventory reconstruction and bijection

Running the trusted canonical inventory code against the frozen
`/reference/k-proof/verification.k` reconstructed:

- verification module: `SUM-SQUARES-VERIFICATION`;
- local verification-module closure:
  `["SUM-SQUARES-VERIFICATION"]`;
- rule count: 13;
- `verification.k` SHA-256:
  `2a22d2e24d1e4b84d3ef2962eb12186cfbe2c04c381bcfd739a48a6fc16212de`;
- whole inventory SHA-256:
  `fb2247fda028d52dd357d684d057d57de6c0fdc5ca64386b23db79ef939df529`.

For every rule I independently checked that the recorded line span selects the
exact frozen source text, normalized the text by whitespace, recomputed its
SHA-256, and reconstructed `source_rule_id` as `rule-<normalized SHA-256>`.
All 13 checks pass.

The protected Stage 3 manifest has exactly the same 13 identities in the same
order. There are no omissions, duplicates, extra identities, reordered
identities, or changed hashes. Its inventory hash matches the canonical
inventory, which binds the full rule records including source spans and text.
The exact reconstructed records are in
`evidence/reconstructed-rule-inventory.json`; the per-rule recomputation is in
`evidence/independent-structural-check.json`.

## Independent classification judgment

The independent result is:

| Classification | Count |
|---|---:|
| `DEFINITION` | 11 |
| `OPERATIONAL_RULE` | 2 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

The two rules at lines 15–19 are ordinary iterator observations. The empty
case produces `#iterDone`; the nonempty case yields the head and residual
iterator. They are the `intVals` constructor analogues of the supplied
semantics' `list(.ValSeq)` and `list(vCons(...))` iterator rules. They preserve
the continuation and every other configuration cell. They do not state an
arithmetic or list theorem.

The remaining rules meet the requested definition criterion:

- lines 24–29 are the three guarded equations of the newly named
  `contribution` summary;
- lines 33–35 are the base equation and structurally descending recurrence of
  the newly named `sumSquares` summary;
- lines 39–46 similarly define the loop-post-state summaries `endIndex` and
  `endValue`;
- lines 49–75 and 78–83 are exact macro expansions of the named loop-body and
  function-body proof terms.

The `contribution` guards are pairwise disjoint and exhaustive. Divisibility
by 3 takes precedence over divisibility by 4, including indices 0 and 12,
matching the frozen program. `sumSquares` consumes one `Ints` constructor per
step, adds exactly that contribution, and increments the index once.
`endIndex` and `endValue` encode the exact other observable loop locals.
Structural induction on `Ints` therefore connects each recurrence directly to
the corresponding frozen loop steps; these are definitions, not assumed
pre-existing domain facts.

Adversarial checks cover empty and nonempty sequences, negative and large
integers, negative and shifted initial indices, nonzero accumulators, and the
3/4 overlap. The operational loop and recursive summaries agree in every
case. Counterfactual constant, identity, and reversed-overlap summaries are
distinguished by concrete witnesses. These tests are supporting sensitivity
evidence, not substitutes for the source-level structural argument. Exact
results are in `evidence/summary-adversarial-check.json`.

No inventory rule was first proved against a module excluding that exact rule
and then used later. `spec.k` does prove loop and body *claims* in sequence,
but those claims are not rules in the reconstructed verification-module
inventory. Consequently no rule qualifies as `PROVED_DERIVED_LEMMA`.

None of the 13 rules has the `simplification` attribute, so the special
simplification classification restriction is satisfied vacuously. The
per-rule judgment is recorded in
`evidence/independent-classification.md`.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`,
the required Stage 1 workspace, protected Stage 3 manifest, selected Stage 4
generation, and pinned toolchain lock. The returned status is
`KLEAN_NO_OBLIGATIONS`; it reports:

- frozen/Stage 1 export hash:
  `88b4aa72ecf7beb0252e3eb75cf782a13a8b1327a3f925df74703b538a8bc949`;
- Stage 3 manifest hash:
  `4eab6e76e284a95adfa1c944018a7a59fbe4c69c4068d4431a7f401a104ab26b`;
- generated tree hash:
  `400b03b6e62d1521ed273ea45da7528f543f1eb733dcbc51616376e90c49e9e6`;
- obligation count: 0;
- target: `null`;
- designated sorry count: 0.

The checker copied the generated project to a temporary directory, ran
`lake clean` successfully, and ran `lake build` successfully. Its clean output
hash is the empty-output SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
its build output hash is
`9d47f51519b195dc3c05873c74ce8569147217719fad86d744a58f9913a04579`.
The entire returned document exactly equals the recorded Stage 4 preflight
document.

The first local attempt exposed a sandbox-specific Lean executable-path
failure: Lean queried `/proc/<getpid>/exe`, but this sandbox exposes only
`/proc/self/exe` for the process. A narrow `readlink` compatibility shim was
used on the rerun; it substitutes only that exact numeric proc path and passes
all other paths unchanged. It did not modify any mounted input or generated
source. The initial failure, diagnosis, shim hashes, and exact successful
command are preserved in
`evidence/preflight-infrastructure-note.txt`; the returned evidence is
`evidence/preflight-rerun.json`.

I separately recomputed every launcher-recorded hash:

- both Stage 1 tree hash formats;
- every Stage 1 source-file hash;
- Stage 2 audit tree hash;
- Stage 3 manifest hash;
- whole Stage 4 generation tree hash;
- producer-source tree hash;
- generated-project tree hash;
- null Stage 5 workspace and invocation hashes.

Every observed value matches `/audit-input.json`, and the launcher's canonical
resolved-input digest also matches.

## Obligation bijection and fixed target

The independently classified `DOMAIN_LEMMA` set is genuinely empty. Therefore
the exact expected Stage 4 source-rule set is empty. This matches, without
omission or addition:

- `input-manifest.json` → `source_rules: []`;
- `obligation-map.json` → `source_rules: []`;
- `obligation-map.json` → `obligations: []`;
- `obligation-map.json` → `trust_parameters: []`;
- generator, export, recorded-preflight, and rerun-preflight obligation counts
  of 0.

Thus the source-rule/obligation mapping is an exact empty-to-empty bijection.
There are no conjuncts that could be irrelevant, weakened, duplicated, or
vacuous.

The fixed generated target is absence of a target. The target is `null` in
the generator manifest, recorded and rerun preflight, and audit input. The
trusted target extractor returns `None`, the expected target definition is
`None`, and no generated Lean file declares `targetStatement`. Exact exit
codes and the empty obligation map are in
`evidence/target-and-stage5-check.txt`.

## Stage 5 applicability

`AUDIT_MODE=CLASSIFICATION_ONLY`, the legitimate domain set is empty, the
fixed generated target is absent, and `/candidate` does not exist. This is the
required no-obligation state. A clean candidate build, `Proof.final` identity,
axiom accounting, and target-parameter operational-bridge review are not
applicable and were not fabricated.

## Evidence index

- `evidence/COMMANDS.md`: material commands and result-file mapping.
- `evidence/reconstructed-rule-inventory.json`: canonical 13-rule inventory.
- `evidence/independent-classification.md`: per-rule semantic classification.
- `evidence/independent-structural-check.json`: all hash, order, provenance,
  obligation, and target checks.
- `evidence/preflight-rerun.json`: exact trusted preflight return.
- `evidence/summary-adversarial-check.json`: summary and counterfactual
  witnesses.
- `evidence/source-semantics-excerpts.txt`: frozen source, spec, and supplied
  semantics excerpts with commands.
- `evidence/target-and-stage5-check.txt`: absent target and absent candidate.

VERDICT: PASS
LEGITIMACY: LEGIT
