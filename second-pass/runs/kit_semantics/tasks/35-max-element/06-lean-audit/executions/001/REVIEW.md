# Independent audit: HumanEval 35-max-element

## Outcome

The Stage 3 classification is complete and mathematically appropriate, and
the deterministic Stage 4 project is provenance-correct, bijective with the
true domain-lemma set, and faithful to the frozen K rules. The Stage 5 Lean
project cleanly proves the exact fixed generated theorem without an
unaccounted logical trust escape.

The candidate is nevertheless not legitimate. Its definition of the target
parameter bound to MPY's full `applyCmp` KORE symbol is hard-coded to implement
only operator `">"` and to return `false` for every other operator. The frozen
operational semantics has real behavior for other operators. This is an
operational-bridge failure under the required audit standard, independently
of the successful Lean proof.

Audit mode was independently confirmed as `CLASSIFICATION_AND_PROOF` in both
`AUDIT_MODE` and `/audit-input.json`; semantics mode was
`SUPPLIED_SEMANTICS`.

## Producer provenance and frozen inputs

The mandatory producer-source gate passed before Stage 4 was judged:

- `klean_export.py`:
  `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`
- `klean.py`:
  `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346`
- producer bundle tree:
  `bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`
- immutable generator image:
  `sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`

The two file hashes agree exactly among the mounted source files,
`source-manifest.json`, `generator-manifest.json`, and `/audit-input.json`.
The image identity agrees among all three records. The mounted producer file
set is exact, with no missing or extra producer source.

All other recorded trees also recomputed exactly: the original K workspace,
Stage 1 export, selected K audit, Stage 4 generation, generated Lean project,
and candidate workspace. The 810 recorded Stage 1 source-file hashes had no
omissions, additions, or mismatches. Thus there is no producer-source
infrastructure error. Raw values and comparisons are in
`evidence/00-producer-provenance.txt`.

## Stage 3: inventory reconstruction and classification

I ran the trusted rule-inventory implementation against the frozen Stage 1
workspace, starting from `verification.k`. Its local module closure is exactly
`VERIFICATION`; it contains 55 rules. The reconstructed verification source
hash is
`cad7035d9ebd863f4d75692b08d03413204df13a74ebcb52e4cda1bfb35e6c10`,
and the whole inventory hash is
`a2523def47030dccad31ef8683dd617cfc620e1f05b3fe7f963639ba8eee7c2f`.

For every rule I independently recomputed the source span, normalized source,
normalized hash, and `source_rule_id`. Comparison with
`lemma-discovery.json` was bijective and order-exact:

- reconstructed entries: 55;
- protected-manifest entries: 55;
- duplicate IDs: none;
- omitted or extra IDs: none;
- reordered identities: none;
- span, normalized-source, per-rule hash, and inventory-hash mismatches: none.

The full machine inventory is in `evidence/01-inventory-reconstructed.json`;
the ordered comparison and a rule-by-rule independent rationale are in
`evidence/02-inventory-bijection-and-stage3.txt`.

My independent classification is:

- `DEFINITION`: 40;
- `DOMAIN_LEMMA`: 15;
- `OPERATIONAL_RULE`: 0;
- `PROVED_DERIVED_LEMMA`: 0.

The 40 definitions are genuinely new summaries, proof terms, or structural
recurrences: guarded total projections, numeric views and their complete
comparison table, string-code projection, numeric/string predicates, float
wrapper, and the maximum-fold recurrences.

The 15 domain lemmas are:

- four definedness characterizations for partial Val projections;
- four reverse projection/total-projection correspondences;
- three `applyCmp` comparison-dispatch facts (static Int, dynamic numeric,
  and string);
- the `maxFloat`/`maxFOpaque` symbolic equality;
- three numeric-sort disjointness facts.

