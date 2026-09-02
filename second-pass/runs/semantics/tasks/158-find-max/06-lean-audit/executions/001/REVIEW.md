# Independent Stage 3–5 audit: HumanEval 158-find-max

## Scope and result

This audit covers condition `semantics`, semantics mode
`SUPPLIED_SEMANTICS`. The launcher and `AUDIT_MODE` both select
`CLASSIFICATION_ONLY`. Stage 4 selected `KLEAN_NO_OBLIGATIONS`; `/candidate`
is absent. Therefore no Stage 5 proof, `Proof.final`, candidate bridge
definition, or proof axiom audit exists or is required.

I did not rely on the prior Stage 2 review, Stage 3 rationales, generation
logs, or any earlier PASS. I treated the mounted material only as evidence.

## Frozen-input and producer provenance

Before evaluating Stage 4, I hashed the exact generation-time producer
sources:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Both hashes exactly match `generator-manifest.json` and
`generation-tools/source-manifest.json`. The generator image identity is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in both manifests, and the same digest is the producer-source bundle
component recorded by `/audit-input.json`. The complete producer bundle tree
hash is
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
also matching the audit input.

Using the trusted hash implementations, I recomputed every hash in
`resolution.hashes`, the signed resolved-input digest, and all 36 Stage 1
source-file hashes. There were no missing files, extra files, or mismatches:

| Binding | Recomputed value |
|---|---|
| Stage 1 pipeline tree | `ad41a1c00d2508d64faee2ddb56aad28eedab1f132a74ca3b58e97ac2830df66` |
| Stage 1 export tree | `0c81427694d371e8d7d7408bffaa802fc9d174c95ba2fc97f4a482a8297bc3d7` |
| Stage 2 selected audit tree | `054b3f14dafd45f8be59c1e317876dbb1a9a5147a123e139230bdae1eb7d09ca` |
| Stage 3 manifest | `6df120734149758befd27c5b9b5a2c704ce01a93b4eafd23fae9329c04d310c8` |
| Stage 4 selected generation tree | `0430acb3a00bce7238a5122a1df33b4189365db5c2d9f7d447f5d08cdf7da797` |
| Generated Lean project | `faab7fa85bf5c1f7d1f66d1d5c6c6b7724f69ca026273b8c5d3373cb389caf91` |
| Signed resolved-input digest | `88c3f484645da2c70ed9b30fef08663ceb5d3b2a9a6ff5d2320582e0a31998cd` |

Raw provenance and hash evidence is in
`evidence/01_producer_and_manifests.txt` and
`evidence/13_recomputed_input_hashes.txt`.

## Inventory reconstruction and Stage 3 bijection

I ran the trusted `tools.k_rule_inventory.inventory_verification` directly
against `/reference/k-proof`. It selected `VERIFICATION` from the final
`kompile verification.k --main-module VERIFICATION` command in `prove.sh`.
The local verification-file import closure contains only that module; imports
from the supplied semantics are external to the local `verification.k`
closure.

The trusted lexical reconstruction:

- found exactly 21 rules in source order;
- recomputed each physical source span;
- normalized each rule as whitespace-separated source text;
- computed `normalized_sha256` and
  `source_rule_id = "rule-" + normalized_sha256`;
- computed source file SHA-256
  `9f4420baf91dcdec08b27c3b890ab909cbc3c2570f68d8d1f7cce66b50eb740d`;
  and
- computed whole inventory hash
  `20b6358e762781800f25ce55eb5c0c191044c9e9a1b81cb80bf453a3cadc4c53`.

The protected Stage 3 manifest also has exactly 21 unique identities. Its
identity set and order exactly equal the reconstructed sequence. There are no
omitted, duplicated, extra, reordered, or hash-changed entries. The full
reconstructed rules are in `evidence/05_reconstructed_inventory.json`; the
ordered comparison is in
`evidence/06_stage3_manifest_and_bijection.txt`.

The complete independently classified inventory is:

