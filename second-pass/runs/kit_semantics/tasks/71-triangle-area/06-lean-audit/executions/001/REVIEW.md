# Independent audit: `71-triangle-area`

Audit mode: `CLASSIFICATION_AND_PROOF`  
Condition: `kit-semantics`  
Semantics mode: `SUPPLIED_SEMANTICS`

I treated the mounted candidate, prior reviews, logs, rationales, and comments
as untrusted evidence. The conclusions below come from the frozen source,
trusted inventory/preflight code, independent hashing, a fresh Lean build, and
new adversarial tests. Raw outputs and the exact command ledger are under
`/audit-output/evidence/`.

## Producer provenance gate

The Stage 4 producer gate passes.

- `/reference/generation-tools/klean_export.py`:
  `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`
- `/reference/generation-tools/klean.py`:
  `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4`
- Producer bundle hash:
  `61e146bfb9d9d51713156383989873e5c48a5c9b156425ef4cf37c57e6ecd5fb`
- Generator image:
  `sha256:2db35f33b29b4ada4f78dd04470349652b5f62e1ff63355111720eee4e3cc162`

Both file hashes agree exactly among the observed files,
`source-manifest.json`, and `generator-manifest.json`. The image ID agrees
among the source manifest, generator manifest, and the image-keyed producer
path signed in `/audit-input.json`. The producer bundle hash also matches the
audit input. There is no producer-source infrastructure error.

The signed audit-input envelope itself validates with resolved-input digest
`d0bd9ac0ef9d9589096939b1b7917227fe396a6ae5afcb39cfdbedaaed79f2be`.
Every mounted tree matches its recorded hash:

| Mounted input | Recomputed hash |
|---|---|
| Stage 1 workspace tree | `5d067b9d5d521fe0e3661ce44cdbd9366941413a65897e3226ad3e39a4a78b85` |
| Stage 1 deterministic export | `2e43bf0dc6489580b603945ea831e20057b0398da5cb7a3639b68dbd698703bd` |
| Stage 2 audit tree | `2589f1dfeda8353ed9540145737b6c153b4f72f71ca5a563db39da287f37df1c` |
| Stage 3 manifest file | `4ae2bc43044b58e4d1bb2a354af633f6aaae85dbf14b87ac3285de502816a357` |
| Stage 4 generation tree | `303b1e71b1900d1cf79dab0231cdbf2633b6a6ae1fb7cf6d8a634549d18e3f18` |
| Generated Lean project | `6a11115cc03b977287c1c8852f062a3f5bd64fdffc2f7eb072b5d0891b8e774a` |
| Producer-source bundle | `61e146bfb9d9d51713156383989873e5c48a5c9b156425ef4cf37c57e6ecd5fb` |
| Stage 5 candidate workspace | `160842015b1c435821e73308be9d07a8e06bd07b5793c1cef07df66616ed22aa` |

The launcher records a Stage 5 invocation hash, but that invocation directory
is not one of the mounted audit inputs. Its workspace output is mounted as
`/candidate`, and that mounted tree exactly matches the signed Stage 5
workspace hash and the workspace hash in `stage5_result`.

## Inventory reconstruction and Stage 3 classification

Using `tools.k_rule_inventory.inventory_verification` on the frozen
`/reference/k-proof` reconstructed:

- verification file SHA-256:
  `0712198a6a504bea42975284bb1711ef3836eb5bf8af9d4fe787c1e22ffbeec4`;
- selected module and complete local closure: `VERIFICATION` only;
- rule count: 6; and
- inventory SHA-256:
  `de92531aa585b933c077c7b03978617a1478b0e8962fb9284eb6a300e9f8de76`.

The reconstructed and Stage 3 ID sequences are exactly equal, not merely set
equal. Both contain six unique IDs. Thus there are no omitted, duplicated,
extra, or reordered rules. Each source span, normalized source hash, and
`source_rule_id` follows directly from the reconstructed frozen text.

My independent classifications are:

