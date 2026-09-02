# Independent audit: `33-sort-third`, `kit-semantics`

Audit mode: `CLASSIFICATION_AND_PROOF`  
Semantics mode: `SUPPLIED_SEMANTICS`

## Conclusion

Stage 3 is correctly classified and Stage 4 is structurally and
mathematically faithful to the three real domain lemmas. The Stage 5 project
also builds cleanly, proves the exact immutable target, does not shadow it,
adds no Lean trust declaration, and has an acceptable kernel axiom list.

The candidate is nevertheless not legitimate because one required target
parameter is not an honest operational implementation. Its
`sortThirdResult` binding sorts selected values only when every selected value
is an integer; for every other representable `SortVal` constructor it chooses
identity. A Boolean counterexample is representable in the generated Lean
domain, disagrees with the frozen Python program, and has no supporting K
equation. The supplied K executable instead becomes stuck at the opaque
`sortVS` term. `[total]`/`[no-evaluators]` does not authorize identity, so this
fallback is an unrecorded, convenient interpretation of a load-bearing
operational symbol.

## Producer provenance and mounted hashes

The producer-source gate passes; there is no infrastructure `AUDIT_ERROR`.

- `/reference/generation-tools/klean_export.py`:
  `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b`.
- `/reference/generation-tools/klean.py`:
  `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4`.
- Both hashes match `source-manifest.json` and `generator-manifest.json`.
- Both manifests and the generator-source path recorded in `/audit-input.json`
  identify immutable generator image
  `sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`.
- The producer bundle tree hash is
  `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`,
  exactly as recorded by the launcher.

The trusted hash procedures also reproduced the mounted Stage 1 workspace
artifact hash, Stage 1 export hash, Stage 2 artifact hash, Stage 3 manifest
hash, Stage 4 artifact and generated-project hashes, and Stage 5 candidate
workspace hash. All 773 recorded Stage 1 file names and byte hashes match with
no omission, extra file, or mismatch. The canonical self-hash of
`/audit-input.json` verifies. The prior Stage 2 review was not used as a
judgment source. Full results are in
[`05-stage4-integrity.txt`](evidence/05-stage4-integrity.txt); raw producer
hashes are in [`01-producer-hashes.txt`](evidence/01-producer-hashes.txt).

## Stage 3 inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` over the
frozen `/reference/k-proof`. The local verification-module closure contains
only `VERIFICATION` and exactly seven rules. The reconstructed
`verification.k` hash is
`0d2fdd47cdaa5ed87f5f5dfd3328dbb9e48c22789d34cd670351f8c689d28957`;
the canonical inventory hash is
`03cd112179c09fbd3bee367ec800153a9171a0e1d7bedcc3f7d88ed7d49ecc52`.

The reconstructed rule sequence is bijective with
`lemma-discovery.json`: identical order, spans, normalized hashes,
`source_rule_id`s, and inventory hash, with no duplicate, omitted, or extra
identity.

| Lines | Source rule ID | Independent class | Judgment |
|---|---|---|---|
| 11–12 | `rule-ea80c64b…82faa` | `DEFINITION` | Terminating base equation of the new `mergeThirdFrom` summary. |
| 14–17 | `rule-8eaaf331…8a019` | `DEFINITION` | Divisible-by-three recurrence of that summary. |
| 19–22 | `rule-4860445c…bba41ca` | `DEFINITION` | Complementary recurrence for non-third positions. |
| 29–35 | `rule-0855e7c5…ee9ed0` | `DEFINITION` | Folding equation that names the complete recurrence `sortThirdResult`; it does not replace program execution. |
| 37–39 | `rule-684bef72…ad8f2` | `DOMAIN_LEMMA` | Zero-length consequence about the named summary, not its general definition. No earlier bridge-free proof exists. It is relevant to the empty input/final summary. |
| 42–44 | `rule-a1197a69…1918` | `DOMAIN_LEMMA` | Associativity of the pre-existing `valSeqConcat`, needed to normalize the loop accumulator. Stage 1 compiled it before proving anything. |
| 47 | `rule-d101e72b…36f9` | `DOMAIN_LEMMA` | Right identity of `valSeqConcat`, needed at the empty suffix/final accumulator. It was not separately proved first. |

