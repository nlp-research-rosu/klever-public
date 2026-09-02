# Independent Stage 3–5 audit: `102-choose-num`

## Scope and result

I audited HumanEval problem `102-choose-num`, condition `bare`, semantics mode
`GENERATED_SEMANTICS`. The launcher record and `AUDIT_MODE` both select
`CLASSIFICATION_ONLY`. I treated the Stage 1 workspace, prior audit, Stage 3
manifest, Stage 4 output, logs, and comments as untrusted evidence. In
particular, I did not adopt the prior Stage 2 verdict or use its review to make
the classification decision.

The Stage 3 rule inventory is complete and correctly classified. Its true
`DOMAIN_LEMMA` set is empty. Stage 4 therefore correctly produced no
obligations and no target proposition, and there is no Stage 5 candidate.

## Launcher and frozen-input integrity

`tools.klean_audit_contract.verify_stage6_audit_input` accepted
`/audit-input.json`. The recomputed resolved-input hash is
`744632f5c97d307d3a446f44f5a7a8247cf2d48fbba855383574edcc5ff8e3dd`,
equal to the launcher record. The document and environment both say
`CLASSIFICATION_ONLY`; the problem, condition, and semantics mode are
`102-choose-num`, `bare`, and `GENERATED_SEMANTICS`.

I independently recomputed the relevant file and tree hashes with the trusted
hash routine appropriate to each artifact:

- Stage 1 selected workspace:
  `16f74ef009145081c921bec498a10a3da9131a76862c77b99adf98ec85997397`.
- Stage 1 deterministic-export tree:
  `ce7fd975f57da7b5082badbb3ab169b5f247a0806bdd1dd72d0442299f5fd0fa`.
- `verification.k`:
  `c96f7964b047c580f9712898be91167f370b1cd4c607dd37cbd51f314699fba3`.
- Stage 3 manifest:
  `9388b38c5a7e728878c8e7d1d3bfb7889218a7590990544c594efb9d3cff3f8c`.
- Selected Stage 2 audit tree:
  `90a3a3f266f45e54a087e1ac8d5ef7d89ceff08a97c14cd3680c8d12d78eb161`.
- Selected Stage 4 generation tree:
  `38231d7c1842835487591c0797ed098ff431b70849789cde85f89827b5f6f03b`.
- Generated Lean project:
  `c6580987e39d9fd9dba655de6236e958f88029e92cd58a80321b080a9ca03ca2`.

All eleven launcher-recorded Stage 1 per-file hashes also match. The generated
tree hash agrees independently with the generator manifest, export result,
recorded preflight, and audit input. The Stage 1, Stage 3, inventory,
obligation-map, and trust-inventory hashes agree across their corresponding
manifests. Evidence: `evidence/13_hash_bijection_target_audit.txt` and
`evidence/18_audit_input_integrity.txt`.

## Rule-inventory reconstruction

I ran the trusted canonical rule-inventory implementation against the frozen
Stage 1 workspace. `prove.sh` selects `VERIFICATION` as the main module.
Within `verification.k`, the local import closure contains only
`VERIFICATION`; its `MPY` import is defined in the separately required
`semantic.k`, not in another local module in `verification.k`.

The reconstructed inventory contains exactly four rules and has whole-inventory
hash
`5e56186dee5df02a7f60717fcba3070dbc99526b9662366e1d7a11886b6a6c57`.
For every rule I independently recomputed the source span, whitespace-normalized
SHA-256, and `source_rule_id`:

| Span | Normalized hash / source rule ID | Independent classification |
|---|---|---|
| 5–18 | `07c48bd418c1f380b592ff32808bf84ee7148c6cb962214c1eb5e62fb1389d2d` / `rule-07c48bd418c1f380b592ff32808bf84ee7148c6cb962214c1eb5e62fb1389d2d` | `DEFINITION` |
| 23–25 | `8fc6fcfc4c25cbda5cad5add17e985d6f0d2c48e69c06c6076d9a90cfcd156c9` / `rule-8fc6fcfc4c25cbda5cad5add17e985d6f0d2c48e69c06c6076d9a90cfcd156c9` | `DEFINITION` |
| 31–38 | `73eb6eedbfbf548fbcd47b0d6c8e9316fc986455b8b3bbb68501e642a20ccca2` / `rule-73eb6eedbfbf548fbcd47b0d6c8e9316fc986455b8b3bbb68501e642a20ccca2` | `DEFINITION` |
| 41–42 | `1cbc5b8826eb3184ebd455e6c0eafb627050f7eb83a90789adfde576808f048f` / `rule-1cbc5b8826eb3184ebd455e6c0eafb627050f7eb83a90789adfde576808f048f` | `OPERATIONAL_RULE` |

