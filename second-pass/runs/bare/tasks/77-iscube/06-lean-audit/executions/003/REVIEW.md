# Independent audit: HumanEval `77-iscube`

Audit mode: `CLASSIFICATION_AND_PROOF`  
Condition: `bare`  
Semantics mode: `GENERATED_SEMANTICS`

## Result

The Stage 3 classification is complete and correct, the selected Stage 4
generation is bound bijectively to the two genuine domain lemmas, and the
Stage 5 candidate cleanly proves the exact fixed target using faithful
implementations of all eight K builtin parameters. I found no omitted rule,
classification error, target weakening, proof hole, unrecorded trust escape,
or operational-bridge mismatch.

I treated the candidate, prior audit, comments, logs, and manifests as
untrusted evidence. The conclusions below come from the frozen sources,
trusted inventory/preflight/mechanical-gate code, independently authored
checks, and fresh builds.

## Frozen-input and inventory reconstruction

The frozen `verification.k` SHA-256 is
`c941d95f59a2ddb57298abbb42ad637dfc84c7753c2907462ce4ebc3cd966659`.
The trusted inventory code selected the local verification-module closure
`VERIFICATION`, `GAP-VERIFICATION`, with `GAP-VERIFICATION` as the last Stage 1
verification main module. It reconstructed exactly four rules:

| Source rule | Module and span | Attributes | Independent classification |
|---|---|---|---|
| `rule-de3f9727c1b2c9f19559bcf49d9facf57997eb3c9d4715f670ff6644a77098f9` | `VERIFICATION:11-24` | none | `DEFINITION` |
| `rule-b88003e929c70fa00f8441eaf77e74ba66845261dacd5efbb19e5da9b5a59865` | `VERIFICATION:27` | none | `DEFINITION` |
| `rule-71fab8be3031badfbb8efe37c8587b786b455d6670cf74a013dbf65634d49027` | `GAP-VERIFICATION:36-44` | `simplification` | `DOMAIN_LEMMA` |
| `rule-5cd618327b17d41867b4a5cadea7277532d58e8066be05ee8bd76b5c99b6690f` | `GAP-VERIFICATION:46-54` | `simplification` | `DOMAIN_LEMMA` |

For every entry, the rule ID equals `rule-` followed by its reconstructed
normalized source hash. The source spans, text, attributes, normalized hashes,
and ordered identities match `/reference/lemma-discovery.json`. Both sides
contain four unique entries, with no omission, duplicate, extra entry, or
reordering. The independently recomputed whole-inventory hash is
`768c6d425e02156c7113c418107467c11510230db45758138d0307d7efd017c9`,
equal to the protected value.

### Independent classification judgment

1. `iscubeProgram => Module(...)` is a `DEFINITION`. It expands a named proof
   term to the exact source-program constructor tree; after expansion, normal
   MPY operational rules execute the program. It is a permitted named macro,
   not a mathematical lemma or an execution shortcut.

2. `cube(I) => I *Int I *Int I` is a `DEFINITION`. The `[function,total]`
   symbol names the cubic expression used by the specifications.

3. The first simplification rule is a `DOMAIN_LEMMA`. Under its premises,
   suppose `I` were not less than `N+1`. Together with `I <= N+1`, this gives
   `I = N+1`. The gap premise gives
   `N^3 + D < (N+1)^3`, while the final guard would give the strict reverse,
   a contradiction. This is a nontrivial arithmetic implication, not a
   definition or ordinary operational observation.

4. The second simplification rule is also a `DOMAIN_LEMMA`. If
   `I != N+1`, integrality and `I <= N+1` give `I <= N`. Nonnegativity makes
   cubing monotone, so `I^3 <= N^3`; but `D > 0` and the final guard imply
   `N^3 < N^3 + D <= I^3`, a contradiction. Thus `I = N+1`.

The Stage 1 script compiles `GAP-VERIFICATION` with both rules already present
and only then proves `GAP-SPEC`. It contains no earlier proof of either exact
rule against a module that omits it, so neither qualifies as a
`PROVED_DERIVED_LEMMA`. Both `[simplification]` rules are classified as
`DOMAIN_LEMMA`, satisfying the simplification restriction.

The domain lemmas are directly relevant. The source loop increments `n` while
`n^3 < a` and returns whether the stopped cube equals `a`; `GAP-SPEC` uses
inputs `a = N^3 + D` strictly between consecutive cubes. The two rules
respectively justify continuing below `N+1` and identifying the stopped index
as `N+1`. Premises are satisfiable: `(N,I,D)=(1,1,1)` witnesses the first
rule and `(1,2,1)` witnesses the second. Fresh executions of the frozen MPY
semantics also produced the expected cube/non-cube results for
`-9,-8,-2,0,1,2,8,9,64,180`.

Evidence:
[`01_reconstruct_inventory.json`](evidence/01_reconstruct_inventory.json),
[`15_stage3_classification_sources.log`](evidence/15_stage3_classification_sources.log),
and [`16_frozen_program_runs.log`](evidence/16_frozen_program_runs.log).

