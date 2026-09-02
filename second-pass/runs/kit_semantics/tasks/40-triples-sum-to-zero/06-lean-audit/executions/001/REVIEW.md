# Independent Stage 3–5 audit: `40-triples-sum-to-zero`

## Result

I independently audited condition `kit-semantics` in
`SUPPLIED_SEMANTICS` mode. Both `AUDIT_MODE` and the launcher resolution
select `CLASSIFICATION_AND_PROOF`. I did not rely on the selected Stage 2
review, the protected Stage 3 rationales, prior PASS records, candidate
comments, or candidate logs as proof of correctness.

The protected classification is complete and correct: the canonical local
inventory contains 26 rules, of which 24 are definitions and exactly two are
domain lemmas. Deterministic Stage 4 generates one exact obligation for each
domain lemma and no others. The Stage 5 candidate defines all eight target
parameters with their honest operational meanings, proves the immutable
generated target, builds from a clean fresh copy, and introduces no
project-specific axiom dependency or forbidden trust escape.

Raw commands, complete build output, exact Lean output, reconstructed
inventories, and test sources are in [`evidence/`](evidence/).

## Launcher and immutable input authentication

The corrected launcher summary is
[`68-launcher-audit-metadata-summary-corrected.txt`](evidence/68-launcher-audit-metadata-summary-corrected.txt).
It records:

- problem `40-triples-sum-to-zero`;
- condition `kit-semantics`;
- mode `CLASSIFICATION_AND_PROOF`;
- semantics mode `SUPPLIED_SEMANTICS`;
- selected Stage 4 status `PASS` with two obligations; and
- Stage 5 status `SUCCEEDED`, which I did not treat as a verdict.

I recomputed every mounted launcher hash with the trusted hash routines.
All available hashes match, including all 774 Stage 1 source paths and file
hashes. The principal values are:

| Artifact | Recomputed and recorded SHA-256 |
|---|---|
| Stage 1 K workspace | `5c4982f216f0a22da0aff695a7684917ecea62d6723b7b7d37fe3332883fba08` |
| Stage 1 export | `a2001708f6750aaa04e0af61fcea29f1c70444ac9dca16f25ea8abd9c3e929ba` |
| Stage 3 manifest | `31ce916e664debb3fc66a68e30186b9d8497f4bbe4743f23ba2215fb211500e8` |
| Selected K audit | `8947b01dbc368038a88f9697b503d34cce7fb188d80d3ec7e646bb7f311f2fc1` |
| Stage 4 generation | `077be21e6a932fac2f6d00ea47e6011cf30ab98e23b6402c74879e212dbae15f` |
| Generated project | `ff5ca8a3734b7118d307b86b391558fb1cbb7f56b7941cde641e11e796aeb5c0` |
| Producer source bundle | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |
| Candidate workspace | `2a4fab1d40b7167abdfbc40b7838eaaa802c7305b72f55d35908b346a8966740` |

The launcher-recorded Stage 5 invocation tree is not mounted, so its recorded
hash cannot be recomputed directly. The successful workspace that it produced
is mounted and its hash matches. This does not affect the clean independent
build of that workspace. Full results are in
[`44-recorded-hash-verification.txt`](evidence/44-recorded-hash-verification.txt).

### Generation-time producer authentication

I hashed the two required producer sources before judging Stage 4:

