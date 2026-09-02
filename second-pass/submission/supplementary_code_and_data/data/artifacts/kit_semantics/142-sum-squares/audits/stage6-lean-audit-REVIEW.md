# Independent audit: HumanEval 142-sum-squares

## Scope and result

The launcher records `CLASSIFICATION_AND_PROOF` for condition
`kit-semantics` and semantics mode `SUPPLIED_SEMANTICS`.  I independently
audited the frozen Stage 1 verification-module inventory, every Stage 3
classification, deterministic Stage 4 provenance and obligations, and the
Stage 5 Lean proof.  I treated all mounted candidate and provenance material
as untrusted evidence.

The audit passes.  There are 19 local verification rules: 14 definitions and
5 genuine, relevant domain lemmas.  Stage 4 generates exactly one obligation
for each domain lemma, with no omission, duplicate, reorder, target change, or
material weakening.  A fresh Stage 5 project builds cleanly, `Proof.final` has
the exact fixed generated type, and all nine operational bridge definitions
implement their frozen meanings on the relevant guarded domains.

Raw commands and results are under [`evidence/`](/audit-output/evidence).

## Producer and input provenance

I performed the producer-source gate before judging Stage 4:

| Producer source | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` |
| `klean.py` | `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346` |

Both hashes match `source-manifest.json` and `generator-manifest.json`.
The immutable generator image is consistently recorded as
`sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`
in the source manifest, generator manifest, and `/audit-input.json`.  The
generation-tools launcher tree hash is
`bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`
and also matches the audit input.  The trusted toolchain lock matches.
Consequently, there is no producer-source infrastructure error.

I recomputed every accessible launcher hash.  The Stage 1 workspace, Stage 1
export tree, discovery manifest, selected Stage 2 audit, Stage 4 directory,
producer-source tree, generated tree, and candidate tree all match their
recorded hashes.  All 781 Stage 1 per-file paths and hashes match exactly.
The preserved copy of `/audit-input.json` is byte-identical to its mounted
source.  Full values are in
[`02-recorded-hashes.log`](/audit-output/evidence/02-recorded-hashes.log).

## Inventory reconstruction

Using the trusted local rule-inventory implementation against the frozen
`/reference/k-proof`, I reconstructed the verification-module closure rather
than accepting the protected discovery file.  The closure is exactly module
`VERIFICATION`; its normalized source hash is
`456be74262967d6adca2ef4b18436ef7de5b892890010fff730d5600b3c2c691`.

The reconstruction contains 19 rules.  For each rule I independently
recomputed its source span, normalized source hash, and
`source_rule_id = "rule-" + normalized_hash`.  I then recomputed the
canonical whole-inventory hash:

`6439ddecb014c1e9198717de95f81e55c2a88c70397d51f90541a880f782765e`

The protected Stage 3 file has the same 19 unique identities in the same
order and the same inventory hash.  There are no omitted, duplicated, extra,
reordered, or hash-altered rules.  The complete ordered spans and hashes are
recorded in
[`03-inventory-reconstruction.log`](/audit-output/evidence/03-inventory-reconstruction.log).

## Independent classification

I classified the frozen rule text using the supplied MPY operational
semantics and the actual source program, not the prior labels:

| Rules / source lines | Independent class | Reason |
|---|---|---|
| 1–3 / 8–43 | `DEFINITION` | Exact macros for the translated loop, function body, and function definition. |
| 4–5 / 47–49 | `DEFINITION` | Base and descending recurrence for named predicate `allInts`. |
| 6 / 54 | `DEFINITION` | Defining equation for fresh predicate `definedProjectInt`. |
| 7 / 59–61 | `DOMAIN_LEMMA` | Definedness property of the pre-existing partial Int projection. |
| 8 / 63–65 | `DEFINITION` | Guarded defining equation for fresh total helper `projectIntTotal`. |
| 9 / 67–69 | `DOMAIN_LEMMA` | Guarded reverse projection rewrite; it does not define the pre-existing projection. |
| 10 / 71–72 | `DEFINITION` | Constructor/collapse equation for `projectIntTotal`. |
| 11 / 74–75 | `DOMAIN_LEMMA` | Idempotence property, not a defining case or recurrence. |
| 12–13 / 80–88 | `DOMAIN_LEMMA` | Guarded symbolic extension of pre-existing `applyBin` multiplication and addition. |
| 14–16 / 92–102 | `DEFINITION` | Three disjoint equations defining `squareContribution`. |
| 17–19 / 108–117 | `DEFINITION` | Base, recursive, and off-domain totalization equations for `sumSquaresAcc`. |

This independently gives 14 `DEFINITION` and 5 `DOMAIN_LEMMA`, exactly as in
the protected classification.

No rule is an `OPERATIONAL_RULE`: the local module contains macros,
mathematical recurrences, and proof-local projection/arithmetic facts, not
ordinary configuration or observation transitions.  No rule is a
`PROVED_DERIVED_LEMMA`: `prove.sh` compiles the complete module with all rules
already present before running any proof, so no exact rule is first proved
against a module that omits it.

All seven simplification-tagged rules have an allowed class.  Rules 8 and 10
define the total helper; rules 7, 9, and 11–13 are domain lemmas.  No domain
lemma was hidden under another category.

The five domain lemmas are relevant to both the translated program and the
postcondition.  The positive claims assume `allInts(VS)` and return
`sumSquaresAcc(VS, 0, 0)`.  Projection-definedness, reverse projection, and
idempotence carry symbolic `Val` elements into that Int recurrence.
Multiplication is required by the square and cube branches of the source;
addition is required by every `result += ...`.  These are proof-local
semantic bridge facts, not human-facing result lemmas.  Detailed
rule-by-rule reasoning is in
[`04-independent-classification.md`](/audit-output/evidence/04-independent-classification.md).

## Deterministic Stage 4 generation

Because the independently classified domain set has five rules, this is
correctly a five-obligation generation, not `KLEAN_NO_OBLIGATIONS`.

The generated obligation map has five unique entries in exact inventory
order, with exact source IDs, spans, normalized hashes, discovery hash, and
inventory hash.  Each generated Lean conjunct hash matches its recorded hash.
The resulting map hash is
`33114794861bd6e6923d1f33f11acfc07105a842af8f9bf72a56e982a4ea41c1`.
The nine target parameters have unique binding hashes and together cover the
source-rule bindings without missing or invented rules.

The five obligations are, in order:

1. Int-projection definedness is equivalent to `definedProjectInt = true`,
   with the translated well-sortedness fact.
2. On that guard, the partial projection equals `projectIntTotal`.
3. `projectIntTotal` is idempotent through Int injection.
4. Guarded Int `applyBin("*", V, W)` equals multiplication of the projected
   operands.
5. Guarded Int `applyBin("+", I, V)` equals addition with the projected
   operand.

The `∧ True` within the first conjunct is the exact translation of
`#Ceil(@V)` for `@V` already typed as `SortVal`.  It does not replace the
projection equivalence or create a vacuous top-level obligation.  Every
top-level conjunct remains a nontrivial, relevant image of one domain lemma.
There are no weakened, irrelevant, duplicate, omitted, or vacuous top-level
obligations.

