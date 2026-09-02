# Independent Stage 3–5 audit: `33-sort-third`

## Outcome

The Stage 3 classification and deterministic Stage 4 generation are structurally and mathematically correct. The Stage 5 project also passes its clean build, exact-target, forbidden-token, and axiom checks. It is nevertheless not legitimate because one required Lean parameter does not implement the frozen program's operational meaning: the submitted `sortThirdResult` definition sorts only all-integer selected values and leaves every non-integer selected sequence unchanged. A representable Boolean witness disagrees with the source program.

This is exactly the kind of operational-bridge defect that a successful build and a clean `#print axioms` result cannot establish away.

## Scope and immutable provenance

The launcher and environment both select:

- problem: `33-sort-third`;
- condition: `kit-semantics`;
- semantics mode: `SUPPLIED_SEMANTICS`; and
- audit mode: `CLASSIFICATION_AND_PROOF`.

I treated the candidate, earlier audit, earlier reports, logs, comments, and rationales as untrusted evidence. No earlier PASS or classification was adopted as a premise.

Before inspecting Stage 4 mathematically, I hashed the exact mounted producer sources:

| Producer | Observed SHA-256 | Manifest SHA-256 |
|---|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` | same |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` | same |

The source manifest and generator manifest both record generator image `sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`; the launcher-recorded producer bundle path ends in the same image key. The bundle contains exactly those two producer sources plus `source-manifest.json`. Its independently recomputed pipeline tree hash is `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`, matching `/audit-input.json`.

All mounted launcher hashes match their recomputed values: the Stage 1 pipeline tree, Stage 1 export tree, discovery manifest, selected Stage 2 audit, selected Stage 4 generation, producer bundle, generated project, and Stage 5 workspace. All 773 individually recorded Stage 1 source paths and hashes are present with no missing, extra, or mismatched entry. The launcher also records a Stage 5 invocation-tree hash, but that invocation tree is not a mounted audit input; the mounted Stage 5 workspace hash is independently verified. Full results are in `evidence/01-producer-provenance.txt` and `evidence/02-hash-reconciliation.txt`.

## Rule inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` directly on `/reference/k-proof`. The resolved local verification-module closure is exactly `VERIFICATION`; imported supplied-semantics modules are outside the local verification-module rule inventory. The frozen `verification.k` SHA-256 is `0d2fdd47cdaa5ed87f5f5dfd3328dbb9e48c22789d34cd670351f8c689d28957`.

The reconstructed inventory is:

| # | Span | Normalized/source identity | Independent class |
|---|---:|---|---|
| 1 | 11–12 | `ea80c64…582faa` | `DEFINITION` |
| 2 | 14–17 | `8eaaf331…8a019` | `DEFINITION` |
| 3 | 19–22 | `4860445c…ba41ca` | `DEFINITION` |
| 4 | 29–35 | `0855e7c5…e9ed0` | `DEFINITION` |
| 5 | 37–39 | `684bef72…8ad8f2` | `DOMAIN_LEMMA` |
| 6 | 42–44 | `a1197a69…51918` | `DOMAIN_LEMMA` |
| 7 | 47 | `d101e72b…b36f9` | `DOMAIN_LEMMA` |

Each source rule ID is `rule-` followed by the displayed full normalized SHA-256. The whole reconstructed inventory hash is `03cd112179c09fbd3bee367ec800153a9171a0e1d7bedcc3f7d88ed7d49ecc52`.

Comparison with `/reference/lemma-discovery.json` is bijective: 7 versus 7 entries; both sets contain 7 unique IDs; the ordered ID lists are identical; every physical span, normalized hash, text, module, and attribute list agrees; and the whole inventory hashes agree. There is no omission, duplicate, extra rule, reordering, or unaccounted classification. The exact reconstructed JSON is in `evidence/03-rule-inventory.json`; the bijection output is in `evidence/04-inventory-bijection.txt`.

## Independent Stage 3 classification

The first three rules are the base and two guarded recurrence equations for the new proof-summary symbol `mergeThirdFrom`. They match no operational cell, name a mathematical suffix, have disjoint and exhaustive recursive guards for `I < N`, and advance `I` by one. They are definitions.

The fourth rule folds the exact complete term

```text
mergeThirdFrom(VS, sortVS(buildVS(VS, 0, vsLen(VS), 3)), 0, vsLen(VS))
```

