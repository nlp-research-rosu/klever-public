# Independent audit: 73-smallest-change

## Scope and result

I audited HumanEval `73-smallest-change`, condition `kit-semantics`, semantics
mode `SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and `/audit-input.json` select
`CLASSIFICATION_AND_PROOF`. I treated all mounted candidate, provenance,
comments, logs, and earlier judgments as untrusted evidence and used the
trusted inventory/preflight/gate code under `/reference/tools` for mechanical
checks. My independent mathematical and operational review found no
classification, generation, proof-identity, trust, or bridge defect.

## Stage 4 producer provenance

I hashed the two mounted producer sources before judging generation:

- `klean_export.py`:
  `f1a7004c0ec7b8be2646f9fdedbc9a9975903f9797e34cdf8b3e4ecb1df3ed59`
- `klean.py`:
  `659c1d1c627ff2ca101ab8f9b5a1f1d73968e019e2a305f4ec1d1afa2d8c5a91`

Both values exactly match `source-manifest.json` and
`generator-manifest.json`. The immutable generator image ID is consistently
`sha256:853cc3153c8c3a393e12a3bbc09f51f7f1384695616f4490f55b252c156a3d0e`
in both manifests and in the producer-source path recorded by
`/audit-input.json`. The trusted pipeline tree hash of the mounted producer
bundle is
`3141041ba4f4427b633483489102d026b053f5f382041e7ae1d1041689619478`,
exactly the audit-input value. Evidence is in `01-producer-provenance.txt`,
`02-producer-tree-and-inventory.txt`, and
`02b-producer-contract-tree.txt`. The latter is the applicable trusted
pipeline-contract tree algorithm; the extra `tree_digest` value recorded in
`02` is a different export-tree algorithm and is not the producer-bundle
contract hash.

## Inventory reconstruction and Stage 3 classification

The trusted rule-inventory code reconstructed the local verification closure
as `VERIFICATION` from `verification.k` plus local imported module
`VERIFICATION-BASE` from `verification-base.k`. It found exactly 14 rules.
The frozen file hashes are:

- `verification.k`:
  `7414b97762856abb54b8fd5ac31428ad5b58727d43ddfcf0a166929b692a142f`
- `verification-base.k`:
  `aa8b13916b898accf3356d6d85104980177ce79ddd2a11d11120ccb0a0d051b0`
- whole inventory:
  `3f2d6f96e2fde04bddd98fb0e5cc6357e5f39a29c219ed0264215d821bec45b9`

For every entry I recomputed its exact source span, normalized source hash, and
`source_rule_id`. The resulting 14 identities are unique and match
`lemma-discovery.json` bijectively and in order. There are no missing, extra,
duplicated, reordered, rehashed, or unclassified rules. The complete
reconstructed texts and metadata are in `reconstructed-inventory.json`; the
comparison is in `03-inventory-reconstruction.txt`.

My independent categories are 10 `DEFINITION`, 1 `OPERATIONAL_RULE`, 3
`DOMAIN_LEMMA`, and no `PROVED_DERIVED_LEMMA`:

- `DEFINITION`: the AST macros `smallestLoopBody`, `smallestBody`, and
  `smallestDef`; constructor macro `fixedBuiltins`; both structural `allInts`
  equations; `halfLen`; `pairDiff`; and both guarded `mismatchCount`
  equations. Each defines a fresh macro, summary, or recurrence.
- `OPERATIONAL_RULE`: rule `7d0900f7...`, which performs the ordinary selected
  branch plus fixed `changes += 1` observation/update while preserving the
  continuation and residual scopes. Earlier true/false branch claims are
  separately guarded and are not this exact rule.
- `DOMAIN_LEMMA`: rule `80907d17...`, the complete initialized loop/return to
  mismatch-summary bridge; rule `0a4fd72c...`, definedness of the in-bounds
  integer `!=` comparison; and rule `53698f5d...`, hooked integer-addition
  associativity. All three are material to the frozen loop/postcondition.
  None was first proved as the exact same rule in a module omitting it. In
  particular, the earlier loop claim is more general in `C,I`, carries an
  additional guard, and concludes `C +Int mismatchCount`, so it is not the
  identical installed rule.

All three rules bearing `simplification` are permitted: `halfLen` is a
definition, and comparison definedness and addition associativity are domain
lemmas. The protected Stage 3 categories agree entry-for-entry with this
independent result. A full rule-by-rule rationale is in
`18-independent-classification.md`.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
on the required Stage 1 workspace, discovery manifest, and generated project.
It returned `status: PASS`, `obligation_count: 3`, and independently completed
its `lake clean` and `lake build` checks. The sandbox's PID namespace initially
made Lean's `/proc/<pid>/exe` probe unavailable; `04-stage4-preflight.txt`
retains that environmental failure. I reran with a narrow recorded preload shim
that only redirects that missing probe to `/proc/self/exe`; it does not alter
Lean sources, declarations, or proof results. The successful returned object
and full diagnostics are in `05-stage4-preflight-with-proc-shim.txt` and
`stage4-preflight-returned.json`.

All mounted hashes recorded in `/audit-input.json` match: discovery manifest,
producer sources, K audit, K workspace, Stage 1 export, Stage 4 generation,
generated tree, and Lean candidate workspace. The complete map of all 836
recorded Stage 1 source-file hashes also matches exactly, with no missing,
extra, or changed entry. The separately recorded Lean invocation directory is
not one of the launcher-mounted inputs, so its invocation-container tree hash
cannot be recomputed here; the mounted Lean workspace tree is independently
verified. Details are in `06-hashes-bijection-target.txt`.

The independently found domain IDs are exactly the three obligation source
IDs, in the same order and without duplicates. For each obligation, its source
span, normalized rule hash, source ID, inventory hash, discovery hash, Lean
conjunct, and conjunct hash match. The obligations are mathematically faithful:

1. The exact complete loop configuration rewrites to
   `mismatchCount(VS, 0, halfLen(VS))` under `allInts(VS)`.
2. Under `allInts`, `0 <= I`, and `I < halfLen(VS)`, the supplied integer `!=`
   comparison at the two mirrored in-bounds positions is defined. Its Lean
   form `isSome = true ↔ True` is the faithful translation of `#Ceil(...) =>
   #Top`; the guard is used in the proof, so this is not a vacuous weakening.
