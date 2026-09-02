# Independent Stage 3–5 audit: `21-rescale-to-unit`

## Scope and result

The launcher records `AUDIT_MODE=CLASSIFICATION_AND_PROOF`,
condition `kit-semantics`, and semantics mode `SUPPLIED_SEMANTICS`.

Stage 3's classification and Stage 4's deterministic generation are
structurally consistent with the frozen K workspace. The Stage 5 project also
clean-builds and proves the exact generated target without a candidate-added
axiom. It is nevertheless not legitimate: one of the six candidate
definitions, the total definition bound to the global KORE `applyBin` symbol,
is a source-case-only implementation with a `noneV` default. It disagrees with
ordinary defined cases of the supplied operational semantics. This is the
operational-bridge failure that determines the final verdict.

## Input and producer integrity

I hashed the two generation-time producer files before judging Stage 4:

- `klean_export.py`:
  `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`
- `klean.py`:
  `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346`

These values agree among the mounted files, `source-manifest.json`, and
`generator-manifest.json`. The immutable image ID also agrees:
`sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`.
The audit input identifies the same image by the final component of its
generation-producer-source path. The producer tree hash is the recorded
`bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`.
There is no producer-source infrastructure error.

All mounted tree/file hashes recorded by the launcher match independently
recomputed values: the Stage 1 workspace and export hashes, all 777 Stage 1
source-file hashes, the Stage 2 audit tree, discovery manifest, selected
generation tree, generated project, producer-source tree, and candidate
workspace. The audit input also contains a Stage 5 invocation digest, but the
launcher did not mount that invocation and did not list it among the available
inputs; it therefore cannot be recomputed locally. No conclusion in this
review relies on that unmounted invocation.

Evidence:
[`producer-provenance.json`](evidence/producer-provenance.json),
[`hash-verification.json`](evidence/hash-verification.json), and
[`stage4-sidecar-hashes.log`](evidence/stage4-sidecar-hashes.log).

## Inventory reconstruction and Stage 3 classification

I ran the trusted `tools.k_rule_inventory.inventory_verification` against
`/reference/k-proof`, starting from the frozen `verification.k`. Its local
verification-module closure is the single `VERIFICATION` module and contains
27 rules. The reconstructed inventory hash is:

`92208488f5b3fbe4f881489dcbdba726ef2025162d4234a071210c0a94048c89`

The protected discovery document has exactly the same 27 `source_rule_id`
values in the same order. There are no missing, extra, duplicated, reordered,
or changed identities. Reconstructed spans, normalized hashes, and whole
inventory hash all match.

Independent classification of every rule:

| Lines | Rule IDs (prefix) | Count | Classification | Reason |
|---|---|---:|---|---|
| 8–10 | `78f2a049`, `868b8e62` | 2 | `DEFINITION` | Base and constructor recurrence of `allFloatVS`. |
| 15 | `9a463fce` | 1 | `DEFINITION` | Defines the named projection-domain predicate. |
| 20–22 | `57727b2a` | 1 | `DOMAIN_LEMMA` | Characterizes definedness of the partial Val-to-Float projection; it is not first proved without the rule. |
| 24–30 | `64da4543`, `aa23fe12`, `fbd51e78` | 3 | `DEFINITION` | Guarded equations and reverse symbolic orientation for the named `projectFloatTotal` proof term. |
| 34–37 | `dc58f41` | 1 | `DOMAIN_LEMMA` | Guarded dynamic-Val restatement of fixed Float subtraction; it is not first proved without the rule. |
| 46–49 | `98a366fb`, `67158192` | 2 | `DEFINITION` | Named opaque proof terms for the supplied `minFloat` and `maxFloat` primitives. |
| 53–58 | `22cecd17`, `c285c7b6`, `597b45fb` | 3 | `DEFINITION` | Complete structural recurrence for `minTailF`. |
| 61–66 | `6d9e38eb`, `9e552a40`, `4beda3e8` | 3 | `DEFINITION` | Complete structural recurrence for `maxTailF`. |
| 69–74 | `1229ed00`, `3729b5a4`, `98b9bb43` | 3 | `DEFINITION` | Complete constructor definition of `minVF`. |
| 77–82 | `d96e2383`, `de6fe0f3`, `fd99ddec` | 3 | `DEFINITION` | Complete constructor definition of `maxVF`. |
| 89–108 | `6df20a82`, `67e4a403`, `f602ef7b` | 3 | `DEFINITION` | Complete accumulator recurrence for the source loop's result sequence. |
| 114–116 | `b0d12452`, `55b5808d` | 2 | `DEFINITION` | Base and recurrence for the loop-target state summary. |