There are no `OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA` entries. All four
rules carrying `[simplification]` are either `DEFINITION` or `DOMAIN_LEMMA`.
None of the three domain lemmas is irrelevant to the program or its result
summary. The complete reconstructed documents and comparison are in
[`02-inventory-reconstruction.txt`](evidence/02-inventory-reconstruction.txt).

## Stage 4 generation and target

The mandated trusted call to `tools.klean_preflight.check_generation`, with
`PYTHONPATH=/reference`, the frozen Stage 1 workspace, protected Stage 3
manifest, selected Stage 4 generation, and pinned toolchain lock, returned
`PASS`. It reports three obligations, zero sorries, 45 generated trust
declarations, and successful fresh `lake clean`/`lake build` diagnostics.

The first call exposed a sandbox-only Lean launcher failure: the sandbox
unshares PIDs while exposing an outer `/proc`, so Lean 4.22 could not resolve
`/proc/<inner-pid>/exe`. The preserved failure is
[`03-stage4-preflight.txt`](evidence/03-stage4-preflight.txt). I used the
documented, source-preserved shim
[`proc_self_readlink_shim.c`](evidence/proc_self_readlink_shim.c), which only
redirects such executable-link lookups to the kernel-supported
`/proc/self/exe`. It does not affect Lean parsing, elaboration, declarations,
or kernel checking. The successful returned evidence is
[`04-stage4-preflight-success.txt`](evidence/04-stage4-preflight-success.txt).

Independent of that preflight, the domain-rule and obligation lists have the
same three unique IDs and the same order:

1. `rule-684bef72…ad8f2`: exactly the guarded equation
   `sortThirdResult(VS) = .ValSeq` when `vsLen(VS) <=Int 0`.
2. `rule-a1197a69…1918`: exactly associativity of `valSeqConcat`.
3. `rule-d101e72b…36f9`: exactly right identity of `valSeqConcat`.

The Lean encodings preserve all quantifiers, guards, arguments, conclusions,
and sorts. The first guard is represented by an assumption that the Boolean
comparison equals `true`; the other two are unconditional equations. None is
`True`, empty, irrelevant, weakened, or vacuous. Every conjunct hash, source
span, normalized source hash, inventory hash, and discovery hash recomputes.
The obligation-map byte hash is
`8f4f043b8ed454cb9626045148ba7460db6ba83e37afb05e99412795d8ab40b4`.

The generated declaration is
`Klean33SortThird.Lemmas.targetStatement`. Its definition is exactly the
three-conjunct conjunction; its definition hash is
`d13be07bd32b662dfe8ba7d34761396d212f16a4babba1d703a33fe600b4b7df`
and its applied-statement hash is
`d7b986c085a09d6aa35d73b25161781be424a33cc426492562ab424291a68f95`.
The extracted target is identical in the generator manifest, launcher input,
and recorded Stage 4 preflight. This is a real three-obligation `PASS`, not a
`KLEAN_NO_OBLIGATIONS` case.

## Stage 5 clean build, exact proof, and trust

I copied the candidate to the fresh directory
`/tmp/audit-work/stage5-audit.GWhMbC` and copied the immutable generated
project into its existing empty `Base` directory. Before and after the build,
`Base` had generated-tree hash
`84df5ee8f24c175c97ad6b512ce5032869165c33cf62417caabb8dd73412c666`.

- `lake clean`: exit 0; complete output in
  [`06-stage5-lake-clean.txt`](evidence/06-stage5-lake-clean.txt).
- `lake build`: exit 0; complete output in
  [`07-stage5-lake-build.txt`](evidence/07-stage5-lake-build.txt).
- The candidate has one `Proof.final`, whose stated type text is exactly the
  fixed generated target application.
- Each of the four target parameters has exactly one candidate `def`.
- The candidate has no target-module shadow file and does not change `Base`.
- A comment uses the English word “opaque,” but the Lean source introduces no
  `axiom` or `opaque` declaration. Comment/string-masked source contains no
  `sorry`, `admit`, or `unsafe`.

The exact `#print axioms Proof.final` result is:

```text
'Proof.final' depends on axioms: [propext]
```

