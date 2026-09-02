# Independent audit: `86-anti-shuffle`

## Scope and result

The launcher and `AUDIT_MODE` both select `CLASSIFICATION_AND_PROOF` for condition `kit-semantics` and semantics mode `SUPPLIED_SEMANTICS`. I independently audited the frozen Stage 3 classification, deterministic Stage 4 export, and Stage 5 Lean proof. All proof-bearing checks pass.

One execution-environment issue occurred before the first Lean build: this container reports a PID-namespace value from `getpid()` while exposing `/proc` from another namespace. Lean 4.22 therefore could not resolve `/proc/<pid>/exe`. The preserved minimal preload shim changes only that lookup to the kernel-equivalent `/proc/self/exe`; after it was applied, Lean identified the pinned 4.22.0 toolchain and all trusted checks ran normally. This did not alter source, generated artifacts, elaboration, compilation, or kernel checking.

## Producer provenance and hashes

The immutable Stage 4 producer sources pass the required precondition:

- `klean_export.py`: `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`.
- `klean.py`: `ba1148c5df311b510d03f95887839e72b878bbe302c54fd0d981cf568ea8eaa1`.
- Producer bundle under the launcher's length-delimited tree-hash contract: `e2997e276bc28e190348cbf865548aaeda9c5a355767876bf0a1e21fec2aada8`.
- Immutable generator image: `sha256:a12daa6dccbac0cead0f384a86899561d3ceb2d478ef3f182ec36ec52ba2cb77`.

The two file hashes agree with both `source-manifest.json` and `generator-manifest.json`. The image ID agrees with those manifests and the image-key component of the producer path recorded in `/audit-input.json`. Thus there is no producer-source infrastructure error.

The signed audit-input envelope digest recomputes to `55f1eed6ca58a98222e1043039ebb7b95ecadd13ddcd3849f9d39b61993c599e`. Every mounted resolution hash recomputes exactly, including the two distinct Stage 1 hashes, selected K audit, selected Klean generation, producer bundle, generated project, discovery manifest, and candidate workspace. All 794 Stage 1 per-file hashes form an exact path/hash map. The launcher-recorded Stage 5 invocation directory itself was not mounted, so its signed invocation hash cannot be recomputed from the available inputs; it is not used as proof evidence. The mounted candidate workspace hash does recompute exactly.

## Inventory reconstruction and classification

I ran the trusted `tools.k_rule_inventory.inventory_verification` implementation directly on `/reference/k-proof`. The local verification-module closure is exactly `VERIFICATION`. It contains nine unique rules in source order. The reconstructed `verification.k` hash is `303963e3703c0a00059f7bd9841056f40f76498247bcbb568700c3de2399ead2`; the canonical whole-inventory hash is `b6a5c8a6de1f4db5b68d5cc26578cacf31fb03dfb7b59d122c3544c81b30760c`.

For every entry below, the normalized source SHA-256 is the suffix of its `source_rule_id`:

| Span | `source_rule_id` | Independent class | Reason |
|---|---|---|---|
| 8–12 | `rule-8035a5d5e2dd908c685b0f3f6b47722aade54582ecf7e781dfd68bc1469d72b1` | `DOMAIN_LEMMA` | Load-bearing singleton-string ordering fact over semantics-defined `strLt`; marked `simplification`. |
| 21–33 | `rule-dc6f73badfec4f23e1af1f381ddb673851960f3a7dd453b5a529e29eea13dbc1` | `DEFINITION` | Exact fresh `antiInnerBody` AST alias. |
| 35–43 | `rule-d8c6975c42f7acfdc026a371bbd271bff09144d250d960f6b474f010e3a77c91` | `DEFINITION` | Exact fresh `antiPostInsert` AST alias. |
| 45–56 | `rule-0f9f3b5d7e5349a6b9e4e08ae6ff00e9b64d8642453a18a90ada8eea2bfa6d08` | `DEFINITION` | Exact fresh `antiOuterBody` AST alias. |
| 58–61 | `rule-5075fc023e8cdbd37d170a98412b835adec6946ebd2141dee39edbea6eb0d8ad` | `DEFINITION` | Exact fresh `antiTail` AST alias. |
| 68–72 | `rule-c4913eca7f7a04a7ced779f502220f126d5ee7b0ee403b488e8b7e5329129ccb` | `DEFINITION` | Base equation for the fresh `insertGo` recurrence. |
| 73–91 | `rule-f0184627a2c4a3d544b5b84141379073793a96b835d2753217df57bda16c9883` | `DEFINITION` | Structurally recursive step for `insertGo`. |
| 95–96 | `rule-652e6e29910efceeca6a31b0b63ec16bfe1d38ac2b9054d6d2a69a37ba8dcec4` | `DEFINITION` | Base equation for the fresh `antiGo` recurrence. |
| 97–107 | `rule-6e83d7b52d40fb31d78ba87b9b7e825cf4ae9515a0fa193cce3b0b083ee08657` | `DEFINITION` | Structurally recursive space/non-space step for `antiGo`. |

