# Independent audit: HumanEval 28-concatenate

Audit mode: `CLASSIFICATION_AND_PROOF`  
Condition: `kit-semantics`  
Semantics mode: `SUPPLIED_SEMANTICS`

## Executive judgment

Stage 3 classification and deterministic Stage 4 generation are structurally
and mathematically correct. The generated target has one real, relevant
domain-lemma obligation and is unchanged throughout the pipeline. The Stage 5
project also builds cleanly, states exactly that target, and has a clean axiom
report.

The proof is nevertheless not legitimate. One target parameter is the global
KORE symbol for `applyBin`. The candidate defines only the string-concatenation
case and maps every other input to `noneV`. This disagrees with many defined
cases in the frozen supplied semantics; a concrete witness is integer addition:
frozen K gives `applyBin("+", 1, 2) => 3`, while the candidate definition gives
`noneV`. This is a theorem-convenient totalization rather than the required
honest total meaning of the bound operational symbol. The clean build and exact
target proof cannot repair that operational-bridge failure.

## Launcher and immutable-input binding

The trusted launcher contract verified the resolved input hash as
`c60f50bdd16861f416c8cef49caf85b65317eab979c6b1ab6e4feee8cb866804`
and confirmed the requested mode, condition, and semantics mode. See
[33-launcher-input-verification.txt](/audit-output/evidence/33-launcher-input-verification.txt).

All accessible recorded hashes matched:

- Stage 1 pipeline tree:
  `898ef000b991ffd60d711d75e84b2550ca69ffeab57b77434c6a5e6bc8579f29`
- Stage 1 deterministic-export tree:
  `82e6583db1a89891d9d3148dd8da71e3c5e838a75707090d86634ee108019b38`
- selected Stage 2 audit tree:
  `25b228efd94f9058bcc45c74835ad526a470260ff6659cc82cd6d9b9ba185a3f`
- Stage 3 manifest:
  `81bc5b664867124ac6040d98e2cda120346c9428ceba71d056cb98f0db7bd3cf`
- Stage 4 generation pipeline tree:
  `b897b0386025188c4a5e31f6cb0c50eaeb1edb97bc92a4cb478c1896cf4b92e3`
- generated project deterministic tree:
  `4aa7abbb3edc3f4a00297119ba6bdeeb714e10f313c33968496c974de3a198e7`
- producer-source bundle:
  `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`
- Stage 5 candidate pipeline tree:
  `0aa476db0b98dd11016a9d50db8b1bd60336b5d18acd53a21f8ffb966e8da7b6`

The launcher-recorded Stage 1 per-file inventory contained 769 files; there
were no missing, extra, or mismatched files. Full results are in
[12-recorded-hash-checks.json](/audit-output/evidence/12-recorded-hash-checks.json).

## Stage 4 producer provenance

Producer provenance passed before judging generation:

- observed `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- observed `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`
- immutable generator image:
  `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`

Both source hashes agree exactly with `source-manifest.json` and
`generator-manifest.json`. The source manifest image ID agrees with the
generator provenance, and the launcher-recorded producer bundle path ends in
the same image digest. The bundle contains exactly the two producer files and
the source manifest. There is no producer-source infrastructure error.

## Rule inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof`. `prove.sh` selects `VERIFICATION`, and the local
module closure within `verification.k` contains only `VERIFICATION`. The frozen
file hash is
`2e889c33acb13e241a4fa27718fed136829aac513168f9b0f2bebbd6d7fcf5fa`.

The reconstruction yielded these nine ordered rules:

| Span | Normalized SHA-256 / source rule ID | Attributes | Independent class |
|---|---|---|---|
| 10 | `d67f74749887fbf3e482ab3b5e009e306d6afabeb7e2bc1483cdcc5bc5d801aa` | none | `DEFINITION` |
| 11 | `fd0940a4d6054e1358229d8416d82d1fdbd9fc9b81a95171ac29cc004419b996` | `owise` | `DEFINITION` |
| 15 | `dcec90ae81b6468389e91083acc95d81ead6981ccababa579f6172a0a877a7e3` | none | `DEFINITION` |
| 16–17 | `7a72869f4d1d964b627bb3b06d70211a5e2d1d60583ce2a867ccbb8d7b284747` | none | `DEFINITION` |
| 23 | `caaa68653c6b00f190e89bd450eb4b1da239abda96d0efd431698e876453410d` | none | `DEFINITION` |
| 24–26 | `164607b7d03894ef15a07854149cb03c9b9031a6e6187bd89611899d0aaac54e` | none | `DEFINITION` |
| 31 | `2bc2a66c772aae97380ca3ab3abdcf702833b825027b9f8fc0da1fe4878d02ac` | none | `DEFINITION` |
| 32–34 | `8d075e2e7a462abce866779cfe5fc6c30b077acc04bc848e0e0bb58c1da430da` | none | `DEFINITION` |
| 39–42 | `d77f984813dd200ec980ca7e00225a96be53f3a6ed10be91093061eb9e528506` | `simplification` | `DOMAIN_LEMMA` |

