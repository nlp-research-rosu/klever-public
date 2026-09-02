# Independent audit: `10-make-palindrome`

## Scope and outcome

I audited condition `kit-semantics` in `SUPPLIED_SEMANTICS` mode. Both
`AUDIT_MODE` and the canonically bound `/audit-input.json` resolution say
`CLASSIFICATION_ONLY`. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`; there is no Stage 5 workspace, invocation, result, or
`/candidate`.

I treated the mounted K, discovery, generation, prior-review, and log content
only as evidence. Rule reconstruction and structural checking used the trusted
code under `/reference/tools`; mathematical classification was redone from
`verification.k`, the source program, and the supplied operational semantics.

The classification is correct, the independently reconstructed domain-lemma
set is genuinely empty, and deterministic Stage 4 has the required empty
obligation map and no generated target.

## Generator-producer provenance

I performed this check before judging Stage 4.

- `/reference/generation-tools/klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `/reference/generation-tools/klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`
- Producer bundle:
  `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`
- Immutable generator image:
  `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`

The two file hashes agree exactly with `source-manifest.json` and the
`exporter_sha256`/`klean_py_sha256` fields in `generator-manifest.json`. The
image ID agrees between those two manifests and the basename of the protected
producer-source path recorded in `/audit-input.json`. The producer bundle has
exactly the two source files and its source manifest—no extra or linked files.
There is therefore no producer-source infrastructure error.

The generation-time exporter's relevant logic selects exactly validated
`DOMAIN_LEMMA` entries, checks their ordered bijection with generated
obligations, and returns no `targetStatement` when that list is empty. I
inspected but did not execute the archived producer source.

## Inventory reconstruction and bijection

The trusted inventory reconstructed the local closure
`VERIFICATION-SYNTAX`, `VERIFICATION` selected by `prove.sh`.

- `verification.k` SHA-256:
  `8d2a28ac8064959eaa0f6389d33177dd7d50e294f62a023066aa7c58bcf74ed0`
- Reconstructed rules: 16
- Inventory SHA-256:
  `55a78cf76899cbb801e44ed21e4217bf95f2ef58a9da1f097435c4d394fafc3e`

For every rule, the trusted code recomputed the physical start/end lines,
whitespace-normalized source hash, and
`source_rule_id = "rule-" + normalized_sha256`. The protected Stage 3 manifest
contains exactly those 16 unique IDs in the reconstructed source order. Its
whole-inventory hash agrees. There are no omissions, duplicates, extras,
reordered identities, changed hashes, or unaccounted classifications.

None of the 16 rules has a `simplification` attribute, so the special
`simplification => DEFINITION or DOMAIN_LEMMA` constraint is satisfied
vacuously.

## Independent classification

I independently classify all 16 entries as `DEFINITION`.

| Frozen spans | Entries | Judgment |
|---|---|---|
| 29–107 | `isPalindromeBody`, `reverseLoopBody`, `searchLoopBody`, `makePalindromeBody`, both closure values, and `solutionModule` | Seven exact macro/named-term definitions of the source AST and closure/module values. They expand to the frozen program and leave ordinary MPY execution in control. |
| 109–114 | Two `reverseAcc` equations and `palIS` | Structurally decreasing reverse-with-accumulator recurrence and a named Boolean summary. |
| 116–120 | Two guarded `seedResult` equations | Complementary branches defining the initial result summary. |
| 122–148 | Three `searchResult` equations | Two consistent base cases and a structurally decreasing recurrence that mirrors one remaining search-loop iteration. |
| 150–158 | `completePal` | Initialization/composition of the preceding execution summaries. |

The supplied semantics supports this reading:

- `#loadAll` and `FuncDef` build the exact closures;
- calls bind parameters and execute the body in a normal frame;
- string iteration uses `#iterNext` and `#loop`, yielding characters in source
  order;
- assignments update the active scope;
- string `+` is `seqConcat`; and
- string equality is equality of the underlying `IntSeq`.

Consequently, `reverseAcc(R,A)` is `reverse(R) ++ A`; the first loop computes
`reverseAcc(S,.IntSeq)`. `palIS` and `seedResult` match the two initial
assignments. `searchResult` carries precisely
`(S, remaining, prefix, reverse_prefix, reverse_string, found, result)`,
updates both prefixes, tests the same equality as the source, returns the
candidate when found, and otherwise recurs on the strict tail. Its `found =
true` and empty-remaining base-case overlap has the same right-hand side.
`completePal` supplies the exact initial tuple.

These summary symbols occur in claim results and symbolic post-state values;
they do not match or preempt source-program `<k>` redexes. The AST macro rules
expand to the exact frozen statements rather than shortcutting their
execution. There are therefore no local `OPERATIONAL_RULE` entries.

There is no `PROVED_DERIVED_LEMMA`: no inventoried rule is first proved in a
module omitting that rule and then installed for a later proof. The loop
reachability claims in `spec.k` are claims, not rules in this inventory.

There is no `DOMAIN_LEMMA`. In particular:

- `palIS` defines a predicate; it does not assert a theorem about output.
- `completePal` defines an initialized recursive summary; its name does not
  assert that the value is a palindrome or shortest.
- No inventoried rule states that the result begins with the input, is
  palindromic, or is minimal.

Thus no domain lemma has been hidden as a definition, operational rule, or
derived lemma. Conversely, there is no irrelevant claimed domain lemma.

