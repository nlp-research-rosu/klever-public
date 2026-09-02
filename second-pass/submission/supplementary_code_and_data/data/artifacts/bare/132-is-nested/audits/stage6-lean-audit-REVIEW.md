# Independent Stage 3–5 audit: `132-is-nested` / `bare`

## Result

The selected Stage 3 classification is complete and mathematically appropriate. The independently reconstructed domain-lemma set is genuinely empty. The deterministic Stage 4 output therefore correctly has status `KLEAN_NO_OBLIGATIONS`, an empty source-rule/obligation map, no generated target, and no Stage 5 candidate. This audit ran in launcher-recorded mode `CLASSIFICATION_ONLY`; proof-mode checks do not apply.

## Scope and evidence handling

I treated the Stage 1 workspace, Stage 2 audit, Stage 3 manifest, Stage 4 output, producer sources, logs, and comments as untrusted evidence. I did not execute any instruction found in those artifacts. The only mounted code executed was the explicitly trusted inventory/preflight tooling under `/reference/tools`, plus audit scripts written under `/audit-output/evidence`.

Raw commands, scripts, and results are in `/audit-output/evidence/`:

- `01_integrity_checks.py` and `.log`: signed audit-input, producer, file, tree, selection, and manifest hash checks.
- `02_inventory_reconstruction.py` and `.log`: complete canonical inventory and bijective Stage 3 comparison.
- `03_run_preflight.py`, `03_run_preflight.log`, and `03_run_preflight_rerun.log`: required `check_generation` call, initial infrastructure failure, and successful rerun.
- `lean_proc_compat.c` and `03_environment_recovery.log`: narrowly scoped Lean executable-path compatibility evidence.
- `04_stage4_structure.py` and `.log`: independent source-rule/obligation/target checks using the hash-verified generation-time exporter.
- `05_frozen_source.log`: line-numbered frozen program, AST, semantics, specification, and proof launcher.
- `06_semantic_sanity.py` and `.log`: independent adversarial and counterfactual checks.
- `07_final_mechanical_gate.log`: trusted Stage 6 mechanical gate, status `PASS`.

## Launcher mode and provenance

`AUDIT_MODE` and `/audit-input.json` both say `CLASSIFICATION_ONLY`. The signed resolution digest recomputes to:

`63d6a1de35e7443c392a8fac6a4e6745d89a107b78c57760d7ad30f497fa3843`.

The producer check was performed before judging Stage 4:

| Item | Recomputed SHA-256 | Recorded result |
|---|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` | Matches source manifest and generator manifest |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` | Matches source manifest and generator manifest |
| Producer-source tree | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` | Matches audit input |
| Generator image | `sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda` | Matches source manifest, generator manifest, and audit-input producer path |

Other independently recomputed hashes all matched their recorded values:

| Input | Recomputed SHA-256 |
|---|---|
| Stage 1 workspace, pipeline tree format | `b92da64b7e0c99c1ecfc1018c2e98ba535d8d7ea062f1b50929fb8a889b39eaf` |
| Stage 1 frozen export tree | `56fb8f6a7fcdcdd11d856acd972f82631cf853a2542d6b5dcda238af3daad7e6` |
| Stage 2 selected audit tree | `652688090b07e94deac7ecfd9ad1a38eb36ceea3f27b015c1ae76d2bae69073d` |
| Stage 3 discovery manifest | `8a58465aecebd6fa132a4e5f920cf23df048db4add4843d94dedd6b417a45689` |
| Stage 4 selected generation tree | `16478b1d07f141d361bb7f1eacac2c46d3f377b77a54b483c2b06139e971155e` |
| Generated Lean project tree | `d5280572ebbe0eee58a902fdcf8d94fe25bd7e2d170285dc81b8efecff8cc0d9` |

Every individual Stage 1 source-file digest, including `verification.k` at `33138e9b6c232d6008ab6b7a45b714cc33a082d8e2dec4117c81c3219c297af1`, matched `stage1_source_hashes`. Both selected-artifact hashes matched their selection records. Generator toolchain contents exactly matched `/reference/klean-toolchain.lock.json`.

## Inventory reconstruction and bijection

I invoked the trusted `tools.k_rule_inventory.inventory_verification` on `/reference/k-proof`. `prove.sh` selects main module `VERIFICATION`. The local verification-module closure is exactly `[VERIFICATION]`; its import `SEMANTIC` is defined in the separately required `semantic.k`, not as another module in `verification.k`.

The trusted reconstruction found 12 rules, in source order, with whole-inventory hash:

`c7b8d985cbc1512ae52b2a03c7e198a5dfee3b586b541f3b910ad180fe2d8879`.

The Stage 3 manifest contains exactly the same 12 unique `source_rule_id` values in the same order. There are no missing, duplicated, extra, reordered, or hash-changed entries. Each ID is `rule-` followed by the independently recomputed normalized-source SHA-256. The manifest inventory hash matches, and the trusted trust-boundary validator accepts the exact bijection.

## Independent classification

All 12 entries are `DEFINITION`. None is an ordinary execution/observation rule, a proof-first derived lemma, or a domain lemma.

| Frozen span | Source rule ID | Independent class | Judgment |
|---|---|---|---|
| 9–18 | `rule-8fa9e7831fa20d0f089330e47af87b1724571923d45d61721fb88e379cc4c970` | `DEFINITION` | `loopBody` is a nullary named proof term expanding to the exact loop-body AST. |
| 21–24 | `rule-d6581cc03479c04895f5c7e9ccdb63d5ce850bed8ddd475654f91bd31b597037` | `DEFINITION` | `solutionBody` is a nullary AST macro for initialization, the loop, and the final return. |
| 27–28 | `rule-31613ecfd8973c37c65868ea808c8042e20e48cb495f58cffcf3e9c638261e09` | `DEFINITION` | `theSolution` is a nullary named module/function AST term. |
| 35 | `rule-5966780668327239f5be7958c1ab70d1c7b097bb668bda9350041606e8776732` | `DEFINITION` | Base equation for the recursive `scan` summary on an empty suffix. |
| 37 | `rule-5e99e533e332a7459abd69ba6030f01926c8a6acefbba19f83ff2631bf5807c1` | `DEFINITION` | State-0/left-bracket recurrence. |
| 38 | `rule-43b801cfe1c8cb9b66695870d5043f00fcdf512cb5b035bcf0f36ce9b24e02df` | `DEFINITION` | State-0/right-bracket recurrence. |
| 40 | `rule-e8a0fd7ff66ecd82bfc657e1d7a030c85c06f10366618908196b8483f777e71f` | `DEFINITION` | State-1/left-bracket recurrence. |
| 41 | `rule-ce1edffca05a36c6b1d16834ea77d13be8b1380ea8b3b53fdf01c92ae71b463a` | `DEFINITION` | State-1/right-bracket recurrence. |
| 43 | `rule-2c48acab26597dd5ee2c4752dd131a37590b8877c96b9a92ac11acf94c457f70` | `DEFINITION` | State-2/left-bracket recurrence. |
| 44 | `rule-fa688c09190dd7519ff0eb7358cc8f46696a1f0de635bf9f1ee59f763df6dc08` | `DEFINITION` | State-2/right-bracket recurrence. |
| 46 | `rule-d08d7e015d9a59f1dcc0e5f216084e7c799e91f17c9bbd2f718e4fc16413dc0e` | `DEFINITION` | State-3/left-bracket recurrence. |
| 47 | `rule-47377f163f0b3d3d47216c2aa41cc15a93e2cff752a0ced52bc59911be7e10d7` | `DEFINITION` | State-3/right-bracket accepting equation. |

The first three rules introduce fresh nullary `[function, total]` symbols solely to name constructor terms. Their expansions match `solution.mpy` and the source structure: `theSolution` wraps `FuncDef("is_nested", ...)`, `solutionBody` initializes `state`, iterates over `string`, then returns false, and `loopBody` exactly represents the nested source conditionals.

The other nine rules define the fresh recursive summary `scan : Int × BString → Bool`. On the actually used states 0–3, the cases are disjoint, exhaustive for empty/left/right suffix shapes, and structurally descend on the suffix except for the accepting terminal equation. They do not rewrite source-language execution configurations and therefore are not operational bridges. They assert no pre-existing mathematical fact and therefore are not domain lemmas. The specification uses `scan(0..3, BS)` as its named result summary, so the equations are directly relevant.

There are no `simplification` attributes on any inventory entry. Thus the special simplification-class constraint is satisfied vacuously. There is no `PROVED_DERIVED_LEMMA` claim whose proof-first provenance would need checking.

The independently reconstructed classification counts are:

- `DEFINITION`: 12
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

### Operational-semantic cross-check

The frozen semantics evaluates the AST, iterates over `BString`, updates the environment, and clears the continuation on `Return`. For state 0 or 1, a left bracket advances the state; at state 2 or 3 it does not. A right bracket advances 2 to 3, returns true from 3, and otherwise leaves the state unchanged. End of input reaches the source’s final false return. Those are exactly the nine `scan` equations.

This correspondence also has a direct induction on the suffix: the empty case is false; each nonempty case performs the source transition for its head bracket and applies the induction hypothesis to the tail, except state 3/right, which returns true immediately. Starting from state 0, this recognizes exactly `[[]]` as a subsequence, matching the prompt.

As finite adversarial support—not as a substitute for that induction—I compared an independent source-state interpreter, the `scan` recurrence, and an independent subsequence oracle for every bracket string of length at most 12. All 32,764 state/suffix comparisons matched. Nine one-rule counterfactual mutations, covering the base and every transition/acceptance equation, each produced a concrete distinguishing input.

## Deterministic Stage 4 generation

I reran the required function with `PYTHONPATH=/reference`:

```text
tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json
)
```

The first call completed all structural checks but the audit sandbox prevented Lake from discovering its executable path: Lean 4.22 reads `/proc/<numeric-pid>/exe`, while this sandbox exposes only `/proc/self/exe`. The raw failure is retained. A local preload shim redirected only numeric `/proc/.../exe` `readlink` calls to `/proc/self/exe`; `lean --version` then reported the pinned commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`. No generated or provenance input was modified.