| Span | Normalized SHA-256 | Independent class |
|---|---|---|
| 9 | `8a97167ed700fe79e5ce8c7cf4f0a748b637187276b44a56ac59818df6de750a` | `DEFINITION` |
| 10–11 | `74e985b86e8fa98ea2ec5af63f463cd7fdc2d96cb68a6ae0371b29001f04dda2` | `DEFINITION` |
| 16–17 | `cd6ef509382fed7c0119dcb3c5dc4ebcdb20606a4a6d0b7ce1645ea2e066db5f` | `OPERATIONAL_RULE` |
| 18–20 | `ccc2deae4fe3c31b889af14874a12ce7c7567dbef73330e3b69ca0cb0867cac2` | `OPERATIONAL_RULE` |
| 24–35 | `8575e9e73ea5e219a26043ba1d8d81a0fb85456d8d7f17a8787f0aa36a5ba31e` | `DEFINITION` |
| 38–44 | `46ff96898cf006ff7bed452e0ab20cbce46b04266cf2b22d5c66f1b559170a75` | `DEFINITION` |
| 51–52 | `461cebdae5fc7db026a47b62f6b16f31326f5189e1fd8bb83f25b2a154e93b70` | `DEFINITION` |
| 54–59 | `ae5b9c41dfcfa2ad78e81f4b15ab34f613fda7e2746b85a03b481c47ec8e7eaf` | `DEFINITION` |
| 61–67 | `d8ccc88ff0c525dac87014d236060434e6784e2b2ec8aa785c21d0559dce9e0e` | `DEFINITION` |
| 69–74 | `1cc52f8c469c59693ebbda8399c5299d2df33558de93fc3b38d18adfdab289d2` | `DEFINITION` |
| 76–82 | `072050bee94ae87364015f263ceb25372fa83fcdb6db57c02cdabcf781cb1e22` | `DEFINITION` |
| 85 | `1f2e1ca5351fbc95c15c4b43efc1eae254b21a7365bd16f743c49c09fe325fe6` | `DEFINITION` |
| 88 | `9f8778c763448e359bcfea0f37e817b501ce0cf9643627facca8094b05f44b6e` | `DEFINITION` |
| 92–95 | `c7c4ccbe54a0d2c5aa977f2c9dbf1c58fd09df82edc155aadc20828c1e3f9a10` | `DEFINITION` |
| 96–99 | `6422d38d27769a7b193f997df1645e0176fbfdf14ea9e5e3316894bb2d9acff3` | `DEFINITION` |
| 101–105 | `0795ae01ea1c6f9f389aa5dee3494e4de154fe8cae29849527ca1463506746d3` | `DEFINITION` |
| 106–110 | `853cdf6746fbbceb7cf556c5465407578ae7b498433409744a92ee39d1ef604a` | `DEFINITION` |
| 112–115 | `1c542b7b0bae997f37b8724555c49be7188a9420572dc89009d5339e74ebd37f` | `DEFINITION` |
| 116–119 | `36c5e124d990f388844b3cd8956387577b6a788a4a3bfcddc98bc7ce6fa69dfe` | `DEFINITION` |
| 121–125 | `32432040df177d54687be844abd7903526336d147bc84b05f4a344f2839d527e` | `DEFINITION` |
| 126–130 | `30c307f97eb5d63feb9aa91c727c1583724bc8d9daae3c80954115659025ca74` | `DEFINITION` |

The Stage 3 class matches every row. Exact per-rule reasoning is preserved in
`evidence/15_independent_classification_result.json`.

## Independent classification judgment

### Definitions

Lines 9–11 are the base and inductive recurrence defining the typed
`WordSeq` to MPY `ValSeq` encoding. Lines 24–35 and 38–44 are macros naming,
respectively, the exact translated loop body and function body from
`solution.mpy`.

Lines 51–82 define the mathematical `findMaxWords` accumulator. The empty
case returns its state. For a nonempty sequence, the score comparison
partitions integers into greater, smaller, and equal cases; the equal case is
then partitioned by `strLt` versus its negation. Each branch recurses on the
strictly smaller tail. Lines 85 and 88 define the two `BestState`
projections.

The eight `simplification` rules at lines 92–130 are also definitions: they
are the four branch recurrences for each of the named projections
`bestWord ∘ findMaxWords` and `bestScore ∘ findMaxWords`. In every case the
guard is identical to the corresponding defining `findMaxWords` branch, and
the right side is precisely that branch's right side under the same
projection. They introduce no independent mathematical property. They are
therefore definitional recurrence/unfolding rules, not unproved domain
lemmas. All simplification rules are classified as one of the permitted
classes.

### Operational rules

Lines 16–20 are ordinary iterator observations. The supplied `MPY-LIST`
semantics has:

- `#iterNext(list(.ValSeq)) => #iterDone`; and
- `#iterNext(list(vCons(V, R))) => #iterYield(V, list(R))`.

After one `wordVals` unfolding, the two verification rules have exactly these
left and right sides. They preserve the arbitrary continuation represented
by the `<k> ... </k>` frame, touch no other cells, and introduce no return,
exception, state, binding, or control effect. Their priority changes rule
selection but not the transition. They are operational observations, not
domain facts.

### No derived or domain lemmas

There are no claims in `verification.k` first proved without a later-added
rule and then reused, so the true `PROVED_DERIVED_LEMMA` set is empty. None
of the 21 rules states an additional domain theorem. The true
`DOMAIN_LEMMA` set is also empty.

