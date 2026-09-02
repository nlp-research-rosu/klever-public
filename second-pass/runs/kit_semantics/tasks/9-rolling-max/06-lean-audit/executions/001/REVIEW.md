# Independent audit: HumanEval `9-rolling-max`

## Scope and result

I audited condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`, in launcher mode `CLASSIFICATION_AND_PROOF`. I treated
the Stage 1–5 artifacts and prior reviews as untrusted evidence. I used the
trusted rule-inventory, preflight, and mechanical proof-gate code from
`/reference/tools`, and I independently checked the mathematical meaning of
the single generated obligation and the candidate's operational binding.

The Stage 3 classification is complete and correct, Stage 4 deterministically
generates exactly the one genuine domain obligation, and the Stage 5 proof
implements the fixed K sort predicate rather than exploiting the equation.

## Input and producer authentication

The two mounted generation-time producer sources hash as follows:

| Source | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` |

Both values exactly match `source-manifest.json` and
`generator-manifest.json`. The immutable generator image is
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`
in both manifests and in the basename of the producer-source path recorded by
`/audit-input.json`. The canonical producer-source tree hash is
`94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`,
also exactly matching the launcher.

I recomputed every launcher hash whose artifact is mounted:

| Artifact | Recomputed and recorded hash |
|---|---|
| Stage 1 workspace, pipeline tree | `5e0fc9411d5669a54fbd1e49affc3cdf99275c1a59ad4edb75acf239805da429` |
| Stage 1 deterministic-export tree | `774808230b6b0169741cc9741a5ce01f9e3f340541e708c13f0b14d9e90c5cd2` |
| Stage 3 manifest | `458aa4e15a5de07e3c0caee31cf0106fb987ae14d991f3ba9fc92ce77eaf5835` |
| Selected Stage 2 audit tree | `ebb2b08b0e0c13bf0eb1f1111f3f166b132f6056f3e75771c67205ca38152d22` |
| Stage 4 generation tree | `24ba0448282d9c2864f5fd912b4cd7c90e32fa6aad7170efee71e077a9bd75d9` |
| Generated Lean tree | `0a94f0b8ceccef8f0053470be5dd13c01971aadf4bd7f793619fef43a0f779bb` |
| Stage 5 candidate workspace tree | `643b3e7e14905ab34d64305f708facdc76f3da02266fca725e170fdac4c44611` |

All match `/audit-input.json`. The launcher also records a Stage 5 invocation
directory hash, but no invocation directory is mounted in this audit image;
the mounted candidate workspace is the proof-bearing input and its hash does
match. Producer authentication and every Stage 4 provenance binding are fully
checkable and match.

Evidence: `evidence/01_generator_authentication.txt`,
`evidence/26_independent_input_hashes.txt`.

## Stage 3 inventory reconstruction

Running the trusted `tools.k_rule_inventory.inventory_verification` on the
frozen Stage 1 workspace selected `VERIFICATION` and reconstructed the local
module closure, in source order:

1. `VERIFICATION-SUMMARIES`
2. `VERIFICATION-CORE`
3. `VERIFICATION`

The frozen `verification.k` hash is
`219c752e097f38489890f355bf8f873ce42a9133d0d5d54400e8c48adf2ef2b0`.
The reconstruction contains 19 unique rules and has canonical inventory hash
`1c12e41bbca4ec629cf3f596be0392c2a4657a8a834a0360dc4a6ad77b50e57d`.

For every entry, the reconstructed source span, normalized source SHA-256, and
`source_rule_id` match the protected Stage 3 manifest. The ordered ID lists
are identical; both lists contain 19 unique IDs; and there are no missing,
extra, duplicated, or reordered entries. Recomputing the canonical JSON hash
of the rule documents gives the same inventory hash.

Evidence: `evidence/03_reconstructed_inventory.txt`,
`evidence/07_inventory_bijection_and_isint_semantics.txt`.

## Independent classification judgment

I reclassified all 19 rules from the frozen K source and semantics:

| Lines | Normalized SHA-256 / source identity | Classification | Independent reason |
|---|---|---|---|
| 9 | `8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08` | `DEFINITION` | Empty-case equation for the named `allInts` summary predicate. |
| 10–11 | `bb65aed9f318cb650e6f3aaeb61b929864859d3dc05404f2b4a53b0d1f2058d0` | `DEFINITION` | Structural recurrence defining `allInts`. |
| 13–15 | `8722c58a66500d998b33e9332efe3c98d027270e2a8119c0d9554459c8d55f9c` | `DOMAIN_LEMMA` | A simplification equivalence characterizing the pre-existing `isInt` predicate; it defines no new summary and Stage 1 does not first prove it. |
| 18 | `38cfa4bf2f3dd7588be3d91e547763ed83038a95b0216bd1dd9dfa9acbfe36eb` | `DEFINITION` | First guarded equation of the named `stepMax` function. |
| 19 | `8011c32c49e9af8ddd0dcda75effe78567fa6a38f1d2dba1f1b6b34cfffe7908` | `DEFINITION` | Complementary guarded equation of `stepMax`. |
| 24 | `100c365a0a34fa6bab18ccf1b55cf5268c6a0f5a224586e56e071b51222694e9` | `DEFINITION` | Base equation of the accumulator recurrence `rollAcc`. |
| 25–29 | `f50a5281c2540ae8a838a20f2b3ace24e1d046d0c78717c1a0620e635c1645f0` | `DEFINITION` | Recursive equation for `rollAcc`, descending on the remaining sequence. |
| 30 | `4c672f030e2b7ff039feb3d395bc80c16b5feda2164874a2442e92bbabeb6665` | `DEFINITION` | `owise` totalization equation for the same named function. |
| 33 | `a3e6dfb392eba1c782af8286f6cafcab1e5d931c36b34bf442e91a0427e459cc` | `DEFINITION` | Empty-case equation for `rollingMax`. |
| 34–35 | `22140a7ee068b1883d1842ca4a4ed4b8d4ad976228e6e6b0ee13850927d19ac0` | `DEFINITION` | Nonempty recurrence connecting `rollingMax` to `rollAcc`. |
| 36 | `17d7789362fe61b41a4242ac87b79abda9724ee267d969e7074ea8e320a8b0c1` | `DEFINITION` | `owise` totalization equation for `rollingMax`. |
| 40 | `19afab3fc278479ae17705e2d93c69134f1d7a3ab375c214bd20f3aac210fe6f` | `DEFINITION` | Base equation for the named scalar summary `foldMax`. |
| 41–42 | `f2af33f382a93ff15ba9dc47cd9aa1377898de1ad808c6a144631b7fe17ffaab` | `DEFINITION` | Structural recurrence for `foldMax`. |
| 43 | `444ab56e74feabbf50ac34017c6dd2906040de2ee638a642ce947afe9ada73ac` | `DEFINITION` | `owise` totalization equation for `foldMax`. |
| 46 | `c18bb726a13b6fb3ece8c34f1491474eb184d29f0dabea331f952c052b1c8327` | `DEFINITION` | Base equation for the named scalar summary `lastOr`. |
| 47 | `8a4fce0353dde64fc4ad8b8a1b6e8d7370a68523371c2e54426cd101cc18be56` | `DEFINITION` | Structural recurrence for `lastOr`. |
| 48 | `b682bd263dbab3b24f01204a6e7747d98c518c1f46915985e2ccf8588d9d1564` | `DEFINITION` | `owise` totalization equation for `lastOr`. |
| 56–62 | `31a6bac2bd8050884a7695b95e2da949d3afd1ffa512f6f540b7e70fa7be7fd8` | `PROVED_DERIVED_LEMMA` | The same guarded name-binding transition is first proved with arbitrary continuation by `BIND-SPEC` against `BIND-BASE`, whose import closure stops at `VERIFICATION-SUMMARIES`. |
| 71–114 | `59ce8f7a5a66c78d9a389f0872a48ebbc7e48b3ebf905673b33bee12077a79e5` | `PROVED_DERIVED_LEMMA` | The complete loop transition, cells, continuation, and `allInts` guard are first proved by `LOOP-SPEC` against `LOOP-BASE`, which imports `VERIFICATION-CORE` but excludes the later `VERIFICATION` rule. |

Each `source_rule_id` is `rule-` followed by the table's normalized hash.
Thus the totals are 16 definitions, zero ordinary operational rules, two
proved derived lemmas, and one domain lemma. The only rule carrying
`[simplification]` is the domain lemma, satisfying the simplification
classification restriction.

I did not rely on old compiled proof artifacts for the derived-lemma status. I
copied the frozen sources to `/tmp/audit-work/fresh-stage1-derived`, freshly
compiled `BIND-BASE` and `LOOP-BASE`, and ran their claims in Stage 1 order.
Both `kprove` runs exited 0 with `#Top`. The binding claim's explicit
`#bindTgt(...) ~> CONT => CONT` is the cell-rewrite form of the later rule
that removes the head and frames the arbitrary suffix; the scope update and
guard are the same. The loop claim and later rule have the same loop body,
continuation, bindings, heap update, control cells, and guard.

