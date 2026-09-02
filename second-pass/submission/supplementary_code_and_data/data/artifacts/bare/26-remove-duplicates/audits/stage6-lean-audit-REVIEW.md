# Independent Stage 3–5 Audit: `26-remove-duplicates`

## Result

The selected Stage 3 classification and deterministic Stage 4
`KLEAN_NO_OBLIGATIONS` result are legitimate. The independent reconstruction
contains exactly three local verification rules, and all three are genuine
definitions of the postcondition summary. There is therefore no true
`DOMAIN_LEMMA` to export as a Lean obligation. Stage 4 correctly contains zero
obligations and no generated target. The signed audit mode is
`CLASSIFICATION_ONLY`, and `/candidate` is absent, so no Stage 5 proof or
operational-bridge audit applies.

I treated all mounted source, manifests, logs, comments, and earlier verdicts as
untrusted evidence. Trusted code from `/reference/tools` was used for the
canonical rule inventory and the required fresh preflight; the classifications
and semantic judgment below were made independently.

## Audit identity and immutable provenance

`/audit-input.json` is a valid schema-4 signed envelope. Its canonical
resolution digest recomputes to
`122d2ad0e12bdf915bf08371c1361af587e5e7eceebcc8922df225f540130fe1`.
The environment and signed fields agree on:

- problem `26-remove-duplicates`;
- condition `bare`;
- semantics mode `GENERATED_SEMANTICS`; and
- audit mode `CLASSIFICATION_ONLY`.

The generation-time producer source was checked before judging Stage 4:

| Producer | Observed SHA-256 | Manifest SHA-256 |
|---|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` | same |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` | same |