to the named proof term `sortThirdResult(VS)`. Its solver-facing orientation does not replace an MPY execution term; it is a definitional abbreviation. Its `simplification` attribute is therefore permitted.

The remaining three simplifiers are domain lemmas:

1. `sortThirdResult(VS) = .ValSeq` under `vsLen(VS) <= 0` is a consequence of the length algebra and the complete result definition. It is relevant to the program's empty input.
2. `valSeqConcat` associativity is the list algebra needed to normalize repeated operational `append` updates in the loop invariant.
3. `valSeqConcat(A, .ValSeq) = A` is the corresponding accumulator boundary law.

The supplied list semantics defines `valSeqConcat` only by structural recursion on its first argument. Both list laws are mathematically true, but `prove.sh` compiles all seven rules before any `kprove` call. Stage 1 never first proves any of these exact statements in a module omitting the rule and only then uses it. None can be `PROVED_DERIVED_LEMMA`. None is an ordinary execution or observation rule. Thus the correct counts are 4 definitions, 0 operational rules, 0 proved derived lemmas, and 3 domain lemmas. Every simplification rule is either a definition or domain lemma.

This independently agrees with Stage 3. Source/semantic details are recorded in `evidence/18-classification-semantics.txt`.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, the frozen Stage 1 workspace, protected Stage 3 manifest, selected generation, and trusted toolchain lock. It returned `PASS`, rebuilt the generated project after `lake clean`, and reported:

- frozen Stage 1 export hash `9546827fde4def2f1b245e14673e6ccbc177e14641cc642db05c09278e847a2e`;
- discovery hash `d9d3f1eae128d397f49e33d535ccd426e5809675c04dd5b8047cfabda10b7312`;
- generated tree hash `84df5ee8f24c175c97ad6b512ce5032869165c33cf62417caabb8dd73412c666`;
- 3 obligations;
- 45 generated trust declarations; and
- 0 designated sorries.

The audit sandbox initially hid the nested PID path Lean queried under `/proc`. I reproduced that infrastructure-only failure and used a temporary shim that redirects only `/proc/<inner-pid>/exe` to `/proc/self/exe`. The pinned Lean then identified itself as version 4.22.0, commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`. No audited input was changed. The shim and complete preflight result are preserved in `evidence/19-proc-exe-shim.c` and `evidence/05-stage4-preflight.json`.

The true domain set is nonempty and has exactly the same three ordered rule IDs as the generated obligations. Each generated conjunct preserves the exact K guard and equation:

1. nonpositive `vsLen` implies empty `sortThirdResult`;
2. `valSeqConcat` associativity; and
3. `valSeqConcat` right identity.

There is no omitted, duplicate, irrelevant, weakened, or extra obligation. The empty-list witness satisfies the first guard, and the other equations quantify actual constructors, so no conjunct is vacuous. The obligation-map SHA-256 is `8f4f043b8ed454cb9626045148ba7460db6ba83e37afb05e99412795d8ab40b4`, matching its manifest.

The generated target extracted independently from `Klean33SortThird/Lemmas.lean` is identical to both `generator-manifest.json` and `/audit-input.json`:

- declaration: `Klean33SortThird.Lemmas.targetStatement`;
- definition SHA-256: `d13be07bd32b662dfe8ba7d34761396d212f16a4babba1d703a33fe600b4b7df`;
- fixed applied-statement SHA-256: `d7b986c085a09d6aa35d73b25161781be424a33cc426492562ab424291a68f95`.

The detailed bijection is in `evidence/06-obligation-bijection.txt`.

## Stage 5 mechanical proof audit

I created `/tmp/audit-work/lean-audit.5FJWJt`, copied the selected generated project into it as `Base`, copied only the candidate project sources at the top level, and ran both required commands:

```text
lake clean   # exit 0, no output
lake build   # exit 0, Build completed successfully.
```

The complete output is in `evidence/07-fresh-copy-and-build.txt`.

The fresh `Base` target retains the exact declaration, statement, and hashes above. The candidate does not define or shadow `targetStatement`. It defines each of the four exact required parameter names once and contains exactly one `theorem final` with the fixed generated statement. Candidate sources contain no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`. The generated Base declarations remain exactly those recorded in `trust-inventory.json`; the candidate adds no new trust declaration.