These are assumptions about pre-existing operational symbols or sort
relationships, not new-symbol-headed definitions. Stage 1 did not first prove
any exact one in a module omitting it and only later consume it; the Stage 1
spec imports the rules directly. Therefore none qualifies as a
`PROVED_DERIVED_LEMMA`. All are load-bearing for the source program's
heterogeneous Int/Bool/Float/Str comparison paths, partial casts, or maximum
postcondition. None is an irrelevant generic fact. Every rule carrying a
`simplification` attribute is classified as either `DEFINITION` or
`DOMAIN_LEMMA`.

Accordingly the protected Stage 3 classification is accepted.

## Stage 4: deterministic generation and obligation judgment

I reran the exact trusted
`tools.klean_preflight.check_generation` call with `PYTHONPATH=/reference` and
the required Stage 1, Stage 3, and Stage 4 paths. The sandbox hides
`/proc/<pid>/exe`, which initially prevented Lean from identifying its own
executable. I used a source-recorded, hashed preload shim that changes only
numeric `/proc/*/exe` `readlink` requests to `/proc/self/exe`; it does not
alter project files or Lean results. The diagnosis, shim source/hash, and
failed attempts are retained in `evidence/04-preflight-rerun.txt` through
`evidence/06-preflight-rerun-elan-home.txt`.

With that runtime accommodation, preflight performed `lake clean` and
`lake build`, both with exit status 0, and returned:

- status: `PASS`;
- obligation count: 15;
- designated sorry count: 0;
- frozen input:
  `a650785d8c11e43b411856b653cbad0f465f6d09df27702a206b6f8768cad759`;
- generated tree:
  `6eedeca43fb0e6ce143a75bfc6ce3f08755dae826ef9b99b0a1fdaaf9bfe38f2`.

The complete result is `evidence/07-preflight-rerun-with-runtime-shim.txt`.

Independent of preflight, the 15 obligations are in exact inventory order and
have a one-to-one correspondence with the independently found 15 domain
lemmas. The obligation list, obligation map, and input manifest have identical
source-rule sequences; there are no omissions or duplicates. Every recorded
source span, normalized rule, conjunct hash, source binding, input hash,
provenance hash, generated-tree hash, trust-inventory hash, and resolved-input
hash recomputes. All 27 target parameter binding hashes match and refer only
to existing source rules.

Each conjunct states the same guarded operational fact as its frozen K rule.
The definedness translations use `Option.isSome`; guarded rules retain their
guards as hypotheses; equality orientations and argument orders are
preserved. Four printed subexpressions end in `∧ True`, but none is a
standalone tautological obligation: `True` is the value translation of the
well-sorted term inside a `#Ceil` definedness equivalence, whose other side is
an independently falsifiable projection predicate. No obligation is
irrelevant, weakened, or vacuous.

The fixed target is:

- declaration: `Klean35MaxElement.Lemmas.targetStatement`;
- file: `Klean35MaxElement/Lemmas.lean`;
- definition hash:
  `d278bfd415e4e5e8119d008f41e83c5fcbecad9d91a029c7d37edb0574ab8418`;
- statement hash:
  `ac69b69a6eb9f68af8cead6d01b6704e4547ab28f72e9c18b14394004aeba7f1`.

It agrees exactly with the generator manifest, generated source, and audit
input. The source/obligation/target analysis is in
`evidence/08-generated-obligations-and-target.txt` and
`evidence/09-stage4-independent-integrity.txt`.

Stage 4 is therefore accepted. This is not a `KLEAN_NO_OBLIGATIONS` case: the
true domain set has 15 entries.

## Stage 5: clean proof and trust accounting

I created `/tmp/audit-work/stage5-fresh`, copied the immutable generated
project into it as `Base`, and copied only the candidate's outer Lean project
files. The copied Base tree retained the exact generated-tree hash. From that
fresh directory:

- `lake clean`: exit 0;
- `lake build`: exit 0.

Complete output is in `evidence/11-fresh-lake-clean-build.txt`.