Each source rule ID is `rule-` followed by the displayed normalized hash. The
whole ordered inventory hash is
`db23f00c4d52498c8b55896d22cd454b5a735cc3d960bd225af2ec15cc2b9995`.
The raw reconstructed texts and spans are in
[01-reconstructed-inventory.json](/audit-output/evidence/01-reconstructed-inventory.json).

The Stage 3 manifest has the same inventory hash, the same nine unique IDs in
the same order, and no omitted, duplicated, or extra identity. See
[07-stage3-bijection.txt](/audit-output/evidence/07-stage3-bijection.txt).

## Independent Stage 3 classification

The first eight rules are genuine definitions:

- `stringCodes` has a string projection equation and an `owise` fallback,
  jointly defining the named total projection.
- `isStringSeq` has empty and structural-recursive equations defining the
  named recognizer.
- `concatFrom` has empty and guarded recursive equations defining the named
  concatenation fold.
- `lastFrom` has empty and guarded recursive equations defining the named
  final-loop-target summary.

None of these rules is an ordinary execution bridge or an unproved
human-facing fact.

The rule at lines 39–42 is correctly a `DOMAIN_LEMMA`, not a definition,
operational rule, or proved-derived lemma. Its statement is:

```text
applyBin("+", str(A), V)
  => str(seqConcat(A, stringCodes(V)))
requires V ==K str(stringCodes(V))
[simplification]
```

Under the guard, `V` must be `str(B)` and `stringCodes(V)` is `B`; the rule
therefore reduces exactly to the frozen `MPY-STR` operational rule
`applyBin("+", str(A), str(B)) => str(seqConcat(A,B))`. It is relevant because
the source loop executes `result += string` over `List[str]` and the Stage 1
loop claim needs that symbolic normalization. It is not `PROVED_DERIVED_LEMMA`:
`prove.sh` compiles the complete `verification.k` before every `kprove` call,
and no earlier claim proves this exact rule in a module without it. It is the
only simplification rule, so every simplification is classified as either a
definition or domain lemma as required.

## Deterministic Stage 4 generation

The first mandated preflight attempt failed before project inspection because
the sandbox PID namespace did not expose the running process at
`/proc/<pid>/exe`, which Lean 4.22 uses for installation discovery. The exact
failure is preserved in
[13-preflight-initial-environment-failure.txt](/audit-output/evidence/13-preflight-initial-environment-failure.txt).
I used an auditor-authored compatibility shim that only answers that executable
path lookup using the kernel `AT_EXECFN` value. Its source and hash are under
`evidence/`; it does not modify Lean/K sources or compiler behavior.

With that environment repair, the exact trusted
`tools.klean_preflight.check_generation` call passed:

- status `PASS`
- obligation count `1`
- generated tree unchanged
- clean and build exit codes `0`
- trust declaration count `42`
- designated sorry count `0`

The returned evidence is
[14-preflight-rerun-with-pid-shim.json](/audit-output/evidence/14-preflight-rerun-with-pid-shim.json).

Independent mapping checks found exactly one independently classified domain
rule, exactly one mapped source rule, and exactly one obligation, all with the
same unique source rule ID. The source span, normalized hash, inventory hash,
discovery hash, conjunct hash, and obligation-map hash all match. See
[31-obligation-bijection.txt](/audit-output/evidence/31-obligation-bijection.txt).

The generated conjunct says, in plain language: for all `V` and `A`, if the K
injection of `V` equals the injection of
`str(stringCodes(V))`, then string `applyBin("+", str(A), V)` equals
`str(seqConcat(A, stringCodes(V)))`. This is the exact guarded K rule above.
With the honest `stringCodes` definition the guard is satisfiable for every
string value, so the conjunct is not vacuous. There are no omitted, duplicated,
irrelevant, or weakened domain obligations.

The fixed target is
`Klean28Concatenate.Lemmas.targetStatement`, with:

- definition hash
  `8dca32cee5a4de83089284f41b25df5beb12774e7885224a28c9d1efc88970f4`
- applied statement hash
  `a67c9ad0a05bb83890d59b9a7b7c2a127b0fa5ea7b6d2fc2f031bb5cad203ae5`