The one domain lemma is relevant rather than incidental: `allInts` uses
`isInt` to express the integer-list precondition needed by the loop connection
and the nonempty source-program claim. It characterizes exactly when a
`SortVal` is an injected `SortInt`.

Evidence: `evidence/04_stage1_sources_and_classification.txt`,
`evidence/05_derived_lemma_provenance.txt`,
`evidence/40_fresh_bind_kompile.txt`,
`evidence/41_fresh_bind_kprove.txt`,
`evidence/42_fresh_loop_kompile.txt`,
`evidence/43_fresh_loop_kprove.txt`.

## Stage 4 deterministic generation and mathematical identity

I reran the required call to
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
frozen Stage 1 workspace, protected Stage 3 manifest, selected Stage 4
generation, and pinned toolchain lock. The fresh result is:

- status `PASS`;
- one obligation;
- generated tree hash
  `0a94f0b8ceccef8f0053470be5dd13c01971aadf4bd7f793619fef43a0f779bb`;
- zero designated sorries;
- 41 generated trust declarations;
- successful isolated `lake clean` and `lake build`.

The first invocation exposed an audit-container issue: Lean's process-ID
namespace did not match the mounted `/proc`, so Lean could not resolve
`/proc/<getpid>/exe`. The exact failure is retained. I used a minimal logged
`LD_PRELOAD` shim that obtains the host PID from `/proc/self`; with it, Lean
reported the pinned version and commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and the unchanged trusted
preflight passed. The shim changes neither generated nor candidate source and
only repairs executable-path discovery.