As finite sensitivity evidence, an independent direct implementation of the K
recurrences matched the frozen source and an independently constructed
shortest-palindrome oracle on all 3,280 sequences over `{0,1,2}` of lengths
zero through seven. An identity-reverse mutation and an inverted search test
each produced 3,120 mismatches. This supports the line-by-line semantic
analysis but is not used as a substitute for it.

## Hash and manifest integrity

I independently recomputed every launcher-recorded hash available from the
mounted inputs:

- Stage 1 pipeline tree:
  `e60f332bcff5f953c78148347a9b477106a52750065af85c3e0e38ada8367883`
- Stage 1 export tree:
  `e3e6dd0e20e31b00b5b7de824b4008f3af538bc7999bc013059531826b255977`
- Stage 2 selected audit tree:
  `cc42ed387fa1152101b1e6319c28a26b15dd604ee702a2661c79b6e52d7a08ce`
- Stage 3 manifest:
  `03f737fca7e2487ba0a53efa41ad6c7e454b1a1d8a2bd8cd09e21ac68212ae6d`
- Stage 4 generation tree:
  `7bb4149bf6b5e46725fb79ab9b72391614b603ed85001012578e5b97e922253d`
- Generated project:
  `6583d2f41be7b39b1b7523f838c07be8d0d3c2db47984c8f6898882aa6e935f9`
- Producer bundle:
  `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`

All match `/audit-input.json`. Its canonical resolved-input digest also
recomputes exactly. All 789 individual Stage 1 file hashes match the protected
map with no missing or extra regular files. Selection artifact hashes agree
with their corresponding tree hashes.

The Stage 4 input manifest exactly reproduces the classified inventory:
16 definitions and empty operational, proved-derived, and domain lists. Its
verification, inventory, Stage 1, and Stage 3 hashes all match the independent
values. Generator provenance, pinned toolchain lock, generated tree, obligation
map hash, export result, trust-inventory hash, and launcher-copied preflight
record also agree exactly.

## Obligation bijection and fixed target

The independently reconstructed domain list is empty. The generated
`obligation-map.json` has:

- `source_rules: []`
- `obligations: []`
- `trust_parameters: []`

This is an exact empty-set bijection, with no omissions, duplicates, irrelevant
obligations, weakened formulas, or vacuous conjuncts. The generator manifest
and export result both record an obligation count of zero and status
`KLEAN_NO_OBLIGATIONS`.

The target identity is consistently null in the generator manifest, Stage 4
preflight record, and `/audit-input.json`. An independent scan of every
generated Lean source finds no `targetStatement` declaration or reference.
There is therefore no target statement/hash that could have been changed,
weakened, duplicated, or made vacuous.

## Fresh mechanical preflight

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and the required three protected inputs plus
`/reference/klean-toolchain.lock.json`.

The container initially denied Lean/Lake's self-executable
`/proc/<pid>/exe` lookup, causing toolchain startup failures before
elaboration. I preserved both failures. I then used a narrow audit-local
`LD_PRELOAD` shim that answers only that self lookup with the kernel-provided
`AT_EXECFN`; every other `readlink` remains a direct syscall. The shim does not
alter the generated project or Lean semantics. With it, the pinned executables
identify as Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and matching Lake 5.0.0.

The fresh trusted check returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count 0;
- target `null`;
- trust declaration count 42;
- designated sorry count 0;
- `lake clean` exit 0 with empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
  and
- `lake build` exit 0 with output SHA-256
  `6d23a9e53a44ab97465b081069c610af5da06eeb21dbe5a6e07cc6c1770c66f3`.

Those diagnostics exactly match the launcher-bound Stage 4 preflight record.
Post-check hashes confirm that all protected inputs remained unchanged.

## Stage 5 applicability

Stage 5 proof auditing is not applicable. The audit mode is
`CLASSIFICATION_ONLY`, the legitimate domain set is empty, the generated
target is absent, `/candidate` is absent, and all Stage 5 path/hash/result
fields are null. Running `#print axioms Proof.final` or checking candidate
parameter bridges would require a theorem and candidate that correctly do not
exist.

## Evidence

Raw commands, transcripts, scripts, and results are under
[`evidence/`](/audit-output/evidence/). The principal records are:

- [producer and Stage 4 manifests](/audit-output/evidence/01_producer_and_stage4_manifests.txt)
- [reconstructed inventory and bijection](/audit-output/evidence/02_reconstructed_inventory_and_bijection.txt)
- [frozen source, spec, and verification](/audit-output/evidence/03_frozen_source_spec_and_verification.txt)
- [relevant supplied operational semantics](/audit-output/evidence/04_relevant_operational_semantics.txt)
- [fresh successful preflight](/audit-output/evidence/06c_fresh_check_generation_success.txt)
- [preflight environment workaround](/audit-output/evidence/06d_shim_reproduction.txt)
- [independent integrity checker result](/audit-output/evidence/08_independent_integrity_check.out)
- [adversarial summary check](/audit-output/evidence/09_summary_differential.out)
- [full independent classification rationale](/audit-output/evidence/10_independent_classification.md)
- [generation-time target/obligation logic](/audit-output/evidence/11_generation_time_exporter_logic.txt)

VERDICT: PASS
LEGITIMACY: LEGIT
