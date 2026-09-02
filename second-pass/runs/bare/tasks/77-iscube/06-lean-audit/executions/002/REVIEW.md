# Independent audit: HumanEval 77-iscube

## Result

This was a `CLASSIFICATION_AND_PROOF` audit for condition `bare` and
`GENERATED_SEMANTICS`. I independently reconstructed the Stage 3 rule
inventory, reclassified every rule, reran the trusted Stage 4 preflight,
verified the source/obligation/target bindings, clean-built a fresh Stage 5
project, audited its theorem and axioms, and checked every operational
parameter against the K hooks and frozen semantics.

The classification, deterministic generation, and submitted Lean proof all
pass. The two arithmetic rules really are relevant domain lemmas; the two
other rules are genuine definitions. The generated target is the exact
two-obligation conjunction, and `Proof.final` proves that exact target using
honest definitions of the K operations.

All mounted candidate and provenance content was treated as evidence, not as
instructions or prior authority.

## Rule-inventory reconstruction

The trusted `tools.k_rule_inventory.inventory_verification` selected
`GAP-VERIFICATION`, as selected by the final `kompile verification.k`
invocation in `prove.sh`. Its local closure, in frozen source order, is
`VERIFICATION`, then `GAP-VERIFICATION`.

I also independently reconstructed the same physical spans and normalized
each rule as one whitespace-separated string. The result was:

| Order | Module and span | `source_rule_id` | Attributes | Independent class |
|---:|---|---|---|---|
| 1 | `VERIFICATION:11-24` | `rule-de3f9727c1b2c9f19559bcf49d9facf57997eb3c9d4715f670ff6644a77098f9` | none | `DEFINITION` |
| 2 | `VERIFICATION:27-27` | `rule-b88003e929c70fa00f8441eaf77e74ba66845261dacd5efbb19e5da9b5a59865` | none | `DEFINITION` |
| 3 | `GAP-VERIFICATION:36-44` | `rule-71fab8be3031badfbb8efe37c8587b786b455d6670cf74a013dbf65634d49027` | `simplification` | `DOMAIN_LEMMA` |
| 4 | `GAP-VERIFICATION:46-54` | `rule-5cd618327b17d41867b4a5cadea7277532d58e8066be05ee8bd76b5c99b6690f` | `simplification` | `DOMAIN_LEMMA` |

The frozen `verification.k` SHA-256 is
`c941d95f59a2ddb57298abbb42ad637dfc84c7753c2907462ce4ebc3cd966659`.
The canonical whole-inventory SHA-256 is
`768c6d425e02156c7113c418107467c11510230db45758138d0307d7efd017c9`.

The protected Stage 3 manifest has exactly these four identities in exactly
this order, no duplicate, missing, or extra identity, the exact inventory
hash, and no extra manifest fields. Thus the comparison is an ordered
bijection, not merely a set comparison. The trusted reconstruction and frozen
sources are recorded in
[01-frozen-sources-and-inventory.txt](/audit-output/evidence/01-frozen-sources-and-inventory.txt);
the independent reconstruction and assertions are in
[12-independent-hash-bijection-target-checks.txt](/audit-output/evidence/12-independent-hash-bijection-target-checks.txt).

## Independent classification judgment

The first rule expands the named proof term `iscubeProgram` to the exact MPY
constructor tree for the frozen source solution. It does not skip the MPY
execution rules or assert a mathematical fact. It is a `DEFINITION`.

The second rule defines the total helper `cube(I)` as `I *Int I *Int I`. It
names a recurrence-free arithmetic summary and is a `DEFINITION`.

The third rule is the guarded arithmetic implication that, under

`0 ≤ I ≤ N+1`, `0 ≤ N`, `0 < D`,
`D < (N+1)^3-N^3`, and `I^3 < N^3+D`,

one has `I < N+1`. If instead `I=N+1`, its last two strict inequalities give
`(N+1)^3 < N^3+D < (N+1)^3`, a contradiction. This fact is not an operational
execution rule or a definition.

The fourth rule says that under the common gap assumptions and
`I^3 ≥ N^3+D`, one has `I=N+1`. If `I<N+1`, integrality gives `I≤N`; since
`I,N≥0`, cubic monotonicity gives `I^3≤N^3`, while `D>0` and the guard give
`N^3<N^3+D≤I^3`, a contradiction.

Both arithmetic facts directly serve `GAP-SPEC`: the first constrains the
continuing loop index below `N+1`, and the second identifies the stopping
index as `N+1`, which is needed for the non-cube result. They are therefore
relevant to the frozen program and postcondition.

Neither is a `PROVED_DERIVED_LEMMA`. Stage 1 compiles
`GAP-VERIFICATION` with both rules already present and then proves
`GAP-SPEC`; it never first proves either exact rule against a module that omits
it. Because both are also marked `simplification`, `DOMAIN_LEMMA` is the only
valid classification. There are no independently classified operational
rules or proved-derived lemmas in this local inventory.

