# Independent audit: HumanEval 33-sort-third

Scope: `kit-semantics`, `SUPPLIED_SEMANTICS`, audit mode
`CLASSIFICATION_AND_PROOF`.

## Result

Stage 3's classification is complete and mathematically sound, and Stage 4 is
an exact deterministic export of the three genuine domain lemmas. The Stage 5
Lean project also clean-builds and proves the unchanged generated target
without an unrecorded axiom. Nevertheless, the candidate is not legitimate:
its binding for `sortThirdResult` fails to implement the frozen operational
semantics for representable string lists. It claims the generated universe has
no string injection, but `SortVal.inj_SortStr` exists. The candidate therefore
leaves the sortable third-position strings in `['b', 'a']` unsorted where both
the frozen K semantics and source program produce `['a', 'b']`.

This is the operational-bridge failure described by the audit contract. A
clean proof of the parameterized domain equations cannot compensate for it.

## Producer provenance gate

I hashed the two mounted generation-time sources before judging Stage 4:

| Source | SHA-256 |
|---|---|
| `klean_export.py` | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` |
| `klean.py` | `ba1148c5df311b510d03f95887839e72b878bbe302c54fd0d981cf568ea8eaa1` |

Both hashes equal the entries in `source-manifest.json` and
`generator-manifest.json`. The immutable image ID is consistently
`sha256:a12daa6dccbac0cead0f384a86899561d3ceb2d478ef3f182ec36ec52ba2cb77`
in both manifests and in the basename of the producer-source path recorded by
`/audit-input.json`. The producer-source pipeline tree hash is
`e2997e276bc28e190348cbf865548aaeda9c5a355767876bf0a1e21fec2aada8`,
also exactly the launcher-recorded value. There is no producer-source
infrastructure error.

Raw evidence: [producer provenance](evidence/01-producer-provenance.txt) and
[independent Stage 4 hash checks](evidence/07-stage4-independent-check.txt).

## Inventory reconstruction and Stage 3 classification

I invoked the trusted rule inventory on the frozen Stage 1 workspace. The
local verification-module closure contains only `VERIFICATION` and exactly
seven rules. The frozen `verification.k` hash is
`0d2fdd47cdaa5ed87f5f5dfd3328dbb9e48c22789d34cd670351f8c689d28957`;
the reconstructed whole-inventory hash is
`03cd112179c09fbd3bee367ec800153a9171a0e1d7bedcc3f7d88ed7d49ecc52`.

For every row below, the independently normalized source hash is the 64-hex
suffix of its `source_rule_id`. Source spans were sliced again from frozen
`verification.k` and matched the reconstructed text.

| Span | Reconstructed `source_rule_id` | Independent class | Meaning |
|---|---|---|---|
| 11–12 | `rule-ea80c64ba3e52dd72b25433dd6dd721d97e283355279ee9fc2a39f905f582faa` | `DEFINITION` | terminating equation for the named `mergeThirdFrom` summary |
| 14–17 | `rule-8eaaf331b2562006a2a6f4704a4b81a167862611d6c8b82d78a59369cb08a019` | `DEFINITION` | divisible-by-three recurrence for that summary |
| 19–22 | `rule-4860445cf3432071a9a322001c5e3ce052bb80b75147a784f2df24a8fbba41ca` | `DEFINITION` | complementary recurrence for that summary |
| 29–35 | `rule-0855e7c5303f3b1835ec56db22a573c2fc2903b161c139dd7b0ff4a1d1ee9ed0` | `DEFINITION` | exact fold of the completed merge term into the named `sortThirdResult` summary |
| 37–39 | `rule-684bef72ba46103ebf75024cdc1fa13051bb1bec81e5c3ebfd659638388ad8f2` | `DOMAIN_LEMMA` | guarded empty/base behavior of the already defined summary |
| 42–44 | `rule-a1197a694d8ff7aa6e41e81faf447c740a45b12fc2bad596cbef040446551918` | `DOMAIN_LEMMA` | associativity of operational `valSeqConcat` |
| 47 | `rule-d101e72bc8dee6c43ac06d55f47939cef9e5ae630efb965cc680c40d10bb36f9` | `DOMAIN_LEMMA` | right identity of operational `valSeqConcat` |

The three domain lemmas are true and relevant to the source program and its
list-result postcondition. None is a `PROVED_DERIVED_LEMMA`: `prove.sh`
compiles `verification.k`, including all three rules, before any `kprove` and
never first proves the exact rule against a module omitting it. No inventory
rule is an ordinary source execution/observation rule. All four rules marked
`simplification` are classified as either `DEFINITION` or `DOMAIN_LEMMA`.

The protected Stage 3 manifest contains these same seven identities in the
same order, with the same spans, normalized hashes, and classifications. There
are no omissions, extras, duplicate IDs, reordered identities, or unaccounted
entries. Its recorded inventory hash also matches. Thus the independent total
is four definitions, three domain lemmas, zero operational rules, and zero
proved-derived lemmas.

Raw evidence: [inventory reconstruction and bijection](evidence/02-rule-inventory.txt),
[frozen sources and proof driver](evidence/03-frozen-source-and-semantics.txt),
and [independent classification rationale](evidence/20-independent-classification.txt).

## Stage 4 deterministic generation

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` over the specified Stage 1 workspace, Stage 3 manifest,
and Stage 4 generation. It returned `PASS`, with three obligations, zero
designated sorries, and generated-tree hash
`f2bdf7d41e2032ee688bff46d3c5857f656b2ccd6234ec88fd0f80765a8e7e53`.