Thus the independent totals are 25 `DEFINITION`, 0 `OPERATIONAL_RULE`,
0 `PROVED_DERIVED_LEMMA`, and 2 `DOMAIN_LEMMA`, exactly as protected Stage 3
records. No rule qualifies as a proved derived lemma because Stage 1 does not
first prove its exact statement in a module omitting it and only later use it.
Every local simplification is either a definition of a named proof term or one
of the two domain lemmas.

Both domain lemmas are material to this source program. The projection
definedness fact permits dynamically typed iterator values to be projected as
Floats in the min/max and scaling paths. The guarded subtraction fact connects
the source's `(number - min_number)` operation to the `subF` term used by the
postcondition's `scaleAcc` summary. Neither is an unrelated mathematical fact.

Evidence:
[`inventory-reconstruction.json`](evidence/inventory-reconstruction.json),
[`inventory-bijection.json`](evidence/inventory-bijection.json), and
[`frozen-verification.log`](evidence/frozen-verification.log).

## Stage 4 generation and target identity

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`,
the frozen Stage 1 workspace, protected discovery manifest, selected
generation, and trusted toolchain lock. The first attempt exposed a sandbox
PID/proc mismatch that prevents Lean from locating its executable. A narrowly
scoped `LD_PRELOAD` shim makes `getpid()` agree with `/proc/self`; the shim
source and diagnosis are preserved. The frozen-toolchain gate then reported
K 7.1.293, pyk/Klean 7.1.293, Lean 4.22.0, and Codex 0.144.6.

The successful preflight result is `PASS`:

- Stage 1 export hash:
  `4a72f06c9152fe5be324bf07c9d39c2b8e3b0512e8508cc1ac083eca0e5b401d`
- discovery hash:
  `17dfcbfeb2fef9ad417d580c8e46dfa4b276c24df468c869929775bde79531fc`
- generated tree hash:
  `c2f18234a0070f4d668e48966f8394e9fc14c5e04ef63e2fb912a69d3e7127ae`
- obligations: 2
- generated trust declarations: 46
- `lake clean`: exit 0
- `lake build`: exit 0

The independently classified domain IDs and obligation IDs are an exact
ordered bijection:

1. `rule-57727b2acd45f64e74f4c2582f643b13345834dfbe7bf3fe97580d59dcd8ba43`
2. `rule-dc58f41e482527dda6d5bd7e29f533ee71f5356475fa5bfad6f9142925059957`

The first obligation is the exact definedness equivalence for the Float
projection. Its literal `True` represents source `#Ceil(@V)` for an already
bound Lean `SortVal`; it does not omit the load-bearing projection-definedness
equivalence. The second is the exact guarded dynamic-Val Float subtraction
equation. There are no duplicate or missing obligations and no changed source
span or normalized hash.

The fixed target is
`Klean21RescaleToUnit.Lemmas.targetStatement`, with:

- definition hash:
  `5dfb019d3d98a8ac1b644aa237d8a022c95339d47bb6c998dff1b30f35c951e1`
- statement hash:
  `38ec95d809391263646d8a1043da31394bf27f2f41522825b49ee36e0a136762`

The parsed generated target equals both `generator-manifest.json` and the
audit input. Since the true domain set has two entries, `PASS` rather than
`KLEAN_NO_OBLIGATIONS` is the only structurally valid Stage 4 status.

Evidence:
[`stage4-preflight-rerun.json`](evidence/stage4-preflight-rerun.json),
[`stage4-obligation-and-target-check.json`](evidence/stage4-obligation-and-target-check.json),
[`environment-workaround.txt`](evidence/environment-workaround.txt), and
[`lean-proc-pid-shim.c`](evidence/lean-proc-pid-shim.c).

## Stage 5 clean build, proof identity, and trust

I made a fresh project under
`/tmp/audit-work/21-rescale-to-unit-audit`, copied the generated project into
its `Base`, and copied the candidate project around it. The copied
`Base/Klean21RescaleToUnit/Lemmas.lean` is byte-identical to the selected
generated target.

Fresh commands:

```text
LD_PRELOAD=/tmp/audit-work/lean-proc-pid-shim.so lake clean
Exit 0

LD_PRELOAD=/tmp/audit-work/lean-proc-pid-shim.so lake build
Exit 0
Build completed successfully.
```

