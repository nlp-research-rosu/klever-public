# Independent audit of `155-even-odd-count`

## Result

This was a `CLASSIFICATION_AND_PROOF` audit for condition `kit-semantics` and
semantics mode `SUPPLIED_SEMANTICS`. Stage 3's classifications and Stage 4's
deterministic generation are sound. The Stage 5 project clean-builds and proves
the fixed generated theorem without an unrecorded axiom, but it is not a
legitimate operational bridge: its definition of the bound KORE symbol `%Int`
uses Lean's Euclidean modulus instead of K's truncated modulus. A concrete
negative-input counterexample distinguishes them. This is the kind of
target-convenient definition the audit contract requires rejecting, so the
overall result is `FAIL` / `NOT_LEGIT`.

## Input and producer provenance

The launcher mode and copied audit input agree, and `/audit-input.json` has
SHA-256 `f9ddfae951ff166cc45498b35fd6c8061bcf70ed2ea1fa5142b2262b163f7e25`.
The initial evidence is in
[`00-launcher-input.log`](evidence/00-launcher-input.log).

Before assessing generation, I hashed the two mounted producer files:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both hashes match `source-manifest.json` and `generator-manifest.json`. The
immutable image ID is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in both manifests, and the same digest is the final component of the producer
path recorded by the launcher. Using the trusted launcher tree-hash algorithm,
the producer bundle is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
exactly the audit-input value. Thus there is no producer-source infrastructure
error. See [`01-producer-provenance.log`](evidence/01-producer-provenance.log)
and
[`01b-producer-bundle-pipeline-hash.log`](evidence/01b-producer-bundle-pipeline-hash.log).

Every recorded hash having a mounted referent was recomputed and matched: the
Stage 1 K tree (`694bf928...c94b0`), Stage 1 export (`e5151069...20d4`), selected
K audit (`9cc20313...34c6`), discovery manifest (`148e0935...6d9c`), Stage 4
tree (`02bd2d0c...9ef0`), generated tree (`dbbc2d3d...f0f7`), producer tree
(`388cac39...f11e`), and candidate tree (`42b35781...045f`). All 803 recorded
Stage 1 file hashes matched with no missing, extra, or changed file. The lone
launcher field `lean_invocation_sha256` has no referent in the specified mounted
input set and therefore cannot be independently recomputed; it was not relied
on for any judgment. Full comparisons are in
[`06-stage4-integrity.log`](evidence/06-stage4-integrity.log).

## Stage 3 inventory reconstruction and classification

I reconstructed the local verification-module closure from frozen
`verification.k` with the trusted rule-inventory implementation. The closure is
the local module `VERIFICATION`; it contains 24 rules spanning lines 8 through
101. The independently computed values are:

- frozen `verification.k` SHA-256:
  `972347fb2f5c1ac10251f295a40ccf9464fea383405626cd87346aff804e6516`;
- whole inventory SHA-256:
  `b2fb8d2f080192ac639ab57ac9b211ee836bb2e63f89b4d157059d4ffc931fe2`.

The reconstruction records every exact source span, normalized source hash, and
derived `source_rule_id` in
[`02-reconstructed-inventory.json.log`](evidence/02-reconstructed-inventory.json.log).
Its ordered identities match the protected discovery manifest bijectively:
24 entries, 24 unique IDs, no omission, extra entry, duplicate, reordering, or
hash change. The manifest file hash is
`148e093570aa2a356c48e66b62d6bccd9e642567d946b04229f6b0d8d4416d9c`.
See
[`03-inventory-manifest-bijection.log`](evidence/03-inventory-manifest-bijection.log).

Independent semantic reclassification agrees with the manifest:

| Classification | Count | Judgment |
|---|---:|---|
| `DEFINITION` | 14 | Correct |
| `DOMAIN_LEMMA` | 10 | Correct |
| `OPERATIONAL_RULE` | 0 | Correct |
| `PROVED_DERIVED_LEMMA` | 0 | Correct |

The 14 definitions are the named translated body and closure, the base and
guarded-base equations for `evenPos`/`oddPos`, their negative totalization, and
the base/positive/negative equations for `decEven`/`decOdd`. Each defines a
named proof term or decimal-count summary. The guarded zero equations are also
valid definitional simplifiers.

