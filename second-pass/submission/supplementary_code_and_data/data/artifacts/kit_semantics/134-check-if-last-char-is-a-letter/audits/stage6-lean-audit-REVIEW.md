# Independent audit: HumanEval 134, `kit-semantics`

## Scope and outcome

I independently audited the protected Stage 3 classification, deterministic
Stage 4 generation, and Stage 5 Lean proof for
`134-check-if-last-char-is-a-letter` under `SUPPLIED_SEMANTICS`.
`AUDIT_MODE` and `/audit-input.json` both say
`CLASSIFICATION_AND_PROOF`, so all three stages are in scope.

The audit passes. The six frozen local rules were reconstructed exactly and
classified correctly; the two genuine domain lemmas map bijectively to two
faithful Lean obligations; the generated target is the exact conjunction of
those obligations; and `Proof.final` proves that unchanged target using honest
implementations of the two bound K equality symbols.

Raw commands and outputs are indexed in
[`evidence/00_COMMANDS.md`](evidence/00_COMMANDS.md).

## Immutable inputs and producer provenance

Before judging Stage 4, I hashed the exact mounted generation-time producer
sources:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both equal the values in `source-manifest.json` and
`generator-manifest.json`. The source manifest contains exactly those two
producer entries. Its generator image ID and the generator manifest provenance
both equal
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`;
the same digest is the terminal component of the immutable producer-source
path recorded in `/audit-input.json`. The framed producer bundle tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
also exactly the launcher-recorded value. The mandatory producer gate
therefore passes; there is no infrastructure `AUDIT_ERROR`.

I independently recomputed the available launcher-bound hashes. All matched:

| Input | Recomputed hash |
|---|---|
| Stage 1 pipeline tree | `5c8d407538748853c231a05373a9eec030937879d06506fd36cf24d4fab2a372` |
| Stage 1 Klean export tree | `feb874730750358d13e7cdf643e16548c9a80382c27a8bf192c558c83680a66b` |
| Stage 3 manifest | `95ca9190628f434bc911a605c9180bbd9dd749a84b1e8360547e7e429e7da2f7` |
| Selected Stage 2 tree | `a9bce272823268aafa707abdbffa9a9b74eeb3270721512e97884944dfcb92e2` |
| Selected Stage 4 tree | `0ce226516d6de783667ecee5210d1b11ab5992244e6fce3f5daa60fbbbcc6c69` |
| Generated Lean tree | `53c10928df467aaf491f6c27feee6e2ad3a93d98bdd732483e954e92766aee96` |
| Mounted Stage 5 candidate tree | `efc45ae61b7d663d0ccda1e67cbf942590090ca67b87eea9a861c22a4f5b42d1` |

The launcher's per-file Stage 1 source manifest contains 806 entries. I
rehashed all 806 mounted files: every path and digest matched, with no missing
or extra file. See
[`17_stage1_source_hashes.log`](evidence/17_stage1_source_hashes.log).

See [`01_hash_provenance.log`](evidence/01_hash_provenance.log).

## Canonical inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof`, without using the prior Stage 2 review. The
selected local verification module is `VERIFICATION`; its local
`verification.k` closure contains that module only. Its source hash is
`7b8118eb5e3e75c51555446032dee2eeaa43a3adacdb3d262019fd0031f9d154`.

The inventory contains exactly six ordered rules. Their canonical JSON
inventory hash is
`d817da6122acbe7a8e69a2d9030e69eb871ccebe2fc9cf22295da968e449544a`.
For each rule, the trusted reconstruction independently recovered the span,
normalized hash, `source_rule_id`, attributes, and text:

| Lines | Normalized SHA-256 / source identity | Attributes | Independent class |
|---|---|---|---|
| 10–11 | `9f3646175b8c8b5cb64ba75a517ccb682e19312b8c145a72deccf1c5a90bad2a` | none | `DEFINITION` |
| 13–15 | `4df32a98b335031084e1e2d44c77c3aee9afd5f217f99ad1251e817e7d17ce01` | none | `DEFINITION` |
| 17–19 | `4e7aa14452104b02dfb2ee9c7d2e2129c943e23411864d4a7c094fc06634aada` | none | `DEFINITION` |
| 21–24 | `cde37f71888ce75952bb23d314c3a846093f8ef594206ebe110b61ae7652000a` | none | `DEFINITION` |
| 28–30 | `e0a5c8a793196820ea84731c2d229d364f6fe3e8c376c15bf12d3d2cfb1f31a4` | `simplification` | `DOMAIN_LEMMA` |
| 33–35 | `61ffc6cd69c6bad2d2ff37db34f5511581d591c5239127275c27ebf328e89030` | `simplification` | `DOMAIN_LEMMA` |

Each `source_rule_id` is `rule-` followed by the displayed normalized hash.
The Stage 3 manifest contains these six identities once each, in exactly this
order, with the same whole-inventory hash. There are no omissions, extras,
duplicates, reordered identities, or unaccounted entries. Full reconstructed
texts and comparison fields are in
[`02_inventory_reconstruction.log`](evidence/02_inventory_reconstruction.log).

## Independent classification judgment

The first four rules are the exhaustive guarded equations of the fresh,
total, named summary `standaloneLastLetter(IntSeq)`. They do not rewrite a
program configuration or replace source execution:

1. Empty input maps to `false`.
2. Positive-length input with a non-alphabetic last modeled character maps to
   `false`.
3. A one-character alphabetic input maps to `true`.
4. A longer input with an alphabetic last character maps to whether its
   penultimate code is space (`32`).

These cases are pairwise disjoint and exhaustive for the supplied
`IntSeq` model. They mirror the frozen source body:

```python
if len(txt) == 0:
    return False
return txt[-1].isalpha() and (len(txt) == 1 or txt[-2] == " ")
```

The supplied semantics defines `IntSeq` as the free constructors `.IntSeq` and
`iCons`, length and positional access recursively, `isalpha` through
nonemptiness plus `allAlpha`, and `isAlphaC` through the modeled upper/lower
code ranges. Thus all four rules genuinely define the mathematical execution
summary. None is an operational bridge or a domain fact disguised as a
definition.

The final two rules are domain lemmas:

- `iCons(C, REST) ==K .IntSeq => false` is constructor
  disjointness.
- `iCons(C, .IntSeq) ==K iCons(D, .IntSeq) => C ==Int D` is
  singleton-constructor injectivity plus integer equality.

They do not introduce a named summary and are not ordinary source execution
rules. They are also not `PROVED_DERIVED_LEMMA`s. `prove.sh` compiles
`verification.k`, including both simplifications, once before every `kprove`
command; there is no earlier proof of either exact rule against a module that
omits it. Both `simplification` entries are therefore correctly classified as
`DOMAIN_LEMMA`, satisfying the special simplification policy.

Both domain lemmas are materially relevant. Supplied `str.isalpha()` tests a
one-character sequence for nonemptiness using `==K .IntSeq`, and the source
comparison `txt[-2] == " "` compares singleton code sequences. These are
precisely the constructor-disjointness and singleton-injectivity reductions,
not unrelated mathematical facts. Frozen source and semantic excerpts are in
[`14_frozen_source_semantics.log`](evidence/14_frozen_source_semantics.log).

There are zero independently classified `OPERATIONAL_RULE`s and zero
`PROVED_DERIVED_LEMMA`s. Stage 3's classifications agree entry-for-entry with
this independent judgment.

## Stage 4 preflight, bijection, and target

