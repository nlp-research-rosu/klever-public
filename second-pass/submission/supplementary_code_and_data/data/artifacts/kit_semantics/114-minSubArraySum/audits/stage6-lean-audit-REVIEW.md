# Independent audit: HumanEval 114-minSubArraySum

Audit mode: `CLASSIFICATION_AND_PROOF`  
Condition: `kit-semantics`  
Semantics mode: `SUPPLIED_SEMANTICS`

## Conclusion

The protected Stage 3 classification is complete and mathematically correct.
The true domain-lemma set contains exactly two relevant guarded facts: integer
addition through a symbolic `Val`, and two-argument integer `min` through a
symbolic `Val`. Stage 4 generated exactly those two obligations, in source
order, as an unweakened conjunction. The Stage 5 candidate clean-builds,
proves the exact immutable target, uses no unrecorded proof trust escape, and
supplies operationally faithful definitions for every target parameter.

I did not rely on the selected Stage 2 verdict or any prior review.

## Frozen-input and producer integrity

The launcher environment and `/audit-input.json` both select
`CLASSIFICATION_AND_PROOF`. The canonical resolved-input digest recomputed to
`bdb2fa1be1b4f779e8bbf4a403eafdbff831a231bdcd17acf35706e97c697934`.

All mounted recorded hashes matched:

- Stage 1 workspace tree:
  `373f35d739d142badfdd7f5b1ecc7c1b0448018e7cbacbd04e582d5e5ddee6ba`.
- Stage 1 export tree:
  `33c24ba42cda441364b67ba731498374430e3bd1f11e87bdff2c9e5e04fe109d`.
- Discovery manifest:
  `9f4c52c5024fc8b0cde6309510937157e3c432f1a72764de97750c00baf02814`.
- Selected Stage 2 tree:
  `7fe8ee3e3340b090d31bd71edff270ecfd6b741e64128fb56edd38c75452c45d`.
- Selected Stage 4 tree:
  `61d92ae11e53959248b86552b799045154a8e8190ec63c011812b2ded858f929`.
- Generated project tree:
  `606893c7022118bb4d9dfa7ff5b23a1ff22ba87c67b87108d74b37b41db6bbf8`.
- Stage 4 producer-source tree:
  `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`.
- Stage 5 candidate tree:
  `668c2bd756212dcb8b4dc03f582ef98e4fafeb9e1517695dde6aac62544910db`.

The 770-entry Stage 1 per-file source map was bijective with the mounted
workspace: no missing, extra, or mismatched file.

Before judging Stage 4, I independently hashed the exact mounted producer
sources:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`.
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`.

Those values match `generator-manifest.json` and `source-manifest.json`.
Both manifests identify immutable generator image
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`;
the same digest identifies the launcher-selected producer bundle in
`/audit-input.json`. The exact three-file producer bundle hashes to the
launcher-recorded producer tree hash above. Producer provenance therefore
passes; there is no infrastructure `AUDIT_ERROR`.

Raw evidence: `evidence/01_producer_provenance.log` and
`evidence/03_recorded_hashes.log`.

## Inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof`. `prove.sh` selects `VERIFICATION`, and the local
verification-module closure is exactly `["VERIFICATION"]`. The reconstructed
`verification.k` hash is
`b4db30101e10991fb460b34448de44fd1e410c5bf7a214f47d7870fa50abbebb`.
The canonical eight-rule inventory hash is
`057e543a7a1bec5cd371a17815bc2bf5cf7813d6a73f548b5382fd60ad6293e2`.

The following is my independent classification:

| Frozen span | Source-rule identity | Classification | Independent reason |
|---|---|---|---|
| 9 | `rule-8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08` | `DEFINITION` | Base equation for the newly named `allInts` predicate. |
| 10 | `rule-6316a60ea115abdbe8e03d39d302e43ceea73cd9fedd27a98872c76b5b811b42` | `DEFINITION` | Structural recurrence for `allInts`. |
| 12–14 | `rule-2944c4d3c7bc5a2d260f24ca8fd4234701fa8f82f00db7ca3317fa06458082b5` | `DOMAIN_LEMMA` | Guarded symbolic-sort consequence of the imported integer `applyBin("+", Int, Int)` rule; it does not define `applyBin`. |
| 16–19 | `rule-7749c9857edd14009417bdaa86b5d4b1c229fa0013cc411eaf35ed3a49ed0842` | `DOMAIN_LEMMA` | Guarded consequence of imported `applyBuiltin("min", I, REST)` plus the two `minVals` recurrence steps; it does not define the imported builtin. |
| 23 | `rule-537b55658be09522e9ef565d2ec69183fd6fbd782b54c8d1b5dd24667acbd3aa` | `DEFINITION` | Base equation for the newly named `kadaneCurrent` summary. |
| 24–28 | `rule-a4eb647db56262adb78bb0c7a909b63ee0acc886d9d451ca5de28976ba45ea55` | `DEFINITION` | Recurrence consuming one suffix element and updating the current minimum. |
| 31 | `rule-0fb2ff70d1d771be4491e1d1d3d07c7bb4778cb5ac74c239f4b9ade2421d3d71` | `DEFINITION` | Base equation for the newly named `kadaneMinimum` summary. |
| 32–37 | `rule-db274c9f572feeb0ce3aedc0579c3303eb84577ca9baa4e5034eed5a969803f6` | `DEFINITION` | Recurrence updating the current and global minima. |