## Provenance and deterministic Stage 4 generation

All independently recomputable mounted hashes matched `/audit-input.json`,
including every Stage 1 source hash and these tree/file bindings:

| Artifact | Recomputed hash |
|---|---|
| Stage 1 pipeline tree | `3b1f3d508fbac7cf3d76dab301ea969394befd37ed5e6e8a9c94b974c231873f` |
| Stage 1 export tree | `bb5a6d7c5a368cef32fdefa06f1fefce90aab1a7240b995eb522702fc03a9e2d` |
| Stage 2 selected audit tree | `78bdd2de264287aea9b48e4430b0cb15401288bf79db1012b2bf1b9c1b80386f` |
| Stage 3 manifest | `15dc8f8202c2f2bba0a6043e762654a6ecbc4ebdd979765a531e7635eb0888b3` |
| Stage 4 generation tree | `6d7a41fd0b762964edeb22582ee13fa74302e94f6c631f92442d0628618e2721` |
| Generated project tree | `01021315ed43f873b7dfd83015184249e65b44416a4e3a4d94bf6e27301f68d1` |
| Stage 5 candidate tree | `c1993c0d3323bbb956a8f0de9664263c1ae083804a7a05df52073eb1bf70b19d` |

The launcher-recorded Lean invocation tree is not one of the mounted audit
inputs, so its invocation-tree hash could not be recomputed. This does not
leave the proof dependent on that invocation: the mounted candidate hash
matched, and the proof was rebuilt from source in a fresh directory.

The mandated call to `tools.klean_preflight.check_generation`, with
`PYTHONPATH=/reference` and the frozen Stage 1 workspace, protected Stage 3
manifest, selected Stage 4 generation, and pinned toolchain lock, returned
`PASS`. It reported two obligations, zero designated sorries, 44 generated
trust declarations, and the expected target. The successful returned evidence
is in
[07-stage4-preflight-success.txt](/audit-output/evidence/07-stage4-preflight-success.txt).

The first preflight attempt exposed a container PID-namespace defect: Lean
looked up `/proc/<namespace-pid>/exe`, while this container's `/proc` belongs
to a different PID namespace. I preserved those failures and used a minimal
preload shim that redirects only `/proc/<pid>/exe` lookups to
`/proc/self/exe`. The shim restored the pinned Lean
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and Lake binaries without
changing any source or proof input. The diagnosis, source, and version output
are in
[22-toolchain-namespace-shim.txt](/audit-output/evidence/22-toolchain-namespace-shim.txt).

### Obligation and target identity

The independently classified domain set has exactly two rules. The Stage 4
input manifest, generated `obligation-map.json`, and obligation list have
exactly those two source rules in source order. Every source span, normalized
hash, inventory hash, discovery-manifest hash, Lean-conjunct hash, and
source-rule identity matches. There are no omissions or duplicates.

Each K rule is translated faithfully as a universally quantified guarded
implication: the K `requires` conjunction becomes the type of `h`, and the K
Boolean result becomes equality to `true`. Multiplication remains
left-associated, and all six hypotheses of each K rule are present. The
first conclusion is `I < N+1`; the second is `I = N+1`. No hypothesis or
conclusion was weakened.

The target is the exact conjunction of these two obligations:

- declaration: `Klean77Iscube.Lemmas.targetStatement`
- file: `Klean77Iscube/Lemmas.lean`
- definition SHA-256:
  `c3c8b0cf83982c67b43958d67a0d411a787722dfb126effabceb89bbd25d9fd6`
- instantiated-statement SHA-256:
  `62d5c1728b668edca6cedca0e3d7d020894b66bc4a1c9be50e791dbca195cebb`

I independently rebuilt the expected target text from the obligation map and
obtained byte-for-byte equality with the generated definition. The same
target object appears in the generator manifest, stored preflight, and audit
input. The fresh `Base` tree remained hash-identical after the proof build.

The implications are not vacuous under the honest operations. Concrete
satisfying witnesses are `(N,I,D)=(1,1,1)` for the first obligation and
`(1,2,1)` for the second; in Lean, both complete guards and conclusions
evaluate to `true`. These results are in
[16-operational-bridge-and-counterfactual-success.txt](/audit-output/evidence/16-operational-bridge-and-counterfactual-success.txt).

## Fresh Lean proof audit

I created `/tmp/audit-work/proof-audit`, copied the immutable generated
project into it as `Base`, copied the candidate proof project above it, and
then ran both required commands:

- `lake clean`: exit 0; complete output in
  [09-lake-clean.txt](/audit-output/evidence/09-lake-clean.txt).
