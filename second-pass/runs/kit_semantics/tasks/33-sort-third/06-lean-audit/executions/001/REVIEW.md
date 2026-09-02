# Independent audit: HumanEval `33-sort-third`

## Result

The Stage 3 classification is complete and correct, and the Stage 4 artifacts
are byte-for-byte consistent with their manifests. The deterministic
preflight passes with three obligations. The Stage 5 project also clean-builds,
proves the exact fixed target, has no candidate trust declarations or proof
holes, and depends only on Lean's foundational `propext`.

The result is nevertheless not legitimate. The generated Lean value universe
omits the frozen K `Str` value constructor even though the source theorem is
over arbitrary `ValSeq` values and the supplied semantics concretely sorts
strings. This weakens the generated universal domain. Independently, the
candidate's `sortThirdResult` parameter sorts only integer constructors and
silently preserves every non-integer selected subsequence. A realizable Boolean
input contradicts the frozen source algorithm, and replacing this parameter by
a constant empty function still permits a clean proof. The required
operational bridge therefore fails.

## Scope and frozen-input integrity

`AUDIT_MODE` and `/audit-input.json` both select
`CLASSIFICATION_AND_PROOF`; the condition is `kit-semantics` and the semantics
mode is `SUPPLIED_SEMANTICS`.

The launcher hashes were recomputed with their respective trusted algorithms.
All match:

- Stage 1 workspace tree:
  `02d2439095e3821e7de05e91a6a05ad55ee6f496fc92b22741c8506c584f787a`
- Stage 1 exported K tree:
  `9546827fde4def2f1b245e14673e6ccbc177e14641cc642db05c09278e847a2e`
- Stage 2 selected audit tree:
  `c8e87ae1974bfcdb19c86c9cedc3525afad79e0c40128469bf3d9943aa957ba7`
- Stage 3 manifest:
  `d9d3f1eae128d397f49e33d535ccd426e5809675c04dd5b8047cfabda10b7312`
- Stage 4 generation tree:
  `3ad01244d88b0677e905d63e03f37388739ec9784b00825a35a533a0d8e69010`
- Generated Lean source tree:
  `84df5ee8f24c175c97ad6b512ce5032869165c33cf62417caabb8dd73412c666`
- Stage 5 candidate tree:
  `803e6bc84aae1f7d19241c2accee662e40b164254c8c89243b06e2fcf44d44e1`

All 773 entries in `stage1_source_hashes` were independently matched with no
missing, extra, or changed file. The complete comparison is in
[09-recorded-hash-checks.log](/audit-output/evidence/09-recorded-hash-checks.log).

## Stage 4 producer provenance

The required generation-time producer files were hashed before relying on the
generation:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` |

Both hashes equal the fields in `generator-manifest.json` and
`source-manifest.json`. The producer bundle tree hash is
`94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`,
matching `/audit-input.json`. Both manifests record immutable image
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`;
the image-keyed producer path recorded in `/audit-input.json` has the same
digest component. Evidence:
[02-stage4-producer-provenance.log](/audit-output/evidence/02-stage4-producer-provenance.log).
There is no producer-source infrastructure error.

## Rule inventory reconstruction

The trusted `tools.k_rule_inventory.inventory_verification` implementation
reconstructed the local module closure of the selected `VERIFICATION` main
module. The closure contains exactly `VERIFICATION` and exactly seven rules.
For every rule it independently recomputed the source span, normalized source
hash, `source_rule_id`, attributes, and text. The ordered inventory hash is:

`03cd112179c09fbd3bee367ec800153a9171a0e1d7bedcc3f7d88ed7d49ecc52`

The protected Stage 3 file contains seven unique identities in the identical
order and has the identical inventory hash. There are no omissions,
duplicates, extra classifications, reordered identities, or hash changes.
The complete reconstructed records and bijection are in
[01-inventory-reconstruction.log](/audit-output/evidence/01-inventory-reconstruction.log).

## Independent Stage 3 classification

| Lines | Source-rule suffix | Class | Independent judgment |
|---:|---|---|---|
| 11-12 | `ea80c6...` | `DEFINITION` | Base equation of the named `mergeThirdFrom` recursive summary. |
| 14-17 | `8eaaf3...` | `DEFINITION` | Divisible-by-three recurrence of that summary. |
| 19-22 | `486044...` | `DEFINITION` | Complementary non-third recurrence. |
| 29-35 | `0855e7...` | `DEFINITION` | Folding equation naming the complete summary `sortThirdResult`; it does not rewrite an MPY execution configuration. |
| 37-39 | `684bef...` | `DOMAIN_LEMMA` | Guarded zero-length consequence of the already named summary. |
| 42-44 | `a1197a...` | `DOMAIN_LEMMA` | Associativity of the pre-existing `valSeqConcat`. |
| 47 | `d101e7...` | `DOMAIN_LEMMA` | Right identity of `valSeqConcat`. |