All entries are relevant: `wordVals` and its iterator observations encode the
formal input and drive the loop; the body macros bind the exact program;
`findMaxWords` and both projections occur in the loop invariant and final
postcondition.

## Program and operational meaning

The source computes `unique = len(set(word))`, replaces the accumulator when
that value is greater, and on a tie replaces it exactly when `word < best`.
The supplied semantics implements these observations as:

- `set(str(CS)) = setV(dedupCodes(CS))`;
- `len(setV(DS)) = isLen(DS)`; and
- string `<` as `strLt` over code sequences.

Thus every summary branch mirrors the operational branch and the initial
state `best = ""`, `max_unique = 0`. Structural induction on `WordSeq`
establishes that the recurrence returns the same selected word and score as
the loop: the base states agree, and the exhaustive step cases perform the
same update before invoking the induction hypothesis on the tail.

As adversarial finite corroboration, an independently written operational
model and the four K recurrences agreed on all 2,801 sequences of length
zero through four over a seven-word universe containing empty words,
negative/zero/positive codes, repeats, and alternate orderings. Constant,
first-word, and raw-length mutations were each separated by concrete
witnesses. This testing is corroboration, not the universal justification;
the latter is the branch-exhaustive structural argument above. See
`evidence/42_summary_adversarial_check.py` and
`evidence/43_summary_adversarial_result.json`.

## Stage 4 generation and target identity

I reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` over
the required Stage 1 workspace, Stage 3 manifest, and selected Stage 4
generation.

The audit image initially exposed a sandbox-specific Lean launcher problem:
Lean's `IO.appPath` could not read `/proc/<pid>/exe`, so the first preserved
attempt failed at `lake clean` with “could not detect the configuration of
the Lake installation.” I diagnosed the exact pinned binary behavior and
used the source-recorded shim
`evidence/36_lean_app_path_shim.c`. It preserves normal `readlink`, and only
when the failed path is `/proc/*/exe` returns the kernel-provided `AT_EXECFN`.
It changes no Lean source, elaboration, kernel checking, or theorem content.
With the direct pinned Lean 4.22.0 toolchain and this compatibility shim,
the required preflight completed:

- `lake clean`: exit 0;
- `lake build`: exit 0;
- status: `KLEAN_NO_OBLIGATIONS`;
- obligation count: 0;
- target: `null`;
- immutable Stage 1, Stage 3, and generated-tree hashes unchanged; and
- generated trust declarations: 47, with zero generated sorries and no
  proposition trust admitted by the preflight policy.

The failed first run is in `evidence/16_rerun_klean_preflight.txt`; the
diagnosis, shim source/hash, pinned Lean version, and successful returned
evidence are in `evidence/17_lean_environment_diagnosis.txt`,
`evidence/37_compile_and_test_lean_shim.txt`, and
`evidence/38_rerun_klean_preflight_repaired.txt`.

I then checked the Stage 4 bindings separately:

- independently classified domain IDs: `[]`;
- `input-manifest.json` source rules: `[]`;
- `obligation-map.json` source rules: `[]`;
- generated obligations: `[]`;
- trust parameters: `[]`;
- obligation-map SHA-256:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- trust-inventory SHA-256:
  `7aa2c2d744e695915c960c816dc5de6c7055cf1b7d43285f972c6dd7b16a3ca9`;
  and
- generator manifest, Stage 4 preflight, and audit input targets: all `null`.

`Klean158FindMax/Lemmas.lean` contains imports and an empty namespace, with
no definition, lemma, theorem, axiom, or opaque target declaration. There is
therefore no omitted or duplicated obligation, no weakened or irrelevant
conjunct, no vacuous target, and no target change. The fixed generated target
is correctly absent because the true domain set is genuinely empty.

The independent Stage 4 report is
`evidence/40_independent_stage4_integrity.txt`. Finally, the trusted
end-to-end mechanical gate returned `PASS` in `CLASSIFICATION_ONLY` mode
with the signed input binding unchanged, no candidate, `target: null`, and
`used_axioms: []`; see `evidence/46_trusted_final_gate.txt`. Its
`semantic_classification` is intentionally `NOT_EVALUATED`; the semantic
classification is the independent analysis above.

## Stage 5

Stage 5 is not applicable. `AUDIT_MODE` is `CLASSIFICATION_ONLY`,
`KLEAN_NO_OBLIGATIONS` has no generated target, and `/candidate` does not
exist. Running candidate clean-build, `#print axioms Proof.final`, target
shadowing checks, or parameter operational-bridge checks would invent a
proof candidate outside the signed audit scope.

VERDICT: PASS
LEGITIMACY: LEGIT