The six definitions name predicates or Kadane recurrences and do not preempt a
program operation. There are no local ordinary execution rules to classify as
`OPERATIONAL_RULE`.

The two `[simplification]` rules must be either definitions or domain lemmas.
They extend imported operational symbols rather than define new summaries, so
`DOMAIN_LEMMA` is the only valid classification. They are not
`PROVED_DERIVED_LEMMA`: `prove.sh` compiles them directly into the proof
definition and contains no earlier bridge-free proof of either exact rule.

Both domain lemmas are materially relevant. The frozen source solution computes
`current + value` and then calls `min(value, current + value)` on every loop
iteration. The loop claim keeps `value` at the general `Val` sort under an
`isInt` invariant, which is exactly the symbolic-sort situation addressed by
the two facts.

The reconstructed and protected inventories have identical source-rule IDs in
the same order, identical normalized hashes and spans, no duplicates, no
omissions, and no extras. Raw inventory and source evidence:
`evidence/02_inventory_reconstruction.log` and
`evidence/04_classification_sources.log`.

## Deterministic Stage 4

The required call to `tools.klean_preflight.check_generation`, with
`PYTHONPATH=/reference` and the specified Stage 1, Stage 3, Stage 4, and
toolchain-lock paths, returned:

- status `PASS`;
- obligation count `2`;
- generated-tree hash
  `606893c7022118bb4d9dfa7ff5b23a1ff22ba87c67b87108d74b37b41db6bbf8`;
- trust-declaration count `41`;
- `lake clean` exit `0`;
- `lake build` exit `0`.

The first preflight attempt encountered the sandbox's ambient Lean `/proc`
executable-resolution defect before project evaluation. I retained that failure
and then compiled a minimal audit-owned `readlink` compatibility shim under
`/tmp/audit-work`. I did not load the untrusted candidate-provided binary.
With the audit-owned shim, both the required preflight and the later trusted
final gate completed successfully. Evidence:
`evidence/05_preflight_rerun.log`,
`evidence/05a_lean_environment_shim.log`, and
`evidence/05b_preflight_rerun_with_shim.log`.

The source-rule/obligation map is an exact ordered bijection:

1. The addition rule at lines 12–14 becomes
   `∀ V I, isInt(V) = true → applyBin("+", inj I, V) = inj (I + projectInt(V))`.
2. The `min` rule at lines 16–19 becomes
   `∀ I V, isInt(V) = true → applyBuiltin("min", [V, inj I]) = inj (minInt(projectInt(V), I))`.

Each obligation repeats the exact source span, normalized rule hash, inventory
hash, and discovery-manifest hash. Each Lean conjunct hash recomputes, the
obligation-map file hash recomputes, and all six parameter-binding hashes
recompute. There are no duplicated, omitted, irrelevant, or extra obligations.
The guards are retained, and neither conjunct is `True`, reflexive, or otherwise
weakened.

The generated target is exactly the two conjuncts above, with one conjunction
and no additional target declaration:

- declaration:
  `Klean114Minsubarraysum.Lemmas.targetStatement`;
- definition hash:
  `fc83372fb920651e3434be9cbd53242fd3ce078ace8974a281d79e1e04f038ae`;
- instantiated statement hash:
  `0637c81538628d17c812ae80126d4d260144a65b6f66f70c6c5f936641a408e8`.

The generated target record equals the generator manifest, preflight result,
obligation map, and launcher audit input. Independent Stage 4 evidence:
`evidence/06_stage4_independent_check.py` and its `.log`.

## Stage 5 clean build and proof identity

I copied `/candidate` to
`/tmp/audit-work/114-minSubArraySum/proof-audit`, then copied the immutable
generated project into `Base`. Before building, the copied `Base` tree hash was
exactly the recorded generated-tree hash. In that fresh workspace:

