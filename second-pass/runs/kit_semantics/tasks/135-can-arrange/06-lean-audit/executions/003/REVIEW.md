# Independent audit: 135-can-arrange / kit-semantics / SUPPLIED_SEMANTICS

Audit mode was independently read as `CLASSIFICATION_AND_PROOF`. All mounted candidate, provenance, prior-review, log, and comment content was treated as untrusted evidence. Trusted reconstruction and mechanical checks used `/reference/tools`; mathematical classification and operational adequacy were judged independently from frozen K source and execution.

## Outcome

Stage 3's classification and Stage 4's file/hash plumbing are structurally consistent, and the Stage 5 project builds without proof holes or axiom dependencies. The result is nevertheless not legitimate: deterministic Stage 4 erased the only constructor of the frozen `Str` sort. Its fixed Lean target therefore omits the string/string part of the sole domain lemma. The Stage 5 definitions cannot repair this because generated `SortStr` is empty and they eliminate its branches with `nomatch`.

The failure is mathematical and operational, not a producer-provenance or Lean-trust failure.

## Producer-source gate

This gate passed, so no infrastructure `AUDIT_ERROR` applies.

- Actual `/reference/generation-tools/klean_export.py`: `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`.
- Actual `/reference/generation-tools/klean.py`: `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`.
- Both hashes exactly match `source-manifest.json` and `generator-manifest.json`.
- Producer tree hash is `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`, exactly matching `/audit-input.json`.
- The source manifest, generator manifest, and audit-input producer-path basename all bind immutable image `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.

Raw command and result: `evidence/00-context-and-producer.log`.

## Inventory reconstruction and bijection

Trusted `tools.k_rule_inventory.inventory_verification` independently reconstructed the local verification-module closure as:

`VERIFICATION-BASE -> VERIFICATION`

It found 23 rules in source order. For each rule it recomputed the physical source span, whitespace-normalized SHA-256, `source_rule_id`, module, attributes, and text. Results:

- `verification.k` SHA-256: `e67f2b057b77184651c67f8fc12a9646e58483fd881ba0ec8ced3df979e493f3`.
- Inventory SHA-256: `f5b69f74b12f0505988375faf85089ef4d83ccca0e2946d2e4e09f482da52564`.
- Reconstructed IDs are unique.
- Protected classification IDs are unique.
- The two ordered ID sequences are exactly equal.
- Omitted IDs: none.
- Extra IDs: none.
- Reordered identities: none.
- Inventory-hash difference: none.

The complete 23-entry span/hash/ID table is in `evidence/01-rule-inventory.log`.

## Independent Stage 3 classification

The protected classifications are substantively correct.

- Rules 1-2 are `DEFINITION`: they define the named domain predicates `isNumericVal` and `orderablePair`.
- Rules 3-6 are `DEFINITION`: they are the structurally descending `scanDefined` recurrence and its guarded totalization.
- Rules 7-17 are `DEFINITION`: they define `orderGe` over nine numeric combinations, the string/string combination, and the guarded non-orderable complement.
- Rules 18-22 are `DEFINITION`: they are the structurally descending `arrangeSeq` recurrence and its guarded totalization.
- Rule 23, `rule-2fd1883e...b19050` at `verification.k:106-108`, is a `DOMAIN_LEMMA`. It equates the pre-existing observation `applyCmp(">=", V, W)` to the proof-local `orderGe(V,W)` under `orderablePair`; it does not define either observation.

The domain lemma is relevant. The source loop executes `>=`, `scanDefined` permits every adjacent numeric pair and string pair, and the supplied operational semantics has all ten corresponding dispatch cases.

It is not a `PROVED_DERIVED_LEMMA`: Stage 1 proves ten sort-specialized claims against `VERIFICATION-BASE`, but never first proves the exact dynamic guarded rule and then imports it for a later proof. Rerunning the ten specialized claims produced `#Top`; their non-identity to the exact rule remains decisive for classification. There are no ordinary `OPERATIONAL_RULE` entries in this local proof-module closure. Every rule bearing `simplification` is classified as `DEFINITION` or `DOMAIN_LEMMA`.