| Producer | SHA-256 |
|---|---|
| `/reference/generation-tools/klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `/reference/generation-tools/klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both hashes match `generator-manifest.json` and
`source-manifest.json`. The producer bundle contains exactly those two files
plus the source manifest. Its immutable generator image ID is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`;
this matches the generator manifest, source manifest, and the image-keyed
producer path recorded in `/audit-input.json`. Evidence:
[`01-input-and-producer-authentication.txt`](evidence/01-input-and-producer-authentication.txt)
and
[`44-recorded-hash-verification.txt`](evidence/44-recorded-hash-verification.txt).
There is no producer-source infrastructure error.

## Canonical rule reconstruction and bijection

I invoked the trusted `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference` on `/reference/k-proof`. The local
verification-module closure is exactly module `VERIFICATION` in
`verification.k`; its source SHA-256 is
`9ce79a8c6fef1de0a82539447c2fbe821595c7dfa7bea7be12e2fa9c697eaa32`.
The reconstruction contains 26 unique ordered rules and has inventory hash
`f14289f2f89f2d52117ca7ad185617a5fe6323e4f4b762382a75f2808399ca6a`.

For every row below, the normalized source SHA-256 is the hexadecimal suffix
of `source_rule_id`. The protected manifest has the same unique IDs in the
same order and the same whole-inventory hash. Thus there are no omissions,
duplicates, additions, reordered identities, changed spans, or changed
normalized hashes.

| # | Frozen span | `source_rule_id` | Rule family | Independent class |
|---:|:---:|---|---|---|
| 1 | 12 | `rule-61708f547727d7aa918ad6bf8a016e92b25d1ccd0e36098b415347016593af3e` | `intVals(.IntSeq)` | `DEFINITION` |
| 2 | 13 | `rule-7e02eb37b7bdf1eab6f0857a5ba0eea03ae8d443148932837b9044d248811a1f` | `intVals(iCons(...))` | `DEFINITION` |
| 3 | 22 | `rule-c7de3cc91957966c2e287056766b0332cf6ffdaec28c37531cbba7f11ac07a3e` | `intAt(.IntSeq, _)` | `DEFINITION` |
| 4 | 23 | `rule-9ef7f75c9d030faf85080705a0465550f676a8729fd89f75a4c89a89f3bef12a` | `intAt(iCons(...), 0)` | `DEFINITION` |
| 5 | 24–25 | `rule-3d31bba42a85cabc815659b58fc221eb876cde2e0d7fc47a65715c7303c3241e` | positive `intAt` recurrence | `DEFINITION` |
| 6 | 26–27 | `rule-d2b38b93f718eb582aeb8e703070db02855786b254179f53ff3ab14e72a536b2` | negative `intAt` totalization | `DEFINITION` |
| 7 | 31 | `rule-041ae6f97e0a64393d4fd3489adb8b7922f6bdd833dd98ec4a40214de3ea0864` | `vsLen(intVals(IS)) = isLen(IS)` | `DOMAIN_LEMMA` |
| 8 | 32–34 | `rule-02406fd68a82c2913a2b54042cfc3145ed95db3409554a09fc0a8d1b6cf799f4` | guarded `valSeqAt(intVals(IS), I) = intAt(IS, I)` | `DOMAIN_LEMMA` |
| 9 | 42–47 | `rule-8f1610587bf737bb5c54e86924e2f79f4154ac8465370be0992a66f42cb7a719` | invalid-domain `thirdFrom` base | `DEFINITION` |
| 10 | 48–53 | `rule-53814ea661857cebfa97d9521b74aa3d0d06bf9a18be90ed9136b73d50641cd7` | exhausted `thirdFrom` base | `DEFINITION` |
| 11 | 54–61 | `rule-c40b0ddfed4444541b0c697e601553b83229e5a57efc9520c0a7a60e7e9e598c` | `thirdFrom` recurrence | `DEFINITION` |
| 12 | 63–66 | `rule-f626c317007e738e3dac4aa639bdbb0a088030a45776e00d26ac958a4eabf70b` | invalid-domain `pairFrom` base | `DEFINITION` |
| 13 | 67–70 | `rule-52c3edb1912d9dd6bc594873c21b975e82d063a40d91fe661425871625b0ccd7` | exhausted `pairFrom` base | `DEFINITION` |
| 14 | 71–76 | `rule-269487dea660700294e0df9c985efaac434cad9dd4842aa465dda12446bc0e07` | `pairFrom` recurrence | `DEFINITION` |
| 15 | 78–79 | `rule-e84b342b33053ff679a2bcde5a77bdde8bac77a1efd7f264e2cc1d6b73b4240e` | negative `tripleFrom` base | `DEFINITION` |
| 16 | 80–81 | `rule-7412da7fc80943dd934d7428207728ea3034e9abc66648c8a2e4a629f5a64a17` | exhausted `tripleFrom` base | `DEFINITION` |
| 17 | 82–85 | `rule-b0e6db4c2b5c2d64dee44292ac1b60d8017b8066600da7a1de8fd3bb5df362d4` | `tripleFrom` recurrence | `DEFINITION` |
| 18 | 96–99 | `rule-3715cb2d6de855e8f0d56c8731dcd44dcb31e91cf93fe184d935ef3cdbd09d4a` | `innerCond()` macro | `DEFINITION` |
| 19 | 101–115 | `rule-872df4534b8344655a82e1ce75ddbff255f4e95cbd683ef7e5ca4c99a14603db` | `innerBody()` macro | `DEFINITION` |
| 20 | 117–120 | `rule-83f913af19781dfc5d6f23b0cc85d1c4f1e5a172d3b546385471cb4ba6dee8da` | `middleCond()` macro | `DEFINITION` |
| 21 | 122–127 | `rule-e0cb22599bc2f08ab0cfb7a81a256d9e601153f92c4fe0e1ffded66240aa242a` | `middleBody()` macro | `DEFINITION` |
| 22 | 129–132 | `rule-c67bd09f1ea5719f1c1892236bebe19987a71a76ed6ee35acabce50477d77d23` | `outerCond()` macro | `DEFINITION` |
| 23 | 134–139 | `rule-c00bad024d03c4fd49146aac0dfb46f478cc8147c36ea7975399490f50973258` | `outerBody()` macro | `DEFINITION` |
| 24 | 141–148 | `rule-46f0e67cc5409babed23b00e43574465e039e224789f6567cbe7e9a3b542ee1f` | `programBody()` macro | `DEFINITION` |
| 25 | 151–152 | `rule-10f2f341850e5b1dba882c01e51fc736628d8ea0e733d0c07c0b4339cf0816ec` | `triplesClosure()` | `DEFINITION` |
| 26 | 155–156 | `rule-5e0fb0ffad7ca37fbc4b92a80ab74a3d7facd687e939787910a1f2e6c53ccf2c` | `solutionBindings()` | `DEFINITION` |

The full canonical rule texts, attributes, spans, normalized hashes, and IDs
are in
[`05-canonical-inventory-reconstruction.txt`](evidence/05-canonical-inventory-reconstruction.txt);
the row-by-row protected/independent comparison is in
[`66-bijective-classification-table.txt`](evidence/66-bijective-classification-table.txt).

## Independent classification judgment

Rules 1–2 define the structural `IntSeq`-to-`ValSeq` embedding. Rules 3–6
define and totalize the named proof function `intAt`. Rules 9–17 are the base
equations and recurrences of the named `thirdFrom`, `pairFrom`, and
`tripleFrom` summaries. They encode the three nested, strictly increasing
index search used by the source program. Rules 18–26 are nullary syntax
macros and named closure/binding terms reproducing the frozen source program.
All 24 therefore meet the requested definition criterion; none is an ordinary
execution or observation rule.

Rules 7 and 8 do not define their left-head symbol. They add structural facts
connecting proof-local `intVals`/`intAt` to the supplied semantics'
`vsLen`/`isLen` and `valSeqAt`. A source-wide exact search finds these rule
texts only in `verification.k`; Stage 1 does not first prove either rule in a
module omitting it and then use it later. They therefore cannot be
`PROVED_DERIVED_LEMMA`, `DEFINITION`, or `OPERATIONAL_RULE`. Both are genuine
`DOMAIN_LEMMA`s.

They are relevant rather than decorative. The frozen source loops use
`len(l)` and in-bounds `l[i]`, `l[j]`, and `l[k]`; the Stage 1 claims store
the source list as `list(intVals(IS))` while the loop summaries use
`isLen(IS)` and `intAt(IS, ...)`. These two facts are precisely the bridge
between those representations. The length equation follows by structural
induction. The index equation follows by induction on an in-bounds,
nonnegative index using the supplied `valSeqAt` recurrence and the
proof-local `intAt` recurrence.

The only rules with the `simplification` attribute are rules 7 and 8, both
classified as `DOMAIN_LEMMA`. There are zero `OPERATIONAL_RULE` entries and
zero `PROVED_DERIVED_LEMMA` entries. Frozen source and operational traces are
in
[`06-domain-lemma-operational-source-trace.txt`](evidence/06-domain-lemma-operational-source-trace.txt)
and
[`61-parameter-operational-source-comparison.txt`](evidence/61-parameter-operational-source-comparison.txt).

## Deterministic Stage 4 generation

I reran the exact trusted function
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and:

- frozen input `/reference/k-proof`;
- discovery input `/reference/lemma-discovery.json`; and
- generation `/reference/klean-generation`.

It returned `PASS`, two obligations, zero designated sorries, generated tree
hash `ff5ca8a3734b7118d307b86b391558fb1cbb7f56b7941cde641e11e796aeb5c0`,
and a successful generated-project clean build. The complete returned
evidence is
[`40-trusted-stage4-preflight-returned-evidence.txt`](evidence/40-trusted-stage4-preflight-returned-evidence.txt).

The audit container exposes `/proc/self/exe` but not the numeric
`/proc/<pid>/exe` path that Lean 4.22's application locator reads. The first
unmodified preflight therefore failed before parsing the project. I diagnosed
that infrastructure mismatch and used a logged, process-local compatibility
shim that changes only `readlink("/proc/<digits>/exe")` to
`readlink("/proc/self/exe")`. Its complete 29-line source, sole exported
symbol, and hashes are in
[`64-compatibility-shim-source-and-scope.txt`](evidence/64-compatibility-shim-source-and-scope.txt).
The pinned compiler is Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, matching the locked toolchain.
The shim affects executable-path discovery, not Lean source, elaboration,
kernel checking, or proof terms.

### Exact domain-rule/obligation bijection

Let:

- `D1 = rule-041ae6f97e0a64393d4fd3489adb8b7922f6bdd833dd98ec4a40214de3ea0864`;
- `D2 = rule-02406fd68a82c2913a2b54042cfc3145ed95db3409554a09fc0a8d1b6cf799f4`.

The independently determined ordered domain set is exactly `[D1, D2]`. The
obligation map has exactly two unique entries in that order:

1. `∀ IS, vsLen (intVals IS) = isLen IS`, sourced only from D1 at line 31,
   with conjunct hash
   `c39d301020c58c8085b0691e94388fd2b4d1835fc82a632a3fa840d1fe92b567`.
2. `∀ I IS, (0 ≤ I ∧ I < isLen IS) → valSeqAt (intVals IS) I =
   inj_SortInt (intAt IS I)`, represented with the exact K Boolean guard,
   sourced only from D2 at lines 32–34, with conjunct hash
   `ebcebb2c7d00f296bc5eba794c57a13ad5de7b79886613e155d825cb65ee9e41`.

Each entry repeats the canonical normalized hash, source span, inventory hash,
and discovery-manifest hash. There are no extra rules, omitted domain rules,
duplicates, changed guards, or weakened equations. The first conjunct is
falsified by a constant-zero `vsLen` on a singleton. The second guard is
satisfiable at index zero on a singleton and the equation is falsified by a
constant-zero `intAt` on a singleton containing 7. Thus neither conjunct is
vacuous under the honest operations. Stage 4 correctly uses `PASS`, not
`KLEAN_NO_OBLIGATIONS`.

### Fixed generated target

The immutable target is
`Klean40TriplesSumToZero.Lemmas.targetStatement` in
`Klean40TriplesSumToZero/Lemmas.lean`. Its two conjuncts are exactly the two
obligations above. The manifest values are:

- definition SHA-256:
  `1be2c7f19dabbc6646e33ccae6532543de3035aafbad1e1bf3dff4965a89dec7`;
- statement SHA-256:
  `55f7e03ce34aa6aee7370c82060a5aad22dac34323b1d803448ba283ff27733d`.

The reparsed generated declaration equals the generator manifest object,
which equals the target object in `/audit-input.json`. All eight parameter
names, types, KORE symbols, binding hashes, and source-rule associations also
match. The exact generated source is in
[`42-target-and-candidate-static-audit.txt`](evidence/42-target-and-candidate-static-audit.txt),
and the independent hash/target comparison is in
[`44-recorded-hash-verification.txt`](evidence/44-recorded-hash-verification.txt).

The generated linter says the name `h` is unused in the equality's body. It is
nevertheless a dependent function binder and therefore is the implication
hypothesis that restricts the equality to in-bounds indices. It is not a
vacuous target conjunct.

## Stage 5 clean proof audit

I made a fresh project at
`/tmp/audit-work/fresh-lean-project-2`, copied the candidate into it, and
copied the exact generated project contents into `Base`. Before building,
both trusted tree-digest algorithms reported equality between the source
generation and fresh `Base`; the generator digest was
`ff5ca8a3734b7118d307b86b391558fb1cbb7f56b7941cde641e11e796aeb5c0`.
Evidence:
[`47-correct-fresh-proof-project.txt`](evidence/47-correct-fresh-proof-project.txt)
and
[`48-fresh-base-identity.txt`](evidence/48-fresh-base-identity.txt).

I then ran the required commands:

| Command | Result |
|---|---|
| `lake clean` | exit 0 |
| `lake build` | exit 0; `Proof` built; only the generated unused-`h` linter warning |

Complete command output is saved in
[`49-fresh-lake-clean.txt`](evidence/49-fresh-lake-clean.txt) and
[`50-fresh-lake-build.txt`](evidence/50-fresh-lake-build.txt). The generated
target file remained byte-identical after the build:
[`71-fresh-base-post-build-source-identity.txt`](evidence/71-fresh-base-post-build-source-identity.txt).

The candidate has exactly one definition for each target binding and exactly
one `theorem final`. Outside `Base`, it contains no `sorry`, `admit`,
`unsafe`, `axiom`, or `opaque`; it neither defines nor shadows
`targetStatement`. The exact scan is
[`63-candidate-forbidden-and-identity-scan.txt`](evidence/63-candidate-forbidden-and-identity-scan.txt).

`#print Proof.final` shows the theorem's type is exactly the manifest statement:

`Klean40TriplesSumToZero.Lemmas.targetStatement Proof._andBool_ Proof.«_<Int_» Proof.«_<=Int_» Proof.«intAt(_,_)_VERIFICATION_Int_IntSeq_Int» Proof.«intVals(_)_VERIFICATION_ValSeq_IntSeq» Proof.«isLen(_)_MPY-CORE_Int_IntSeq» Proof.«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» Proof.«vsLen(_)_MPY-CORE_Int_ValSeq»`.

It is not a duplicated, weakened, or alternative theorem. Exact printed proof
and type:
[`51-proof-final-and-axioms.txt`](evidence/51-proof-final-and-axioms.txt).

### Axiom accounting

Running Lean with `#print axioms Proof.final` produced exactly:

`'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]`

There is no `sorryAx`. There is also no dependency on any of the 47 generated
axiom declarations listed by `trust-inventory.json`, including none of the
automatically repaired summary declarations. The three reported names are
Lean's standard core logical axioms; the trusted final-gate policy explicitly
adds exactly `Classical.choice`, `propext`, and `Quot.sound` to the generated
inventory allowlist. No other or unrecorded project proof escape appears.

The trusted `tools.klean_final_gate.evaluate_proof_candidate` independently
repeated the clean build, exact target check, axiom parsing, `sorryAx`
rejection, and allowlist reconciliation and returned `PASS`. Evidence:
[`53-trust-inventory-reconciliation.txt`](evidence/53-trust-inventory-reconciliation.txt),
[`55-trusted-final-gate-policy.txt`](evidence/55-trusted-final-gate-policy.txt),
and
[`56-trusted-final-gate-returned-evidence.txt`](evidence/56-trusted-final-gate-returned-evidence.txt).

