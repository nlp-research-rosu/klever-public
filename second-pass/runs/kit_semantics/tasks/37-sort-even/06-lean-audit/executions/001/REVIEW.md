# Independent Stage 3–5 Audit: `37-sort-even`

## Scope and result

This audit covers HumanEval problem `37-sort-even`, condition `kit-semantics`, with `SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and `/audit-input.json` select `CLASSIFICATION_ONLY`. The selected Stage 4 status is `KLEAN_NO_OBLIGATIONS`; there is no Stage 5 candidate.

I treated the mounted Stage 1–5 artifacts, their prose, logs, classifications, and earlier verdicts as untrusted evidence. I reconstructed the rule inventory with `/reference/tools/k_rule_inventory.py`, applied the frozen operational semantics directly, authenticated the generation-time producer source before judging Stage 4, reran the trusted deterministic preflight, and independently recomputed the recorded hashes and the source-rule/obligation relation.

## Frozen input and inventory reconstruction

The frozen `verification.k` has SHA-256 `d2ae562c0947b167ec2b5143491da99d1871ff04b56c2bc059010b7da1ac050f`. The trusted inventory selected main module `VERIFICATION` and reconstructed its local verification-module closure, in source order, as:

1. `VERIFICATION-SYNTAX`
2. `VERIFICATION-BASE`
3. `VERIFICATION`

The reconstruction found exactly seven rules. Its canonical whole-inventory hash is `97f503f0101ebe78977b771b6b95ffc103d3457cd3f5c7ce08ae6874023a1512`.

| Span | Recomputed `source_rule_id` | Attributes | Independent class |
|---|---|---|---|
| 27–30 | `rule-02349ceffec1049d372ce10bf9984d2a928dca91bcce4f527ff08aaa50e88e5a` | none | `DEFINITION` |
| 32–49 | `rule-61a087dbf540316c7ffe409d318ed1abd81afdc67636986d622fbbcabe7ea30a` | none | `DEFINITION` |
| 51–52 | `rule-86d3fae28ae4ec7cefa52ecbaea1a03c0f94bfc931a350e0c2beb28c6cd7123e` | none | `DEFINITION` |
| 54–55 | `rule-84057d0c37cb0c2e1e806eb747f7016bbc4854bd23ecaad20e6fc13cfcac8ccf` | none | `DEFINITION` |
| 57–63 | `rule-da9594733502733c5baea5c07345e60cff4228109cd5931016f3801b06910350` | none | `DEFINITION` |
| 65–70 | `rule-6d751676da4edbf999ca6d4c967d22060cd612334941e4e2f1dd1c404926d54e` | none | `DEFINITION` |
| 85–134 | `rule-4cee3e3fae5dc24dccfe7ee0495478a590993ee6d2488173adbb104fb8345a92` | `priority(40)` | `PROVED_DERIVED_LEMMA` |

For every entry, the recomputed span, normalized source SHA-256, and `source_rule_id` match the protected Stage 3 entry. The Stage 3 IDs are unique and occur in exactly canonical order. There are no missing, duplicated, extra, reordered, or hash-changed identities. The protected manifest's inventory hash also equals the independently reconstructed hash. The trusted Stage 3 contract validation passed.

Raw reconstruction and bijection evidence is in [03-reconstructed-rule-inventory.txt](/audit-output/evidence/03-reconstructed-rule-inventory.txt) and [04-stage3-bijection.txt](/audit-output/evidence/04-stage3-bijection.txt).

## Independent classification judgment

The first two rules expand the named `sortEvenLoopBody` and `sortEvenBody` AST macros. They are definitions of proof terms corresponding exactly to the translated source body, not facts about execution.

`evenCount(N)` names the supplied-semantics integer expression `(N + 1 - pyMod(N + 1, 2)) / 2`, which is the loop bound used by the source for nonnegative sequence lengths. It defines a summary term; it does not assert a domain property.

The two `fillEven` equations are the guarded base and recursive clauses of a named recurrence. Their guards `I >= STOP` and `I < STOP` cover the integer cases; the recursive branch advances `I` by one and records exactly the source loop's update at index `2*I` using the corresponding element of `SORTED`. These clauses define the recurrence rather than postulate a theorem about a pre-existing function.

`sortEvenResult(VS)` defines the result summary by composing the fixed-semantics slice `buildVS(VS, 0, vsLen(VS), 2)`, the supplied opaque sorting primitive `sortVS`, `evenCount`, and `fillEven`. It does not assert ordering, permutation, or another human-facing domain proposition. The source calls `sorted(l[::2])` and then writes those elements at the even positions, so this definition is relevant and operationally aligned with the source and postcondition.

The final rule is an execution shortcut over the complete loop/call configuration and therefore required the special `PROVED_DERIVED_LEMMA` history. That history is present and was independently checked:

- `VERIFICATION-NO-BRIDGE` imports only `VERIFICATION-BASE`, so it does not contain the shortcut in sibling module `VERIFICATION`.
- The body, cells, rewrite, and `I >=Int 0` guard of `SPEC-CONNECTION.loop-connection` are textually identical to the reusable rule body; the comparison differs only in the outer claim/rule marker and the later rule's priority attribute. The normalized body diff was empty.
- `prove.sh` compiles `VERIFICATION-NO-BRIDGE` and proves `SPEC-CONNECTION` before it compiles `VERIFICATION` and runs the later target proof.
- I reran `kprove spec-connection.k --definition verification-no-bridge-kompiled --spec-module SPEC-CONNECTION`; it exited 0 with `#Top`.