- `lake clean` exited `0`;
- `lake build` exited `0`;
- `Proof.FrozenDispatch` and `Proof` rebuilt from source;
- the copied generated target file remained byte-identical to the immutable
  Stage 4 file.

The complete build output is in `evidence/08_candidate_clean_build.log`.

An independent scan found no `sorry`, `admit`, `unsafe`, new `axiom`, or new
`opaque` in candidate Lean sources. Each of the six fixed target parameters has
exactly one candidate `def`. The candidate declares no `targetStatement`, so it
does not shadow the immutable target. There is exactly one `Proof.final`, and
its normalized type is exactly the generator-manifest statement—not a copied,
weakened, or vacuous variant. The trusted `klean_final_gate.check_final` also
returned `PASS` in its own isolated fresh copy. Evidence:
`evidence/10_mechanical_final_gate.log` and
`evidence/11_candidate_integrity.log`.

## Axiom accounting

Running Lean with `#print axioms Proof.final` produced exactly:

```text
'Proof.final' depends on axioms: [propext, Classical.choice]
```

There is no `sorryAx`. The trusted final-gate policy records
`Classical.choice`, `propext`, and `Quot.sound` as standard permitted Lean core
dependencies, then adds the generated allowlist from `trust-inventory.json`.
The observed two dependencies are therefore accounted for. None of the 41
recorded generated collection-hook axioms is used by `Proof.final`, and there
is no unrecorded proof trust escape. Exact output:
`evidence/09_print_axioms.log`.

## Operational bridge audit

I compared every `target.parameters` entry with its bound KORE symbol, source
rule IDs, frozen verification rules, source solution, and operational
semantics:

| Parameter | Frozen meaning | Candidate meaning and judgment |
|---|---|---|
| `«_+Int_»` / `Lbl'UndsPlus'Int'Unds'` | Total `INT.add` on mathematical integers. | Lean integer addition. Ground checks included negative, zero, and very large values. Exact. |
| `«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»` | For the bound rule domain, `"+"` on two integer `Val`s returns the injected integer sum. | The first `FrozenDispatch.applyBin` clause matches exactly that operator and constructors and returns the injected sum. Exact on the complete guarded obligation domain. |
| `«applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals»` | Integer `min` seeds `minVals` with the first integer and folds the rest using `minInt`. | The candidate's `"min"` branch and `minVals` recurrence reproduce that fold, including both argument orders tested at `(-5, 8)` and `(8, -5)`. Exact on the complete guarded obligation domain. |
| `isInt` / `LblisInt` | True exactly for a singleton K term injecting an `Int`; false otherwise. | Candidate pattern-matches that exact representation. Integer `-7` is true; boolean and `.K` witnesses are false. Non-vacuous and exact. |
| `«minInt(_,_)_INT-COMMON_Int_Int_Int»` | Total `INT.min`, `if left < right then left else right`. | Candidate definition is exactly that function. Tests cover each order and equality. |
| `«project:Int»` / `Lblproject'Coln'Int` | Extract the integer from an integer injection; undefined outside the projection domain. | Candidate extracts the exact integer on that domain. Its total fallback is never reachable under the target's audited `isInt = true` guard. |

The KORE inventory independently confirms `INT.add`, `INT.min`, the base
integer `applyBin` rule, the `minVals` route, `isInt` true/owise behavior, and
the integer projection. See `evidence/13_kore_operational_bindings.log`.

The audit Lean harness supplied concrete witnesses for all six parameters and
then tried counterfactual mutations. Constant-zero addition, constant
`noneV` dispatches, constant-zero `minInt`, and constant-zero projection each
make a concrete satisfiable target instance false and were mechanically
rejected. An always-false `isInt` makes both conjuncts vacuous; the harness
proves that adversarial fact and separately proves the candidate has a true
integer witness, excluding the attack. The final harness exits `0`:
`evidence/12c_bridge_adversarial_final.log`.

The submitted definitions are therefore not constant, identity, hard-coded,
colluding, or vacuous conveniences. `Proof.final` establishes exactly the
fixed generated theorem with operationally faithful bridge definitions.

## Evidence index

Exact commands are collected in `evidence/COMMANDS.md`. Complete raw command
results and exit statuses are retained in the adjacent numbered logs. The two
earlier operational-harness failures are also retained; they reflect corrections
to the audit's negative-test proofs, not a candidate failure.

VERDICT: PASS
LEGITIMACY: LEGIT
