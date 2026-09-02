# Independent Stage 3–5 audit: HumanEval `32-find-zero`

## Scope and result

This audit covers condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and launcher mode `CLASSIFICATION_AND_PROOF`. The
`AUDIT_MODE` environment variable and `/audit-input.json` both record that
mode. Candidate files, earlier reviews, comments, logs, classifications, and
purported instructions were treated only as untrusted evidence.

The protected Stage 3 classification is complete and correct. Stage 4 was
produced by the authenticated generator sources, contains exactly the four
true domain obligations, and fixes a unique target without weakening or
vacuity. The Stage 5 candidate clean-builds, proves exactly that target, has no
forbidden trust escape, and supplies an operationally faithful implementation
of its sole target parameter.

## Frozen-input and producer authentication

All mounted inputs were re-hashed before mathematical judgment. The independent
hash pass checked all 787 regular files in the frozen Stage 1 workspace
bijectively against `stage1_source_hashes`, with no missing, extra, or changed
file. It also reproduced these launcher-bound tree hashes:

| Input | Recomputed SHA-256 |
|---|---|
| Stage 1 workspace, pipeline tree encoding | `3c3125b90c0fcf378bd1a03d47eb8551e6a557c9dc36dabad118fe15b445b924` |
| Stage 1 export, Klean tree encoding | `0f02b98a37e466cd692c50f73ac67a59d4a8c9f9ab4b0c53cca08a4f7a180425` |
| Stage 2 audit | `d60859dcab0d33d1d824a58125eb16f72f154b5495e7c56c6f48b6fb26890c18` |
| Stage 3 manifest | `c32c5d2f344ae78d00c7a0c954844b60931c2c60cc4936068f7b0fb4cd67f284` |
| Stage 4 generation | `0cdaae0482dd9c9a19d1de61c3c518a679a46964873d17d1b01682624b1045d5` |
| Generated project, Klean tree encoding | `8fb9796c2a3edce846af0e5fd5b48140c44018c100075ab191f843f298a3ba83` |
| Stage 4 producer bundle | `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4` |
| Mounted Stage 5 workspace | `37b74253639120e96de7eb2a414d79d6f15c6c4d1a61ebbf1fae3a0c63f4d8a3` |