There are no local `OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA` entries.
Stage 1's `prove.sh` compiles all seven rules into
`verification-kompiled` before any `kprove` invocation; it never first proves
any of the final three rules against a module omitting that rule. Therefore
those rules do not meet the required derived-lemma protocol.

All four `[simplification]` rules are classified as either `DEFINITION` or
`DOMAIN_LEMMA`. The domain lemmas are materially relevant: the zero rule
handles the completed empty suffix, while associativity and right identity
normalize the append-built loop accumulator. Detailed reasoning is preserved
in
[04-independent-classification.md](/audit-output/evidence/04-independent-classification.md).

## Deterministic Stage 4 generation

The trusted call

```text
PYTHONPATH=/reference tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json)
```

returns `PASS`, obligation count 3, trust declaration count 45, and zero
designated sorries. Its internal copied project passes `lake clean` and
`lake build`. The complete returned evidence is in
[03b-klean-preflight.log](/audit-output/evidence/03b-klean-preflight.log).

The first invocation exposed an audit-container PID/proc mismatch: Lean 4.22
looks up `/proc/<getpid()>/exe`, while the sandbox's namespace did not expose
that numeric proc entry. `/proc/self/exe` was available. A local preload shim
was compiled which rewrites only numeric `/proc/<pid>/exe` `readlink` calls to
`/proc/self/exe`; its source and build are
[proc_self_exe_shim.c](/audit-output/evidence/proc_self_exe_shim.c) and
[06-shim-build.log](/audit-output/evidence/06-shim-build.log). With the shim,
Lean reports version 4.22.0 and commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly matching the lock.
The initial environmental failure remains recorded in
[03a-klean-preflight-initial-environment-failure.log](/audit-output/evidence/03a-klean-preflight-initial-environment-failure.log).

The independently classified domain-rule IDs, in order, are exactly:

1. `rule-684bef72ba46103ebf75024cdc1fa13051bb1bec81e5c3ebfd659638388ad8f2`
2. `rule-a1197a694d8ff7aa6e41e81faf447c740a45b12fc2bad596cbef040446551918`
3. `rule-d101e72bc8dee6c43ac06d55f47939cef9e5ae630efb965cc680c40d10bb36f9`

`input-manifest.json`, both `source_rules` lists, and the obligations contain
exactly those three unique IDs in that order, one obligation per rule. Every
source span, normalized hash, inventory hash, discovery hash, conjunct hash,
and trust-parameter binding hash matches. The generated target is exactly the
three conjuncts, with no omitted, duplicated, added, or syntactically vacuous
conjunct:

- guarded `sortThirdResult(VS) = .ValSeq` when `vsLen(VS) <= 0`;
- `valSeqConcat` associativity; and
- `valSeqConcat` right identity.

Under honest parameter interpretations, the first guard has the realizable
empty-sequence witness, and the other two are universal structural laws. These
obligations are relevant and not target weakening by altered equations.

The obligation map hash is
`8f4f043b8ed454cb9626045148ba7460db6ba83e37afb05e99412795d8ab40b4`.
The fixed target is:

- declaration: `Klean33SortThird.Lemmas.targetStatement`
- definition hash:
  `d13be07bd32b662dfe8ba7d34761396d212f16a4babba1d703a33fe600b4b7df`
- applied statement hash:
  `d7b986c085a09d6aa35d73b25161781be424a33cc426492562ab424291a68f95`

The recomputed target equals the generator manifest, recorded preflight, and
audit input. Full evidence:
[10-stage4-identity-checks.log](/audit-output/evidence/10-stage4-identity-checks.log).

### Stage 4 mathematical failure

Structural integrity does not establish a faithful semantic domain. Frozen
`core.k` declares `Str ::= str(IntSeq)` and makes `Str` an `Iterable`, hence a
`Val`. Frozen `sort.k` lines 27-32 concretely insertion-sort string values.
The generated Lean `SortIterable` has constructors for lists, ranges, tuples,
and zips, but no `Str` or string-value constructor; no generated `SortStr`
exists. Therefore generated `SortValSeq` cannot represent all values quantified
by the frozen K `ValSeq`.

This is a strict universal-domain reduction, so the generated associativity
and identity theorems do not literally quantify over the complete frozen K
sort even though their equations are structurally true. The discrepancy is
recorded mechanically in
[17-lean-domain-bridge.log](/audit-output/evidence/17-lean-domain-bridge.log).
A fresh K build and auditor-created string test execute successfully and show
the supplied semantics sorting `["z", "a"]` at the selected indices:
[15-kompile-operational-string.log](/audit-output/evidence/15-kompile-operational-string.log)
and
[16-krun-operational-string.log](/audit-output/evidence/16-krun-operational-string.log).
Thus this is not an unwitnessed claim that the fixed model lacks string values;
the fixed model represents and executes them, while the generated Lean domain
does not.