Case-by-case comparison with `int.k`, `bool.k`, `float.k`, and `str.k` confirms the domain lemma's mathematics: the fixed dispatch and `orderGe` agree for Int/Int, Bool/Bool, Bool/Int, Int/Bool, Float/Float, Int/Float, Float/Int, Bool/Float, Float/Bool, and Str/Str.

Details are in `evidence/02-independent-classification.log`; the complete live K proof output is in `evidence/11-connection-kprove.raw.log`.

## Deterministic Stage 4 integrity

The required trusted call to `tools.klean_preflight.check_generation` was rerun with `PYTHONPATH=/reference`. The audit namespace initially hid `/proc/<pid>/exe`, which Lean 4.22 uses for self-location; a narrow readlink shim redirected only that path form to `/proc/self/exe`. With it, the pinned toolchain identified itself as Lean 4.22.0 commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and the preflight returned `PASS` after a real temporary `lake clean` and `lake build`.

Recomputed structural bindings all agree:

- Stage 1 tree: `1b3dd0a9969538031ffe5ae120ffe22df07388f253b5e6234def725583cb4dbf`.
- Stage 3 manifest: `aafc91d063f2bf10a1025b189e023aa40814f6c46eaa293b97bc1e6e67cb1beb`.
- Generated tree: `3385ac6364d0b8e9436c7956e6dc7dec10fcb838ccb0c447cd8075cf70622641`.
- Obligation map: `b810ff3614a4b526554d9bb44e08fe759df914b1ed3ddbc557acf857d9be45ae`.
- Domain-rule IDs, obligation source-rule IDs, and mapped source-rule IDs are the same unique one-element ordered list.
- Obligation count is 1, so this is correctly not `KLEAN_NO_OBLIGATIONS`.
- There are no duplicated obligations or vacuous top-level conjuncts; the guard has realizable numeric witnesses.

The fixed generated declaration is exactly `Klean135CanArrange.Lemmas.targetStatement`. Its recomputed definition hash is `29c9d56b6c41f072e1ffbf7a268135fe25c7df1e7221ad70d5f8d0796d516fc3`; statement hash is `f6546a0c884ecb415a7b6dffde624a2418ff099073c317144ff6bc9b0d5340d0`. Both exactly match the generator manifest and audit input. Structurally, it states:

```lean
forall (W V : SortVal),
  orderablePair V W = true ->
  applyCmp ">=" V W = orderGe V W
```

Preflight evidence is in `evidence/03-trusted-preflight.log`; independent manifest and target recomputation is in `evidence/04-manifest-bijection-and-target.log`.

## Stage 4 mathematical failure: erased strings

Structural identity does not make the generated obligation equivalent to the frozen rule.

Frozen K declares `syntax Str ::= str(IntSeq)` in `semantics/core.k:15`. That constructor is a `Val` through `Str < Iterable < Val`. Frozen `verification.k` explicitly includes strings in `orderablePair`, gives `orderGe(str(A),str(B)) = notBool strLt(A,B)`, and the source domain lemma therefore covers string pairs. Frozen `semantics/str.k:59` independently defines `applyCmp(">=", str(A), str(B))` by the same lexicographic observation.

Generated `Klean135CanArrange/Sorts.lean:7` instead contains only:

```lean
inductive SortStr : Type
```

There is no `str : SortIntSeq -> SortStr` constructor anywhere in the generated tree. Although `SortVal` has `inj_SortStr : SortStr -> SortVal`, no such value can be formed. The fixed theorem's string subdomain is therefore empty.

This is not an irrelevant model boundary. Frozen K executes strings. Independently rerunning `krun smoke.mpy --definition runtime-kompiled` completed with `.K` and exit code 0, including the asserted source execution `can_arrange(["b","a","c"]) == 1`; its heap contains the concrete `str(iCons(...))` values. Strings are also material to the source program and postcondition because adjacent string ordering controls the returned index.