The required producer-source gate passed:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` |

Those hashes agree exactly with both `source-manifest.json` and
`generator-manifest.json`. The source bundle has exactly the two producer
files plus its manifest. Its image identity agrees in all three independent
records—the source manifest, generator manifest, and the image-key component
of the launcher-recorded producer path:

`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`.

Thus there is no missing or mismatched producer-source infrastructure error.
The complete authentication output is in
[`09_authenticate_and_hash_inputs_result.json`](evidence/09_authenticate_and_hash_inputs_result.json).

## Inventory reconstruction

I invoked `tools.k_rule_inventory.inventory_verification` from the trusted
`/reference/tools/k_rule_inventory.py` against `/reference/k-proof`. The last
applicable `kompile verification.k` command in `prove.sh` selects
`VERIFICATION-BASE`; its local verification-module closure, in frozen source
order, is:

1. `VERIFICATION-SYNTAX`
2. `VERIFICATION-BASE`

The syntax module contains declarations but no rules. The base module contains
42 rules. For every rule, the reconstructed exact source slice equals the
recorded line span; the normalized text independently hashes to
`normalized_sha256`; and `source_rule_id` equals `rule-` followed by that hash.
All IDs are unique and appear in the same order as the protected manifest.

The canonical hash of the complete ordered rule documents is
`009e8ed17e488802f3e2dd33c4513a337ffb64265a0cd9ad1aefcef93e2f9c86`.
It matches the protected Stage 3 inventory hash and all Stage 4 provenance
records. There are no omitted, duplicated, extra, reordered, or hash-changed
rules. The complete 42-row reconstruction and comparison is in
[`06_independent_stage3_result.json`](evidence/06_independent_stage3_result.json).

## Independent Stage 3 classification

I classified each rule from its frozen text and operational role, without
using the protected label as the decision procedure:

| Frozen source span | Count | Independent class | Reason |
|---|---:|---|---|
| 51–53 | 3 | `DEFINITION` | Constructor recurrence defining the total `NumSeq` to `ValSeq` embedding |
| 57–70 | 4 | `DOMAIN_LEMMA` | Logical empty-image, injectivity, and constructor-inversion facts about that embedding |
| 72–74 | 3 | `DEFINITION` | Structural `numLen` recurrence |
| 76–82 | 5 | `DEFINITION` | Structural `lastNonZero` recurrence |
| 84–87 | 1 | `DEFINITION` | Named `validCoeffs` predicate |
| 89–151 | 8 | `DEFINITION` | Exact named macros for translated source syntax and function bodies |
| 155–181 | 10 | `DEFINITION` | Polynomial accumulator, power, and last-element summaries |
| 185–198 | 4 | `DEFINITION` | Guarded expansion-loop endpoint recurrences |
| 202–225 | 4 | `DEFINITION` | Bisection and composed solver recurrences |

Totals are 38 `DEFINITION`, 4 `DOMAIN_LEMMA`, 0 `OPERATIONAL_RULE`, and
0 `PROVED_DERIVED_LEMMA`. This exactly matches Stage 3.

The four domain lemmas are:

- `rule-0dfb3ea463a2e10ce61e8445bcf95e2aa2d4748b432b47ccd1f9825f8cca2630`:
  an embedded sequence is empty exactly when the source `NumSeq` is empty.
- `rule-f684bfbef1c0219f754e562f1888c8a1b7236498affdcf8c5681f52ef8e6175f`:
  injectivity of `numVals`.
- `rule-4f3a4fc13d02a156f3a8d695f13fdac54badb56cceabf4cbe100c7ea4aca4d57`:
  inversion of an integer-headed embedded sequence.
- `rule-f2662dddafe1054c19c3ddaf31b8c9e9a8971c2baafdf6d7f8bfb1785b1ff321`:
  inversion of a float-headed embedded sequence.

They do not qualify as pre-proved derived lemmas. `prove.sh` compiles
`VERIFICATION-BASE`, already containing all four simplifications, before every
`kprove` command, and contains no earlier proof of the same statements against
a module that excludes them.

They are relevant rather than incidental. The K claims pass the source input
as `list(numVals(NS))`; `MPY-LIST` destructs that `ValSeq` through
`.ValSeq`/`vCons` while the constructor-split polynomial loop claims must
recover the corresponding `NumSeq` case. These four facts are precisely the
logical connection between the proof-domain input and the source program's
operational iterator. All rules carrying `[simplification]` are either these
four domain lemmas or recursive definitions.

## Deterministic Stage 4

I reran the required
`tools.klean_preflight.check_generation(/reference/k-proof,
/reference/lemma-discovery.json, /reference/klean-generation, ...)` with
`PYTHONPATH=/reference`.

The first invocation exposed an audit-container issue: the inner process
reported PID 2 while the mounted `/proc` represented the outer PID namespace,
so Lean could not resolve `/proc/<getpid()>/exe`. A narrowly scoped
`LD_PRELOAD` compatibility shim made `getpid()` return the host-visible PID
from `/proc/self/status`; it changed no K, Lean, generator, candidate, or
theorem source. With the pinned `LAKE_HOME` and `LEAN_SYSROOT`, Lean reported
version 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, matching the lock.

The unchanged trusted preflight then returned `PASS`:

- `lake clean`: exit 0;
- `lake build`: exit 0;
- obligation count: 4;
- designated sorry count: 0;
- trust declaration count: 50;
- all immutable input and generated-tree hashes reproduced.

The returned evidence is
[`17_preflight_rerun_result.json`](evidence/17_preflight_rerun_result.json);
the shim source and diagnosis are preserved in
[`16_lean_proc_pid_bridge.c`](evidence/16_lean_proc_pid_bridge.c) and
[`11_lake_environment_diagnosis.txt`](evidence/11_lake_environment_diagnosis.txt).

### Source-rule/obligation bijection

`input-manifest.json`, `obligation-map.json`, the generated target, the
generator manifest, both preflights, and `/audit-input.json` agree exactly.
The independent mapping is:

| Source | Generated obligation |
|---|---|
| Lines 57–59, empty inversion | Universal biconditional between `numVals NS = .ValSeq` and `NS = .NumSeq` |
| Lines 60–62, injectivity | Universal biconditional between equal images and equal `NumSeq`s |
| Lines 63–66, integer-head inversion | Universal biconditional using the exact `nInt`, `vCons`, and `SortInt → SortVal` injection |
| Lines 67–70, float-head inversion | Universal biconditional using the exact `nFloat`, `vCons`, and `SortFloat → SortVal` injection |

Each source ID occurs once, in frozen order. Each conjunct hash, source span,
normalized source hash, inventory hash, and discovery hash recomputes. There
are no extra obligations, omissions, duplicates, changed variables, weakened
directions, hypotheses, literal `True`/`False`, or empty conjuncts. The
biconditionals are the correct truth-preserving formulation of K
simplification rules.

The independently checked target is unique:

- declaration: `Klean32FindZero.Lemmas.targetStatement`;
- statement:
  `Klean32FindZero.Lemmas.targetStatement «numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq»`;
- definition hash:
  `c81220e061bd4ebb9360ad41c3f5745f2b3a76c17a57a60038d87264207f5a8b`;
- statement hash:
  `0a8f6af6d2444051e286b71b908bc64c60eb8610fb54b4e26675426c54637388`;
- parameter binding hash:
  `81f4f72d6f5925c796656dfd9268515ba6bb9e6d2b4be93cd509f0a4a4264f44`.

`SortNumSeq` and `SortValSeq` are nonempty inductive datatypes, and every
conjunct constrains universally quantified images in both directions. The
target is not vacuous. Because the true independent domain set has four
members, Stage 4 correctly uses `PASS`, not `KLEAN_NO_OBLIGATIONS`. Full
results are in
[`20_independent_stage4_result.json`](evidence/20_independent_stage4_result.json).

## Stage 5 clean build, target identity, and trust

I created `/tmp/audit-work/stage5-fresh.HEsYTA`, copied only the candidate
proof/configuration files, and copied the authenticated generated project into
it as `Base`. Before building, `diff -ru` showed `Base` identical to the
generated project. The Base source tree remained identical after the build and
retained generated-tree hash
`8fb9796c2a3edce846af0e5fd5b48140c44018c100075ab191f843f298a3ba83`.

The required complete command logs are:

- [`23_stage5_lake_clean_complete.txt`](evidence/23_stage5_lake_clean_complete.txt):
  `lake clean`, exit 0.
- [`24_stage5_lake_build_complete.txt`](evidence/24_stage5_lake_build_complete.txt):
  `lake build`, exit 0, including a fresh build of `Proof`.

The candidate-controlled Lean source contains no `sorry`, `admit`, `unsafe`,
`axiom`, or `opaque`, including in comments. It declares no `targetStatement`,
so it neither changes nor shadows the generated target. It has exactly one
definition for the required parameter and exactly one `theorem final`.
The local Lake dependency is only `./Base`.

Lean independently elaborated the exact identity:

`Proof.final : Klean32FindZero.Lemmas.targetStatement Proof.«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq»`

and accepted an audit `example` whose type is that same fixed proposition.
See [`35_proof_identity_lean_check.txt`](evidence/35_proof_identity_lean_check.txt).

The exact requested command produced:

```text
'Proof.final' depends on axioms: [propext]
```

See
[`25_print_axioms_proof_final_exact.txt`](evidence/25_print_axioms_proof_final_exact.txt).
There is no `sorryAx`. The generated trust inventory records 50 generated
axiom declarations and zero designated or other sorries; none of those 50
declarations occurs in `Proof.final`'s transitive axiom list. `propext` is
Lean's named core propositional-extensionality axiom, explicitly reported by
Lean, not a new candidate declaration or an unallowlisted generated
declaration. Thus every dependency is accounted for and there is no
unrecorded proof escape.

The static and trust reconciliation is in
[`36_stage5_static_and_trust_result.json`](evidence/36_stage5_static_and_trust_result.json).

## Operational-bridge audit

The sole target parameter is bound to KORE symbol
`LblnumVals'LParUndsRParUnds'VERIFICATION-SYNTAX'Unds'ValSeq'Unds'NumSeq`
and to all four domain-rule IDs. The compiled KORE declares that exact symbol
as a total functional `SortNumSeq → SortValSeq` symbol and contains the three
defining equations from frozen `verification.k` lines 51–53.

The candidate's exact definition is:

- `.NumSeq ↦ .ValSeq`;
- `nInt(i, rest) ↦ vCons(inj_SortInt i, numVals(rest))`;
- `nFloat(f, rest) ↦ vCons(inj_SortFloat f, numVals(rest))`.

This is exactly the frozen K recurrence, not a constant, identity, hard-coded
answer, or theorem-shaped convenience. It also matches the source program and
operational semantics:

- the source `poly` iterates `xs` from head to tail;
- the K proof supplies `xs` as `list(numVals(NS))`;
- `MPY-CORE` defines `ValSeq` as `.ValSeq | vCons(Val, ValSeq)`;
- integers and floats are distinct `Val` injections;
- `MPY-LIST` yields the `vCons` head and recurses on the tail;
- `MPY-CONTROLS` binds each yielded value before executing the loop body.

I compiled an independent universal Lean connection theorem:

```text
∀ ns,
  generated_K_numVals ns =
    some (Proof.numVals ns)
