# Independent audit: HumanEval 86-anti-shuffle

## Scope and outcome

This audit covers condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and launcher mode `CLASSIFICATION_ONLY`.  I treated the
candidate and provenance mounts only as evidence.  I did not rely on the prior
Stage 2 review, protected Stage 3 rationale, prior preflight verdict, or Stage 1
comments as authority.

The selected generation is structurally self-consistent and reproducible, but
it is not legitimate.  Stage 3 mislabeled one relevant domain lemma as a
definition.  The independently correct domain set contains that rule, while
Stage 4 generated zero obligations and no target.  The audit prompt explicitly
requires `FAIL`/`NOT_LEGIT` for a nonempty true domain set behind a
`KLEAN_NO_OBLIGATIONS` result.

## Mode and immutable-input checks

`AUDIT_MODE` and `/audit-input.json` both report `CLASSIFICATION_ONLY`.
`/candidate` is absent, both Lean workspace/invocation hashes are null, and the
launcher-recorded Stage 4 selection is `KLEAN_NO_OBLIGATIONS`.  This is the
structurally expected layout for the recorded mode.

I recomputed every launcher tree/file binding relevant to this audit with the
trusted hash implementations:

| Binding | Recomputed value | Result |
|---|---|---|
| Stage 1 workspace tree | `2b2b691113800e4fb1458e1fb3dbb568eb0bc827d363bbb69887b9acf215eb7a` | matches |
| Stage 1 export tree | `30ee607e4db2c763d3a61fbd783e6d1d4e23c5f2e1d49916ea0f428d024add1d` | matches |
| selected Stage 2 tree | `68a873defed5891c0a4f4636e5c5d130047a585391d7952abaa44401743174bd` | matches |
| Stage 3 manifest | `f9beba61b82ac748b1a73e5cfdddddd1e187a043aa7b8538d3b585540f0b3ccf` | matches |
| Stage 4 generation tree | `ba8a2461e9655687f3b81946460f43a08671ea4155f888f2be478c3c66f16d76` | matches |
| generated project tree | `1674b1db22fed880156b73d95f892508ff3681d5cb4484d12dab1fe1e5bbe61e` | matches |
| producer-source tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` | matches |

All 794 launcher-recorded Stage 1 per-file hashes matched bijectively: no
missing files, extra files, or content mismatches.  The full comparison is in
`evidence/38_hash_and_structure_verification.txt`.

## Stage 4 producer authentication

I authenticated the producer sources before judging Stage 4:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both hashes exactly match `/reference/generation-tools/source-manifest.json`
and the corresponding `exporter_sha256`/`klean_py_sha256` fields in
`generator-manifest.json`.  The generator image ID is identically
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in the source manifest, generator provenance, and the launcher-recorded
producer-source path.  The producer-source tree hash also matches the audit
input.  There is no producer-provenance `AUDIT_ERROR`.

## Canonical inventory reconstruction

I ran `tools.k_rule_inventory.inventory_verification` from the trusted
`/reference/tools` code over the frozen `/reference/k-proof` workspace.  The
selected main module is `VERIFICATION`; its local in-file module closure is
exactly `[VERIFICATION]`.  The reconstruction produced:

- `verification.k` SHA-256
  `303963e3703c0a00059f7bd9841056f40f76498247bcbb568700c3de2399ead2`;
- nine unique rules in source order; and
- inventory SHA-256
  `b6a5c8a6de1f4db5b68d5cc26578cacf31fb03dfb7b59d122c3544c81b30760c`.

The protected Stage 3 manifest has exactly the same nine ordered
`source_rule_id` values and the same inventory hash.  Because each ID embeds
the independently recomputed normalized-source hash and the inventory hash
commits the complete rule documents, the comparison accounts for every source
span, normalized hash, module, attributes list, and rule text.  There are no
omissions, extras, duplicates, or reordered identities.  The full reconstructed
documents and all bijection booleans are in
`evidence/09_reconstructed_inventory.txt`.

## Independent Stage 3 classification

My independent classification is:

| Source span | Source rule ID | Correct class |
|---:|---|---|
| 8–12 | `rule-8035a5d5e2dd908c685b0f3f6b47722aade54582ecf7e781dfd68bc1469d72b1` | `DOMAIN_LEMMA` |
| 21–33 | `rule-dc6f73badfec4f23e1af1f381ddb673851960f3a7dd453b5a529e29eea13dbc1` | `DEFINITION` |
| 35–43 | `rule-d8c6975c42f7acfdc026a371bbd271bff09144d250d960f6b474f010e3a77c91` | `DEFINITION` |
| 45–56 | `rule-0f9f3b5d7e5349a6b9e4e08ae6ff00e9b64d8642453a18a90ada8eea2bfa6d08` | `DEFINITION` |
| 58–61 | `rule-5075fc023e8cdbd37d170a98412b835adec6946ebd2141dee39edbea6eb0d8ad` | `DEFINITION` |
| 68–72 | `rule-c4913eca7f7a04a7ced779f502220f126d5ee7b0ee403b488e8b7e5329129ccb` | `DEFINITION` |
| 73–91 | `rule-f0184627a2c4a3d544b5b84141379073793a96b835d2753217df57bda16c9883` | `DEFINITION` |
| 95–96 | `rule-652e6e29910efceeca6a31b0b63ec16bfe1d38ac2b9054d6d2a69a37ba8dcec4` | `DEFINITION` |
| 97–107 | `rule-6e83d7b52d40fb31d78ba87b9b7e825cf4ae9515a0fa193cce3b0b083ee08657` | `DEFINITION` |

The four `anti*Body`/`antiTail` rules are sole equations for fresh,
zero-argument named AST macros.  The two `insertGo` rules are the base and
constructor recurrences of a fresh insertion-loop summary and consume the old
word structurally.  The two `antiGo` rules are the base and constructor
recurrences of a fresh outer-loop summary and consume the remaining input
structurally.  Their branches match the frozen program's insertion, space, and
non-space behavior.  They satisfy the required meaning of `DEFINITION`.

The singleton `strLt` simplification at lines 8–12 does not.  `strLt` is
declared and operationally defined before `verification.k`, in the supplied
`semantics/str.k` at lines 48–54.  Those rules say:

- singleton codes with `C <Int D` compare `true`;
- singleton codes with `C >Int D` compare `false`; and
- equal heads recurse to empty/empty, which compares `false`.

Consequently the added equation
`strLt(iCons(C,.IntSeq), iCons(D,.IntSeq)) => C <Int D` is a true compressed
fact about an existing domain operation.  It does not introduce or define a
summary, recurrence, macro, or named proof term.  Since it has the
`[simplification]` attribute, the audit policy permits only `DEFINITION` or
`DOMAIN_LEMMA`; its correct class is `DOMAIN_LEMMA`.

The lemma is material, not irrelevant.  String iteration emits singleton
strings for `char` and `old_char`; source line 17 performs `char < old_char`;
the supplied comparison rule routes that expression through `strLt`; and the
`insertGo` summary uses the corresponding `C <Int OLD` branch.  The rule
therefore directly connects operational source execution to the Stage 1
summary/postcondition.

`lemma-spec.k` contains three guarded reachability claims for less, greater,
and equal cases.  I reran those claims against `MPY` without `VERIFICATION`;
`kprove` exited 0 and printed `#Top`.  This confirms the domain fact's truth,
but it does not change its required category.  The Stage 1 artifact did not
first prove the exact same unguarded simplification rule and then use that
exact rule.  It therefore does not satisfy the prompt's strict
`PROVED_DERIVED_LEMMA` exception.  The protected rationale's assertion that
the simplification constraint “places it under DEFINITION” reverses the
classification rule: the constraint allows a relevant domain lemma and does
not turn an equation over an existing semantic symbol into a definition.

