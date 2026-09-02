# Independent audit: `95-check-dict-case`

## Result

I audited `kit-semantics` in `SUPPLIED_SEMANTICS` mode with launcher mode
`CLASSIFICATION_AND_PROOF`. I find the Stage 3 classification complete and correct,
the Stage 4 generation deterministic and obligation-preserving, and the Stage 5 proof
an exact, axiom-accounted proof of the fixed generated target. The candidate's eight
operational definitions implement the frozen meaning on the complete domain of the
two obligations; they are not constant, identity, hard-coded, or vacuous bridges.

The raw command index is
[evidence/COMMANDS.md](/audit-output/evidence/COMMANDS.md). All cited command outputs
are beneath `/audit-output/evidence/`.

## Producer provenance and frozen inputs

I performed the required producer check before judging Stage 4. The actual hashes are:

- `klean_export.py`:
  `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`
- `klean.py`:
  `b5168e18e064b737f09d9332335eb76e78f7ac5c4a73a60c345649cad2cdd26f`

Each equals the corresponding hash in both `generator-manifest.json` and the source
manifest. The immutable image identifier is
`sha256:cef3bf63d3f1a1df5e8c5e6c788f60cc26b0b64aa857f73d907d65c64147c345`;
it agrees between the two manifests and the image-qualified producer-source path in
`/audit-input.json`. The producer-source tree hash
`807266be9d75e18d2fb9e05eaff407609e69e5affe9fd144822293c310d1d111`
also matches the launcher record. There is therefore no producer-provenance
`AUDIT_ERROR`. See
[producer summary](/audit-output/evidence/02-producer-provenance-summary.txt).

I also independently recomputed all launcher tree/file hashes. The K workspace, K
audit, generation, producer sources, Lean candidate, and discovery hashes all equal
their `/audit-input.json` values. The launcher `resolved_input_sha256` recomputes to
`1fc03a024b22eee2de45bd35829df68b1bf4061c1fd8ed53f1013e51f1402724`.
All 825 recorded Stage 1 paths are present, with no extra path and no content-hash
mismatch. See [launcher hashes](/audit-output/evidence/34-launcher-tree-hash-verification.txt)
and [resolved inputs](/audit-output/evidence/36-audit-binding-and-source-hashes.txt).

## Stage 3 inventory reconstruction

Using the trusted `tools.k_rule_inventory.inventory_verification` code, I reconstructed
the local verification-module closure from the frozen `verification.k`. The closure is
the `VERIFICATION` module and contains exactly six rules in source order. The
verification source hash is
`cd3a6bdc6c1985b56fdff715b06106a6a7dddcaf3e5f7725de86b1e9f517c152`;
the whole inventory hash is
`da6d570ca5aad66979a01df14308854813e040e7b91e7662cc90b7713d10cb67`.

For every rule, the trusted reconstruction reproduced the start/end lines, normalized
source text, normalized SHA-256, attributes, and `source_rule_id` (the latter is
`rule-` followed by the normalized hash). The protected classification has six unique
identities in the same order and the same inventory hash. There are no omissions,
duplicates, extras, reordered identities, or unaccounted entries. The complete texts
and hashes are in the [reconstructed inventory](/audit-output/evidence/05-reconstructed-inventory.json.txt),
and the bijection is in [inventory comparison](/audit-output/evidence/07-inventory-bijection.txt).

My independent classifications are:

| Source span / rule identity | Classification | Independent reason |
|---|---|---|
| lines 9–30, `rule-81fe…2549` | `DEFINITION` | Exact expansion of the named, total `checkDictLoopBody()` AST proof term. |
| lines 33–37, `rule-1162…8b5` | `DEFINITION` | Exact expansion of the named, total `checkDictReturn()` AST proof term. |
| lines 40–50, `rule-08f1…44f7` | `DEFINITION` | Exact named `checkDictBody()` composition of initialization, loop body, and return AST. |
| lines 54–57, `rule-abdb…38b5c` | `DOMAIN_LEMMA` | Adds a guarded symbolic `applyMethod(...,"islower",.Vals)` simplification for an existing operation. Stage 1 did not first prove this exact guarded rewrite. |
| lines 58–61, `rule-fd44…0a0b8c` | `DOMAIN_LEMMA` | The corresponding guarded symbolic `isupper` simplification; likewise not first proved as this exact rewrite. |
| lines 66–71, `rule-3c57…c962` | `PROVED_DERIVED_LEMMA` | The exact non-reference `isinstance(_,str)` `#applyK` transition, including arbitrary continuation, is first proved against `CONNECTION`, which excludes `VERIFICATION`, and is only then used by later proofs. |