Lean checked the exact final type and printed:

```text
Proof.final : Klean33SortThird.Lemmas.targetStatement Proof.«_<=Int_»
  Proof.«sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq»
  Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
  Proof.«vsLen(_)_MPY-CORE_Int_ValSeq»
'Proof.final' depends on axioms: [propext]
```

There is no `sorryAx` and no generated allowlist axiom in the dependency set. `propext` is a fixed Lean foundational axiom accepted by the trusted final gate; it is not a candidate declaration or unrecorded generated escape. The exact source and output are in `evidence/09-axiom-audit.lean` and `evidence/10-axiom-audit.txt`.

The trusted final gate also returned `PASS`, used axioms `[propext]`, and explicitly reported `semantic_classification: NOT_EVALUATED`. Its result in `evidence/17-trusted-final-gate.json` is consistent with the clean mechanical checks and does not answer the operational-bridge question.

## Required parameter and operational-bridge audit

### `«_<=Int_»`

The candidate is `decide (left ≤ right)`. This is the exact Boolean meaning of the hooked KORE `INT.le` symbol `Lbl'Unds-LT-Eqls'Int'Unds'`. Boundary reductions `-1 <= 0 = true` and `1 <= 0 = false` pass.

### `«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»`

The candidate recurs on the first `SortValSeq`, returning the suffix at `.ValSeq` and rebuilding one `vCons` per head. This exactly matches the two frozen `MPY-LIST` equations. Distinct-element concatenation and the generated laws reduce correctly.

### `«vsLen(_)_MPY-CORE_Int_ValSeq»`

The candidate counts `.ValSeq` as zero, adds one at each `vCons`, and converts the natural count to mathematical `Int`. This exactly matches the frozen `MPY-CORE` recurrence. A seven-element witness reduces to 7.

These checks and a nontrivial integer `sort_third` example are machine-checked in `evidence/11-parameter-audit.lean` and `evidence/12-parameter-audit.txt`.

### `«sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq»` — failure

The frozen proof summary is the complete weave using `sortVS(buildVS(VS, 0, vsLen(VS), 3))`. The source program calls Python `sorted` on all values at positions divisible by three. The candidate instead defines:

```text
proofSortFrozenIntegers values :=
  if every value is SortVal.inj_SortInt then insertionSort values
  else values
```

and then weaves that result. This is an integer-only interpretation plus a convenient identity fallback, not the total source-program meaning.

The adversarial input `[True, True, False, False]` is normally sortable by the untyped source program and is directly representable by generated `SortVal.inj_SortBool`. The selected positions are `[True, False]`, so the source produces `[False, True, False, True]`. Lean independently proves and reduces the submitted public binding to the unchanged `[True, True, False, False]`, and proves it unequal to the source-expected result. The full witness and reductions are in `evidence/13-bridge-audit.lean` and `evidence/14-bridge-audit.txt`.

This is not merely a question of finite coverage. The candidate explicitly chooses identity for every non-integer selected sequence it can represent. The supplied operational semantics defines `sortVS` over `ValSeq`, treats it as the ascending-sort trust boundary symbolically, and includes concrete insertion-sort rules for both integer and string sequences. The source solution likewise sorts normally sortable non-integer values. An integer-only bridge does not implement that frozen operational contract.

The generated theorem cannot detect this error because its `sortThirdResult` conjunct constrains only the empty-list case. As an adversarial mutation, I supplied an identity `sortThirdResult` together with an independently reimplemented honest `.ValSeq`/`vCons` length recurrence; Lean still proves the exact generated proposition. That successful counterfactual is recorded in `evidence/15-counterfactual-audit.lean` and `evidence/16-counterfactual-audit.txt`. It does not invalidate Stage 4—the exported target correctly contains only the three domain lemmas—but it confirms that Stage 5 legitimacy depends on the separate operational-bridge check required by this audit.

## Judgment

- Stage 3 inventory and classification: passes.
- Stage 4 producer provenance, deterministic generation, obligation bijection, and target identity: passes.
- Stage 5 clean build, target identity, forbidden-token scan, and axiom accounting: passes mechanically.
- Stage 5 operational bridge: fails for `sortThirdResult`; a representable, normally sortable input produces the wrong value.

Because a required target parameter has a convenient definition that closes the equation without implementing the frozen source operation, the proof candidate is not legitimate.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
