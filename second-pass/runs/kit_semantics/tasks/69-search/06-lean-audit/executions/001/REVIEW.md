# Independent audit: HumanEval `69-search`

## Scope and result

This audit covers condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and launcher mode `CLASSIFICATION_AND_PROOF`. I treated
all candidate and provenance prose as untrusted evidence and based the result
on the frozen sources, the trusted inventory/preflight code, fresh Lean
execution, and independent semantic comparison.

Stage 3 classification and Stage 4 generation are sound for the frozen
program. The candidate also cleanly proves the exact generated Lean target
without a proof hole or an unrecorded axiom. It is nevertheless not a
legitimate Stage 5 operational bridge: two definitions bound to full KORE
symbols discard behavior that the frozen K semantics defines. In particular,
the candidate maps integer subtraction through `applyBin` to `noneV` and maps
`noneV is noneV` through `applyCmp` to `false`.

## Audit mode and immutable producer gate

`AUDIT_MODE` and `/audit-input.json` both say
`CLASSIFICATION_AND_PROOF`; see
[`01-audit-mode-env.stdout.txt`](evidence/01-audit-mode-env.stdout.txt) and
[`00-audit-input.stdout.txt`](evidence/00-audit-input.stdout.txt).

I performed the producer-source gate before judging Stage 4:

| Input | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` |
| `klean.py` | `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346` |
| producer-source tree | `bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e` |

The two file hashes match both `generator-manifest.json` and
`source-manifest.json`. The producer-tree hash matches `/audit-input.json`.
The generator manifest, source manifest, and the producer path recorded by the
launcher all identify immutable generator image
`sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`.
The complete comparison is in
[`19-producer-gate.stdout.txt`](evidence/19-producer-gate.stdout.txt); its
`producer_gate_pass` is `true`.

All 777 launcher-recorded Stage 1 file hashes were recomputed with no missing
or mismatched file. Every other mounted launcher hash also matches: discovery
manifest, generated tree, producer tree, K audit tree, Stage 1 tree under both
hash conventions, Stage 4 generation tree, and candidate tree. The Stage 5
invocation tree itself is not mounted and is therefore listed, not
recomputed. See
[`61-recorded-hashes.stdout.txt`](evidence/61-recorded-hashes.stdout.txt).

## Inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof`. It selected module `VERIFICATION`; its local
verification-module closure contains only that module. The reconstruction
found 23 rules in source order.

For every rule I independently checked:

- the inclusive start/end line span against `verification.k`;
- normalization by whitespace joining;
- the SHA-256 of that normalized text;
- `source_rule_id = "rule-" + normalized_sha256`; and
- its position in the ordered manifest identity list.

All checks pass. There are no duplicate, omitted, extra, or reordered IDs.
The recomputed inventory hash is
`1066209b71a607b520f502ba2fce41fc9fb386169ed80067c8bcb7576819bf34`,
exactly the protected Stage 3 value. The complete reconstructed records,
including source text, spans, attributes, normalized hashes, IDs,
classifications, and rationales, are in
[`20-inventory-reconstruction.stdout.txt`](evidence/20-inventory-reconstruction.stdout.txt).
The independent contract result is summarized in
[`21-discovery-contract.stdout.txt`](evidence/21-discovery-contract.stdout.txt).

## Independent Stage 3 classification

The correct split is 18 `DEFINITION`, zero `OPERATIONAL_RULE`, zero
`PROVED_DERIVED_LEMMA`, and five `DOMAIN_LEMMA`.

The definitions are:

- lines 11–15: the two equations for `isIntVal` and the
  `definedProjectInt` alias;
- lines 24–34: the guarded forward/reverse equations and normalizations for
  the named proof term `projectIntTotal`;
- lines 61–65: the base and recursive equations for `allPositive`;
- lines 69–76: the three equations for `frequencyOf`;
- lines 80–85: the three exhaustive cases for `updateAnswer`; and
- lines 89–107: the base and two recursive cases for `searchSummary`.