| Lines | Source rule | Classification | Judgment |
|---|---|---|---|
| 13 | `rule-4118d893fdb23a03019d470e2b1c6fcba5249000dd31f5eede7a49b9bb496c57` | `DOMAIN_LEMMA` | Correct. It equates the supplied proof-opaque `intToF` symbol to a fresh proof symbol. This equality is neither a definition nor an operational rule, and Stage 1 never first proves it in a module omitting the rule. |
| 18–49 | `rule-8198bac7b8824309265af7441122c8de309aa29e610f052e2ef585d0cf940c16` | `DEFINITION` | Correct. It is a nullary definition of the exact program syntax tree. |
| 54–57 | `rule-211b8b0393e5ae2a5e8ee78c603f8efc838adffd3c3e11440d210eb7aa3e3394` | `DEFINITION` | Correct. It names the three triangle-invalidity comparisons. |
| 60–61 | `rule-563c1f5294a0f04495366f41b46928debc138e2960273a2b7233fbf30037a326` | `DEFINITION` | Correct. It names the source program's semiperimeter expression. |
| 64–74 | `rule-9e3d2b1def67f5eadfc05db79e46d7a27f186bfa84d0fcfeca76f52099eff93a` | `DEFINITION` | Correct. It names the four-factor Heron product. |
| 77–84 | `rule-0824bba9e5ff88475bdea02d8e1fe2faeda87b8b33bf10adc9aeee485a1e94c7` | `DEFINITION` | Correct. It names the invalid/valid result expression using the supplied operators, square root, and rounding primitive. |

There are no local `OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA` entries. The
only `simplification` rule is classified as `DOMAIN_LEMMA`, satisfying the
simplification restriction.

The program quotation and `solution.mpy` are textually identical after only
whitespace and `.Stmts` empty-list normalization; both compact forms hash to
`35b77ba21b0f8f22fad4d32968f87aea27b4a9c77d7f967269791a856f76be72`.
The other five formulas correspond directly to the Python condition,
semiperimeter, Heron product, and returned result.

The domain lemma is relevant. In the supplied `MPY-FLOAT` semantics,
`intToF(Int)` is a total proof-opaque symbol with the concrete rule
`Int2Float(I, 53, 11)`. Valid executions with integer or Boolean sides reach it
through mixed Float/Int arithmetic after true division. The fresh
`proofIntToF` symbol has no independent operational meaning. Therefore their
universal equality is a genuine additional domain assumption needed to align
the proof representations; it is not an irrelevant mathematical fact.

## Deterministic Stage 4 generation

The required direct call to
`tools.klean_preflight.check_generation`, with `PYTHONPATH=/reference`, the
frozen Stage 1 workspace, protected Stage 3 manifest, selected Stage 4
generation, and pinned toolchain lock returned `PASS`.

The first call exposed an audit-container issue: Lean could not resolve its
installation because the sandbox denies `/proc/<pid>/exe`. I preserved that
failure, authored a minimal `readlink` compatibility shim under
`/tmp/audit-work`, verified Lean 4.22 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and reran the identical trusted
function. The rerun's internal `lake clean` and `lake build` both exited 0 and
reproduced the recorded diagnostic hashes. No mounted input was changed.

There is exactly one Stage 4 obligation:

```lean
∀ (I : SortInt), (intToF I : SortFloat) =
  (proofIntToF I : SortFloat)
```

It is the exact universal translation of the line-13 K rule. It retains the
input, both sides, the source and result sorts, and the full unguarded domain.
It is neither weakened nor vacuous. The obligation map contains exactly one
source rule and exactly one obligation with the same unique rule ID, span,
normalized hash, inventory hash, and discovery-manifest hash. There are no
extra conjuncts or duplicate obligations.

The obligation-map file hash is
`74c8a5e4f36f1d830d9f5c153eacf1ed9de26fe52588c5a911f82d79ebc175a3`;
the conjunct hash is
`ffe82312dd8a5a3334b4e5e91e4807e2fe1d8daf7ed46a0f979dbd7f17dec14b`.
The trust-inventory file hash is
`80506503a3c3464927fc9baa11eef2abf2fe54757c658504156f3c4af2d4f63b`.
All agree with their manifests.

The generated target is exactly:

```lean
def Klean71TriangleArea.Lemmas.targetStatement
    (intToF : SortInt → SortFloat)
    (proofIntToF : SortInt → SortFloat) : Prop :=
  ∀ I, intToF I = proofIntToF I
```

Its recorded declaration, file, parameter bindings, statement, and definition
all recompute exactly:

- definition hash:
  `c1b7b84afcf69fc957b6b594bf980b81431d5ec1c3bce5b0a2b2b403fa088ed7`;
- statement hash:
  `4648c7167e5acb44bb053acb98eb2f2ab13fe9d0b8e2a213380a97487a60cf05`;