I invoked `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, `/reference/k-proof`,
`/reference/lemma-discovery.json`,
`/reference/klean-generation`, and the pinned toolchain lock.

The audit PID namespace omits `/proc/<getpid()>/exe`, which Lean 4.22 uses
before elaboration. The first two calls consequently failed at `lake clean`
with “could not detect the configuration of the Lake installation.” I
preserved those failures. A narrow compatibility library answered only Lean's
numeric self-executable `readlink` from ELF `AT_EXECFN`; it did not alter Lean
sources, terms, kernel behavior, or any mounted input. With that environment
repair, the same required function returned:

- status `PASS`;
- two obligations;
- 41 generated trust declarations;
- zero designated sorries;
- the exact frozen Stage 1, Stage 3, and generated-tree hashes above;
- successful fresh `lake clean` and `lake build`; and
- build-output SHA-256
  `9e0c20ef4a4144c9d67fe7d1321707010d487bbfdfd0090190f0004f9677c330`,
  identical to the recorded Stage 4 preflight.

The successful returned evidence is
[`05_check_generation_compat.log`](evidence/05_check_generation_compat.log).

I then independently checked the source/obligation mapping:

1. Rule
   `rule-e0a5c8a793196820ea84731c2d229d364f6fe3e8c376c15bf12d3d2cfb1f31a4`
   maps to the universal Lean equation saying K equality between the embedded
   `iCons(C, REST)` and embedded `.IntSeq` is `false`.
2. Rule
   `rule-61ffc6cd69c6bad2d2ff37db34f5511581d591c5239127275c27ebf328e89030`
   maps to the universal equation saying K equality between embedded
   singletons with heads `C` and `D` equals integer equality of `C` and `D`.

The order is identical to the independently found domain set. Each source
span, normalized hash, inventory hash, discovery hash, and source identity
matches. There are no duplicated or omitted obligations. The conjunct hashes
recompute to:

- `5005812a1819c43ca1926e82e479b9b34f5bab4aece468ad58a67943ddde91ce`;
- `2777790e011098a881a9531b2cfa4f2e0c96f252ea084351c9478cf8b0f25371`.

The obligation-map file hash is
`9adb517702ec2dce8079582c9b61bf346b1bdf8d8f71293c1dccd3db2791ff18`.
Both opaque-parameter binding hashes also recompute exactly:

- `_==Int_`: `107f259f0625fef2985ddf05eaedc49a35a77ee733d3ef7a5b320c1db7b5c816`;
- `_==K_`: `88fa63628c0ebbe09ef4c0b03954957d820b604585e01bc9cc85752508665843`.

Mathematically, both obligations are exact translations. Quantification is
unrestricted, no source guard was dropped, and the `SortK.kseq` plus
`SortKItem.inj_SortIntSeq` wrappers are the generated representation of the
source `==K` operands. Compiled KORE confirms the bindings are the hooked
`INT.eq` and `KEQUAL.eq` symbols and shows the same embedded source rules; see
[`16_kore_symbol_bindings.log`](evidence/16_kore_symbol_bindings.log).
The obligations are inhabited and non-vacuous: examples include head `65`
with empty rest, equal singleton heads `65/65`, and unequal heads `65/66`.
Neither obligation is irrelevant or weakened.

The single generated target is
`Klean134CheckIfLastCharIsALetter.Lemmas.targetStatement`. Its definition is
byte-for-byte the expected conjunction of the two mapped obligations. Its
definition hash is
`31e5c331ab4fd4a774d9f802fe9b0f3c8d6bb40ade95abf9e53c72df80ffb747`;
its instantiated-statement hash is
`18484b18cfc95ad2aa1460726ce87621b72b8f0e7556a54c62bb5552027f0174`.
The declaration, file, parameters, statement, and both hashes agree across
the generation-time producer reconstruction, generator manifest,
`/audit-input.json`, and fresh Stage 5 `Base`. The fresh `Base` retained the
generated tree hash after the build. Detailed comparisons are in
[`10_stage4_stage5_identity.log`](evidence/10_stage4_stage5_identity.log).

This is correctly a nonempty `PASS` generation, not
`KLEAN_NO_OBLIGATIONS`.

## Stage 5 isolated build and proof identity

I created `/tmp/audit-work/stage5-review`, copied the mounted candidate into
it, and copied the immutable generated project into `Base`. From that fresh
project I ran both `lake clean` and `lake build` under the pinned Lean
4.22.0 toolchain. Both exited zero; complete transcripts are
[`06_stage5_lake_clean.log`](evidence/06_stage5_lake_clean.log) and
[`07_stage5_lake_build.log`](evidence/07_stage5_lake_build.log).

Outside immutable `Base`, the candidate contains no `sorry`, `admit`,
`unsafe`, `axiom`, or `opaque`. It defines no `targetStatement` and therefore
does not shadow or replace the generated target. It defines each required
parameter exactly once. `Proof.final` has exactly this type:

```lean
Klean134CheckIfLastCharIsALetter.Lemmas.targetStatement
  Proof.«_==Int_» Proof.«_==K_»