```

It passed for every `SortNumSeq`. Concrete empty and mixed
`nInt(7, nFloat(2.5, .NumSeq))` witnesses additionally check order, payload,
and sort injection.

Three adversarial alternatives were then defined and formally rejected as
incapable of satisfying the fixed target:

1. a constant-empty function;
2. a head-only function that drops the tail;
3. a function that hard-codes every integer payload as zero.

The audit theorem and successful output are
[`34_operational_bridge_check.lean`](evidence/34_operational_bridge_check.lean)
and
[`34_operational_bridge_universal_and_mutation_checks_final.txt`](evidence/34_operational_bridge_universal_and_mutation_checks_final.txt).
An identity function is not even type-correct because `SortNumSeq` and
`SortValSeq` are distinct inductives. These checks establish the operational
bridge independently of the fact that `Proof.final` builds.

## Redundant trusted final gate

The trusted `klean_final_gate.py` independently revalidated the signed audit
input, reran the Stage 4 clean preflight, copied the mounted candidate into
another temporary project, replaced its Base with the authenticated generated
project, clean-built it, type-checked the exact final theorem, and reran
`#print axioms`. It returned `PASS`, with used axioms exactly `["propext"]`.
Its complete result is
[`40_trusted_final_gate_formatted.txt`](evidence/40_trusted_final_gate_formatted.txt).
As that gate states, semantic classification is not mechanically evaluated;
the independent classification and operational judgments above supply that
required mathematical audit.

VERDICT: PASS
LEGITIMACY: LEGIT