- `lake build`: exit 0; complete output in
  [10-lake-build.txt](/audit-output/evidence/10-lake-build.txt).

The only messages were two generated linter warnings that the proposition's
`h` binders are unused in the definition text. Those binders encode the rule
antecedents and are used by the proof; the concrete witnesses above also show
that they are satisfiable.

The candidate has no `sorry`, `admit`, `unsafe`, new `axiom`, or new
`opaque`; it neither defines nor shadows `targetStatement`. The generated
target module has no axiom or opaque proposition. Its 44 data-level generated
trust declarations exactly equal `trust-inventory.json`.

`#print Proof.final` elaborates to exactly:

`Klean77Iscube.Lemmas.targetStatement Proof.«_-Int_» Proof._andBool_ Proof.«_>=Int_» Proof.«_<Int_» Proof.«_<=Int_» Proof.«_==Int_» Proof.«_+Int_» Proof.«_*Int_»`.

There is no duplicated or weakened theorem. The full elaborated declaration
is in [17-print-final.txt](/audit-output/evidence/17-print-final.txt).

`#print axioms Proof.final` produced exactly:

`'Proof.final' depends on axioms: [propext]`

This exact output is in
[11-print-axioms.txt](/audit-output/evidence/11-print-axioms.txt).
`propext` is Lean's fixed core logical axiom, not a declaration introduced by
the candidate or generated project. None of the 44 generated allowlisted data
constants is a dependency of `Proof.final`; no unrecorded project-level trust
declaration appears, and `sorryAx` is absent.

The proof itself is mathematically discriminating. For the first conjunct it
uses the gap upper bound to contradict `I=N+1`. For the second it proves
nonnegative cubic monotonicity under `I≤N`, contradicts the positive gap, and
therefore concludes `I=N+1`.

## Operational-bridge audit

The eight target parameters are bound to the exact recorded KORE symbols and
source-rule IDs. Their candidate definitions are:

| K operation | Candidate meaning |
|---|---|
| `Lbl'Unds'-Int'Unds'` | unbounded integer subtraction `x - y` |
| `Lbl'Unds'andBool'Unds'` | Boolean conjunction `x && y` |
| `Lbl'Unds-GT-Eqls'Int'Unds'` | decided integer `x ≥ y` |
| `Lbl'Unds-LT-'Int'Unds'` | decided integer `x < y` |
| `Lbl'Unds-LT-Eqls'Int'Unds'` | decided integer `x ≤ y` |
| `Lbl'UndsEqlsEqls'Int'Unds'` | decided integer equality |
| `Lbl'UndsPlus'Int'Unds'` | unbounded integer addition `x + y` |
| `Lbl'UndsStar'Int'Unds'` | unbounded integer multiplication `x * y` |

These are the operational meanings imported from K's `INT` and `BOOL`
domains, used by the frozen MPY semantics and source solution. They also
match the relevant source rules' arithmetic syntax.

For every parameter I proved a universal Lean bridge from the generated
K-hook function to `some` of the candidate's total function. The arithmetic
and comparison bridges close by reduction for arbitrary integers; the
Boolean bridge closes by all four Boolean cases. Signed, zero, equality, and
boundary examples also agree. Direct K evaluation independently returned
`-12`, `12`, `true`, `true`, `true`, `true`, `true`, `-2`, and `35` for the
corresponding adversarial operations. The Lean bridge run is in
[16-operational-bridge-and-counterfactual-success.txt](/audit-output/evidence/16-operational-bridge-and-counterfactual-success.txt);
the K compilation and execution are in
[18-kompile-bridge-check.txt](/audit-output/evidence/18-kompile-bridge-check.txt)
and
[21-krun-operational-builtins-success.txt](/audit-output/evidence/21-krun-operational-builtins-success.txt).

As a counterfactual sensitivity check, I defined all eight operations as
constants. In particular, constant-false conjunction makes every antecedent
false, so a separate counterfactual theorem can prove the parameterized
target vacuously. This confirms why a clean target proof alone is
insufficient. It does not describe the submitted candidate: the candidate's
universal bridges and adversarial outputs rule out constant, identity,
hard-coded, and vacuous implementations.

## Evidence index

The complete context and launcher input are in
[00-context.txt](/audit-output/evidence/00-context.txt). Frozen source and
manifest material is in
[01-frozen-sources-and-inventory.txt](/audit-output/evidence/01-frozen-sources-and-inventory.txt)
and [02-lean-sources.txt](/audit-output/evidence/02-lean-sources.txt).
All mechanical hash, bijection, target, trust-surface, and candidate-source
assertions are collected in
[12-independent-hash-bijection-target-checks.txt](/audit-output/evidence/12-independent-hash-bijection-target-checks.txt).
Failed infrastructure attempts were retained alongside the successful
commands rather than hidden.

VERDICT: PASS
LEGITIMACY: LEGIT