The selected Stage 4 status is `PASS`, not `KLEAN_NO_OBLIGATIONS`; the
no-obligation branch is inapplicable.

## Stage 5 Lean proof

A fresh project was created at
`/tmp/audit-work/33-sort-third-audit`, with only the candidate source/metadata
copied at the root and the exact generated project copied as `Base`. Commands
and results:

- `lake clean`: exit 0, empty output
  ([05b-lake-clean.log](/audit-output/evidence/05b-lake-clean.log))
- `lake build`: exit 0, `Proof` built successfully
  ([05c-lake-build.log](/audit-output/evidence/05c-lake-build.log))

After the build, the `Base` tree still hashes to
`84df5ee8f24c175c97ad6b512ce5032869165c33cf62417caabb8dd73412c666`
and its target still equals the immutable reference target. Candidate sources
contain exactly one definition for each of the four target parameters and one
`Proof.final`; they contain no `targetStatement` shadow and no code occurrence
of `sorry`, `admit`, `unsafe`, a new `axiom`, or a new `opaque`. Evidence:
[11-candidate-static-checks.log](/audit-output/evidence/11-candidate-static-checks.log).

`#check` and `#print` show that `Proof.final` has exactly the fixed target
applied to the four candidate definitions—there is no duplicate or weakened
theorem:
[12-proof-identity.log](/audit-output/evidence/12-proof-identity.log).

The exact axiom command output is:

```text
'Proof.final' depends on axioms: [propext]
```

There is no `sorryAx`. None of the 45 generated declarations recorded by
`trust-inventory.json` occurs in the dependency list. `propext` is Lean's
standard foundational proposition-extensionality axiom from the pinned
toolchain, not a generated or candidate declaration, so it is reconciled as
intrinsic Lean kernel trust rather than an unrecorded candidate escape.
Evidence:
[08-print-axioms.log](/audit-output/evidence/08-print-axioms.log) and
[20-axiom-reconciliation.md](/audit-output/evidence/20-axiom-reconciliation.md).

## Target-parameter bridge audit

| Parameter | Frozen meaning | Candidate meaning | Judgment |
|---|---|---|---|
| `«_<=Int_»` | K integer `<=` hook | `decide (left ≤ right)` | Faithful. |
| `«sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq»` | Complete `mergeThirdFrom` using `sortVS(buildVS(...))` | Select/weave algorithm whose insertion comparison handles only two `inj_SortInt` values and otherwise preserves order | **Operational-bridge failure.** |
| `«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»` | Empty-left and `vCons`-left recursion from `list.k` lines 18-20 | Identical structural recursion | Faithful. |
| `«vsLen(_)_MPY-CORE_Int_ValSeq»` | Zero/successor length from `core.k` lines 223-225 | Structural `Nat` length converted by `Int.ofNat` | Faithful. |

The failing definition is load-bearing as an operational bridge even though
the fixed theorem uses only its empty guarded case. For the realizable source
input `[True, None, None, False]`, only the selected values `[True, False]`
are sorted, so the source algorithm is defined and returns
`[False, None, None, True]`. The independently implemented source oracle records
that result in
[14b-source-oracle-adversary.log](/audit-output/evidence/14b-source-oracle-adversary.log).

The Lean witness uses the generated Boolean value constructors. Kernel
reduction proves that the candidate returns the unchanged unsorted input and
proves it differs from the source-expected result:
[13b-lean-operational-adversary.log](/audit-output/evidence/13b-lean-operational-adversary.log).
This happens because the candidate compares only the pair
`inj_SortInt`/`inj_SortInt`; its fallback inserts every other value unchanged.
That fallback is neither the frozen source's `sorted` behavior nor a justified
interpretation of the supplied opaque symbolic `sortVS`.

As an independent sensitivity check, a separate copy changed only
`sortThirdResult` to the constant empty sequence. The exact mutation is in
[18d-mutation-diff.log](/audit-output/evidence/18d-mutation-diff.log).
Both `lake clean` and `lake build` still exit 0:
[18e-mutation-clean.log](/audit-output/evidence/18e-mutation-clean.log) and
[18f-mutation-build.log](/audit-output/evidence/18f-mutation-build.log).
Thus the clean proof validates only the empty consequence and is insensitive
to every nonempty operational result. The candidate's more convenient
non-integer totalization cannot be accepted merely because it proves the fixed
equation.

The complete per-parameter record is
[19-parameter-bridge-judgment.md](/audit-output/evidence/19-parameter-bridge-judgment.md).

## Final judgment

The Stage 3 classifications are sound and the Stage 4 provenance, hashes,
obligation identity, and target identity are structurally exact. The generated
value-domain omission is nevertheless a mathematical weakening relative to
the frozen K sort. More decisively, the Stage 5 `sortThirdResult` definition
fails an operationally relevant, normally sortable source input, and a
constant counterfactual proves the theorem is unable to detect the defect.
A clean build and clean generated-axiom dependency list therefore do not make
the proof legitimate.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