I reran the required
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` on the
three mandated paths.  It returned `PASS`, obligation count 5, generated tree
hash
`dc238324f971c8377f25471dc1684050f163a9705e518732e0fa75757da8ae48`,
trust declaration count 42, and designated-sorry count 0.  The complete
returned evidence is
[`06-preflight.json`](/audit-output/evidence/06-preflight.json).

The audit container did not expose `/proc/<numeric-pid>/exe`, while pinned
Lean 4.22 requests that path.  The initial preflight therefore failed before
checking the project.  I diagnosed and recorded this environmental issue,
then used a narrow `LD_PRELOAD` shim that redirects only
`readlink("/proc/<own-pid>/exe")` to `/proc/self/exe`.  The checker itself,
inputs, project, and Lean proof checking were unchanged.  The pinned Lean
binary and the full preflight then succeeded.  This compatibility detail and
the initial failure are preserved in
[`01-producer-and-environment.log`](/audit-output/evidence/01-producer-and-environment.log).

## Fixed target identity

The fixed declaration is
`Klean142SumSquares.Lemmas.targetStatement`.  Its definition hash is
`9ecbf97adfeb3047cdc659a0f9a3543b264e2ee2b88f9cd85bc5a71aa6354212`;
its instantiated statement hash is
`035a507b4967b9fc87cbdab8e3fc3a960b99e881361474d3aeaef2aa7c316490`.
The declaration, definition hash, statement, statement hash, target file, and
all parameter bindings agree among the generated file, generator manifest,
preflight result, and audit input.

The Base target copied into the fresh proof workspace is byte-identical to
the generated reference file; both have file hash
`059f9d6281bf1849ecb5ce83bb9e82b87942ae3dff70d123c354c7c5e4d9fa38`.
The candidate imports that target, declares it zero times, and declares
exactly one `Proof.final`.  It therefore neither changes nor shadows the
fixed target.

## Fresh Lean proof and trust accounting

I made a fresh workspace at `/tmp/audit-work/lean-audit.wOaxmy`, copied the
candidate into it, and copied the generated project into `Base`.  With the
pinned Lean 4.22 toolchain, both `lake clean` and `lake build` exited 0.
`Proof` and the immutable generated modules built successfully; the only
messages were three generated unused-variable linter warnings.  The complete
transcript is
[`07-lean-clean-build.log`](/audit-output/evidence/07-lean-clean-build.log).

After stripping comments, the candidate contains no `sorry`, `admit`,
`unsafe`, `axiom`, or `opaque`.  The trusted declaration scanner also finds
no candidate trust declaration.  The candidate imports only the generated
lemmas module.

An explicit exact-type Lean example using `Proof.final` compiled.  Its type
is precisely:

```lean
Klean142SumSquares.Lemmas.targetStatement
  Proof._andBool_ Proof.«_+Int_» Proof.«_*Int_»
  Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
  Proof.«definedProjectInt(_)_VERIFICATION_Bool_Val»
  Proof.isInt Proof.«project:Int» Proof.projectIntTotal Proof.«project:Int?»