The first attempt exposed an audit-container PID-namespace problem: Lean
4.22 could not resolve the reported numeric `/proc/<pid>/exe`. I retained that
failure, diagnosed it, and reran with an audit-only `readlink` shim that maps
only that missing numeric path to `/proc/self/exe`. The pinned Lean binary,
libraries, lock file, generated inputs, and checker were unchanged. The
successful complete preflight output is retained separately.

The generated source-rule list, input-manifest list, obligation-map source
list, and obligation list are an exact ordered bijection over the independently
identified domain set:

1. guarded `sortThirdResult(VS) = .ValSeq` when `vsLen(VS) <=Int 0`;
2. `valSeqConcat` associativity; and
3. `valSeqConcat` right identity.

Each Lean conjunct hash recomputes exactly. The obligation-map hash is
`8f4f043b8ed454cb9626045148ba7460db6ba83e37afb05e99412795d8ab40b4`,
and the trust-inventory hash is
`404ce5288982b558b1ac92da91dc836c522158a8912bb33a0f0a814e39de0958`.
Counts are three in the map, generator manifest, and export result; there are
no omissions or duplicates.

Mathematically, all three conjuncts are exact translations of their frozen K
rules. The guarded first conjunct is not vacuous under the bound operational
meaning: structural `vsLen` is zero on `.ValSeq`, so its premise is realized.
No conjunct changes a guard, result, quantifier, or argument order. The domain
set is genuinely nonempty, so this is correctly a normal `PASS` generation,
not `KLEAN_NO_OBLIGATIONS`.

The fixed generated target is:

- declaration: `Klean33SortThird.Lemmas.targetStatement`;
- definition SHA-256:
  `d13be07bd32b662dfe8ba7d34761396d212f16a4babba1d703a33fe600b4b7df`;
- instantiated-statement SHA-256:
  `d7b986c085a09d6aa35d73b25161781be424a33cc426492562ab424291a68f95`.

The declaration, full statement, parameter metadata, and both hashes are
identical in the generated source, generator manifest, and audit input.

Raw evidence: [initial environmental failure](evidence/04-stage4-preflight-rerun.txt),
[namespace diagnosis](evidence/04b-toolchain-namespace-diagnostic.txt),
[shim source](evidence/lean-proc-shim.c),
[successful trusted preflight](evidence/05-stage4-preflight-success.txt),
[generated artifacts](evidence/06-stage4-artifacts.txt), and
[independent obligation/target audit](evidence/07-stage4-independent-check.txt).

## Stage 5 proof mechanics and identity

I made the fresh workspace `/tmp/audit-work/stage5-audit.xwx7bj`, copied the
candidate into it, and populated its `Base` from the selected generated
project. Source hashes remained exact. In that fresh copy, both `lake clean`
and `lake build` exited 0. The only build diagnostic was an unused-variable
warning in generated `Lemmas.lean`.