`generator-manifest.json`, `source-manifest.json`, and the image-key component
of the producer path recorded in `/audit-input.json` all identify exactly
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`.
The producer bundle contains exactly those two producer files plus its source
manifest. Its trusted pipeline tree hash recomputes to
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
matching the signed audit input. Producer provenance therefore passes; there is
no producer-source infrastructure error.

All other signed mounted-input hashes also recompute exactly:

| Input | Recomputed hash |
|---|---|
| Stage 1 pipeline tree | `ff6e6d4139746883e23e50bba9499a63e85fa1e851622be9c68a3ea9e87aa3c6` |
| Stage 1 deterministic-export tree | `d295653a03e9a4e6b2547181763983a7353f40effef235efe2383c45354f4a55` |
| selected Stage 2 tree | `7ded8b949f7c97ca98b0152e5fd92cfdea617fd8cb2ec20a9257feb2e997cd43` |
| protected Stage 3 file | `1178339d32221bb51ae9d59cfc34538f39787047e3aea2c6a0abc5c08a85c18e` |
| selected Stage 4 tree | `fc29bbc44b9e25434254496e5dabbaa6f5aa125707413f5653715540ffbcfb08` |
| generated Lean project tree | `66f09be1d836a38d02552531377ce78bb0b58a45bea77bfa06d794f09dc4099d` |

The two Stage 1 tree hashes use two distinct trusted framing algorithms and
each matches its corresponding recorded field. Every individual Stage 1 source
hash, including `verification.k` at
`ba9d7784d074a4f06e303a7679dabdaa44e85c0586ec3d2bbc158d13b20107ee`,
also matches. Generator provenance, input-manifest provenance, the pinned
toolchain object, the signed preflight hashes, and the absence of Lean
workspace/invocation hashes all agree.

Raw evidence: `evidence/01_mode_and_producer_provenance.txt`,
`evidence/03_hash_audit_and_candidate_absence.txt`, and
`evidence/hash_audit.py`.

## Canonical inventory reconstruction

I ran `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference` on `/reference/k-proof`. The trusted lexical closure is
the single local module `VERIFICATION`; imported `MPY` is in the required
`semantic.k`, not another local module in `verification.k`.

The reconstruction contains exactly these three ordered rules:

| Index | Source span | Normalized SHA-256 / `source_rule_id` | Attributes |
|---|---:|---|---|
| 0 | 11–12 | `eead64180cce1cdc54b47266673a3b5fdf72418beb97f8d7bc07df03affe9237` / `rule-eead64180cce1cdc54b47266673a3b5fdf72418beb97f8d7bc07df03affe9237` | none |
| 1 | 13 | `4b2e81eee048157b7718fb38321ccd6a0df2d72177e63dbc46d4d028c48dffff` / `rule-4b2e81eee048157b7718fb38321ccd6a0df2d72177e63dbc46d4d028c48dffff` | none |
| 2 | 14–17 | `21d0f4e4939c7bf24a8212763a583e9e9f1d7cc35fcef917a31103579967b976` / `rule-21d0f4e4939c7bf24a8212763a583e9e9f1d7cc35fcef917a31103579967b976` | none |

For each entry I independently extracted the recorded physical lines,
normalized whitespace, recomputed the normalized source hash, rebuilt
`source_rule_id` as `rule-<hash>`, and compared the extracted text with the
trusted span. The canonical JSON hash of the ordered rule documents recomputes
to
`299595343062f656fea669a80342ae0b598531f47908bc8acbe035e9c4d9af71`.

The ordered Stage 3 identity list is exactly the reconstructed ordered identity
list. Both lists contain three unique IDs. The manifest has no omission,
duplicate, extra rule, reordering, changed hash, or unaccounted entry, and its
whole inventory hash is exact. The trusted Stage 3 boundary validator also
accepts the structural correspondence.

Raw evidence: `evidence/04_inventory_reconstruction.txt` and
`evidence/inventory_audit.py`.

## Independent classification judgment

All three entries are correctly classified `DEFINITION`.

1. Lines 11–12 have the newly declared function symbol `removeRepeated` at the
   left-hand head and define it as `removeRepeatedOnto` with an empty suffix.
   This introduces the public summary; it does not state an independent
   proposition or rewrite an operational configuration.
2. Line 13 has the newly declared function symbol `removeRepeatedOnto` at the
   left-hand head and gives its empty-input base equation. It returns the
   supplied suffix.
3. Lines 14–17 have the same summary symbol at the left-hand head and give its
   structurally descending cons equation. It tests whether the head occurs
   exactly once in `ORIGINAL`, recursively processes the strict tail, and uses
   the semantics’ `ifCons` to prepend the head precisely when the test holds.

For a list `xs`, original list `O`, and suffix `S`, structural induction on
`xs` gives:

`removeRepeatedOnto(xs, O, S) =
filter (fun x => count(x, O) = 1) xs ++ S`.

The base equation is immediate. In the cons case, the frozen `ifCons` rules
either prepend the head or return the recursive tail result, exactly matching
the corresponding filter branch. Consequently,
`removeRepeated(INPUT, INPUT)` is the stable list of elements occurring
exactly once in `INPUT`, which is precisely the frozen Python comprehension.

This reading also matches the operational K semantics:

- the entry environment binds `numbers` to the input list;
- `walkComp` traverses that list and evaluates
  `numbers.count(number) == 1`;
- the generator binding `number` is pushed in front of the captured
  environment, while lookup of `numbers` continues to the original-list
  binding;
- the `count` ground equations count integer equality over the original list;
- `walkComp` processes the tail before `emitComputed`, after which `ifCons`
  prepends the current head, preserving source order; and
- the verification recurrence uses the same `count` observation and the same
  `ifCons` behavior.

Thus these rules name and define the mathematical result used by the
postcondition. They are not ordinary execution/observation rules, domain facts,
or unproved operational bridges. No rule is claimed as
`PROVED_DERIVED_LEMMA`, so the two-stage derived-lemma criterion is not invoked.
No reconstructed rule has a `simplification` attribute, so the simplification
classification restriction is satisfied. Most importantly, no
`DOMAIN_LEMMA` has been disguised as another category: every left-hand side is
headed by one of the two freshly declared summary functions and the equations
give their complete structurally recursive definition.

Finite ground checks covered empty, singleton, repeated-only, mixed,
negative-integer, and order-sensitive inputs, plus nonempty suffixes. They
agreed with an independent executable reading of the source comprehension.
Constant-empty, identity, retain-duplicates, and reverse-output
counterfactuals were all rejected by a concrete witness. These tests support,
but do not replace, the structural induction and operational comparison.

Raw evidence: `evidence/02_frozen_sources_and_semantics.txt`,
`evidence/06_classification_ground_checks.txt`, and
`evidence/classification_examples.py`.

## Deterministic Stage 4 generation

I reran the required call:

`tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json)`.

The first unmodified launcher attempt exposed a sandbox/toolchain integration
issue before generated code was built: Lean 4.22 reads
`/proc/<numeric-current-pid>/exe`, which this sandbox denies, although
`/proc/self/exe` is readable. This caused Lake to report that it could not
detect its installation. The failure and diagnosis are preserved in
`evidence/07_fresh_check_generation.txt`,
`evidence/08_lake_environment_diagnosis.txt`, and
`evidence/09_fresh_check_generation_pinned_path.txt`.

For the successful rerun I used the recorded audit-local compatibility source
`evidence/readlink_self_fix.c`. It interposes only the exact
`/proc/<current-pid>/exe` `readlink` request and redirects it to
`/proc/self/exe`; every other `readlink` is passed unchanged to the real
function. With that narrow environment repair, the pinned tools report Lean
4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and Lake 5.0.0.
The trusted `check_generation` implementation and all mounted inputs remained
unmodified. Its after-run snapshot check also confirmed that Stage 1, Stage 3,
the Stage 4 sidecars, and the generated project did not change.

The fresh returned evidence is:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean` exit 0 with empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build` exit 0 with output SHA-256
  `a143f1e5258e8806222e00a1b9de78e917235e80fa9c21aff4b230d46cddd9f7`;
- generated tree
  `66f09be1d836a38d02552531377ce78bb0b58a45bea77bfa06d794f09dc4099d`;
- zero obligations;
- zero designated sorries;
- 41 allowlisted generated translation-library trust declarations; and
- target `null`.

The entire fresh result is exactly equal to both
`/reference/klean-generation/preflight.json` and the signed
`resolution.stage4_preflight` object in `/audit-input.json`.

Raw evidence: `evidence/10_lean_sandbox_compatibility_shim.txt`,
`evidence/11_fresh_check_generation_success.txt`, and
`evidence/14_preflight_exact_comparison.txt`.

## Obligation bijection and target identity

My independent classification yields the exact true domain set `[]`.
`input-manifest.json` carries all three reconstructed entries in `definitions`
and has empty `operational_rules`, `proved_derived_lemmas`, and `source_rules`.
The generated `obligation-map.json` is exactly:

- `source_rules: []`;
- `obligations: []`; and
- `trust_parameters: []`.

Its byte hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching `generator-manifest.json`. The source-ID and obligation-ID sequences
are therefore an exact empty bijection with no omissions, duplicates, or extra
entries. Since there are no obligations, there are no irrelevant, weakened, or
vacuous conjuncts.

The trusted target parser returns `None`, the expected target definition is
`None`, and an independent raw scan finds zero `def targetStatement`
declarations. The generator manifest, recorded preflight, fresh preflight, and
signed audit input all record target `null` and obligation count zero. There
has been no target change.

This is a genuinely empty domain set, not a self-consistent omission.
`KLEAN_NO_OBLIGATIONS` is therefore the correct Stage 4 result. The 41
allowlisted declarations belong to the generated translation library; there
is no generated proposition or Stage 5 theorem whose proof could depend on
them.

Raw evidence: `evidence/12_stage4_generated_inspection.txt`,
`evidence/13_stage4_structural_audit.txt`, and
`evidence/stage4_structural_audit.py`.

## Stage 5 applicability

Stage 5 is not selected. `AUDIT_MODE` and the signed resolution are both
`CLASSIFICATION_ONLY`; the generated target is absent; the true domain set is
empty; the audit input records null Lean workspace and invocation paths and
hashes; and `/candidate` does not exist. Creating `Base`, running a candidate
clean build, printing `#print axioms Proof.final`, auditing
`target.parameters`, or checking an operational bridge would invent a proof
candidate where the protocol requires none, so those proof-mode procedures
are correctly inapplicable.

## Final judgment

The inventory is complete and bijective, every Stage 3 category matches the
frozen rule’s actual semantic role, the mathematical summary matches the
frozen source and K execution, producer and input provenance are intact, the
fresh trusted preflight passes, and the empty Stage 4 mapping and null target
are exact. There are no substantive concerns.

VERDICT: PASS
LEGITIMACY: LEGIT
