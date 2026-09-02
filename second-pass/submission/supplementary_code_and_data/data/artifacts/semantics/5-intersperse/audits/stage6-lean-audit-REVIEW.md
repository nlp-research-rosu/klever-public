# Independent audit: HumanEval `5-intersperse`

## Scope and outcome

This audit independently reviewed Stage 3 lemma classification and deterministic
Stage 4 generation for condition `semantics`, semantics mode
`SUPPLIED_SEMANTICS`. `/audit-input.json` and `AUDIT_MODE` both select
`CLASSIFICATION_ONLY`. Stage 4 records `KLEAN_NO_OBLIGATIONS`; `/candidate` is
absent, so Stage 5 proof construction, `Proof.final`, axiom printing, and
operational-bridge parameter review are not applicable.

I treated the prior K audit, manifests, generated code, logs, and comments as
untrusted evidence. The rule inventory was reconstructed from the frozen Stage
1 source with the locked trusted inventory implementation. Hashes, provenance,
obligation mappings, and the generated target were then recomputed rather than
accepted from prior verdicts.

The result is PASS/LEGIT. All six local verification rules genuinely define
fresh proof summaries; none is an operational rule, a derived lemma, or a
domain lemma. The independently classified domain-lemma set is therefore
genuinely empty, and the no-obligation Stage 4 result is appropriate.

## Trusted tooling and producer provenance

The Stage 6 checker bundle passed its signed lock gate. The lock SHA-256 is
`5f2476d09635fc2f32625592bd667dd87a374068cd5b6610d9513ee6dacc066f`,
exactly the value recorded by the launcher.