## Stage 4 producer authentication and provenance

I authenticated the producer sources before judging Stage 4:

| Producer source | Observed SHA-256 |
|---|---|
| `klean_export.py` | `2f04f1bc0f49f9f8c6f009875e730866a61c76ac029663d2ed2ffaffeab4e773` |
| `klean.py` | `308fb4d213034fc0c00cd37e9617f6b05f10bda7bc7e383994786911f8a04bcc` |

These hashes match both `source-manifest.json` and `generator-manifest.json`.
The immutable image ID is
`sha256:9b919795ce70e46b5f58b36984cd9be4f84d1b056135e41498da6390ff4c5fa2`
in both manifests; its digest component is also the producer-bundle key in
the launcher-recorded path. The bundle contains exactly the two producer
files and its source manifest. Its recomputed tree hash,
`305f865953323958cc46250998c0ae761309c7bc7c60d6a2206b72df280f8354`,
matches `/audit-input.json`. There is therefore no producer-source
infrastructure error.

All mounted launcher-bound tree/file hashes recomputed exactly: Stage 1 K
workspace, Stage 1 export tree, discovery manifest, selected K audit, selected
Klean generation, producer bundle, generated project, and Lean candidate.
The per-file Stage 1 source hash map also matches exactly. The obligation-map
hash is
`36d31bd7379829c8f298da4634c2dbb6da06e2bca62d7becfbb0a9352453da8d`
and the trust-inventory hash is
`4e3ffaed4e0bb2de84ae4175f107d1eb379936c7a1275a51e4dc23d2079a2a4c`,
matching their manifests. The generator toolchain object equals the trusted
lock. The audit envelope digest validates as
`8284846178aad8d9c29560bdce87a62b4e7c966ce1eaf2ee707a95c842067c33`.

The launcher also records a Lean-invocation tree hash, but no Lean-invocation
tree is among the mounted inputs, so that one signed metadata value cannot be
independently recomputed. It is not used as proof or Stage 4 evidence; the
mounted Lean workspace itself was rehashed and rebuilt.

Evidence:
[`02_producer_authentication.log`](evidence/02_producer_authentication.log),
[`03_verify_recorded_hashes.json`](evidence/03_verify_recorded_hashes.json),
and [`18_all_manifest_hashes.json`](evidence/18_all_manifest_hashes.json).

## Stage 4 preflight, obligation bijection, and fixed target

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
over the required three inputs. The first attempt exposed a runner-specific
PID-namespace problem: Lean 4.22 queried `/proc/<nested-pid>/exe`, while this
container exposes `/proc` in the outer namespace. I retained that failed
attempt. A minimal compatibility preload redirected only that `readlink`
shape to `/proc/self/exe`; it then reported the pinned Lean
`4.22.0`, commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.
With that environment correction, the unchanged trusted checker returned
`PASS`; `lake clean` and `lake build` both exited zero. The replayed evidence
is byte-for-byte equal as JSON to the selected preflight recorded by the
launcher.

The independently classified domain set has exactly these two ordered IDs:

1. `rule-71fab8be3031badfbb8efe37c8587b786b455d6670cf74a013dbf65634d49027`
2. `rule-5cd618327b17d41867b4a5cadea7277532d58e8066be05ee8bd76b5c99b6690f`

`input-manifest.json`, the obligation map's source records, and its obligations
contain exactly those same IDs in that order. Each source record matches the
reconstructed module, span, text, attributes, and normalized hash; each
obligation carries the same span and hash, and each Lean-conjunct hash
recomputes. There are no other source obligations, duplicates, or omissions.

The generated propositions are exact translations of the K rules: K's
left-associated `andBool` premise becomes a Boolean conjunction equal to
`true`, and `rule lhs => true requires premise` becomes a universally
quantified implication from that premise to `lhs = true`. All arithmetic and
comparison operations are retained as explicit target parameters. Neither
conjunct is weakened or irrelevant. The warning that binder `h` is unused is
the normal Lean encoding of implication—`h` occurs as the typed premise
binder, while the conclusion need not mention the proof object. Both premise
types are inhabited by the witnesses above, and deliberately strengthened
conclusions are false on those witnesses.

The generated target is unique:

- declaration: `Klean77Iscube.Lemmas.targetStatement`;
- definition SHA-256:
  `c3c8b0cf83982c67b43958d67a0d411a787722dfb126effabceb89bbd25d9fd6`;
- instantiated-statement SHA-256:
  `62d5c1728b668edca6cedca0e3d7d020894b66bc4a1c9be50e791dbca195cebb`;
- generated-tree hash:
  `01021315ed43f873b7dfd83015184249e65b44416a4e3a4d94bf6e27301f68d1`.

I independently assembled the target definition from the two obligation
strings and eight bindings; it is textually identical to the generated
declaration. The computed target object equals the generator manifest, audit
input, selected preflight, and replayed preflight. This is correctly a
two-obligation `PASS` generation, not `KLEAN_NO_OBLIGATIONS`.

