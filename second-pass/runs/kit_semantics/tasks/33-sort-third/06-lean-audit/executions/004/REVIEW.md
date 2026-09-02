# Independent audit: HumanEval 33-sort-third

## Scope and outcome

The launcher records `CLASSIFICATION_AND_PROOF`, condition `kit-semantics`, and `SUPPLIED_SEMANTICS`. I independently reconstructed and classified Stage 3, reproduced Stage 4's provenance and mechanical checks, and rebuilt and audited the Stage 5 Lean proof in a fresh project. I treated mounted prose, prior verdicts, comments, and logs only as untrusted evidence.

Stage 3 is correctly classified. Stage 4 is byte-for-byte deterministic and has an exact three-rule obligation-record bijection, but its generated Lean value domain omits the frozen K string-value constructor. This narrows the universal `ValSeq` quantifiers despite the frozen source and supplied operational semantics explicitly supporting string lists. The Stage 5 proof is mechanically clean and its integer implementation behaves correctly, but its `sortThirdResult` parameter cannot implement the omitted string branch because no generated Lean input can represent such a K value. Under the requested exact-domain and operational-bridge criteria, the overall result is therefore not legitimate.

## Producer provenance

Before judging generation, I hashed the mounted generation-time sources:

- `klean_export.py`: `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b`
- `klean.py`: `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4`
- producer-source tree: `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`

These values match `generator-manifest.json`, `/reference/generation-tools/source-manifest.json`, and `/audit-input.json`. The immutable image identifier is consistently `sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`; the same digest identifies the producer bundle path recorded by the launcher. There is no producer-source infrastructure error. Raw comparisons are in [01-producer-provenance.txt](/audit-output/evidence/01-producer-provenance.txt).

## Inventory reconstruction and Stage 3 classification

The trusted inventory code reconstructed a local verification-module closure containing only `VERIFICATION`, with verification source hash `0d2fdd47cdaa5ed87f5f5dfd3328dbb9e48c22789d34cd670351f8c689d28957` and whole inventory hash `03cd112179c09fbd3bee367ec800153a9171a0e1d7bedcc3f7d88ed7d49ecc52`.

The seven ordered entries are:

| Span | Normalized hash / identity suffix | Independent class | Reason |
|---|---|---|---|
| 11-12 | `ea80c64b...582faa` | `DEFINITION` | Empty/base equation for the fresh `mergeThirdFrom` summary. |
| 14-17 | `8eaaf331...8a019` | `DEFINITION` | Divisible-by-three recurrence for the same summary. |
| 19-22 | `4860445c...a41ca` | `DEFINITION` | Complementary non-third-position recurrence. |
| 29-35 | `0855e7c5...e9ed0` | `DEFINITION` | Folding macro/named term connecting the complete merge to fresh `sortThirdResult`. |
| 37-39 | `684bef72...d8f2` | `DOMAIN_LEMMA` | Zero-length consequence for that summary; compiled before proof and never first proved without itself. |
| 42-44 | `a1197a69...18918` | `DOMAIN_LEMMA` | Associativity of pre-existing `valSeqConcat`; true by induction but never first proved in a module omitting the rule. |
| 47 | `d101e72b...b36f9` | `DOMAIN_LEMMA` | Right identity of `valSeqConcat`, with the same trust status. |

There are no `OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA` entries. The Stage 1 build compiles every `verification.k` rule before either `kprove` call, so the comments describing the last two laws as “derived” do not meet the required proof-before-use test. All four `[simplification]` rules are classified only as `DEFINITION` or `DOMAIN_LEMMA`.

All three domain lemmas are relevant: the zero rule covers the empty complete-result summary; associativity re-associates the loop accumulator with the generated suffix; right identity closes that concatenation at loop exit. The protected Stage 3 file matches every reconstructed span, text, normalized hash, ID, classification, and order bijectively, with no omission, duplicate, extra entry, or unaccounted classification. Full reconstruction is in [02-rule-inventory.txt](/audit-output/evidence/02-rule-inventory.txt) and the independent semantic classification is in [03-independent-classification.txt](/audit-output/evidence/03-independent-classification.txt).

## Stage 4 mechanical integrity and target identity

With `PYTHONPATH=/reference`, the required `tools.klean_preflight.check_generation` rerun passes after an audit-local environment workaround for the launcher's `/proc/<namespace-pid>/exe` visibility issue. The workaround redirects only that Lean executable-location read to `/proc/self/exe`; it changes no mounted or generated input. The pinned tool reports Lean 4.22.0, commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

The successful preflight reports:

- frozen Stage 1 export: `9546827fde4def2f1b245e14673e6ccbc177e14641cc642db05c09278e847a2e`
- Stage 3 manifest: `d9d3f1eae128d397f49e33d535ccd426e5809675c04dd5b8047cfabda10b7312`
- generated tree: `84df5ee8f24c175c97ad6b512ce5032869165c33cf62417caabb8dd73412c666`
- three obligations, 45 generated trust declarations, and zero designated sorries
- successful generated-project `lake clean` and `lake build`

All launcher tree hashes and every one of the 773 recorded Stage 1 file hashes reproduce. The exact source-rule/obligation order is the three Stage 3 domain rules `684bef...`, `a1197...`, and `d101e...`; their conjunct hashes are respectively `bf0898...`, `c08533...`, and `e13f6f...`. There are no omitted or duplicate domain IDs, extra obligations, `True` conjuncts, or changed source spans.