The candidate contains one `Proof.final`, no target declaration or shadow, no
`sorry`, `admit`, `unsafe`, `axiom`, or `opaque`, and no trust declaration
detected by the trusted Lean scanner. `Proof.final` has exactly the fixed
generated target statement rather than a duplicate or weakened theorem.

Exact axiom query:

```text
'Proof.final' depends on axioms: [propext, Classical.choice]
```

These are Lean core logical dependencies. None of the 46 generated axioms in
`trust-inventory.json` is used by `Proof.final`; there is no `sorryAx`, and the
candidate adds no axiom or opaque declaration. The trusted Stage 5 mechanical
checker independently returned `PASS` with the same two used core axioms.

Evidence:
[`stage5-lake-clean.log`](evidence/stage5-lake-clean.log),
[`stage5-lake-build.log`](evidence/stage5-lake-build.log),
[`stage5-axioms.log`](evidence/stage5-axioms.log),
[`stage5-mechanical-check.log`](evidence/stage5-mechanical-check.log),
[`candidate-static-scan.json`](evidence/candidate-static-scan.json), and
[`stage5-target-identity.json`](evidence/stage5-target-identity.json).

## Operational-bridge audit

The six candidate definitions were printed and compared with their exact
`target.parameters` bindings, the associated frozen rules, and the supplied
semantics:

| Parameter | Judgment |
|---|---|
| `definedProjectFloat` | Correct: true exactly for `SortVal.inj_SortFloat`. |
| `isFloat` | Correct: true exactly for a single Float K item followed by `.K`. |
| `projectFloatTotal` | Correct on its guarded operational domain; the off-domain zero is an arbitrary total extension not used by the rule. |
| `subF` | Correctly uses Lean IEEE Float subtraction, matching supplied concrete Float subtraction. |
| `project:Float?` | Correct: `some` exactly on the Float projection form and `none` otherwise. |
| global `applyBin` KORE symbol | **Incorrect total meaning.** It implements only Float/Float subtraction and maps every other input to `noneV`. |

The failing definition is:

```lean
match op, left, right with
| "-", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
    SortVal.inj_SortFloat (Float.sub left right)
| _, _, _ => SortVal.«noneV_MPY-CORE_Val»
```

The bound KORE symbol is the global supplied-semantics `applyBin`, not a fresh
symbol restricted to this one theorem. The frozen semantics has, among many
other defined cases:

```k
rule applyBin("+", I1:Int, I2:Int) => I1 +Int I2
rule applyBin("-", I1:Int, I2:Int) => I1 -Int I2
```

The executable adversarial test confirms the mismatch:

- candidate `applyBin("+", 2, 3)` is `noneV`;
- it is not an integer value, whereas fixed semantics yields integer `5`;
- candidate `applyBin("-", 2, 3)` is also `noneV`, whereas fixed semantics
  yields integer `-1`.

The candidate does implement the one Float-subtraction branch needed to make
the generated equation close, but the total definition supplied for the
global KORE symbol is a convenient hard-coded partial implementation. The
audit instructions expressly make that an operational-bridge failure. A clean
proof of the parameterized equation cannot repair the mismatch.

Counterfactual tests reinforce the separation between equation closure and
bridge fidelity: the same generated target remains provable with `isFloat`
defined constantly false, and also with both `definedProjectFloat` constantly
false and the projection constantly `none`. Those counterfactual definitions
are not the submitted definitions, but their successful checking demonstrates
why `Proof.final` alone cannot establish the operational meanings.

Evidence:
[`candidate-definitions.log`](evidence/candidate-definitions.log),
[`AuditOperational.lean`](evidence/AuditOperational.lean),
[`operational-adversarial.log`](evidence/operational-adversarial.log),
[`fixed-applyBin-int-rules.log`](evidence/fixed-applyBin-int-rules.log),
[`fixed-applyBin-float-rules.log`](evidence/fixed-applyBin-float-rules.log),
[`AuditCounterfactual.lean`](evidence/AuditCounterfactual.lean), and
[`counterfactual-target.log`](evidence/counterfactual-target.log).

## Final determination

Stage 3's classification is accepted, and Stage 4's two-obligation target is
the deterministic target bound to that classification. Stage 5 proves that
target mechanically with a clean axiom account, but its global `applyBin`
parameter does not implement the frozen supplied semantics. The required
operational bridge therefore fails.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