Thus the shortcut was first proved against a module without it and only then installed for later use. It is not an unproved domain lemma. None of the seven rules has a `simplification` attribute, so the simplification-class restriction is satisfied vacuously.

The independently determined class counts are six `DEFINITION`, zero `OPERATIONAL_RULE`, one `PROVED_DERIVED_LEMMA`, and zero `DOMAIN_LEMMA`. Relevant frozen semantics and the derived-lemma replay are recorded in [07-relevant-operational-semantics.txt](/audit-output/evidence/07-relevant-operational-semantics.txt), [08-rerun-derived-lemma-proof.txt](/audit-output/evidence/08-rerun-derived-lemma-proof.txt), and [09-derived-lemma-identity-and-order.txt](/audit-output/evidence/09-derived-lemma-identity-and-order.txt).

## Producer-source and immutable-image authentication

Authentication was completed before the Stage 4 judgment:

- `/reference/generation-tools/klean_export.py`: `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`
- `/reference/generation-tools/klean.py`: `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4`

Those observed hashes exactly equal both `generator-manifest.json` fields and the two entries in `source-manifest.json`. The producer bundle contains exactly those two files plus `source-manifest.json`. Its trusted pipeline tree hash is `61e146bfb9d9d51713156383989873e5c48a5c9b156425ef4cf37c57e6ecd5fb`, matching `/audit-input.json`.

The generator image ID is `sha256:2db35f33b29b4ada4f78dd04470349652b5f62e1ff63355111720eee4e3cc162` in the generator manifest and source manifest. The same image digest is the terminal component of the launcher-recorded immutable producer-source path. All three bindings agree. Evidence is in [05-producer-authentication.txt](/audit-output/evidence/05-producer-authentication.txt) and [06-producer-comparison.txt](/audit-output/evidence/06-producer-comparison.txt).

## Recorded hashes and manifest bindings

I independently recomputed all launcher-recorded hashes using the trusted file/tree hash implementations. Every one matched:

- Stage 1 pipeline tree: `519eee3351c9ab00c6ccdca001102e514f9774868f55c49349d14183eb9c157c`
- Stage 1 deterministic export tree: `253017ebdf2175e981e603b2b82e0088ab1563a3e3bf4b559a3e82b9ec1a19b9`
- Stage 2 audit tree: `27b019e3100e0c3e6453e01dd307662ba73b023566df808988001a8123796d6b`
- Stage 3 manifest file: `26d0def9d6452ee7b7d30e42a7f3fff7fd89d98497e9a99c5ea1b6161e3e586b`
- Stage 4 generation tree: `a3ef4e7d595dc6735f8b3d88fbb7e147b29b5f2b6e84171e89cd2f72185e7ecb`
- Producer-source bundle: `61e146bfb9d9d51713156383989873e5c48a5c9b156425ef4cf37c57e6ecd5fb`
- Generated project tree: `7caa10e18bac3ff4223945c0dc7649fca97314de8d2fb87c4c33945fef8100ec`
- Lean workspace and invocation: both correctly recorded as null.

The selected Stage 2 and Stage 4 artifact hashes match the recomputed trees. I also recomputed the complete Stage 1 file set: all 786 regular files are recorded, there are no missing or extra paths, and all 786 file hashes match. The generator, input, export-result, preflight, obligation-map, and trust-inventory hash bindings all agree with these independently observed values.

The audit envelope's canonical resolution digest independently recomputes to the recorded `e9e4d111251b1139c61de9dae1cfcf91525d90107f57cee68c79ede160106da1`. The mounted mechanical-checker lock hashes to the launcher-recorded `1cca0c10fa61c806f07242ba46c7aa84149c9e547741914e702cd1bbcc4d6eb8`; each of its nine file entries matches both `/reference/tools` and the installed `/opt/humaneval/tools` copy. The Stage 4 preflight embedded in the signed resolution equals the generation sidecar, and its clean/build output hashes equal the independent replay's output hashes.

Full results are in [15-independent-hash-verification.txt](/audit-output/evidence/15-independent-hash-verification.txt) and [18-audit-envelope-and-tool-lock.txt](/audit-output/evidence/18-audit-envelope-and-tool-lock.txt).

## Deterministic Stage 4 preflight