The two `[simplification]` rules are thus both `DOMAIN_LEMMA`, satisfying the required
classification constraint. They are load-bearing and relevant: the frozen source loop
calls `key.islower()` and `key.isupper()`, and the postcondition distinguishes the case
where all nonempty dictionary keys are uniformly lowercase or uniformly uppercase.
Neither can be reclassified as a definition, an ordinary execution rule, or a derived
rule merely because the concrete string-method semantics exists at constructor level.

For the derived rule, `CONNECTION-SPEC.isinstance` has the same call, result, guard, and
arbitrary continuation as the verification rule. `CONNECTION` imports
`PROOF-THEORY`, not `VERIFICATION`; `prove.sh` runs this proof before the loop and target
proofs. I independently reran that exact claim and obtained `#Top` with exit 0. See
[frozen source/proof order](/audit-output/evidence/08-frozen-proof-and-program.txt) and
[independent predecessor proof](/audit-output/evidence/53-derived-lemma-kprove.txt).

## Stage 4 generation and mathematical obligation identity

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
three required paths. It returned `status: PASS`, two obligations, zero designated
sorries, the expected frozen Stage 1 and Stage 3 hashes, generated-tree hash
`ab697d8866e1f80101de0ccaa8a6fda46c25a2468ba9b33f25ea31bfd67140c3`,
and the fixed target. Its full returned evidence is
[preflight result](/audit-output/evidence/29-preflight-rerun-success.txt).

Independent comparison establishes an ordered bijection among:

1. the independently identified domain-rule set;
2. the Stage 4 input manifest's source-rule list;
3. `obligation-map.json` source identities; and
4. the two generated conjuncts.

For each obligation, the source span, normalized source hash, inventory hash, discovery
hash, and conjunct hash all match. The obligation-map hash is
`40a8c701eee7ae7730a09468f5d21c1ebe1fae1e04cd54ffe4ba52ab3d0ddb79`,
the two conjuncts are distinct, and there are no missing or duplicated rules. See
[obligation bijection](/audit-output/evidence/37-obligation-bijection.txt).

Mathematically, the conjuncts preserve the K rules exactly. For every `V` satisfying
`isStringKey(V) andBool notBool isRefV(V) = true`, they state respectively:

```text
applyMethod(V, "islower", .Vals) = injBool(lowerKeyCodes(stringCodes(V)))
applyMethod(V, "isupper", .Vals) = injBool(upperKeyCodes(stringCodes(V)))
```

The receiver, empty argument list, exact method names, guard, Bool injection, and
right-hand summary functions are unchanged. The guard is satisfiable by concrete
non-reference string values (for example `"a"` and `"A"`), so neither conjunct is
vacuous. These facts are necessary to connect the frozen source's two method calls to
the loop summary and postcondition. Thus the domain set is genuinely nonempty, and the
selected generated proof target—not `KLEAN_NO_OBLIGATIONS`—is required and correct.

The fixed declaration is `Klean95CheckDictCase.Lemmas.targetStatement`. Its extracted
definition hash is
`d09d5b0be50ff5667570dd7a99f5d11e8e0638300ca0b6ac88bb1499108646b0`,
and its fully applied statement hash is
`2e9b768e4bd8906c2431172b343da5b25d23f0885a1a59d702414c218ded046b`.
Both independently recompute from `Lemmas.lean` and equal the generator manifest and
audit input. See [target recomputation](/audit-output/evidence/32-independent-hash-and-target-recomputation.txt).

## Stage 5 clean build, proof identity, and policy scan

I created `/tmp/audit-work/lean-proof-audit.Y1Auq5`, copied the generated project into
it as `Base`, and then copied only the candidate proof project around that base. Before
building, the fresh `Base` export hash was exactly the generator hash
`ab697d…40c3`; the separate pipeline hashes also matched. See
[fresh assembly](/audit-output/evidence/44-fresh-project-assembly.txt).

In that fresh directory, both required commands succeeded:

- `lake clean`: exit 0; complete output in
  [45-fresh-lake-clean.txt](/audit-output/evidence/45-fresh-lake-clean.txt).
- `lake build`: exit 0, `Build completed successfully`; complete output in
  [46-fresh-lake-build.txt](/audit-output/evidence/46-fresh-lake-build.txt).

The trusted `stage5_mechanical_check.py` independently made another fresh base, cleaned,
built, and axiom-checked it, returning `status: PASS`; see
[trusted Stage 5 check](/audit-output/evidence/52-trusted-stage5-mechanical-check.txt).