- `intToF` binding hash:
  `9c914e11106860ab1b2006156ebd3e271ecdff83777f68025e89b2b84cef1079`;
- `proofIntToF` binding hash:
  `a81a2ede23e371836c5d29224f075bfeeb7bd0c7828de188d3d34ac6bb793d30`.

This is not a `KLEAN_NO_OBLIGATIONS` case: the independently classified domain
set contains the one legitimate rule above, and Stage 4 generated its target.

## Stage 5 clean build, target identity, and trust

I created the fresh project
`/tmp/audit-work/lean-audit-71.8ZE0zZ`, copied the candidate into it, and copied
the immutable generated project into `Base`. The copied Base tree retained
hash `6a11115cc03b977287c1c8852f062a3f5bd64fdffc2f7eb072b5d0891b8e774a`.

Both required commands succeeded from that project:

- `lake clean`: exit 0;
- `lake build`: exit 0, ending with `Build completed successfully.`

The candidate has exactly one `def intToF`, one `def proofIntToF`, and one
`theorem final`. Its non-Base Lean sources contain no `sorry`, `admit`,
`unsafe`, `axiom`, or `opaque` declaration. They contain no declaration or
namespace that changes or shadows
`Klean71TriangleArea.Lemmas.targetStatement`. The trusted Stage 5 mechanical
checker independently copied, cleaned, built, type-checked, and axiom-checked
the candidate and returned `PASS`.

`Proof.final` states the exact fixed target:

```lean
Klean71TriangleArea.Lemmas.targetStatement intToF proofIntToF
```

It is not a duplicate or weakened theorem. The target itself is the exact
single generated obligation, universally quantified over the inhabited
`SortInt = Int` domain.

The exact `#print axioms Proof.final` output was:

```text
'Proof.final' depends on axioms: [propext, Classical.choice]
```

There is no `sorryAx`. `propext` and `Classical.choice` are Lean core axioms
explicitly permitted by the trusted final gate; neither is a candidate-added
declaration. None of the 88 generated declarations recorded in
`trust-inventory.json` occurs in the dependency list, and the candidate adds
no trust declaration. Thus every reported dependency is accounted for and
there is no unrecorded proof escape.

## Operational-bridge validation

The generated parameter bindings are:

- `intToF`, KORE symbol `LblintToF`, `SortInt → SortFloat`;
- `proofIntToF`, KORE symbol `LblproofIntToF`,
  `SortInt → SortFloat`;
- both bound to the exact line-13 source rule.

The generated types reduce to `SortInt = Int` and `SortFloat = Float`. The
candidate definitions are:

```lean
def intToF (value : SortInt) : SortFloat := Float.ofInt value
def proofIntToF (value : SortInt) : SortFloat := Float.ofInt value
```

This implements the supplied operational meaning. K's concrete
`intToF(I) => Int2Float(I, 53, 11)` is nearest binary64 integer conversion;
Lean 4.22 documents `Float.ofInt` as the closest 64-bit float, with signed
infinity when the range is exceeded. Defining `proofIntToF` identically gives
the fresh proof symbol precisely the meaning asserted by the domain lemma.

I tested zero, positive and negative values, `2^53-1`, `2^53`, the rounding
ties `2^53+1` and `2^53+3`, `-(2^53+1)`, `2^1023`, and overflow at `2^1024`.
The candidate functions produced the same bit pattern for every input. The
patterns matched an independent Python binary64 oracle exactly. A separate
MPY program executed through the frozen K LLVM definition and successfully
asserted the same signed and `2^53`-boundary conversions. The outputs are
input-sensitive and exhibit the expected tie-to-even rounding and overflow;
they are not constant, identity, or hard-coded to problem examples.

The counterfactual tests demonstrate the load-bearing bridge check. Replacing
both functions by the constant `0.0` still lets the bare generated equality
build, so the Lean proof alone would not establish operational adequacy.
Replacing only `proofIntToF` by `0.0` makes `rfl` fail. The actual candidate
uses neither shortcut: both definitions independently implement the frozen
conversion semantics across adversarial boundaries.

## Judgment

Stage 3 is complete and correctly classified. Stage 4 has authenticated
producer provenance, an exact one-to-one nonvacuous obligation, and an
unchanged fixed target. Stage 5 cleanly proves that exact target without a
candidate trust escape, and both target parameters faithfully implement their
bound K symbols. The mechanical and mathematical audits agree.

VERDICT: PASS
LEGITIMACY: LEGIT