3. Integer addition is associative, exactly as used to reconnect the loop
   accumulator with the recursive summary.

There are no irrelevant, omitted, duplicated, weakened, or vacuous
obligations. This is not `KLEAN_NO_OBLIGATIONS`: the true domain set has three
entries and the generated target is required.

The fixed target is
`Klean73SmallestChange.Lemmas.targetStatement` in
`Klean73SmallestChange/Lemmas.lean`. Its definition hash is
`0ab816739b5a6850e624bfc1f61557352c77b4cdf7589c2c6b84a412479fd6dc`
and its instantiated-statement hash is
`84b4d7c6539bd1c9ddfeb8cadfb4b4f9b145e163900436a03d1a74ee0236f055`.
The declaration, exact statement, 16 parameter bindings, source-rule binding
sets, hashes, and generated tree
`99c12aa3f055c058760d5137d3f57bdab3942e6c3d8e729eabc9d90855a6bf22`
agree across the generator manifest, obligation map, preflight return, and
audit input.

## Fresh Stage 5 build and proof identity

I created fresh project `/tmp/audit-work/lean-audit-project.rwO5Kz`, copied the
candidate project into it, and copied the immutable generated project into
`Base`. I then ran both required commands from that fresh root:

- `lake clean`: exit 0 (`09-proof-lake-clean.txt`)
- `lake build`: exit 0 (`10-proof-lake-build.txt`)

Only unused-variable/simp-argument linter warnings appeared. After the build,
`Base` still had the exact immutable generated-tree hash above and `Proof.lean`
still had candidate hash
`e7f5351ffe59d202022024e69cf03aa23e5a7bf64920bdbfe703a67325dac621`.
The trusted candidate gate found exactly one definition for each of the 16
parameters and exactly one `Proof.final`; its normalized theorem statement is
the fixed generated target. The candidate does not declare or shadow
`targetStatement` and contains no `sorry`, `admit`, `unsafe`, new `axiom`, or
new `opaque`. See `13-candidate-structure-target.txt`.

`Proof.final` unfolds the one fixed generated three-conjunct target; it does
not prove a duplicate, weakened, or vacuous theorem. The first conjunct is an
explicit operational reachability derivation of the loop, the second consumes
the integer-list/bounds guard to establish comparison definedness, and the
third proves the exact addition equation.

## Axiom accounting

In the fresh project I ran Lean on `import Proof` followed by
`#print axioms Proof.final`. The exact output is in
`11-proof-print-axioms.txt`. It reports 30 dependencies. Three are Lean's
standard `Classical.choice`, `propext`, and `Quot.sound`. The other 27 are all
present by exact declaration name in `trust-inventory.json`: the recorded
generated hooks/repairs for float, string, power/absolute-value, MD5, sorting,
sequence building, substring counting, and related generated dispatcher
dependencies. `12-axiom-reconciliation.txt` records every name, source file,
line, type, kind, and trust reason.

There is no `sorryAx`, no candidate-created axiom/opaque declaration, and no
unrecorded dependency. Some recorded hooks are outside the integer execution
path but occur because the immutable generated `applyCmp` dispatcher references
all operand domains; this broad generated dependency is visible and fully
accounted for rather than hidden by the candidate.

## Operational bridge

I independently compared every parameter definition with its `kore_symbol`,
bound rule IDs, frozen rules, the source solution, and MPY semantics. The
collection constructors, integer and Boolean hooks, structural integer-list
predicate, length, in-bounds indexing, half-length formula, mirrored
comparison, and fuel-based mismatch recurrence all have their operational
meanings. Map concatenation agrees on the disjoint domain used by the K
configuration; its behavior on overlapping keys is only a total completion of
K's undefined case and is not used by the proof. Likewise, the chosen
out-of-bounds `valSeqAt` value completes an explicitly underspecified total K
function and is excluded by the obligation guard.

I compiled an additional adversarial Lean file against the fresh project. It
checks empty/singleton collections, disjoint nonempty map union, arithmetic and
Boolean cases, integer versus mixed sequences, length/index cases, half-length
at lengths 0/1/2/5, both true and false integer `!=`, and concrete mismatch
counts 1 and 2. These refute identity subtraction, constant predicates,
identity/constant indexing and half-length, constant-empty map union, and
constant-zero or skipped-index mismatch summaries. The source and successful
exit are in `14e-bridge-test-source.txt` and
`14d-bridge-adversarial-lean.txt`; the full bridge judgment is in
`19-operational-bridge-judgment.md`.

VERDICT: PASS
LEGITIMACY: LEGIT