Before judging Stage 4, I independently hashed the two mounted generation-time
producer files:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Both values agree exactly with `source-manifest.json` and
`generator-manifest.json`. Both manifests record immutable generator image
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`.
The launcher-recorded producer-source path ends in that same image digest. The
producer bundle contains exactly the two producer files plus its source
manifest, and its independently recomputed framed tree hash is
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
matching `/audit-input.json`. Producer provenance is therefore complete and
consistent; there is no producer-source infrastructure error.

Evidence: `evidence/01_producer_provenance.log`,
`evidence/02_producer_manifests.log`, and
`evidence/14_checker_bundle.log`. The first log also preserves an unavailable
`jq` attempt; subsequent inspection used ordinary read-only output and the
locked Python tooling.

## Stage 1 inventory reconstruction

The trusted inventory code selected `INTERSPERSE-VERIFICATION` from
`prove.sh`. Its local closure inside frozen `verification.k` contains only that
module: imported `MPY` is supplied by the separate frozen semantics files, not
another local module in `verification.k`.

Independent reconstruction produced:

- frozen `verification.k` SHA-256:
  `797980743c5c5bc62a788c4a0bf80ac1d0ec5db67ea9bdbee238e039d688dc9a`;
- six ordered rules, with no duplicate normalized hashes or source IDs; and
- whole inventory SHA-256:
  `32c2f2c43bcefd71043e6c8f0f67f2e2b5a4c34a01460b5deac9971afa3bd2cf`.

Every reconstructed span, normalized source hash, and `source_rule_id` is:

| Span | `source_rule_id` | Attributes |
|---|---|---|
| 7–7 | `rule-05af82756816da99d1e49a9f8d009c94185476c6c7d0fb7678256f49b7839b01` | none |
| 8–9 | `rule-a69c7f927a81762ea2c4fbf188360727e079a96344cde3099709abd953299501` | none |
| 10–17 | `rule-96273f0b4eae15373ec58939dbd00740dde58870a697d93b32a5a4bd04ed197b` | none |
| 20–21 | `rule-9be9c742f13371df267a06b8e67ec2e35592c9ac3cd5aa5b772100f6bf8c3abe` | none |
| 24–24 | `rule-20166af5adb55b2aa1e6c90c631d9e6c733f576541555c546a5a90c9a7e7f3b7` | none |
| 25–26 | `rule-1602c9e6a845786876a75dac174363782ca1ac8b767d2e5f3baca81621fbc25b` | none |

The ordered Stage 3 identities equal this ordered list exactly. Counts and sets
also agree, and both sides are duplicate-free. Thus there are no omissions,
extras, duplications, reordering, changed rule hashes, or unaccounted
classifications.

Evidence: `evidence/03_inventory_compare.py` and
`evidence/03_inventory_compare.log`.

## Independent classification judgment

All six rules are `DEFINITION`. This judgment comes from the frozen rule bodies,
their fresh function declarations, their uses in `spec.k`, and the operational
list/loop semantics—not from the Stage 3 rationales.

1. `rule-05af...` is the base equation for the fresh total function
   `intersperseAcc`. When the remaining sequence is empty, it returns the
   accumulated sequence. This names the accumulator summary and does not
   rewrite program execution.

2. `rule-a69c...` is the first-element recurrence for `intersperseAcc`. With an
   empty accumulator and a nonempty remainder, it places the first value into
   the accumulator and structurally recurses on the tail.

3. `rule-9627...` is the later-element recurrence for `intersperseAcc`. With a
   nonempty accumulator and a nonempty remainder, it appends the delimiter and
   then the next value using the supplied semantics' total `valSeqConcat`, and
   structurally recurses on the tail.

4. `rule-9be9...` defines the fresh named summary `intersperseVS` by invoking
   `intersperseAcc` with an empty initial accumulator.

5. `rule-2016...` is the empty-tail equation for the fresh structural helper
   `lastNumber`; it preserves the previously bound loop value.

6. `rule-1602...` is the nonempty-tail recurrence for `lastNumber`; it advances
   the remembered value and structurally recurses on the tail.

For `intersperseAcc`, the remainder is either empty or nonempty, and in the
nonempty case the accumulator is either empty or nonempty. The three cases are
pairwise disjoint and exhaustive over the algebraic `ValSeq` constructors. Both
recursive cases strictly decrease the second sequence. `lastNumber` likewise
has disjoint, exhaustive empty/cons cases and strictly decreases its sequence.
The wrapper `intersperseVS` has no recursion of its own. The equations are
therefore covering, non-overlapping, and structurally descending over every
use.

The supplied operational semantics makes an empty list false and a nonempty
list true; list iteration yields values in order; and `append` updates the heap
list by concatenating a singleton. Consequently the source loop first appends
only the first element, then appends the delimiter followed by each later
element. This is exactly the `intersperseAcc` recurrence. `lastNumber` exactly
tracks the final value assigned to the `for` target. The main claim connects
the returned heap object to `intersperseVS`, while the loop claims use
`intersperseAcc` and `lastNumber`, so all three summaries are relevant to the
source program and postcondition.

None of these rules has a program redex, `<k>` cell, `#loop`, `Call`, heap
transition, continuation, or source-language operation on its left-hand side.
Each left-hand side is headed by a fresh proof-local function. They therefore
do not preempt, accelerate, or alter ordinary execution and are not
`OPERATIONAL_RULE`s or operational bridges. They state no property of
pre-existing operations (such as associativity, commutativity, or an
inequality), so they are not `DOMAIN_LEMMA`s. Stage 1 did not first prove any of
these exact rules in a module without the rule, and Stage 3 does not claim
`PROVED_DERIVED_LEMMA`; that category is correctly empty.

All reconstructed rule attribute lists are empty. In particular there is no
`simplification` rule requiring a domain-lemma obligation, so the requirement
that every simplification rule be a definition or domain lemma is satisfied.

As finite sensitivity evidence, an independently coded reading of the
recurrences agreed with the source loop on 1,092 exhaustive small cases and
rejected constant-empty, identity, omitted-delimiter, and
delimiter-before-first mutations. This testing is not used as a universal
proof; the universal classification judgment rests on constructor coverage,
disjointness, structural descent, and the operational rules described above.

Evidence: `evidence/09_classification_sources.log`,
`evidence/10_definition_semantics.py`, and
`evidence/10_definition_semantics.log`.

## Stage 4 preflight and integrity