I invoked `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and exactly these inputs:

- frozen input: `/reference/k-proof`
- discovery manifest: `/reference/lemma-discovery.json`
- generation: `/reference/klean-generation`
- toolchain lock: `/reference/klean-toolchain.lock.json`

The first invocation reached its `lake clean` subcheck but the audit container's Lean shim could not detect its installation. Diagnosis showed that this container has a PID-namespace/procfs mismatch: Lean attempted `readlink("/proc/9/exe")`, which returned `ENOENT`, while `/proc/self/exe` remained available. This was an audit-environment issue, not generated-project behavior.

I applied a narrowly scoped preload correction during the replay. It changes only a failed `readlink` of `/proc/<digits>/exe` with `ENOENT` into a retry of `/proc/self/exe`; all other calls and results remain untouched. With that correction, the pinned toolchain identified itself as Lean 4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly as locked. The same trusted `check_generation` call then returned:

- status `KLEAN_NO_OBLIGATIONS`
- obligation count `0`
- target `null`
- the expected Stage 1, Stage 3, and generated-tree hashes
- `lake clean` exit 0
- `lake build` exit 0, ending with `Build completed successfully.`
- zero designated sorries.

The original failure, root-cause trace, correction source, and successful returned evidence remain visible in [10-check-generation-rerun.txt](/audit-output/evidence/10-check-generation-rerun.txt), [17-proc-namespace-root-cause.txt](/audit-output/evidence/17-proc-namespace-root-cause.txt), and [14-check-generation-proc-corrected.txt](/audit-output/evidence/14-check-generation-proc-corrected.txt).

## Obligation bijection and fixed target

The independently classified true domain-lemma set is empty. This makes the selected no-obligation status mathematically legitimate, not merely self-consistent metadata.

The Stage 4 input manifest has `source_rules: []`. The generated obligation map has `source_rules: []`, `obligations: []`, and `trust_parameters: []`; its SHA-256 is `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`, exactly the generator-manifest value. The generator manifest records obligation count zero. Therefore the exact source-rule/obligation mapping is a bijection between two empty sets: no source rule is omitted or duplicated, and there is no irrelevant, weakened, vacuous, or extra conjunct.

For an empty obligation set, the fixed generated target must be absent. Independently calling the trusted expected-target and target-statement functions returned `None` for both. `generator-manifest.json` and `/audit-input.json` record a null target, `Klean37SortEven/Lemmas.lean` contains only an empty namespace, and a declaration search found no generated target. This is exact target identity for the no-target case. Evidence is in [16-no-obligation-target-check.txt](/audit-output/evidence/16-no-obligation-target-check.txt).

## Stage 5 applicability and trust accounting

Stage 5 is correctly absent: `/candidate` does not exist, and the launcher records null Lean workspace and invocation paths/hashes. Because there is no generated theorem, no `Proof.final`, no target parameters, and no candidate, the proof-mode clean-copy build, candidate token scan, `#print axioms Proof.final`, operational-bridge definitions, and candidate axiom reconciliation are not applicable. Running any of those as though a proof target existed would contradict the legitimate `KLEAN_NO_OBLIGATIONS` status.

The generated Stage 4 project itself was nevertheless clean-built by the mandatory preflight. Its recorded executable trust declarations do not prove or alter a target proposition; there is no proposition target in this generation.

## Evidence index

All raw commands and results are under `/audit-output/evidence/`. The principal records are:

- [02-frozen-k-sources.txt](/audit-output/evidence/02-frozen-k-sources.txt): numbered frozen verification, claims, proof order, and source solution.
- [03-reconstructed-rule-inventory.txt](/audit-output/evidence/03-reconstructed-rule-inventory.txt): canonical reconstructed inventory.
- [04-stage3-bijection.txt](/audit-output/evidence/04-stage3-bijection.txt): exact order, uniqueness, missing/extra checks, and class counts.
- [07-relevant-operational-semantics.txt](/audit-output/evidence/07-relevant-operational-semantics.txt): relevant supplied K operations.
- [08-rerun-derived-lemma-proof.txt](/audit-output/evidence/08-rerun-derived-lemma-proof.txt): independent `#Top` replay.
- [14-check-generation-proc-corrected.txt](/audit-output/evidence/14-check-generation-proc-corrected.txt): complete successful preflight return.
- [15-independent-hash-verification.txt](/audit-output/evidence/15-independent-hash-verification.txt): launcher, file-set, and Stage 4 binding checks.
- [16-no-obligation-target-check.txt](/audit-output/evidence/16-no-obligation-target-check.txt): empty obligations, absent target, and absent candidate.
- [18-audit-envelope-and-tool-lock.txt](/audit-output/evidence/18-audit-envelope-and-tool-lock.txt): signed-resolution digest, checker lock, all locked tool hashes, and preflight diagnostic hashes.

VERDICT: PASS
LEGITIMACY: LEGIT