The candidate contains exactly one definition for each of the eight target parameters.
It neither declares nor shadows `targetStatement`; its sole target reference is the
type of `Proof.final`. A token/declaration scan finds no `sorry`, `admit`, `unsafe`, new
`axiom`, or new `opaque`. The fresh base still has the exact generator target hash and
statement. See [target and policy scan](/audit-output/evidence/50-target-identity-and-candidate-policy.txt).

`#print Proof.final` displays exactly the fully applied fixed generated statement, not
a duplicate or variant. `#print axioms Proof.final` reports exactly:

```text
'Proof.final' depends on axioms: [propext, Quot.sound]
```

The generated `trust-inventory.json` contains 41 explicit List/Map/Set hook axioms and
no designated sorries; none of those custom axioms is a dependency of `Proof.final`.
The trusted final gate's recorded Lean-kernel baseline explicitly permits
`Classical.choice`, `propext`, and `Quot.sound`, so both reported dependencies are
accounted for by the baseline and are not unrecorded trust escapes. `sorryAx` is absent.
See [exact axiom output](/audit-output/evidence/48-print-axioms-proof-final-success.txt)
and [trust reconciliation](/audit-output/evidence/49-trust-inventory-axiom-reconciliation.txt).

## Operational bridge audit

I compared every `target.parameters` definition to its bound KORE symbol, both bound
source-rule IDs where applicable, the corresponding frozen K/KORE rules, the source
solution, and operational semantics. The load-bearing meanings are:

| Target parameter | Candidate definition and independent judgment |
|---|---|
| `_andBool_` | Lean Boolean conjunction, matching K `andBool`; all four truth-table cases checked. |
| `applyMethod` | Projects direct or transitive string injections and dispatches exact zero-argument `islower`/`isupper` branches to the frozen `hasLower ∧ ¬hasUpper` / `hasUpper ∧ ¬hasLower` meanings. |
| `isRefV` | True exactly for the frozen `ref(_)` constructor; false for strings and integers. |
| `isStringKey` | True exactly for direct string values and the raw transitive Str-to-Iterable-to-Val representation; false for int/ref values. Generated injection rules canonicalize the transitive representation consistently. |
| `lowerKeyCodes` | `hasLowerCode(codes) && !hasUpperCode(codes)`, matching the proof-theory recurrence and method rule. |
| `notBool_` | Boolean negation, matching K `notBool`. |
| `stringCodes` | Returns the exact code sequence for both generated representations of `str(CS)`, matching `stringCodes(str(CS)) => CS`. |
| `upperKeyCodes` | `hasUpperCode(codes) && !hasLowerCode(codes)`, matching the proof-theory recurrence and method rule. |

The character predicates use the frozen ASCII ranges `65..90` and `97..122`. I ran
audit-only executable tests over empty sequences, digits, mixed case, the four range
boundaries and adjacent nonletters, direct and transitive string injections, int/ref
values, incorrect method arity, and an unknown method. Every expected operational test
evaluated `true`. I also mutated each kind of parameter to a convenient left projection,
identity, constant Boolean, constant empty code sequence, constant method result, or
receiver-returning method. Concrete lowercase, uppercase, ref, int, and Boolean
witnesses rejected every mutation. Full results are in
[operational adversarial tests](/audit-output/evidence/54-operational-adversarial-tests.txt).

`stringCodes` and `applyMethod` choose fixed total values where the frozen K source has
no applicable equation. Those choices are outside the generated obligations: the
guard restricts `V` to a non-reference string and both conjuncts fix the exact method
name and empty arguments. On every guarded value the candidate uses the genuine code
sequence and exact frozen method result. The off-rule totalizations therefore neither
make the proof vacuous nor substitute a convenient meaning on the theorem's domain.

## Environment note

The initial Lean invocation exposed a container PID-namespace defect: Lean could read
`/proc/self/exe`, but its equivalent `/proc/<pid>/exe` lookup returned `ENOENT` or
`EACCES`, causing Lake installation detection to fail before reading any project. I
diagnosed the exact failing `readlink` and used a narrow compatibility preload which
only retries a failed numeric `/proc/.../exe` read as `/proc/self/exe`. Its exact source
is [55-proc-self-exe-compatibility.c](/audit-output/evidence/55-proc-self-exe-compatibility.c).
It does not intercept file reads, generated artifacts, theorem elaboration, or hashes.

With the immutable locked paths selected, the trusted gate reports K 7.1.293,
pyk/Klean 7.1.293, Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, Lake 5.0.0, and Codex 0.144.6.
The diagnosis and gate result are in
[toolchain evidence](/audit-output/evidence/28-toolchain-gate-with-proc-fix.txt).
This compatibility action resolved an invocation-path defect without changing any
candidate, provenance, generator, or trusted-tool input.

VERDICT: PASS
LEGITIMACY: LEGIT