## Operational bridge audit

I located the exact candidate `def` for every `target.parameters` entry and
compared it with the manifest KORE symbol, associated D1/D2 source rules,
frozen `verification.k`, supplied K semantics, and the source program.

| Candidate definition | Manifest KORE symbol / source IDs | Independent operational judgment |
|---|---|---|
| `Proof._andBool_` | `Lbl'Unds'andBool'Unds'` / D2 | `left && right`, the exact K Boolean conjunction truth table. |
| `Proof.«_<Int_»` | `Lbl'Unds-LT-'Int'Unds'` / D2 | `decide (left < right)` over Lean `Int`, matching K mathematical integer `<`. |
| `Proof.«_<=Int_»` | `Lbl'Unds-LT-Eqls'Int'Unds'` / D2 | `decide (left ≤ right)` over Lean `Int`, matching K `<=Int`. |
| `Proof.«intAt(_,_)_VERIFICATION_Int_IntSeq_Int»` | `LblintAt'LParUndsCommUndsRParUnds'VERIFICATION'Unds'Int'Unds'IntSeq'Unds'Int` / D2 | Exact four-case meaning of frozen lines 22–27: empty/negative return zero, index zero returns the head, positive indices recurse on the tail with `I-1`. |
| `Proof.«intVals(_)_VERIFICATION_ValSeq_IntSeq»` | `LblintVals'LParUndsRParUnds'VERIFICATION'Unds'ValSeq'Unds'IntSeq` / D1,D2 | Exact structural embedding from frozen lines 12–13, injecting each integer as `SortVal.inj_SortInt`. |
| `Proof.«isLen(_)_MPY-CORE_Int_IntSeq»` | `LblisLen'LParUndsRParUnds'MPY-CORE'Unds'Int'Unds'IntSeq` / D1,D2 | Exact supplied `core.k` empty/cons recurrence at lines 227–229. |
| `Proof.«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»` | `LblvalSeqAt'LParUndsCommUndsRParUnds'MPY-SUBSCRIPT'Unds'Val'Unds'ValSeq'Unds'Int` / D2 | Exact supplied zero/positive in-bounds reductions at `subscript.k` lines 11–14. It returns `noneV` only for empty, negative, or out-of-bounds cases that the frozen `[total]` function intentionally leaves abstract and that D2's guard excludes. |
| `Proof.«vsLen(_)_MPY-CORE_Int_ValSeq»` | `LblvsLen'LParUndsRParUnds'MPY-CORE'Unds'Int'Unds'ValSeq` / D1 | Exact supplied `core.k` empty/cons recurrence at lines 223–225. |