The generated target consequently proves only nine numeric dispatch combinations, not the ten source combinations named by its sole obligation. This is a weakened Stage 4 obligation and requires `FAIL`/`NOT_LEGIT` despite self-consistent manifests and hashes.

Exact source/generated/candidate lines and the operational witness are in `evidence/05-string-universe-weakening.log` and `evidence/10-k-string-witness.log`.

## Stage 5 clean build, target identity, and source hygiene

A fresh project was created at `/tmp/audit-work/135-can-arrange-proof-audit`; the immutable generated project was copied as `Base`. Its tree hash remained exactly `3385ac...622641`.

Under the pinned Lean toolchain:

- `lake clean`: exit 0.
- `lake build`: exit 0; `Proof` and the immutable target module built successfully.

The candidate does not change or shadow the generated target:

- Fresh `Base/Klean135CanArrange/Lemmas.lean` file SHA-256 equals the reference file SHA-256: `747802744cbc1cdeaf0fbe298526decb2ded24aca359c1deecbfcc09ce9bc627`.
- The candidate's writable Lean files are only `Proof.lean` and `lakefile.lean`.
- They define no `targetStatement` and no duplicate target module.
- They contain zero `sorry`, `admit`, or `unsafe` tokens and no new `axiom` or `opaque` declarations.
- `Proof.final` has exactly the fixed target applied to the three manifest-bound parameter definitions, not a duplicate or separately weakened theorem.

Complete build and static-scan output: `evidence/06-proof-clean-build.log` and `evidence/08-candidate-static-audit.log`.

## Axiom accounting

The exact audit command `lake env lean AuditAxioms.lean`, where the file imports `Proof` and runs `#print axioms Proof.final`, returned:

```text
'Proof.final' does not depend on any axioms
```

The trusted Stage 4 preflight found 44 generated executable-hook trust declarations and reconciled them exactly with `trust-inventory.json`; `Proof.final` uses none. There is no `sorryAx` and no recorded or unrecorded proof-trust dependency. See `evidence/07-axioms.log`.

## Stage 5 parameter operational bridge

The three exact candidate definitions are at `Proof.lean:306`, `:310`, and `:314` and bind the manifest KORE symbols `applyCmp`, `orderGe`, and `orderablePair` to sole source rule `rule-2fd1883e...b19050`.

For every generated numeric inhabitant, their definitions match the frozen rule table. Direct adversarial evaluation passed ordinary Int and Bool cases, mixed Int/Float around 2^53, positive and negative infinity, NaN under the supplied K `not(<)` rule, and the minimum positive subnormal. These finite checks support, but do not replace, the line-by-line semantic comparison.

The bridge fails on the required string domain. Candidate `operationalOrderGe` handles `inj_SortStr` only by `nomatch`, and `operationalApplyCmp` does the same. A Lean audit theorem `SortStr -> False` compiles. The candidate itself acknowledges that the MPY-STR rules are unrepresentable. Thus none of the three parameter definitions implements its bound KORE symbol over the complete frozen rule domain.

The proof is also intentionally easy to satisfy once parameter meanings are not independently enforced: a counterfactual with constant-false `orderGe` and an `applyCmp` whose `>=` branch calls it still proves the exact fixed target. That mutation compiled. The submitted numeric definitions are not constant, but the mutation demonstrates why clean elaboration and a clean axiom list cannot compensate for the missing operational domain.

Adversarial outputs and the compiled counterfactual are in `evidence/09-operational-adversarial.log`.

## Final judgment

Stage 3 classification is accepted. Stage 4 passes provenance, hash, bijection, and mechanical preflight checks, but fails the required mathematical equivalence by erasing reachable strings. Stage 5 builds and is axiom-free, yet necessarily inherits that weakened universe and fails the operational bridge for all string values. The fixed theorem therefore does not establish the sole domain lemma over the frozen program's complete relevant domain.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
