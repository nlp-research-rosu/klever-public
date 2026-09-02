# Independent audit: `33-sort-third`, `kit-semantics`

## Result

The selected Stage 3 classification is complete and semantically correct, the
Stage 4 output is the authenticated deterministic generation of exactly the
three true domain lemmas, and the Stage 5 candidate cleanly proves the fixed
target with honest implementations of all four operational bindings. No
unrecorded proof trust escape was found.

The launcher and environment both record `CLASSIFICATION_AND_PROOF`; the
semantics mode is `SUPPLIED_SEMANTICS`. The trusted audit-input verifier accepts
the input and computes resolved-input hash
`810221e86fb5490d9b77ec62f4db1f191b10956d2bcc9141ec252dfce34d7688`.

## Producer and input integrity

I authenticated the Stage 4 producer before judging its output:

| Producer | Observed SHA-256 | Recorded SHA-256 |
|---|---|---|
| `klean_export.py` | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` | same in source and generator manifests |
| `klean.py` | `ba1148c5df311b510d03f95887839e72b878bbe302c54fd0d981cf568ea8eaa1` | same in source and generator manifests |

The source manifest, generator manifest, and the basename of the producer path
bound in `/audit-input.json` all identify immutable generator image
`sha256:a12daa6dccbac0cead0f384a86899561d3ceb2d478ef3f182ec36ec52ba2cb77`.
The complete producer-source tree hash is
`e2997e276bc28e190348cbf865548aaeda9c5a355767876bf0a1e21fec2aada8`,
also exactly as recorded in the audit input. Thus there is no producer-source
infrastructure error.

All mounted top-level hashes recomputed exactly: Stage 1 pipeline tree
`02d243...`, Stage 1 export tree `954682...`, Stage 2 audit `c8e87a...`,
Stage 3 manifest `d9d3f1...`, complete Stage 4 generation `cdb452...`,
generated tree `f2bdf7...`, and Stage 5 workspace `890916...`. I also checked
all 773 per-file Stage 1 source hashes from the audit input; there were zero
missing files or mismatches. The Stage 5 invocation directory itself is not a
mounted audit input, so its separately recorded invocation-tree hash is not
used as evidence; the mounted selected workspace and its binding are verified.
Full values are in [01-integrity.json](/audit-output/evidence/01-integrity.json).

The first Lean preflight attempt exposed a sandbox-only path-discovery problem:
this execution namespace exposes `/proc/self/exe` but not
`/proc/<current-pid>/exe`, so Lean could not locate its installation. I retained
that failure. A minimal preload shim redirects only that failed self-executable
lookup to `/proc/self/exe`; it does not change source, generated files, proof
terms, or compiler behavior. With the shim, the trusted frozen-toolchain gate
confirmed K 7.1.293, pyk/Klean 7.1.293, Lean 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and Codex 0.144.6. The mandated
preflight then passed reproducibly.

## Inventory reconstruction and Stage 3 classification

Using the trusted `k_rule_inventory` implementation, I reconstructed the local
module closure selected by `prove.sh`. It contains only local module
`VERIFICATION` and exactly seven rules. The frozen `verification.k` hash is
`0d2fdd47cdaa5ed87f5f5dfd3328dbb9e48c22789d34cd670351f8c689d28957`;
the canonical inventory hash is
`03cd112179c09fbd3bee367ec800153a9171a0e1d7bedcc3f7d88ed7d49ecc52`.

The reconstructed order, spans, normalized hashes, `source_rule_id`s, and
whole-inventory hash match `/reference/lemma-discovery.json` bijectively. There
are no omitted, extra, duplicate, or reordered rules. See
[02-inventory-reconstruction.json](/audit-output/evidence/02-inventory-reconstruction.json).

My independent semantic classification is:

| Frozen span | Rule role | Class |
|---:|---|---|
| 11–12 | `mergeThirdFrom` base equation | `DEFINITION` |
| 14–17 | divisible-by-three recurrence | `DEFINITION` |
| 19–22 | complementary recurrence | `DEFINITION` |
| 29–35 | fold the exact complete summary into `sortThirdResult` | `DEFINITION` |
| 37–39 | zero-length consequence for the named result summary | `DOMAIN_LEMMA` |
| 42–44 | associativity of supplied `valSeqConcat` | `DOMAIN_LEMMA` |
| 47 | right identity of supplied `valSeqConcat` | `DOMAIN_LEMMA` |

The first four rules introduce and define a summary, its recurrence, and its
named folded proof term; none executes or observes an MPY program redex. The
last three are mathematical consequences about already-defined symbols.
`prove.sh` compiles all three into `VERIFICATION` before any `kprove` call and
does not first prove any exact rule in a module omitting it, so none qualifies
as `PROVED_DERIVED_LEMMA`. There are no local `OPERATIONAL_RULE`s. Every
`[simplification]` rule is therefore either a definition or a domain lemma.

All three domain lemmas are relevant. The zero-length lemma connects empty
execution to the named postcondition. Associativity and right identity
normalize the append-built output appearing in the loop invariant and final
heap result. The detailed per-ID reasoning is in
[18-independent-classification.md](/audit-output/evidence/18-independent-classification.md).

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`,
the frozen Stage 1 workspace, protected discovery manifest, selected Stage 4
generation, and trusted toolchain lock. It returned `PASS`, built the generated
project after `lake clean`, found three obligations, 45 recorded generated
trust declarations, and zero sorries. Returned evidence is in
[04-klean-preflight-rerun.json](/audit-output/evidence/04-klean-preflight-rerun.json).