```

The printed definitions, theorem type, and target are in
[`12_print_proof_identity.log`](evidence/12_print_proof_identity.log).
There is no weakened, duplicated, or vacuous alternate theorem.

## Axiom accounting

Running Lean with exactly `#print axioms Proof.final` produced:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

This exact output is saved in
[`08_print_axioms.log`](evidence/08_print_axioms.log). There is no `sorryAx`.
None of the 41 generated collection-hook axioms listed in
`trust-inventory.json` occurs in the dependency set. The trust-inventory hash
recomputes to
`9e07f04409ef81ffe2fdb8438a7ff84d01bef2d3f7941e096822611b45535cdc`,
matching `export-result.json`.

The three reported names are Lean's pinned foundational axioms, not candidate
declarations or generated proposition assumptions. The trusted mechanical
gate explicitly recognizes `Classical.choice`, `propext`, and `Quot.sound` as
the foundational set in addition to the generated inventory allowlist. It
reran clean, build, exact-type checking, and axiom printing and returned
`PASS`; see
[`13_stage5_mechanical_gate.log`](evidence/13_stage5_mechanical_gate.log).
Thus every reported dependency is accounted for, and there is no unrecorded
candidate proof escape.

## Operational-bridge audit

The generated target parameters bind to:

- `Lbl'UndsEqlsEqls'Int'Unds'` (`INT.eq`), used by the singleton
  injectivity rule;
- `Lbl'UndsEqlsEqls'K'Unds'` (`KEQUAL.eq`), used by both domain rules.

The candidate's exact definitions are:

```lean
def «_==Int_» (x y : SortInt) : SortBool := decide (x = y)

noncomputable def «_==K_» (x y : SortK) : SortBool :=
  @decide (x = y) (Classical.propDecidable (x = y))
```

`SortInt` is generated as Lean `Int`, `SortBool` as `Bool`, and `SortK`,
`SortKItem`, and `SortIntSeq` as algebraic generated syntax. Accordingly,
these definitions implement total integer equality and total structural K-term
equality, which are exactly the two frozen hooked symbols' meanings. They do
not depend on the target proposition, source-rule IDs, or selected
constructor patterns.

I machine-checked stronger bridge properties than the generated obligations:

```text
Proof.«_==Int_» x y = true ↔ x = y
Proof.«_==K_» x y = true ↔ x = y
```

Adversarial examples covered equal and unequal positive integers, equal and
unequal negative integers, nonempty versus empty sequences, identical
singletons, different singleton heads, and identical leading terms with
different K continuations. All behaved as operational equality requires.

Counterfactual testing was important here. A dishonest pair that defines both
equalities as constant `false` can still prove the fixed target, demonstrating
that clean target closure alone would be insufficient. The actual candidate
is observably not that shortcut: it returns `true` for equal integers and
equal arbitrary K terms, and the universal bridge theorems hold. Separate
mutation theorems show the honest bridge rejects flipping the
constructor-disjointness result and rejects flipping the singleton equality
result. The complete checked adversarial and mutation evidence is in
[`15_bridge_mutation_checks.log`](evidence/15_bridge_mutation_checks.log).

Therefore neither parameter is constant, identity-based, hard-coded to the
two obligations, vacuous, or otherwise convenient at the expense of frozen
operational meaning. The operational bridge passes.

## Final judgment

Stage 3 is complete and correctly classified. Stage 4 has verified producer
provenance, exact immutable hashes, a true two-rule domain set, an exact
source/obligation bijection, and an unchanged conjunction target. Stage 5
cleanly proves exactly that target with fully faithful equality definitions,
no forbidden declarations or holes, and a completely reconciled axiom set.

VERDICT: PASS
LEGITIMACY: LEGIT