The reconstructed IDs, spans, texts, attributes, normalized hashes, and order are bijective with `/reference/lemma-discovery.json`: no omission, duplicate, extra rule, reordered identity, changed hash, or unaccounted class exists.

The four AST aliases expand exactly to the source statements at `solution.py` lines 9–26. `insertGo` is the insertion-loop recurrence: its base appends the pending character exactly when it has not yet been inserted, and its step consumes one old character while preserving insertion order and flag state. `antiGo` is the outer recurrence: spaces flush `word` plus a space into `result`, while non-spaces use `insertGo`; its base appends the final word. These rules name syntax or mathematical summaries and do not preempt the MPY machine, so `DEFINITION` is the correct class.

The remaining rule is not a definition because `strLt` belongs to supplied module `MPY-STR`. It is not an ordinary operational rule and is not labeled `PROVED_DERIVED_LEMMA`. The supplied semantics gives the three lexicographic head cases: less is `true`, greater is `false`, and equal recurses to empty/empty, which is `false`; therefore the singleton result is exactly `C <Int D`. It is relevant, not decorative: source line 17 branches on `char < old_char`, string iteration yields singleton strings, and `applyCmp("<", ...)` calls `strLt`. Its `simplification` attribute is permitted because its independent class is `DOMAIN_LEMMA`. Stage 1's separate `LEMMA-SPEC` case claims import `MPY`, not `VERIFICATION`, and support truth of the domain fact without changing its category.

There are no independently classified `OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA` entries. The independent class sequence exactly matches Stage 3.

## Stage 4 generation and fixed target

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` on the required three inputs and the frozen toolchain lock. It returned `PASS`, rebuilt the generated project successfully, reported one obligation and zero sorries, and reproduced:

- Stage 1 export: `30ee607e4db2c763d3a61fbd783e6d1d4e23c5f2e1d49916ea0f428d024add1d`.
- Stage 3 discovery manifest: `8b892fc118ea37134ed4830b5884a29bd7cee238dcb7dfdc52df1157138f744b`.
- Generated tree: `3100c8f10f114de235c3a5648e26915592b6514fdf7732d25c9a6ca61e8460e4`.

The independently reconstructed domain set contains exactly the one singleton `strLt` rule, so `KLEAN_NO_OBLIGATIONS` would have been illegitimate. The selected status is correctly `PASS` with one obligation.

The obligation map is an ordered one-to-one mapping from that rule ID to this exact non-vacuous conjunct:

```lean
∀ (D : SortInt) (C : SortInt),
  strLt (iCons C .IntSeq) (iCons D .IntSeq) = intLt C D
```

The actual generated identifiers are the quoted Klean names recorded in the manifest. The proposition quantifies all `SortInt` values, has no stronger precondition, no dropped case, no `True` padding, and no irrelevant conjunct. It is exactly the frozen K rewrite with harmless binder reordering/renaming.

`Klean86AntiShuffle.Lemmas.targetStatement` is the exact conjunction of that sole obligation. Its definition hash is `aba8f4d2a1c79951c87c408cf510ad23e55c9635499c269298109850f925c20a`; its applied-statement hash is `e3bf236183914b6dcbb7f27f777c3e9afcc0c26891e92ec12a7b58b0a1c8da2e`. Declaration, file, definition, statement, parameter order, KORE symbols, source-rule links, binding hashes, and target hashes agree among the generated source, obligation map, generator manifest, stored and rerun preflight, and `/audit-input.json`.

## Stage 5 build, proof identity, and trust

I created `/tmp/audit-work/stage5-proof-audit`, copied the immutable generated project into it as `Base`, and copied the candidate around it. `Base` had the exact generated-tree hash before the build and remained exact afterward. In that fresh workspace:

- `lake clean` exited 0.
- `lake build` exited 0 with `Build completed successfully.`
- The trusted Stage 5 mechanical gate independently repeated clean, build, exact-target checking, and axiom checking and returned `PASS`.

The candidate defines each target parameter exactly once, imports the fixed target, and does not define or shadow `targetStatement`. Outside `Base`, no Lean source contains `sorry`, `admit`, `unsafe`, a new `axiom`, or a new `opaque`. `Proof.final` has exactly the fixed type

```lean
Klean86AntiShuffle.Lemmas.targetStatement
  Proof.«_<Int_»
  Proof.«strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq»
