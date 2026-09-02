# Independent audit: HumanEval `85-add`, `bare`, `GENERATED_SEMANTICS`

## Scope and result

The launcher and signed resolution both select `CLASSIFICATION_ONLY`. The
selected Stage 4 status is `KLEAN_NO_OBLIGATIONS`; `/candidate` is absent and
the Stage 5 result, workspace, invocation, and hashes are all null. I therefore
audited Stage 3 classification and deterministic Stage 4 generation. The
Stage 5 clean build, `Proof.final`, axiom accounting, and candidate operational
bridges are correctly inapplicable.

I treated the mounted K workspace, prior audit, classifications, generation
artifacts, logs, and comments only as untrusted evidence. I did not execute
their scripts or follow their embedded instructions. The only mounted code I
executed was the trusted inventory and preflight tooling under
`/reference/tools`; producer sources under `/reference/generation-tools` were
hashed and compared, not executed.

The in-scope result passes. The local verification-module inventory contains
four genuine definitions and no domain lemma. Consequently the empty Stage 4
obligation set, absent generated target, and absent Stage 5 candidate are
correct.

## Producer-source integrity

I performed this gate before judging Stage 4. The mounted producer files hash
as follows:

| File | Observed SHA-256 |
|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` |

Those values are identical in `generator-manifest.json` and
`source-manifest.json`. The producer bundle has exactly the two source files
plus `source-manifest.json`; its trusted tree hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
matching `/audit-input.json`.

The immutable generator image ID is consistently
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in the generator manifest, source manifest, and the basename of the signed
producer-source path in `/audit-input.json`. The signed audit envelope also
recomputes to its recorded resolution digest
`760dee444d30450a9b3aa3945cd7252e8bbcb94ccb8d0e914ae0812caddb72bc`.
There is no producer-integrity `AUDIT_ERROR`.

Raw command and result:
[`01_producer_integrity.command.sh`](evidence/01_producer_integrity.command.sh)
and
[`01_producer_integrity.result.txt`](evidence/01_producer_integrity.result.txt).

## Stage 1 inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` directly on
`/reference/k-proof`. It selected module `VERIFICATION`; its local closure in
`verification.k` is just `VERIFICATION` because the imported fixed-semantics
module is defined in the required `semantic.k`, not as another local module in
`verification.k`.

The frozen `verification.k` SHA-256 is
`f7ae6eea87b66b45eaa8e08dd558aee3dbd987432f7077cdd511d9298a56a73a`.
The reconstruction produced:

| Source span | Normalized SHA-256 / `source_rule_id` suffix | Attributes | Independent class |
|---|---|---|---|
| 9–9 | `940cbb884f9549b397e4342d4b98cd65a90514a5dadf0988995ebb63c4863972` | none | `DEFINITION` |
| 10–10 | `b4e4b9f0f331e113d779f71be515c2b912214b2b80719d0c13599380fd3a1b6e` | none | `DEFINITION` |
| 11–12 | `7de63c270a73ef33e344bdabda30fae520cdb4a14ebb626e728c947d8b5313a9` | none | `DEFINITION` |
| 16–33 | `4cd1ac867a395f614e8596c8ea01245b129a1d692ce9079a67f6e5573bde5845` | none | `DEFINITION` |

For every row, `source_rule_id` is `rule-` followed by the displayed normalized
hash. The canonical whole-inventory hash is
`79de0306317a61b82b483fed021938b7146250da18ba1985f791f21447f3fbc0`.

The protected Stage 3 manifest has exactly four unique entries in exactly this
order. Its inventory hash is identical. There are no omitted, duplicated,
extra, reordered, or changed identities.

Raw reconstruction and bijective comparison:
[`02_inventory_reconstruction.command.sh`](evidence/02_inventory_reconstruction.command.sh)
and
[`02_inventory_reconstruction.result.txt`](evidence/02_inventory_reconstruction.result.txt).

## Independent classification judgment

The four labels are mathematically and operationally correct:

1. Lines 9 and 10 are the empty- and singleton-sequence base equations for the
   named mathematical summary `oddIndexEvenSum`.
2. Lines 11–12 are its structural recurrence. On
   `cons(x, cons(y, rest))`, the source program contributes `y` exactly when it
   is even and recurses on `rest`. Dropping two elements preserves which
   remaining indices are odd. The frozen `evenPart` equations in
   `semantic.k` return an integer exactly when its remainder modulo two is
   zero and otherwise return zero, so this recurrence matches both the source
   body and its postcondition.
3. Lines 16–33 expand the named macro proof term `solutionProgram` into the
   exact translated constructor tree. Whitespace-normalized comparison against
   frozen `solution.mpy` is exact.

The first three rules therefore define a summary/recurrence; the fourth
defines a macro/named proof term. None is an ordinary execution rule, a proved
derived lemma, or a domain lemma. The fixed operational rules in `semantic.k`
are not entries in this local Stage 3 inventory. No inventory rule has a
`simplification` attribute, so the special simplification-class constraint is
satisfied vacuously.