These rules introduce or recursively define named summaries, predicates, or
proof terms. None is an ordinary program-AST/configuration execution rule.
The summary definitions match the frozen source solution: `frequencyOf`
counts equality occurrences; `updateAnswer` applies the `frequency >=
candidate` and `candidate > answer` tests; and `searchSummary` folds that
update over the input. `allPositive` is the stated Stage 1 precondition.

The five domain lemmas are:

| Frozen span | Rule | Why it is a domain lemma and relevant |
|---|---|---|
| 20–22 | `rule-031285…8b43` | Characterizes definedness of the existing partial `Val`-to-`Int` cast; it is not a definition of that cast and is used by the guarded projection bridge. |
| 39–42 | `rule-884f16…9e7d` | Extends the existing `applyCmp("==", …)` dispatcher to guarded dynamic values; equality is used by the inner frequency loop. |
| 44–47 | `rule-ffcf40…5f02` | Extends guarded `applyCmp(">=", …)`; this is the candidate-frequency qualification test. |
| 49–52 | `rule-3e1ce8…8c2c` | Extends guarded `applyCmp(">", …)`; this is the maximum-answer test. |
| 54–57 | `rule-45c3bb…9c66` | Extends guarded `applyBin("+", …)`; addition is used by the frequency increment and the assignment expression. |

All five existed in the theory before Stage 1 proved its claims, and Stage 1
does not first prove any exact rule in a module omitting it. They therefore
cannot be `PROVED_DERIVED_LEMMA`. They also do not define new symbols and
cannot be `DEFINITION`. Every local rule with a `simplification` attribute is
in either the definition or domain-lemma set. The frozen source is recorded
in [`11-verification-source.stdout.txt`](evidence/11-verification-source.stdout.txt),
the source solution in
[`13-solution-py.stdout.txt`](evidence/13-solution-py.stdout.txt), and the
operational dispatcher rules in
[`56-operators-semantics.stdout.txt`](evidence/56-operators-semantics.stdout.txt),
[`57-int-semantics.stdout.txt`](evidence/57-int-semantics.stdout.txt), and
[`58-bool-semantics.stdout.txt`](evidence/58-bool-semantics.stdout.txt).

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, the three required frozen inputs, and the pinned
`/reference/klean-toolchain.lock.json`. The first ambient invocation could
not locate the stripped image's standalone Lean frontend; its exact failure is
preserved in
[`22-check-generation.stderr.txt`](evidence/22-check-generation.stderr.txt).
Using a controlled bridge to the same pinned Lean 4.22 compiler, the identical
checker completed both `lake clean` and `lake build` and returned `PASS`.
The returned evidence is
[`35-check-generation-rerun.stdout.txt`](evidence/35-check-generation-rerun.stdout.txt).

Independent checks, separate from that preflight, establish:

- the true domain set has five entries, so `KLEAN_NO_OBLIGATIONS` would have
  been invalid;
- `input-manifest.json`, `obligation-map.json`, and the reconstructed domain
  list contain the same five full source records in the same order;
- the five source IDs and five obligation IDs are each unique and identical
  in order;
- every obligation has the exact frozen source span, normalized hash,
  inventory hash, discovery hash, and recomputed Lean-conjunct hash;
- `obligation-map.json` hashes to
  `478d3cf7d8543cd6a0e6bd833bbfe9b57d165fc70aec5eac04e8c7ae7ce8095d`;
- the generated tree hashes to
  `5e9ca0c8083d76c100e9b600c6665227c690fd36fe690fc9e902d382e12cda75`;
  and
- generator manifest, prior preflight, `/audit-input.json`, and fresh parsing
  all identify the same target.

The complete result is
[`60-stage4-independent.stdout.txt`](evidence/60-stage4-independent.stdout.txt),
whose `stage4_structural_pass` is `true`.