The Stage 3 manifest contains the same four full identities once each, in the
same order. There are no omissions, duplicates, extras, changed hashes, or
reordered identities. Its inventory hash equals the independently canonicalized
inventory. `validate_trust_boundary` also passes. Evidence:
`evidence/02_reconstructed_inventory.json`,
`evidence/03_stage3_manifest.txt`, and
`evidence/05_inventory_bijection.txt`.

## Independent classification judgment

The classifications follow from the frozen rules themselves and the operational
semantics:

1. `chooseNumProgram => Module(...)` is a zero-argument named proof/program
   term whose right-hand side is the exact constructor tree in `solution.mpy`.
   It names the translated source body and does not replace a `Run` execution.
   This is a macro/named proof-term `DEFINITION`.
2. `noEvenInRange(X,Y)` is a fresh Boolean summary defined by a direct equation.
   It has no pre-existing operational meaning that the rule asks K to prove.
   It is therefore a summary `DEFINITION`, not a disguised domain lemma.
3. `chooseNumContract(X,Y,R)` is likewise a fresh named postcondition expanded
   to the sentinel and greatest-even cases. It is a predicate
   `DEFINITION`, not an inferred arithmetic fact.
4. The `<k> VInt(R) ~> checkChooseNum(X,Y) => ... </k>` rule observes an
   already produced integer and evaluates the named checker. It neither
   rewrites `Run` nor skips the source expression. It is an ordinary
   `OPERATIONAL_RULE` under the required observation category.

No rule has a `simplification` attribute. There is no candidate
`PROVED_DERIVED_LEMMA`, and Stage 1 does not purport first to prove one of these
exact rules in a module omitting it and then use it later. Most importantly,
none of the four rules is an arithmetic proposition used to assist proof search
while retaining an independently fixed left-hand symbol. The independent
classification counts are thus three definitions, one operational observation,
zero proved-derived lemmas, and zero domain lemmas.

This empty domain set is mathematically credible rather than an artifact of
labeling. For integers:

- if `X > Y`, the interval is empty;
- if `X = Y`, it has no even member exactly when that member is odd; and
- if `X < Y`, the interval contains two consecutive integers and hence an even
  member.

That is exactly the defining equation for `noEvenInRange`. In the non-sentinel
contract branch, the bounds and evenness place `R` in the interval, while
`Y < R + 2` excludes the next even integer and therefore establishes
maximality. These formulas are relevant to the prompt and postcondition, but
their rules define the fresh summary names; they do not constitute extra domain
lemmas.

The frozen `Run` rule evaluates the translated return expression in an
environment binding `x` and `y`. A fresh Haskell-backend compilation of the
frozen semantics produced `VInt(14)` for `(12,15)` and `VInt(-1)` for
`(13,13)`. An audit-only wrapper then placed the frozen `Run` computation before
`checkChooseNum`: it produced `VBool(true)`. Direct observation accepted the
maximal result `4` for `[1,4]` and rejected the convenient nonmaximal result
`2`. The wrapper and inputs are recorded alongside complete build/run output in
`evidence/16_fixed_semantics_runtime.txt`,
`evidence/17_operational_observation_inputs.txt`, and
`evidence/17_operational_observation_runtime.txt`.

As finite corroboration, an independent evaluator and interval oracle agreed
on all 10,201 pairs in `[-50,50]²`; every returned value satisfied the contract.
Adversarial sentinel, odd, nonmaximal, and out-of-range outputs were rejected.
Dropping the odd-singleton case and mutating the odd branch from `Y-1` to
`Y-3` both produced explicit counterexamples. This testing supports, but is not
substituted for, the classification reasoning above. Evidence:
`evidence/14_semantic_classification_checks.py` and
`evidence/14_semantic_classification_checks.txt`.

## Generation-producer provenance

Before judging Stage 4, I hashed the mounted generation-time producer sources:

- `klean_export.py`:
  `4fa919ac98483620c7024ed7424c8b19f21406a2146feafad84ab4c813117881`;
- `klean.py`:
  `5d419b1cf907ab880eeb88a68e0d6da0bf59a92a56a0803b34d53698d91caabe`.

Both equal the hashes in `source-manifest.json` and the corresponding
`exporter_sha256`/`klean_py_sha256` fields in `generator-manifest.json`.
The source manifest and generator manifest both record immutable generator
image
`sha256:15baeb15b1ea8266bfad3dbc3a75ee531cf429f1b73e0e3ff478f279e6308f63`;
the launcher-recorded producer path has the same image digest as its final
component. The producer bundle contains exactly the two sources and source
manifest. Its launcher-algorithm tree hash is
`7b7fdfe618031c11f79bb3d7eec7df24bc64a9a480fc470c1176ce36a593286a`,
matching `/audit-input.json`.