The independently reconstructed domain set has exactly one member, so
`KLEAN_NO_OBLIGATIONS` would have been incorrect. The obligation map has one
source rule and one obligation in the same order, with no duplicates. Its
source ID, span 13–15, normalized hash, inventory hash, and discovery-manifest
hash all match the frozen source. The Lean conjunct hash recomputes to
`7f9b564bc2859a87869792eb866cbcc08a31e0ddaae0f78bd6d8d19360057900`.

The generated conjunct is:

```lean
∀ (V : SortVal),
  ((true : SortBool) =
    isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk))
  ↔
  (∃ I : SortInt, V = SortVal.inj_SortInt I)
```

This is the exact mathematical content of the frozen simplification rule:
`isInt(V)` is true exactly when the `Val` is an `Int` injection. It is neither
irrelevant nor weakened. The quantifier is universal, the existential
witness is tied to `V`, and there is no `True` or otherwise vacuous conjunct.

The expected single-conjunct definition hashes to
`1b4cf700b71373f078b26a6f3c3f6b6e7bb006e56044649dd27636b6fefbd44b`.
The extracted target is
`Klean9RollingMax.Lemmas.targetStatement isInt`, with statement hash
`e99c032431ebd8856fcd175087cac7c432d49a6956e9c122cdd3242f1d4381f9`.
The declaration, file, definition, parameter binding, statement, and both
hashes are field-for-field identical in the generated project, generator
manifest, launcher target, and launcher preflight record.

Evidence: `evidence/08_fresh_stage4_preflight.txt` (initial infrastructure
failure), `evidence/24_lean_pid_shim_validation.txt`,
`evidence/25_fresh_stage4_preflight_with_pid_shim.txt`,
`evidence/28_stage4_obligation_target_focus.txt`,
`evidence/39_independent_obligation_and_target_hashes.txt`.