The fixed target is
`Klean69Search.Lemmas.targetStatement`, in
`Klean69Search/Lemmas.lean`. Its definition hash is
`41c68a20a7b72edbebde6180033852958ce073aa81dbd4849116efb1a190080b`;
its applied statement hash is
`9e5acf6c4d631e565f38de8237e3cb6c11803e97f5bb387721b78a57fee5868c`.
The generated source is in
[`16-generated-lemmas.stdout.txt`](evidence/16-generated-lemmas.stdout.txt).

Mathematically, the first conjunct is the exact cast-definedness
equivalence. Its literal `∧ True` is the translation of `#Ceil(@V)` for an
already typed element variable; it does not replace a substantive
obligation. The equivalence between cast success and `definedProjectInt`
remains nontrivial on integer versus non-integer values. The other four
conjuncts are the exact guarded `==`, `>=`, `>`, and `+` dispatcher equations.
Their guards are satisfiable with the honest definitions, and the adversarial
run below includes successful integer controls. No whole generated conjunct
is irrelevant, duplicated, weakened, or vacuous for the frozen program.

## Fresh Lean build, target identity, and forbidden constructs

I copied the candidate below `/tmp/audit-work` and copied the immutable
generated project into it as `Base`. The first copy command nested the
generated directory under an already-present empty `Base/`; the resulting
expected configuration error is preserved in
[`39-candidate-lake-clean.stderr.txt`](evidence/39-candidate-lake-clean.stderr.txt).
I then made a second fresh copy and placed the generated contents directly in
`Base/`.

In `/tmp/audit-work/lean-proof-audit-fresh`:

- `lake clean` exited 0 with no output:
  [`43-candidate-lake-clean.command.txt`](evidence/43-candidate-lake-clean.command.txt),
  [`43-candidate-lake-clean.exitcode.txt`](evidence/43-candidate-lake-clean.exitcode.txt);
- `lake build` exited 0 and built `Proof`:
  [`44-candidate-lake-build.stdout.txt`](evidence/44-candidate-lake-build.stdout.txt);
- the copied `Base` still has exactly the generated tree hash:
  [`78-base-target-immutability.stdout.txt`](evidence/78-base-target-immutability.stdout.txt);
- the trusted candidate structural gate found each of the 11 exact parameter
  definitions once and found `Proof.final` stated with the exact fixed target:
  [`63-candidate-structural-gate.stdout.txt`](evidence/63-candidate-structural-gate.stdout.txt);
  and
- scanning candidate Lean sources found no `sorry`, `admit`, `unsafe`,
  `axiom`, or `opaque`, and no `targetStatement` declaration or shadow:
  [`62-candidate-forbidden-shadow-scan.stdout.txt`](evidence/62-candidate-forbidden-shadow-scan.stdout.txt).

## Proof identity and axiom accounting

I added a separate audit-only Lean module to the fresh copy containing:

1. `#check (Proof.final : <exact generated statement>)`; and
2. `#print axioms Proof.final`.

After another `lake clean`, Lean 4.22 rebuilt the generated base, `Proof`, and
the audit module. Its exact output is in
[`50-axiom-audit-clean-build.stdout.txt`](evidence/50-axiom-audit-clean-build.stdout.txt):

```text
final : Klean69Search.Lemmas.targetStatement _andBool_ «_>Int_» «_>=Int_» «_==Int_» «_+Int_»
  «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
  «definedProjectInt(_)_VERIFICATION_Bool_Val» «isIntVal(_)_VERIFICATION_Bool_Val» projectIntTotal «project:Int?»
'Proof.final' depends on axioms: [propext]
```

`sorryAx` is absent. `propext` is one of the Lean core axioms explicitly
recognized by the trusted gate's baseline policy. None of the 42 generated
trust declarations in `trust-inventory.json` is a dependency of
`Proof.final`, and there is no unexpected dependency. The machine-parsed
reconciliation is
[`77-axiom-reconciliation.stdout.txt`](evidence/77-axiom-reconciliation.stdout.txt).