I invoked `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, `/reference/k-proof`,
`/reference/lemma-discovery.json`, `/reference/klean-generation`, and the
trusted toolchain lock.

The first invocation reached the clean-build phase but failed because this
audit sandbox reports a namespaced PID while exposing a host-mounted `/proc`;
Lean 4.22 looks up `/proc/<getpid()>/exe`, which did not exist. The exact failure
is retained in `evidence/04_check_generation.log`. A narrowly scoped preload
compatibility shim redirected only `/proc/<digits>/exe` `readlink` calls to the
equivalent available `/proc/self/exe`. Its source, failed warning-strict first
compile, successful compile, and toolchain probe are all retained. With the
shim, Lean identified version 4.22.0 and commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly the lock.

The same trusted checker then returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0, empty output;
- `lake build`: exit 0, output hash
  `91b9f4eb6db9019c40c3cc6094f35a2fd48dcd18a18ac48e8b379671be8e7a1a`;
- obligation count 0;
- target `null`;
- designated sorry count 0; and
- 47 generated non-propositional trust declarations, exactly matching
  `trust-inventory.json`.

The rerun result is byte-for-byte consistent with the recorded preflight
diagnostics. Evidence:
`evidence/proc_exe_compat.c`, `evidence/05_lean_compat_probe.log`,
`evidence/06_lean_compat_probe.log`, and
`evidence/07_check_generation_rerun.log`.

Independent recomputation also established:

| Artifact/hash domain | Observed SHA-256 |
|---|---|
| Stage 1 framed workspace tree | `06fdf0315620d56d025ccac12a419587c4ad4adfa4a5bfef1431b92cf22864ac` |
| Stage 1 Klean export tree | `ca40ab7c0668efb2c352eaa2ff2cacca9b8c22f1d25b4900bed63849b1ea8fdc` |
| Stage 3 manifest | `d02a5a5db00b1a7c4cb25641b8eb09c5529cfc5db503a4cec4a5b10e63b4be22` |
| Selected Stage 2 tree | `57d1105065374888a2c46ef1ddab9b1183f6c5f6a21c0ac6c44099f6749f0e55` |
| Selected Stage 4 tree | `e79213845092e48911adf8b00b3bf01abe71adffd2d3a61d7ae02604921cc3a2` |
| Generated Lean tree | `caee5ea8dbe3af1d609738d77682ce4c96930e30e79a67dc4c5918d5e8db6b0e` |
| Obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| Trust inventory | `55aa43cdcdd2b245b1183020bc6bf8e86f19d67b22a0c80f94bb0e6cee93bffd` |

Every value matches all corresponding launcher, input-manifest,
generator-manifest, export-result, and preflight fields. The complete
per-file Stage 1 hash map is also a bijection with the launcher record.
The signed resolution digest is valid, and the root and audit-output copies of
the launcher input are identical.

The independently classified Stage 3 domain ID list is empty.
`input-manifest.source_rules`, `obligation-map.source_rules`,
`obligation-map.obligations`, and `obligation-map.trust_parameters` are all
empty ordered lists. Counts are zero everywhere. This is an exact
source-rule/obligation bijection, not an omission or duplicate.

`klean_export.target_statement` independently found no generated target.
That `null` result agrees with the obligation map, generator manifest,
preflight, and audit input. There is no target to weaken,
duplicate, make vacuous, or relocate. `/candidate` is absent as required.

Evidence: `evidence/08_integrity_audit.py` and
`evidence/08_integrity_audit.log`.

## Deterministic producer replay

I replayed Stage 4 below `/tmp/audit-work` using copies of the exact hashed
generation-time `klean_export.py` and `klean.py`, the frozen Stage 1 workspace,
the protected Stage 3 manifest, the pinned toolchain lock, problem
`5-intersperse`, and the recorded generator image ID.

The replay returned `KLEAN_NO_OBLIGATIONS` and reproduced:

- the generated project byte-for-byte, including generated tree hash
  `caee5ea8dbe3af1d609738d77682ce4c96930e30e79a67dc4c5918d5e8db6b0e`;
- `generator-manifest.json` byte-for-byte;
- `trust-inventory.json` byte-for-byte; and
- `export-result.json` byte-for-byte.

The only raw `input-manifest.json` difference was the expected absolute
read-only mount prefix: generation used `/frozen-k/`, while the audit replay
used `/reference/k-proof/`. Replacing only that prefix makes the manifests
identical. Thus the selected generated target state is deterministically
reproduced by the immutable producer.

Evidence: `evidence/11_producer_replay.log`,
`evidence/12_producer_replay_compare.log`,
`evidence/13_replay_normalized.py`, and
`evidence/13_replay_normalized.log`.

## Final judgment

Stage 3 is a complete, ordered, hash-stable classification of every local
verification rule. Each rule genuinely defines a fresh, relevant, total
structural summary and no true domain lemma is hidden under another category.
The true domain set is empty. Stage 4 faithfully and deterministically maps
that empty set to zero obligations and no target, with no Stage 5 candidate.
All producer, source, manifest, toolchain, tree, obligation, and target
integrity checks pass.

VERDICT: PASS
LEGITIMACY: LEGIT