The ten proposition-to-`#Top` rules are genuine domain lemmas, not ordinary
execution rules or previously proved derived lemmas. They comprise two public
zero facts, four `absInt`/summary normalization equalities (both K matching
orientations), and four positive decimal recurrences (both orientations for
even and odd counts). Stage 1 admits them in `verification.k`; it does not first
prove the exact rules against a module omitting them and then consume them, so
none qualifies as `PROVED_DERIVED_LEMMA`. They are all relevant: the first six
connect the source program's initial `abs` and zero case to the postcondition,
and the last four match the loop's parity updates and division by ten. Every
rule carrying `[simplification]` is consequently either a `DEFINITION` or a
`DOMAIN_LEMMA`.

## Stage 4 deterministic generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
against `/reference/k-proof`, the protected discovery JSON, and the selected
generation. It returned `PASS`, 10 obligations, zero designated sorries, the
expected Stage 1 hash `e5151069...20d4`, and generated-tree hash
`dbbc2d3d...f0f7`. The first invocation exposed a sandbox-only Lean launcher
failure because numeric `/proc/<pid>/exe` links are absent here; that raw
failure is retained in
[`04-preflight-rerun.log`](evidence/04-preflight-rerun.log). I reran with a
narrow local readlink compatibility shim that maps only the current process's
numeric path to the available `/proc/self/exe`; it did not alter any mounted
input or Lean source. The complete successful result is in
[`05-preflight-rerun-with-proc-shim.log`](evidence/05-preflight-rerun-with-proc-shim.log).

The ten independently confirmed domain-rule IDs, exported source rules, and
generated obligation IDs are unique and equal in the same order. Each source
rule and conjunct hash matches exactly. There is no omitted, extra, or generated
duplicate obligation; the opposite equality orientations are distinct frozen
source rules, not generator duplication. The guards are satisfiable (`N = 0`
for the zero facts and `N = 1` for the positive facts), and the consequents are
substantive, so no conjunct is vacuous. Inspection against the frozen solution
and operational semantics confirms that the obligations preserve the zero
case, post-`abs` summaries, parity update, and decimal quotient. The true domain
set is nonempty, so this is correctly a ten-obligation generation rather than
`KLEAN_NO_OBLIGATIONS`.

The fixed target is exactly:

- declaration: `Klean155EvenOddCount.Lemmas.targetStatement`;
- file: `Klean155EvenOddCount/Lemmas.lean`;
- definition SHA-256:
  `1b3125aa6574304838e19004df800355d6a96a1f8ad1262817dcc3614b591446`;
- applied-statement SHA-256:
  `64f32e5bf396b4786df83e6b17fe3992fc262c5abfd98180547f2a1b7cd488eb`.

The generator manifest, audit input, observed declaration, complete generated
definition, all 11 parameter bindings, and both target hashes agree. The full
bijection and target report is
[`06-stage4-integrity.log`](evidence/06-stage4-integrity.log).

## Stage 5 proof mechanics and identity

I created the fresh project `/tmp/audit-work/proof-audit.fWiTlY`, copied the
candidate into it, and copied the selected generated project into its `Base`
directory. Both mandatory commands succeeded: the complete `lake clean` and
`lake build` outputs are
[`07-stage5-lake-clean.log`](evidence/07-stage5-lake-clean.log) and
[`08-stage5-lake-build.log`](evidence/08-stage5-lake-build.log).

The independent candidate scan found exactly one `Proof.final`, whose statement
is the exact fixed target application. The candidate declares none of the Base
target, defines each of the 11 parameters exactly once, and contains no
`sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`. It therefore neither
changes nor shadows the target. See
[`16-candidate-structure.log`](evidence/16-candidate-structure.log). The trusted
final mechanical gate also returned `PASS`; as that gate reports, its
`semantic_classification` is deliberately `NOT_EVALUATED`, so it cannot settle
the operational bridge question. See
[`10-trusted-final-mechanical-gate.log`](evidence/10-trusted-final-mechanical-gate.log).