The fixed target is:

- declaration: `Klean33SortThird.Lemmas.targetStatement`
- definition hash: `d13be07bd32b662dfe8ba7d34761396d212f16a4babba1d703a33fe600b4b7df`
- statement hash: `d7b986c085a09d6aa35d73b25161781be424a33cc426492562ab424291a68f95`
- statement: `targetStatement` applied, in order, to integer `<=`, `sortThirdResult`, `valSeqConcat`, and `vsLen`

These values agree among the generator manifest, trusted recomputation, audit input, immutable generated project, and the fresh `Base` copy. See [04-generation-preflight.txt](/audit-output/evidence/04-generation-preflight.txt) and [05-hashes-obligations-target.txt](/audit-output/evidence/05-hashes-obligations-target.txt).

### Mathematical Stage 4 failure: narrowed value domain

The structural integrity above is not sufficient. Frozen `core.k` defines `Str ::= str(IntSeq)`, includes `Str` in `Iterable`, and includes `Iterable` in `Val`; therefore `ValSeq` includes string values. Frozen `sort.k` lines 25-32 give explicit lexicographic concrete sorting equations for sequences of `str(IntSeq)`. The source has no integer-only precondition, and its frozen concrete suite includes `sort_third(["z", "keep", "also", "a"]) = ["a", "keep", "also", "z"]`.

By contrast, printing the generated Lean types shows that `SortIterable` has only list, range, tuple, zip, and zipS constructors. Generated `SortVal` injects `Bool`, `Float`, `Int`, and that narrowed `SortIterable`, but has no `SortStr`, no `str(IntSeq)` constructor, and no string-value injection. Uses of `SortString` in names, builtins, and metadata constructors do not represent K string values.

Consequently, a generated universal quantifier over `SortValSeq` ranges over a strict subset of the frozen K `ValSeq`: there is no Lean term corresponding to `vCons(str(...), ...)`. This is a target-domain weakening even though the three emitted conjunct strings and their source IDs are otherwise exact. It violates the requirement that generated obligations match the frozen rules over their actual operational domain. Exact K lines and complete Lean constructor output are in [09-value-domain-mismatch.txt](/audit-output/evidence/09-value-domain-mismatch.txt).

## Stage 5 clean build, proof identity, and trust

I copied `/candidate` to `/tmp/audit-work/proof-audit.PdhDnI`, copied the immutable generated project into that copy as `Base`, and ran both `lake clean` and `lake build`. The complete build succeeds; the only diagnostic is the generated target's unused `h` linter warning. The `Base` source tree remains exactly `84df5e...c666`. Full output is in [06-fresh-clean-build.txt](/audit-output/evidence/06-fresh-clean-build.txt).

The candidate does not modify or shadow the generated target. Its only public target-related declarations are the four exact parameter definitions and `Proof.final`; the theorem's type is exactly the fixed generated target application. Candidate source contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`.

Running Lean with `#print axioms Proof.final` produces exactly:

`'Proof.final' depends on axioms: [propext, Classical.choice]`

Both are permitted Lean core baseline dependencies. `Proof.final` depends on none of the 45 generated allowlisted trust declarations, and there is no `sorryAx` or unrecorded proof escape. Candidate scans and exact axiom output are in [07-candidate-integrity-axioms.txt](/audit-output/evidence/07-candidate-integrity-axioms.txt).

## Operational bridge review

The four bound definitions were checked against their `kore_symbol`, source-rule IDs, frozen rules, source solution, and operational semantics:

- `«_<=Int_»` is `decide (left ≤ right)`, matching the K integer hook. Negative/positive and false cases evaluate correctly.
- `«valSeqConcat(_,_)...»` is exactly the empty/`vCons` structural recursion in frozen `list.k` lines 19-20.
- `«vsLen(_)...»` is structural length converted to `Int`, matching frozen `core.k` lines 223-225.
- `«sortThirdResult(_)...»` honestly implements the source algorithm on the representable integer branch: select indices 0, 3, 6, ..., stable-sort them, and merge them at those positions. Adversarial integer evaluations include `[9,1,2,4] -> [4,1,2,9]`, which distinguishes it from identity, and the longer negative/multi-chunk case from Stage 1.

However, the fourth definition cannot implement the frozen `sortVS` string branch: the generated argument type cannot express a K string value at all. Its comparator contains no such branch because no such constructor exists. This is the requested operational-bridge failure for a normal source input and a supplied-semantics path, not merely a missing convenience case.

As a counterfactual test, I defined operationally correct integer `<=`, `vsLen`, and `concat` but replaced `sortThirdResult` with identity. Lean still proves the unchanged generated target with only `propext`. Thus the theorem constrains `sortThirdResult` only at empty/nonpositive length and cannot independently expose a nonempty implementation error. The submitted integer code survives separate examples, but the counterfactual confirms why the missing string-domain bridge cannot be excused by the clean theorem proof. Exact evaluation and counterfactual outputs are in [08-operational-bridge-tests.txt](/audit-output/evidence/08-operational-bridge-tests.txt).

## Final judgment

Stage 3's classifications are correct, and Stages 4-5 pass their mechanical provenance, hashing, build, target-identity, and axiom gates. They do not pass the required mathematical equivalence gate: deterministic generation narrowed frozen `ValSeq` by deleting its supported string constructor, and the proof bridge therefore cannot implement the source's supplied string-sorting behavior. Exact hashes cannot make that weakened target legitimate.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