Independent static checks found each of the four target parameter definitions
exactly once. Candidate Lean files contain no `sorry`, `admit`, `unsafe`, new
`axiom`, or new `opaque`. They neither define `targetStatement` nor reopen its
namespace. `Proof.final` is stated directly at the exact fixed generated
instantiation, not at a duplicate or weakened theorem. Candidate and generated
pipeline tree hashes both match `/audit-input.json`. The trusted final gate
also passed all of its mechanical checks.

The exact `#print axioms Proof.final` result is:

```text
'Proof.final' depends on axioms: [propext, Classical.choice]
```

There is no `sorryAx`. Neither printed dependency is a candidate-added or
generated declaration: `propext` and `Classical.choice` are Lean core axioms
explicitly recognized by the trusted final gate. The generated
`trust-inventory.json` has 45 recorded declarations, but none appears in
`Proof.final`'s printed axiom closure. Therefore there is no unrecorded proof
trust escape.

Raw evidence: [candidate source scan](evidence/08-candidate-static-source.txt),
[isolated copy](evidence/09-stage5-isolated-copy.txt),
[clean](evidence/10-stage5-lake-clean.txt), [full build](evidence/11-stage5-lake-build.txt),
[#print axioms](evidence/12-stage5-print-axioms.txt),
[trusted final gate](evidence/14-trusted-final-gate.txt), and
[independent static target identity](evidence/19-stage5-static-identity.txt).

## Operational-bridge audit

I located the exact candidate definition for every `target.parameters` entry
and compared it to its `kore_symbol`, attached rule IDs, frozen K rules,
source solution, and operational semantics.

| Candidate parameter | Independent operational judgment |
|---|---|
| `«_<=Int_»` | Correct: `decide (left ≤ right)` implements K `<=Int`; true and false adversarial checks reduce correctly. |
| `«sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq»` | **Incorrect**: its private comparator handles booleans, integers, floats, lists, and tuples, then returns `none` for every other `SortVal`, including generated `inj_SortStr`. Consequently its sort does not implement frozen `sortVS` on strings. |
| `«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»` | Correct: exact structural recursion matching the two K `valSeqConcat` rules. |
| `«vsLen(_)_MPY-CORE_Int_ValSeq»` | Correct: structural sequence length converted to `Int`, matching the two K `vsLen` rules. |

The failure is concrete and in-scope. The frozen Stage 1 spec quantifies a
generic `VS` with no integer-element precondition, its frozen concrete tests
explicitly test string sorting, and `sort.k` lines 25–32 define lexicographic
insertion for `str(IntSeq)`. Generated `Sorts.lean` defines `SortStr` and
`SortVal.inj_SortStr`. Candidate `Proof.lean` nevertheless says Base has no
such injection and falls through to `none` for strings.

I constructed the representable input corresponding to
`['b', 0, 0, 'a']`. The third-position slice is `['b', 'a']`; frozen K and the
source solution sort it to `['a', 'b']`, so the required result is
`['a', 0, 0, 'b']`. The candidate witness prints `true` for equality with the
unchanged input and `false` for equality with the required result. An
independent execution of the frozen source algorithm produces the required
result.

Additional integer, length, comparison, and concatenation witnesses show that
the candidate is not merely a constant implementation and does work for the
integer examples. That does not repair the string counterexample. I also
proved the same generated target with intentionally dishonest bindings
(false comparison, constant-empty sort, left-projection concatenation, and
constant-zero length) without axioms. This counterfactual confirms why the
target proof alone cannot establish operational fidelity; the required bridge
audit is decisive.

Raw evidence: [operational string witness source](evidence/OperationalWitness.lean)
and [result](evidence/13-operational-string-witness.txt),
[other parameter witness source](evidence/ParameterWitnesses.lean) and
[result](evidence/15-parameter-witnesses.txt),
[counterfactual source](evidence/CounterfactualBindings.lean) and
[result](evidence/16-counterfactual-bindings.txt),
[source oracle](evidence/17-source-string-oracle.txt), and
[frozen/generated/candidate rule excerpts](evidence/18-operational-rule-excerpts.txt).

## Final judgment

Stage 3 and Stage 4 pass their independent classification, provenance,
bijection, and mathematical checks. Stage 5 passes build, target-identity, and
axiom-accounting checks but fails the mandatory operational bridge. Because a
representable input covered by the frozen source and K semantics produces the
wrong result, the proof candidate is not a legitimate proof of the requested
frozen operational meaning.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