Evidence:
[`04_check_generation_returned.json`](evidence/04_check_generation_returned.json)
records the initial environment failure,
[`06_check_generation_returned.json`](evidence/06_check_generation_returned.json)
is the successful returned evidence, and
[`09_stage4_target_bijection.json`](evidence/09_stage4_target_bijection.json)
contains the independent bijection and target reconstruction.

## Stage 5 clean proof and target identity

I created `/tmp/audit-work/77-iscube-proof-audit`, copied the candidate there,
and copied the immutable generated project as `Base`. Before building, `Base`
had the required generated-tree hash. I then ran, in that fresh project:

```text
lake clean
lake build
```

Both commands exited zero; the complete build output is retained. The build
compiled the immutable generated modules and `Proof`. The `Base` tree hash and
the target file hash remained unchanged afterward.

Candidate-source scanning found no `sorry`, `admit`, `unsafe`, `axiom`, or
`opaque`. It declares exactly the eight required definitions and
`theorem final`; it declares no competing `targetStatement`. `#print
Proof.final` shows that the theorem's type is exactly:

```text
Klean77Iscube.Lemmas.targetStatement
  Proof.«_-Int_» Proof._andBool_ Proof.«_>=Int_» Proof.«_<Int_»
  Proof.«_<=Int_» Proof.«_==Int_» Proof.«_+Int_» Proof.«_*Int_»
```

Thus `Proof.final` proves the fixed generated theorem, not a duplicate,
shadow, or weakened variant.

Running Lean with `#print axioms Proof.final` produced exactly:

```text
'Proof.final' depends on axioms: [propext]
```

The trusted mechanical gate explicitly recognizes `propext` (along with
`Classical.choice` and `Quot.sound`) as a standard Lean foundational axiom
outside the generated declaration inventory. Reconciliation found:

- used generated allowlisted axioms: none of 44;
- used standard foundational axioms: `propext`;
- unexpected or unrecorded proof escapes: none;
- `sorryAx`: absent.

The trusted final mechanical gate independently repeated preflight, clean
build, exact-type checking, and axiom parsing and returned `PASS`.

Evidence:
[`08_clean_build_fresh_project.log`](evidence/08_clean_build_fresh_project.log),
[`10_candidate_source_gate_corrected.log`](evidence/10_candidate_source_gate_corrected.log),
[`11_print_axioms_and_final.log`](evidence/11_print_axioms_and_final.log),
[`12_mechanical_final_gate.json`](evidence/12_mechanical_final_gate.json), and
[`17_axiom_and_bridge_reconciliation.json`](evidence/17_axiom_and_bridge_reconciliation.json).

## Operational bridge

The pinned K `domains.md` declares the eight bound KORE symbols as total
`BOOL.and`, `INT.sub`, `INT.ge`, `INT.lt`, `INT.le`, `INT.eq`, `INT.add`, and
`INT.mul` hooks. Generated `SortInt` is Lean `Int` (unbounded mathematical
integers) and `SortBool` is Lean `Bool`. The candidate implements each exact
meaning:

| Target parameter | Frozen K meaning | Candidate definition |
|---|---|---|
| `«_-Int_»` | integer subtraction | `x - y` |
| `_andBool_` | Boolean conjunction | `x && y` |
| `«_>=Int_»` | integer `>=` | `decide (x >= y)` |
| `«_<Int_»` | integer `<` | `decide (x < y)` |
| `«_<=Int_»` | integer `<=` | `decide (x <= y)` |
| `«_==Int_»` | integer equality | `decide (x = y)` |
| `«_+Int_»` | integer addition | `x + y` |
| `«_*Int_»` | integer multiplication | `x * y` |

These operations also align with the source solution and frozen operational
MPY rules: unary negation uses subtraction; loop increments use addition;
cube expressions use multiplication; source branches/loop/return use `<` and
`==`; and the two exact domain rules additionally use conjunction, `>=`, and
`<=`.

Independent Lean checks establish universal definitional equality of every
candidate definition to its intended Lean operation and exhaust the Boolean
truth table. Independently authored K execution produced matching reports for
`(5,2)`, `(2,5)`, `(-3,-3)`, `(-3,2)`, and
`(1000000000000,-3)`, including order reversal, equality boundaries,
negative values, and unbounded multiplication.

Counterfactual candidate mutations were also checked and distinguished:
identity subtraction, `or` in place of conjunction, strict/non-strict
comparison swaps, always-true equality, identity addition, and addition in
place of multiplication all disagree with the candidate on explicit
witnesses. The two obligation witnesses evaluate to true premises and true
actual conclusions, while strengthened/counterfactual conclusions evaluate
to false. The bridge is therefore body-sensitive and not constant,
hard-coded, identity-based, or vacuous.

Evidence:
[`13_operational_bridge_sources.log`](evidence/13_operational_bridge_sources.log)
and [`14_operational_bridge_tests.log`](evidence/14_operational_bridge_tests.log).

VERDICT: PASS
LEGITIMACY: LEGIT