The independently correct domain set is therefore the singleton:

```text
rule-8035a5d5e2dd908c685b0f3f6b47722aade54582ecf7e781dfd68bc1469d72b1
```

## Deterministic Stage 4 generation

After authenticating the producer sources, I reran the required
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
specified Stage 1 workspace, Stage 3 manifest, Stage 4 generation, and pinned
toolchain lock.

The first run exposed an audit-container PID/procfs mismatch: Lean 4.22 uses
`/proc/<getpid()>/exe`, while this sandbox reports a namespace PID from
`getpid()` but mounts host `/proc`.  I preserved that failure and the namespace
diagnostics.  I then used a local `LD_PRELOAD` compatibility shim solely for
the `lake` subprocesses; it makes `getpid()` return the host PID visible at
`/proc/self`.  The shim source, binary hash, wrapper, and smoke test are all
recorded.  It does not modify or bypass the trusted checker, Lean project, or
any mounted input.

The trusted preflight then returned successfully:

- status `KLEAN_NO_OBLIGATIONS`;
- frozen/Stage 1 hash
  `30ee607e4db2c763d3a61fbd783e6d1d4e23c5f2e1d49916ea0f428d024add1d`;
- Stage 3 manifest hash
  `f9beba61b82ac748b1a73e5cfdddddd1e187a043aa7b8538d3b585540f0b3ccf`;