For transparency, `evidence/07_producer_provenance_check.txt` also records an
initial comparison made with `klean_export.tree_digest`, an algorithm intended
for generated Klean trees; that inapplicable algorithm naturally produced a
different aggregate value. I traced the launcher code and repeated the check
with its required `tools.pipeline_contract.sha256_tree`; the matching result is
in `evidence/08_producer_bundle_launcher_hash.txt`. The individual producer
hashes and image identity never differed. There is no producer-source
infrastructure error.

## Stage 4 preflight, obligation bijection, and target identity

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and exactly these immutable inputs:

- `/reference/k-proof`;
- `/reference/lemma-discovery.json`;
- `/reference/klean-generation`;
- `/reference/klean-toolchain.lock.json`.

The first invocation reached `lake clean` but the sandbox’s mismatched PID and
`/proc` views prevented Lean from resolving `/proc/<pid>/exe`; Lake reported
“could not detect the configuration of the Lake installation.” Diagnostics are
preserved in `evidence/09_preflight_rerun.txt` and
`evidence/10_lean_environment_diagnostic.txt`.

I did not alter any frozen input, generated file, checker, or toolchain. I used
a narrowly scoped `LD_PRELOAD` shim below `/tmp/audit-work` that changes only
numeric `/proc/*/exe` `readlink`/`readlinkat` calls to the pinned Lean
executable path. The complete source, binary hashes, and recovered tool versions
are in `evidence/11_lean_proc_shim.txt`. Lean then reported version 4.22.0,
commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, matching the lock.

With that sandbox compensation, the unchanged trusted checker returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean` exit 0;
- `lake build` exit 0;
- obligation count 0;
- target `null`;
- designated sorry count 0;
- 41 generated trust declarations;
- all Stage 1, Stage 3, and generated-tree hashes equal to the frozen records.

The complete returned evidence is
`evidence/12_preflight_rerun_compensated.txt`. Its clean/build output hashes and
build output exactly match the previously recorded preflight diagnostics.

I separately checked the semantic and structural bijection:

- independently classified domain-rule IDs: `[]`;
- Stage 3 `DOMAIN_LEMMA` IDs: `[]`;
- `input-manifest.json` source rules: `[]`;
- `obligation-map.json` source rules: `[]`;
- generated obligations: `[]`;
- trust parameters: `[]`.

All five ordered lists are equal, with no duplicate or omitted identity.
Because there are no obligations, there are no irrelevant, weakened,
duplicated, or vacuous conjuncts. The exact producer source emits
`targetStatement` only when its proposition list is nonempty.

An independent scan found no `targetStatement` in any generated Lean source.
`Klean102ChooseNum/Lemmas.lean` contains only its import and namespace.
The trusted target extractor, generator manifest, recorded preflight, and audit
input all report target `null`. Thus the fixed generated target is correctly
absent, rather than changed or weakened. Evidence:
`evidence/13_hash_bijection_target_audit.txt` and
`evidence/19_generated_target_source_scan.txt`.

The 41 generated Prelude axioms are exactly the mechanically inventoried
collection-operation trust declarations; the preflight independently rejects
proposition trust. With no target proposition or proof, they cannot supply a
Stage 5 proof escape.

## Stage 5 applicability

Stage 5 proof auditing is not applicable in `CLASSIFICATION_ONLY`. The audit
input records `lean_workspace`, `lean_invocation`, and both corresponding hashes
as `null`; `/candidate` does not exist. This is exactly the required state for a
genuinely empty domain-lemma set and `KLEAN_NO_OBLIGATIONS`. There is therefore
no `Proof.final`, generated theorem, candidate definition, or axiom dependency
to rebuild or account for.

## Evidence index

All raw commands and outputs are under `/audit-output/evidence/`. The principal
records are:

- `00_audit_input.txt` — launcher mode and complete audit input;
- `02_reconstructed_inventory.json` through
  `05_inventory_bijection.txt` — canonical inventory and exact Stage 3
  comparison;
- `06_generation_manifests.txt` through
  `08_producer_bundle_launcher_hash.txt` — manifests and producer provenance;
- `09_preflight_rerun.txt` through
  `12_preflight_rerun_compensated.txt` — initial environment failure,
  compensation, and successful mandated preflight;
- `13_hash_bijection_target_audit.txt` — all frozen/provenance hash checks,
  empty bijection, target identity, and candidate absence;
- `14_semantic_classification_checks.*`,
  `16_fixed_semantics_runtime.txt`, and
  `17_operational_observation_*` — independent semantic and adversarial
  evidence;
- `18_audit_input_integrity.txt` and
  `19_generated_target_source_scan.txt` — launcher integrity and exact target
  absence;
- `20_review_consistency.txt` — final rule-ID ordering and verdict-tail check.

VERDICT: PASS
LEGITIMACY: LEGIT