Thus the build, theorem identity, and proof trust accounting all pass. They
do not establish that the supplied target-parameter definitions implement
their bound operational symbols.

## Operational-bridge audit

The candidate definitions for Boolean conjunction, integer `>`, `>=`, `==`,
and `+`, integer-value recognition, cast-definedness, the guarded integer
projection, and the actual `project:Int?` retraction agree with their frozen
meanings on their defined/source domains.

Two full-symbol bindings do not:

| Target parameter | Frozen behavior | Candidate behavior | Result |
|---|---|---|---|
| `LblapplyBin…Val_String_Val_Val` | `MPY-INT` line 13 defines `applyBin("-", 5, 2) => 5 -Int 2`, hence integer `3`. | The integer/integer branch handles only operator `"+"`; every other operator returns `noneV`. | Bridge failure |
| `LblapplyCmp…Bool_String_Val_Val` | `MPY-OPERATORS` line 19 defines `applyCmp("is", V, noneV) => V ==K noneV`; at `V = noneV` the result is `true`. | The `noneV`/`noneV` branch handles only `"=="` and `"!="`; `"is"` returns `false`. | Bridge failure |

These are not undefined totalization cases. They are concrete members of the
frozen operational domains of the exact KORE symbols named by the target
parameters. The candidate definitions are generic functions of an arbitrary
operator string and arbitrary `SortVal` operands; they are not specialized
`+` or integer-comparison symbols. Hard-coding only the cases needed by the
five exported equations therefore fails the required operational bridge,
even though the frozen HumanEval program itself exercises the correctly
implemented cases.

The Lean adversarial module first checks positive controls and then the two
counterexamples. Its output is
[`65-operational-bridge-adversarial-rerun.stdout.txt`](evidence/65-operational-bridge-adversarial-rerun.stdout.txt):

```text
true
true
false
true
false
```

In order, this says: source-case `5 + 2` is integer `7`; source-case `5 > 2`
is true; adversarial `5 - 2` is not integer `3`; it is `noneV`; and
adversarial `noneV is noneV` is false. The frozen rules require the last three
observations to be `true`, `false`, and `true`, respectively.

Counterfactual builds further separate the issues:

- changing the exported integer-addition branch to add one leaves an explicit
  unsolved goal `x + y + 1 = x + y`, so the generated `+` conjunct itself is
  discriminating:
  [`75-cf-plus-build-expected-fail.stdout.txt`](evidence/75-cf-plus-build-expected-fail.stdout.txt);
- replacing `isIntVal` with the constant `false` still builds the exact
  theorem, because all four dispatcher guards become impossible:
  [`76-cf-guard-build.stdout.txt`](evidence/76-cf-guard-build.stdout.txt).

The second mutation is precisely why the requested independent
operational-bridge check is necessary. The submitted `isIntVal` is honest,
but the submitted full `applyBin` and `applyCmp` definitions demonstrably are
not. A clean build and the clean axiom list cannot cure that mismatch.

## Evidence and toolchain notes

Every executed audit command has a corresponding
`evidence/<label>.command.txt`, separate stdout/stderr files, and an exit-code
file. The trusted Stage 5 wrapper's outer frozen-toolchain assertion could not
read the absent `kframework` package metadata in this audit image; that
diagnostic is preserved in
[`45-stage5-mechanical-check.stdout.txt`](evidence/45-stage5-mechanical-check.stdout.txt)
and
[`46-frozen-toolchain-gate.stdout.txt`](evidence/46-frozen-toolchain-gate.stdout.txt).
This did not block the audit: the pinned Lean compiler executed the required
clean builds and exact `#print axioms` module, while the trusted candidate
structural gate was run directly. The earlier producer-source gate, required
to distinguish infrastructure failure from a proof verdict, passed fully.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