- generated tree hash
  `1674b1db22fed880156b73d95f892508ff3681d5cb4484d12dab1fe1e5bbe61e`;
- zero obligations, null target, 41 recorded trust declarations, and zero
  designated sorries;
- `lake clean` exit 0 with empty-output hash
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
  and
- `lake build` exit 0 with output hash
  `2c424777e015508f17e168dd1b4f83ca8e2eb4c1ac2f7886878ca9cde55bb8f1`.

The returned document reproduces the recorded preflight fields and build
diagnostic hashes.  The complete result is in
`evidence/47_rerun_klean_preflight_success.txt`.

I separately checked every sidecar binding.  The verification, Stage 1,
Stage 3, inventory, generated-project, obligation-map, trust-inventory,
toolchain, export-result, and producer hashes all match.  The obligation-map
hash is `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
the trust-inventory hash is
`f1ce5c3405e31ca8e898c397d95b90da3f6d1e91e85787029ceea95fc6e5681e`.

Relative to the protected Stage 3 labels, the structural mapping is exact:
`input-manifest.source_rules`, `obligation-map.source_rules`, the obligation
list, and the trust-parameter list are all empty.  There are no duplicate or
vacuous conjuncts because there are no conjuncts.  The generator manifest,
recorded preflight, rerun preflight, and audit input all bind a null target;
there is no generated target file or declaration.

Relative to the independently correct classification, however, the mapping is
not bijective.  The required `strLt` source rule is omitted, so its relevant
obligation is absent and the generated target is missing.  Mechanical
self-consistency over a misclassified empty set is insufficient.  Because the
true domain set has cardinality one, `KLEAN_NO_OBLIGATIONS` is false in the
substantive sense required by the audit.

## Stage 5

Stage 5 proof auditing is not applicable in `CLASSIFICATION_ONLY` mode.  No
candidate exists, as required by the recorded no-obligations layout.  I did not
perform candidate copying, candidate clean builds, `#print axioms Proof.final`,
or operational-parameter bridge checks.  The successful build above is the
trusted Stage 4 preflight's clean build of a temporary copy of the generated
project, not a Stage 5 proof.

## Evidence index

Material commands are recorded in `evidence/COMMANDS.md`.  Principal raw
results are:

- `evidence/04_producer_authentication.txt` — producer hashes and image ID;
- `evidence/09_reconstructed_inventory.txt` — full canonical inventory and
  bijection;
- `evidence/38_hash_and_structure_verification.txt` — every launcher/source/
  sidecar hash comparison;
- `evidence/39_bridge_free_strlt_claims.txt` — independent `kprove` rerun;
- `evidence/47_rerun_klean_preflight_success.txt` — required successful
  preflight result;
- `evidence/48_generated_target_absence.txt` and
  `evidence/49_recorded_target_identity.txt` — empty obligation map, null
  target, and absent candidate; and
- `evidence/50_independent_classification.md` — rule-by-rule classification.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