- obligation-map hash
  `0ed08f8e6d2d68fcedac326113e5debe7902245ddfe37a5c313d40ba75d4cbac`

The extracted definition is exactly the deterministic conjunction generated
from the obligation map and exactly matches the generator manifest and audit
input. See
[27-independent-target-extraction.txt](/audit-output/evidence/27-independent-target-extraction.txt).

## Stage 5 mechanical proof audit

I created the fresh project
`/tmp/audit-work/lean-proof.eOaxU0/project`, copied the candidate into it, and
copied the immutable generated project into `Base`. `Base` and the mounted
generated project both hash to
`4aa7abbb3edc3f4a00297119ba6bdeeb714e10f313c33968496c974de3a198e7`;
`diff -qr` reported no differences.

Both required commands passed:

- `lake clean`: exit `0`
- `lake build`: exit `0`

Complete output is in
[20-lake-clean.log](/audit-output/evidence/20-lake-clean.log) and
[21-lake-build.log](/audit-output/evidence/21-lake-build.log).

The candidate:

- defines each of the three exact target parameter names once;
- contains exactly one `theorem final`;
- states the exact generated applied target;
- does not redefine or shadow `targetStatement`;
- contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`.

The scan is in
[28-candidate-token-and-shadow-scan.json](/audit-output/evidence/28-candidate-token-and-shadow-scan.json).
The trusted final mechanical gate also passed and independently rebuilt the
candidate; see
[26-final-mechanical-gate.json](/audit-output/evidence/26-final-mechanical-gate.json).

`#print axioms Proof.final` produced exactly:

```text
'Proof.final' depends on axioms: [propext]
```

There is no `sorryAx`. `propext` is one of the trusted Lean foundational axioms
explicitly accepted by the trusted final gate, not a candidate declaration.
None of the 42 generated allowlisted K trust declarations is used by
`Proof.final`, and there is no unrecorded candidate trust escape. Exact output
is in
[22-print-axioms-Proof-final.txt](/audit-output/evidence/22-print-axioms-Proof-final.txt).

## Stage 5 operational-bridge audit

Two parameter definitions are faithful:

- `seqConcat` is the exact total structural recursion from frozen `str.k`:
  empty-left returns the right sequence, and a cons-left preserves its head and
  recurses on its tail.
- `stringCodes` is the exact two-rule `verification.k` projection: strings
  return their payload; all other `Val` constructors return `.IntSeq`.

The candidate's string `applyBin` branch is also universally correct on the
generated rule's guarded match domain. The audit Lean artifact proves the
universal `seqConcat` base/step equations, the string projection equation, and
the string-plus connection equation. It also proves that relevant mutations of
`applyBin` and `seqConcat` are rejected.

The global `applyBin` binding itself is not faithful. The candidate defines:

```text
applyBin("+", str(lhs), str(rhs)) = str(append(lhs,rhs))
applyBin(_, _, _)                 = noneV
```

But the bound KORE symbol is the supplied semantics' global
`applyBin(String,Val,Val)`, whose frozen rules also include integer addition,
subtraction, multiplication, modulus, division, exponentiation, boolean/integer
mixed addition, float operations, and other defined cases. A total
interpretation may choose a value where frozen K is genuinely undefined; it
may not replace already defined cases.

The machine-checked adversarial witness is:

```text
candidate applyBin("+", inj_Int(1), inj_Int(2)) = noneV
```

while frozen `semantics/int.k` gives:

```text
applyBin("+", I1, I2) => I1 +Int I2
```

so that input must produce `inj_Int(3)`. The exact candidate and frozen-source
lines, plus the checked witness, are collected in
[35-operational-bridge-mismatch.txt](/audit-output/evidence/35-operational-bridge-mismatch.txt).

This mismatch is not detected by the theorem because its only occurrence of
`applyBin` is the guarded string-plus case. The adversarial artifact further
proves that the target can be satisfied by coordinated constant
interpretations, and that a constant `stringCodes` can make most guards
unsatisfiable. Those facts do not invalidate deterministic Stage 4 structure;
they demonstrate why independent operational binding is mandatory. The
candidate supplied honest definitions for `seqConcat` and `stringCodes`, but
not for the globally bound `applyBin` symbol.

Therefore `Proof.final` proves the fixed Lean proposition under a
theorem-convenient interpretation, not the required proposition with every
target parameter implementing its frozen operational meaning. This is the
specified operational-bridge failure and determines the final result.

## Evidence index

Exact commands are in
[00-COMMANDS.md](/audit-output/evidence/00-COMMANDS.md), and the complete
artifact listing is in
[34-evidence-index.txt](/audit-output/evidence/34-evidence-index.txt).

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