Running Lean with `#print axioms Proof.final` produced exactly:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The exact output is in
[`09-proof-final-axioms.log`](evidence/09-proof-final-axioms.log). These three
are the trusted final gate's explicit Lean core baseline. None of the 45
generated axioms recorded in `trust-inventory.json` is actually reached by
`Proof.final`; there is no unrecorded dependency and no `sorryAx`. The complete
set reconciliation is in
[`17-axiom-reconciliation.log`](evidence/17-axiom-reconciliation.log).

## Stage 5 operational-bridge audit

I located and compared every target parameter definition with its bound KORE
symbol, all listed source-rule IDs, the frozen K rules, the Python solution, and
the supplied operational semantics:

| Parameter(s) | Candidate meaning | Independent judgment |
|---|---|---|
| `«_-Int_»`, `«_+Int_»` | `Int.sub`, `Int.add` | Exact K integer operations |
| `«_>Int_»`, `«_==Int_»` | decided integer order/equality | Exact K Boolean observations |
| `«_/Int_»` | `Int.tdiv` | Exact `INT.tdiv` hook on the bound nonzero uses |
| `«absInt(_)_INT-COMMON_Int_Int»` | `Int.ofNat n.natAbs` | Exact integer absolute value |
| `«evenPos(_)_VERIFICATION_Int_Int»`, `«oddPos(_)_VERIFICATION_Int_Int»` | recursive decimal counts over `natAbs`, with zero as terminator | Matches the frozen base, recurrence, and negative totalization |
| `«decEven(_)_VERIFICATION_Int_Int»`, `«decOdd(_)_VERIFICATION_Int_Int»` | magnitude counts with public zero results `1` and `0` | Matches all frozen public-summary branches |
| `«_%Int_»` | `Int.emod` | **Incorrect:** bound KORE symbol is K `%Int`, hooked to `INT.tmod` |

The decisive mismatch is not a naming preference. Frozen compiled K declares
`_%Int_` with `hook(INT.tmod)`, while `/Int` separately uses `INT.tdiv`. The
candidate instead says:

```lean
def «_%Int_» : SortInt → SortInt → SortInt := Int.emod
```

An independently compiled minimal K harness evaluates `-3 %Int 2` to `-1`.
The candidate definition evaluates `Int.emod (-3) 2` to `1`; Lean's
`Int.tmod (-3) 2` evaluates to `-1`. The exact K hook/source comparison is in
[`14-operational-bridge-source-comparison.log`](evidence/14-operational-bridge-source-comparison.log),
the Lean evaluations are in
[`11b-lean-bridge-adversarial-examples.log`](evidence/11b-lean-bridge-adversarial-examples.log),
and the K result is in
[`13a-k-tmod-negative-dividend.log`](evidence/13a-k-tmod-negative-dividend.log).
The same adversarial run confirms the honest summary behavior on `-1203` as
`(2, 2)` and on zero as `(1, 0)`.

The supplied Python semantics does define source-level `%` through a normalized
`pyMod(a,b) = ((a %Int b) +Int b) %Int b`; that reinforces rather than excuses
the mismatch. The generated parameter is bound to the raw KORE `%Int` symbol,
and the frozen domain recurrences explicitly use that raw operation inside the
normalization formula.

The proof succeeds because every generated recurrence assumes `N > 0` and uses
positive literal divisors 2 and 10. On that restricted path, truncated and
Euclidean remainders coincide. As a counterfactual check, changing the same
definition to return the arbitrary value `777` for every negative divisor still
allows the unchanged fixed-target proof to clean-build; the mutation and result
are in
[`15b-counterfactual-bridge-source.log`](evidence/15b-counterfactual-bridge-source.log)
and
[`15-counterfactual-bridge-build.log`](evidence/15-counterfactual-bridge-build.log).
This demonstrates that the theorem constrains only the convenient positive
fragment and cannot certify the parameter's total operational meaning.

Thus `Proof.final` really does prove the immutable generated proposition, but
one of the definitions supplied to it does not implement the frozen operation
to which it is bound. A clean build and clean axiom list do not cure that
operational-bridge failure.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