```

and is not a duplicate or weakened theorem.

Lean's exact output is:

```text
'Proof.final' depends on axioms: [propext]
```

There is no `sorryAx`. The generated trust inventory contains 41 allowlisted declarations; none is a dependency of `Proof.final`. The trusted mechanical gate's baseline Lean trust set explicitly accounts for core `propext` (as well as `Classical.choice` and `Quot.sound` if used). Thus the sole dependency is recorded as standard Lean foundational trust, with no unexpected or candidate-created escape.

## Operational meaning of target parameters

The manifest binds `«_<Int_»` to KORE symbol `Lbl'Unds-LT-'Int'Unds'` and the singleton-domain rule. `SortInt` is Lean `Int`; the candidate definition is exactly `decide (left < right)`. It is neither constant nor hard-coded and agrees definitionally with K integer order, including negative and equal values.

The manifest binds `«strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq»` to the supplied `MPY-STR` KORE symbol and the same rule. The candidate exhaustively implements all six frozen operational cases:

- empty/empty is false;
- empty/nonempty is true;
- nonempty/empty is false;
- a smaller head is true;
- a greater head is false; and
- equal heads recurse on both tails.

The final branch recurses when Lean integers are neither less nor greater, which by integer trichotomy is exactly K's `A ==Int B` guard. The definition is a pure total value function and has no control or state footprint to omit.

An audit-only universal Lean theorem proves, for every pair of finite integer lists encoded as `SortIntSeq`, that the candidate function equals an independent executable restatement of those supplied operational cases. The theorem checks with only standard `propext`; the direct integer bridge theorem is axiom-free. Adversarial evaluations cover all empty boundaries, negative heads, less/greater heads, equal-head recursion, strict prefixes in both directions, equal sequences, and head-dominant suffixes; all candidate/oracle pairs agree.

Counterfactual probes demonstrate why the clean target proof alone was insufficient:

- Coordinated constant-false definitions satisfy the generated singleton equation.
- A head-only comparator also satisfies the generated singleton equation but incorrectly reports `[1] < [1, 0]` as false.
- The candidate reports that prefix case as true and the universal bridge theorem fixes its behavior on all tails.
- Pairing the honest integer comparator with constant-false `strLt` is rejected on the concrete singleton witness `0 < 1`.

These probes rule out the constant, identity, hard-coded, vacuous, and singleton-only operational-bridge failures called out by the audit contract.

## Evidence

Authoritative raw commands and results are in `/audit-output/evidence/`:

- `01-provenance-inventory-v2.log`: producer provenance, full reconstructed inventory, ordered bijection, and classifications.
- `02-preflight-rerun.log`: returned trusted preflight evidence.
- `02a-lean-runtime-repair.log` and `procself_shim.c`: reproducible PID/procfs environment correction and pinned-toolchain identification.
- `03-stage4-integrity.log`: audit-input signature, all mounted hashes, 794 Stage 1 file hashes, obligation bijection, and target identity.
- `04-fresh-workspace.log`, `05-lake-clean.log`, and `06-lake-build.log`: isolated workspace and complete clean-build transcripts.
- `07-candidate-static-v3.log`: forbidden-token, trust-declaration, shadowing, parameter, and exact-statement checks.
- `08-print-axioms.log`, `09-proof-identity.log`, `10-final-gate.log`, and `13-axiom-accounting.log`: exact theorem, axiom output, trusted mechanical gate, and trust reconciliation.
- `11-operational-bridge-v2.log` and `14-compiled-definitions.log`: universal bridge check, adversarial/counterfactual results, and Lean's compiled definitions.
- `12-relevant-source.log`: frozen K rules, supplied `MPY-STR` semantics, source solution, generated target, and candidate proof.

The `diagnostic-*` logs preserve auditor-side trial-method corrections (the wrong tree-digest family and two regex patterns); the authoritative corrected results are the versioned logs named above. The initial `02-preflight.log` preserves the pre-shim environment failure.

VERDICT: PASS
LEGITIMACY: LEGIT