```

Thus `Proof.final` proves the fixed generated theorem, not a weakened,
duplicated, or vacuous variant.

The required Lean command `#print axioms Proof.final` produced exactly:

```text
'Proof.final' depends on axioms: [propext, Classical.choice]
```

There is no `sorryAx`.  The two reported names are Lean core logical
foundations, not candidate or generated declarations.  The generated trust
inventory contains 42 explicitly allowlisted axioms (41 collection-hook
declarations in `Prelude.lean` and one generated function declaration in
`Func.lean`); none occurs in the actual dependency set of `Proof.final`.
The candidate adds no axiom or opaque declaration.  Consequently there is no
unrecorded candidate/generated trust escape.  Exact output and reconciliation
are in
[`09-axioms-and-trust.log`](/audit-output/evidence/09-axioms-and-trust.log).

## Operational bridge

I located the exact candidate `def` for every target parameter and compared
it with its manifest `kore_symbol`, `source_rule_ids`, frozen verification
rules, source solution, and supplied MPY semantics:

| Parameter | Independent operational judgment |
|---|---|
| `_andBool_` | Boolean conjunction, exactly the guard connective. |
| `«_+Int_»` | Lean integer addition, matching K `+Int`. |
| `«_*Int_»` | Lean integer multiplication, matching K `*Int`. |
| `applyBin` | On the two bound guarded rules, `"*"` and `"+"` over injected Ints dispatch to exactly multiplication and addition. |
| `definedProjectInt` | True exactly for the Int injection. |
| `isInt` | True exactly for the singleton K sequence containing an injected Int, the form used in these obligations. |
| `project:Int` | Recovers the integer from the guarded singleton injected-Int term. |
| `projectIntTotal` | Recovers the integer from an injected Int. |
| `project:Int?` | Returns `some i` exactly on the projection domain and `none` on a tested non-Int. |

The K declaration intentionally makes `projectIntTotal` a total helper but
constrains it operationally only under `definedProjectInt`.  Its candidate
fallback of zero is outside every relevant guarded use; it cannot satisfy the
equations conveniently on the actual domain.  Extra `applyBin` cases likewise
do not alter the two bound operational rules.

Lean accepted adversarial examples using negative and distinct integers,
positive and negative projection cases, Bool rejection, Int multiplication,
Int addition, and Int/Bool addition.  Separate constant mutations for
addition, projection, and `applyBin` all failed the corresponding expected
examples.  These checks distinguish the candidate from constant, identity,
hard-coded, zeroed, and vacuous implementations.  The bridge evidence and
exact mutation failures are in
[`11-operational-bridge.log`](/audit-output/evidence/11-operational-bridge.log).

## Final judgment

The Stage 3 classification is complete and mathematically sound; Stage 4 is
producer-authentic, deterministic, bijective, and target-preserving; and the
Stage 5 proof cleanly proves that exact target with faithful operational
bindings and no forbidden trust escape.  I found no concern that changes the
proof or classification judgment.

VERDICT: PASS
LEGITIMACY: LEGIT