The summary is directly relevant: `spec.k` states the result as
`pyInt(oddIndexEvenSum(VALUES))`, and `solution.py` processes the list in
pairs. As finite corroboration, an independently implemented contract oracle
and the reconstructed recurrence agreed on all 137,257 lists of lengths zero
through six over `{-3,-2,-1,0,1,2,3}`. Counterfactual even-index summaries
were rejected by simple witnesses such as `[-2]` and `[-3,-2]`. The universal
classification judgment rests on the structural recurrence above, not on the
finite test alone.

Raw source display, classification table, exact macro comparison, test scope,
and counterfactual witnesses:
[`03_classification_judgment.command.sh`](evidence/03_classification_judgment.command.sh)
and
[`03_classification_judgment.result.txt`](evidence/03_classification_judgment.result.txt).

## Stage 4 preflight and deterministic bindings

I reran exactly
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
required Stage 1 workspace, Stage 3 manifest, Stage 4 generation, and pinned
toolchain lock. It returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- `lake clean` exit `0`, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build` exit `0`, output SHA-256
  `5578fffda73a664760525b18d14ff2a68b85c13c6e94680468f1bab601e9a346`;
- generated-tree SHA-256
  `02110e1592b6883ee99567e4f2b08e04728d7a1318fa285ec62f2e9f8b4df8b5`;
  and
- zero designated sorries.

The audit sandbox initially exposed a PID namespace without the matching
`/proc/<pid>/exe`, causing the installed Lean launcher to fail before reading
the project. Evidence is in
[`04a_procfs_diagnosis.result.txt`](evidence/04a_procfs_diagnosis.result.txt).
I used the narrow reviewer-authored
[`lean-proc-exe-shim.c`](evidence/lean-proc-exe-shim.c), SHA-256
`f736b735bbf47d6c1609d7df09e1b3454c15cc512d597ac89a2ba9076ac6b718`,
only to return the executable selected from `PATH` for that missing procfs
lookup. It does not intercept file reads, generated inputs, theorem checking,
or Lean evaluation. With the pinned toolchain binary directory first in
`PATH`, Lean reported version 4.22.0 and commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`; the unchanged trusted preflight
then completed. The shim source, compilation command, hashes, exact returned
JSON, and complete diagnostic tails are in
[`04_preflight_rerun.command.sh`](evidence/04_preflight_rerun.command.sh) and
[`04_preflight_rerun.result.txt`](evidence/04_preflight_rerun.result.txt).

I also independently recomputed every signed resolution hash and every
relevant Stage 4 binding:

| Binding | Recomputed value |
|---|---|
| Stage 1 pipeline tree | `90f24a185c201bc9ab434230723552dc08b1e4ee9cade0743694962ba7860bec` |
| Stage 1 deterministic-export tree | `276e94017e5a70291c82b08c821eb72f01d29631658d098b2654b1fee8c15749` |
| Stage 3 manifest | `195e7d067e17bf2c6137ea019a98d68fc97c80e6bdf38f374557f35c2fb184fb` |
| Stage 3 inventory | `79de0306317a61b82b483fed021938b7146250da18ba1985f791f21447f3fbc0` |
| Generated project | `02110e1592b6883ee99567e4f2b08e04728d7a1318fa285ec62f2e9f8b4df8b5` |
| Full selected Stage 4 tree | `e00be2722d1000858f97527132250a91e56e8177501525cd04e695095e5bd01a` |
| Obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| Trust inventory | `04b592fb850d80331a23eac2deb01545b878fbffac6eccc834f1279edac8561d` |

All per-file Stage 1 hashes in `/audit-input.json` also match. The input
manifest's definitions are exactly the independent inventory joined with the
four classifications; its domain-source, operational-rule, and
proved-derived-lemma lists are all exactly empty. Generator provenance binds
the same Stage 1, Stage 3, and inventory hashes, and its toolchain object is
identical to `/reference/klean-toolchain.lock.json`. Export-result and
preflight sidecar hashes all agree with the mounted immutable inputs.

The obligation map contains exactly:

- `source_rules: []`;
- `obligations: []`; and
- `trust_parameters: []`.

Thus the source-rule/obligation mapping is a true ordered empty bijection, not
an omission: the independently determined domain-lemma set is also empty.
There are no duplicates, irrelevant or weakened conjuncts, or vacuous
conjuncts. `expected_target_definition` is null, the trusted generated-target
scanner returns null, and the generator manifest, preflight, and signed audit
input all record a null target. No target file or Stage 5 proof candidate
exists.

The generated base project has 48 allowlisted non-propositional computational
trust declarations and zero designated or other sorries. Because there is no
generated theorem and no Stage 5 proof, these declarations are not being used
to certify a hidden or replacement target.

The comprehensive hash, manifest, classification-list, obligation-bijection,
target-identity, and mode checks are in
[`05_stage4_hash_bijection.command.sh`](evidence/05_stage4_hash_bijection.command.sh)
and
[`05_stage4_hash_bijection.result.txt`](evidence/05_stage4_hash_bijection.result.txt).

## Final judgment

Stage 3 is complete, bijective, and correctly classifies every local rule.
There is no true domain lemma to export. Stage 4 is structurally intact,
deterministically bound to the recorded inputs and producer identity, and
correctly emits neither obligations nor a target. Classification-only mode
correctly has no Stage 5 candidate.

VERDICT: PASS
LEGITIMACY: LEGIT