The candidate has exactly one definition for every target parameter and does
not redeclare or shadow `Klean35MaxElement.Lemmas.targetStatement`. Its
`Proof.final` statement applies that exact target declaration to the 27
candidate definitions; it is not a copied, weakened, or separately stated
theorem. The candidate introduces no `sorry`, `admit`, `unsafe`, `axiom`, or
`opaque`. Static evidence is in
`evidence/10-candidate-static-inspection.txt`. The trusted final-gate rerun
also passed and confirmed the same target identity; see
`evidence/13-trusted-final-gate-rerun.txt`.

An independent Lean run of `#print axioms Proof.final` returned exactly:

`[propext, Classical.choice, Quot.sound]`

There is no `sorryAx`. These three are the trusted gate's explicit Lean core
baseline; they are not candidate-added declarations. The 57 generated
Klean trust declarations recorded by `trust-inventory.json` are not
dependencies of `Proof.final`, and no unrecorded generated or candidate proof
escape appears. Exact output is in `evidence/12-print-axioms.txt`.

Thus the candidate really does prove the fixed generated theorem, cleanly.
That structural fact is necessary but does not establish the operational
meaning of its parameters.

## Stage 5: operational bridge

I located and compared all 27 exact candidate `def`s with their recorded
`kore_symbol`, source-rule bindings, frozen verification rules, source
solution, and supplied operational K semantics. The full per-parameter
account is `evidence/20-parameter-operational-audit.txt`.

The Bool connectives, Int comparison, sort predicates, string-code
projection, numeric membership/view/comparison table, partial and guarded
total projections, lexicographic string comparison, `maxFOpaque`, and
`maxFloat` agree with their frozen meanings. Tests included wrong-sort and
non-singleton K terms, string prefix/head cases, NaN, infinities, both
signed-zero orders, and an arbitrary-precision Int just above binary64's
exact-integer range. Direct K float witnesses are in
`evidence/14-k-float-max-compile.txt` and
`evidence/15-k-float-max-witnesses.txt`; corresponding Lean witnesses are in
`evidence/18-lean-bridge-witnesses.txt`.

One parameter fails:

`Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»`

Its recorded KORE binding and type represent the full operation

`SortString → SortVal → SortVal → SortBool`.

The candidate implementation begins with `if op == ">"` and returns `false`
for every other operator. The supplied MPY semantics defines dispatch for
other comparisons. Executing that frozen semantics and evaluating the
candidate gives concrete disagreements:

| Input | Supplied K semantics | Candidate Lean |
|---|---:|---:|
| `applyCmp("<", 1, 2)` | `true` | `false` |
| `applyCmp("==", 2, 2)` | `true` | `false` |
| `applyCmp("<", 1.0, 2.0)` | `true` | `false` |

The K test module imports the frozen supplied semantics rather than
reimplementing `applyCmp`; its compile and full `krun` output are in
`evidence/16-k-applycmp-compile.txt` and
`evidence/17-k-applycmp-witnesses.txt`.

The mismatch is not detected by the generated theorem because all three
domain rules involving `applyCmp` specialize the operator to `">"`. As an
adversarial counterfactual, I changed only the candidate's final
`op != ">"` branch from `false` to `true`, retained the same immutable Base
target, ran `lake clean`, and rebuilt successfully. The exact one-line diff
and full successful output are in
`evidence/19-counterfactual-unconstrained-applycmp.txt`.

The HumanEval source uses `">"`, so the candidate happens to implement the
fragment exercised by this theorem. But the fixed target does not ask for a
separately typed `applyCmpGreaterThan`; it binds a candidate definition to the
full operational KORE symbol. Returning a constant for all other operator
inputs is precisely a convenient, hard-coded definition that proves the
generated equations without implementing the frozen operational meaning.
Under the required parameter-by-parameter operational-bridge check, this
single failure makes the Stage 5 proof illegitimate.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