It is preserved in [`08-print-axioms.txt`](evidence/08-print-axioms.txt).
`propext` is one of the trusted Lean foundational axioms recognized by the
mechanical final-gate policy. `Proof.final` depends on none of the 45 generated
allowlisted Klean axioms, on no candidate-created axiom, and not on `sorryAx`.
The full target/trust reconciliation is in
[`09-stage5-static-trust.txt`](evidence/09-stage5-static-trust.txt).

Thus the build, theorem identity, and axiom gates pass. They do not cure the
operational bridge below.

## Operational meaning of every target parameter

### `«_<=Int_»`

The candidate defines this as `decide (left ≤ right)`. `SortInt` is Lean
`Int`, so this implements K symbol `Lbl'Unds-LT-Eqls'Int'Unds'` and the
`<=Int` guard in `rule-684bef72…ad8f2`. Compiled boundary checks establish
`1 <= 2 = true` and `2 <= 1 = false`. This binding passes.

### `«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»`

The candidate uses the exact two frozen equations: empty-left returns the
suffix; a `vCons` left operand emits its head and recurses on its tail. This
matches `semantics/list.k` lines 18–20 and supports both associated domain
lemmas. Empty-left and concrete right-identity boundary checks compile. This
binding passes.

### `«vsLen(_)_MPY-CORE_Int_ValSeq»`

The candidate structurally counts `ValSeq` constructors and maps the natural
count to `Int`. This is extensionally the two frozen `vsLen` equations in
`semantics/core.k` lines 223–225. Empty and singleton boundary checks compile.
This binding passes.

### `«sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq»` — failure

The frozen verification definition denotes

```text
mergeThirdFrom(VS, sortVS(buildVS(VS, 0, vsLen(VS), 3)), 0, vsLen(VS))
```

which is the result of selecting indices divisible by three, sorting those
selected values, and merging them back while preserving other positions. The
source program performs exactly that computation with Python `sorted`.

The candidate does implement this correctly when every selected value is an
integer. The frozen HumanEval integer example and a counterfactual mutation at
a selected position both reduce definitionally to the source results in the
compiled [`BridgeAudit.lean`](evidence/BridgeAudit.lean).

But candidate lines 31–34 recognize only `SortVal.inj_SortInt`; lines 57–60
return the selected list unchanged for every other representable constructor.
Generated `SortVal` includes `inj_SortBool` and `inj_SortFloat`, so this is not
an unreachable branch of the target parameter's total Lean domain.

The adversarial Boolean value sequence corresponds to Python list
`[True, None, None, False]`. Its selected positions are `[True, False]`.

- The candidate Lean definition reduces to the original input (identity).
- A separately compiled theorem proves that result differs from
  `[False, None, None, True]`; the Lean check exits 0 in
  [`10-lean-bridge-adversarial.txt`](evidence/10-lean-bridge-adversarial.txt).
- The independent Python operation returns
  `[False, None, None, True]`, as recorded in
  [`11-python-operational-oracle.txt`](evidence/11-python-operational-oracle.txt).
- The supplied K semantics represents `Bool` as a `Val`, but `sortVS` has
  concrete equations only for empty, integer, and string sequences. Running
  the frozen runtime on the same Boolean test exits 113 stuck at
  `sortVS(vCons(true, vCons(false, .ValSeq)))`; see
  [`12-k-bool-operational.txt`](evidence/12-k-bool-operational.txt).

That K result is important: it does not make identity correct. It proves that
the frozen equations supply no bridge-free connection theorem from Boolean
`sortVS` to identity. The semantics describes symbolic `sortVS` as an opaque
trusted ascending sort; `[total]` makes it a total logical symbol, not an
identity function. The candidate therefore both disagrees with the source
operation and assigns an arbitrary convenient value where fixed operational K
execution supplies none. This is exactly the operational-bridge failure the
audit instructions require rejecting.

Numbered excerpts of the verification rules, operational semantics, source
program, and candidate definitions are preserved in
[`13-operational-source-excerpts.txt`](evidence/13-operational-source-excerpts.txt).
All material commands are listed in [`COMMANDS.md`](evidence/COMMANDS.md).

## Final judgment

The protected Stage 3 classifications and deterministic Stage 4 target pass
independent audit. The optional Lean theorem is structurally exact and
kernel-checked, but its `sortThirdResult` parameter is not an honest total
implementation of the frozen/source operational meaning over its declared
domain. Because the audit explicitly makes this bridge a necessary condition,
the overall proof is not legitimate.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