The source program initializes all three indices at zero and increments them
inside `i < j < k < len(l)` loops. Consequently the guarded `valSeqAt`
behavior is exactly the operational behavior needed for every source
subscript. The candidate proof derives the bounds from the honest Boolean
guard and uses only the specified in-bounds `valSeqAt` reductions; it does not
exploit its arbitrary total value outside the supplied semantics' specified
cases.

I compiled an independent Lean adversarial suite containing 27 concrete
examples. It covers the complete Boolean conjunction truth table, integer
comparison equality/negative boundaries, empty/singleton/multi-element
sequences, valid indices, negative indices, out-of-range indices, embedding,
and both length functions.

I also compiled these counterfactual mutations:

- `zeroVsLen` is rejected on a singleton;
- `emptyIntVals` is rejected on a singleton;
- `zeroIntAt` is rejected at index zero on a singleton containing 7; and
- an always-false `_andBool_` is, as an adversarial control, accepted by the
  equation because it makes the guarded conjunct vacuous.

The last control confirms why a clean equation proof alone is insufficient.
The real candidate does not use that exploit: its `_andBool_` is the honest
K operation and passes the full truth table, while its comparisons and
sequence operations likewise implement their frozen meanings.

The final adversarial command exits 0:
[`69-operational-adversarial-counterfactual-tests-expanded.txt`](evidence/69-operational-adversarial-counterfactual-tests-expanded.txt).
The exact independently added audit source is
[`OperationalAudit.lean`](evidence/OperationalAudit.lean).

## Superseded diagnostic attempts

For transparency, the evidence directory preserves a few failed diagnostic or
test-authoring attempts. The initial preflight failure was the numeric
`/proc/<pid>/exe` infrastructure issue described above. An initial temporary
copy put the generated project one directory too deep; I detected it before
building and created the correctly laid-out fresh project used for all final
commands. The first adversarial source used the unavailable `norm_num`
tactic; replacing it with kernel-checked `simp` produced the successful final
run. None of those superseded attempts changed any read-only candidate or
provenance input.

## Final judgment

The inventory reconstruction is bijective, the protected classifications
match independent operational classification, the two true and relevant
domain lemmas map exactly to two faithful generated obligations, the generated
target is immutable and hash-identical, and the candidate proves that exact
target with honest operational bindings and an accounted trust boundary.

VERDICT: PASS
LEGITIMACY: LEGIT