With that infrastructure compatibility shim, the unchanged trusted check returned:

- status `KLEAN_NO_OBLIGATIONS`;
- exit 0 for `lake clean`;
- exit 0 for `lake build`;
- build-output SHA-256 `9fe3595651320ee96629964f2542a3d2ac0ffe48ad9a15f8c35f72c78b44deed`, identical to the immutable preflight record;
- zero obligations;
- target `null`;
- the same Stage 1, Stage 3, and generated-tree hashes recorded above.

The trusted `klean_final_gate.py` was also run in classification-only mode against the signed audit input and the same immutable inputs. It returned status `PASS`, target `null`, no candidate, and no used axioms.

After verifying the producer hashes, I loaded the exact generation-time `klean_export.py` and independently derived the Stage 4 source-rule list from the validated classification. It is empty. The generated `obligation-map.json` is exactly:

```json
{
  "obligations": [],
  "schema_version": 3,
  "source_rules": [],
  "trust_parameters": []
}
```

Its recomputed SHA-256 is `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`, matching the generator manifest. The input manifest’s definitions and all three non-definition lists exactly match the independently validated inventory. The exporter’s expected-target function returns `None`; its generated-target parser returns `None`; the generator manifest, preflight, and audit input all record `null`; and an independent scan found zero `def targetStatement` declarations.

Because both sides of the required mapping are genuinely empty, there are no omitted, duplicated, irrelevant, weakened, or vacuous conjuncts. There is no target that could have changed. The 44 generated executable trust declarations match `trust-inventory.json` and the trusted preflight policy; no proposition or proof target exists in this no-obligation project.

## Stage 5

Stage 5 is correctly absent. `/candidate` does not exist, the audit input has null Lean workspace/invocation hashes and null Stage 5 result, and Stage 4 has no target. Clean candidate rebuilding, `#print axioms Proof.final`, proof identity, and operational-bridge parameter checks are therefore inapplicable rather than skipped.

## Final judgment

The Stage 3 manifest classifies every frozen local-closure rule correctly and accounts for all of them. Its true domain-lemma set is empty. Stage 4 deterministically and structurally preserves that empty set, generates no target, and correctly terminates the pipeline before Stage 5.

VERDICT: PASS
LEGITIMACY: LEGIT