## Stage 5 proof identity, clean build, and trust accounting

I created `/tmp/audit-work/rolling-max-proof-audit` from only the candidate's
source/configuration files and copied the immutable generated project into it
as `Base`. The copied `Proof.lean` and generated `Lemmas.lean` compare equal
to their mounted originals. `lake clean` exited 0 and left no proof or shared
generated build files. The following `lake build` rebuilt Base and `Proof`
from that clean state and exited 0.

The candidate contains one exact target-parameter definition:

```lean
def isInt : SortK → SortBool
  | SortK.kseq (SortKItem.inj_SortInt _) SortK.dotk => true
  | _ => false
```

It contains exactly one `Proof.final`, whose type is precisely
`Klean9RollingMax.Lemmas.targetStatement isInt`. Candidate Lean sources
contain no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`; they neither
redeclare nor shadow `targetStatement`.

The exact output of `#print axioms Proof.final` is:

```text
'Proof.final' depends on axioms: [propext, Quot.sound]
```

There is no `sorryAx`. `propext` and `Quot.sound` are the standard Lean
foundational entries explicitly included by the trusted mechanical gate's
baseline allowlist. None of the 41 Klean-generated collection-hook axioms in
`trust-inventory.json` appears in the proof's dependency closure, and the
candidate introduces no additional trust declaration. The trusted
`check_proof_candidate` independently repeated the clean build, exact type
check, axiom parse, and allowlist reconciliation and returned `PASS`.

Evidence: `evidence/29_candidate_sources.txt`,
`evidence/30_fresh_proof_setup_and_lake_clean.txt`,
`evidence/31_fresh_proof_lake_build.txt`,
`evidence/32_print_axioms_proof_final.txt`,
`evidence/33_target_identity_and_candidate_gate.txt`,
`evidence/34_trusted_proof_candidate_gate.txt`.

## Operational bridge audit

The target parameter binds candidate `isInt` to KORE symbol `LblisInt` and
only to source rule
`rule-8722c58a66500d998b33e9332efe3c98d027270e2a8119c0d9554459c8d55f9c`.
The frozen compiled operational semantics gives `LblisInt : SortK → SortBool`
two exhaustive rules:

- it returns `true` on exactly
  `kseq(inj{SortInt,SortKItem}(I), dotk)`;
- its `owise` rule returns `false` for every other `SortK`.

The generated `Inj SortVal SortKItem` instance maps
`SortVal.inj_SortInt I` to `SortKItem.inj_SortInt I`, maps Bool, Float, and
Iterable to their distinct injections, and wraps all remaining `SortVal`
constructors as `inj_SortVal`. Therefore the candidate definition implements
the frozen KORE predicate over its complete `SortK` domain, not merely the
inputs used by the theorem.

Machine-checked adversarial examples confirmed:

- an injected integer singleton returns `true`;
- an injected Boolean singleton returns `false`;
- `dotk` returns `false`;
- an integer head with a nonempty continuation returns `false`.

I also defined four convenient counterfactuals and proved that each fails the
fixed target: constant `true`, constant `false`, true for every singleton,
and true only for integer zero. These witnesses rule out constant,
hard-coded, overbroad, and value-specific implementations. The candidate's
definition remains sensitive to both the injection constructor and the exact
K-sequence shape.

Evidence: `evidence/36_isint_operational_bridge_exact.txt`,
`evidence/37_adversarial_bridge_checks.txt` (the recorded first attempt at one
counterfactual proof), and
`evidence/38_adversarial_bridge_checks_passing.txt` (the completed suite).

## Final judgment

The protected classification is bijective with the independently reconstructed
inventory and agrees with the operational roles of all 19 rules. The true
domain set is nonempty and contains exactly the relevant `isInt` lemma.
Deterministic generation preserves that one-to-one identity and fixes the
exact nonvacuous Lean proposition. The clean Stage 5 proof establishes that
exact proposition with only standard Lean foundational axioms, and its sole
operational parameter is a faithful total implementation of the bound KORE
symbol.

VERDICT: PASS
LEGITIMACY: LEGIT