The independently classified domain set and generated obligation IDs are the
same ordered three-element list:

1. `rule-684bef72ba46103ebf75024cdc1fa13051bb1bec81e5c3ebfd659638388ad8f2`
2. `rule-a1197a694d8ff7aa6e41e81faf447c740a45b12fc2bad596cbef040446551918`
3. `rule-d101e72bc8dee6c43ac06d55f47939cef9e5ae630efb965cc680c40d10bb36f9`

For each obligation, the ID, source span, normalized hash, inventory hash,
discovery hash, Lean conjunct, and conjunct hash match. The obligation-map hash
is `8f4f043b8ed454cb9626045148ba7460db6ba83e37afb05e99412795d8ab40b4`.
There are no duplicates, omissions, added `True`/`False` conjuncts, or weakened
guards. The first conjunct is nonvacuous because the empty `ValSeq` satisfies
its length guard; the other two universally state the exact associativity and
right-identity equations.

The target is exactly the conjunction generated from that map:

- declaration: `Klean33SortThird.Lemmas.targetStatement`;
- definition SHA-256:
  `d13be07bd32b662dfe8ba7d34761396d212f16a4babba1d703a33fe600b4b7df`;
- instantiated statement SHA-256:
  `d7b986c085a09d6aa35d73b25161781be424a33cc426492562ab424291a68f95`.

The extracted target equals the copies in the generator manifest, Stage 4
preflight record, and audit input. Complete comparisons are in
[14-stage4-target-checks.json](/audit-output/evidence/14-stage4-target-checks.json).
Because the true domain set has three entries, `KLEAN_NO_OBLIGATIONS` is not at
issue.

## Stage 5 proof identity and trust

I made a fresh project at the path recorded in
[05-proof-workdir.txt](/audit-output/evidence/05-proof-workdir.txt), copied the
candidate into it, and copied the immutable generated project contents into
`Base`. The copied Base hash was exactly the recorded generated-tree hash. I
then ran both required commands:

- `lake clean`: exit 0;
- `lake build`: exit 0; `Proof` and all Base modules built successfully.

Complete output is in [06-lake-clean.log](/audit-output/evidence/06-lake-clean.log)
and [07-lake-build.log](/audit-output/evidence/07-lake-build.log). The trusted
combined final gate also passed all input bindings, preflight, build, target,
and axiom checks; see
[09-mechanical-final-gate.json](/audit-output/evidence/09-mechanical-final-gate.json).

Outside immutable Base, the candidate has exactly four target-parameter `def`s
and one `theorem final`. It contains no `sorry`, `admit`, `unsafe`, `axiom`, or
`opaque` token. It neither defines nor shadows
`Klean33SortThird.Lemmas.targetStatement`; `Proof.final` states its exact fixed
instantiation. The copied target source retained SHA-256
`46a8684703bcb29a3f11c044ea87c4423dcb6cad4d8a28abbdb318c019271752`
after the build. Static evidence is in
[15-candidate-static-scan.log](/audit-output/evidence/15-candidate-static-scan.log).

Running Lean with `#print axioms Proof.final` produced exactly:

`'Proof.final' depends on axioms: [propext, Classical.choice]`

There is no `sorryAx`, no unrecorded dependency, and no use by `Proof.final` of
any of the 45 generated trust declarations. `propext` and `Classical.choice`
are baseline axioms explicitly allowed by the trusted gate (as is unused
`Quot.sound`). Exact Lean output and reconciliation are in
[08-axiom-audit.log](/audit-output/evidence/08-axiom-audit.log) and
[16-axiom-reconciliation.json](/audit-output/evidence/16-axiom-reconciliation.json).

## Operational bridge

I checked every target parameter against its bound KORE symbol and frozen
rules:

| Parameter | Candidate definition | Judgment |
|---|---|---|
| `«_<=Int_»` | `decide (left ≤ right)` | Exact Boolean implementation of K integer `≤`. |
| `«vsLen(_)_MPY-CORE_Int_ValSeq»` | structural length followed by `Int.ofNat` | Exact match for `.ValSeq ↦ 0` and `vCons ↦ 1 + length`. |
| `«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»` | structural recursion on the first sequence | Exact match for both supplied concatenation rules. |
| `«sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq»` | select positions `0,3,6,…`, stable-sort them, then merge only those positions | Exact implementation of the source solution and the frozen `buildVS`/`sortVS`/`mergeThirdFrom` summary on the operationally fixed integer and string cases. |

For sorting, the candidate's integer insertion condition is equivalent to the
K rule `X <=Int Y`; its string comparison is exactly the frozen `strLt`
recurrence on integer code sequences. The supplied semantics deliberately
keeps symbolic `sortVS` opaque and supplies concrete integer/string behavior;
the candidate matches those fixed cases and implements the source operation
for additional comparable represented values.

I freshly compiled the supplied operational semantics and ran the concrete
source program: all empty, boundary-length, negative, nontrivial integer, and
string assertions terminated with exit code 0. Independent Lean reductions
checked the same cases plus primitive comparison, length, and concatenation
boundaries. The Python source matched an independent slice-assignment oracle
on 895 cases with zero mismatches. Evidence is in
[11-kompile-llvm.log](/audit-output/evidence/11-kompile-llvm.log),
[12-krun-concrete.log](/audit-output/evidence/12-krun-concrete.log),
[10-adversarial-lean.log](/audit-output/evidence/10-adversarial-lean.log), and
[17-source-differential.log](/audit-output/evidence/17-source-differential.log).

As an adversarial sensitivity test, I replaced only the result bridge with a
constant-empty function in a separate file. That bad bridge still proves the
three-domain-lemma generated proposition, with the same two baseline axioms.
This demonstrates why the mechanical theorem is insufficient by itself. The
submitted bridge is not constant, identity, hard-coded to examples, or
vacuous: its nonempty examples reduce to the freshly observed operational
results, and its recursive clauses implement the frozen program summary.
Counterfactual evidence is in
[13-counterfactual-constant.log](/audit-output/evidence/13-counterfactual-constant.log),
with the full bridge analysis in
[19-operational-bridge.md](/audit-output/evidence/19-operational-bridge.md).

The complete command index, including the retained initial environment failure
and narrowly scoped path-resolution workaround, is in
[COMMANDS.md](/audit-output/evidence/COMMANDS.md).

VERDICT: PASS
LEGITIMACY: LEGIT
