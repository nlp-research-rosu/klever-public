# Independent Stage 3/4 audit: `6-parse-nested-parens`

## Outcome and scope

The launcher and `/audit-input.json` both record
`AUDIT_MODE=CLASSIFICATION_ONLY`, condition `kit-semantics`, and semantics mode
`SUPPLIED_SEMANTICS`.  The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`.  There is no `/candidate`, Lean workspace, Lean
invocation, Stage 5 result, or generated target.  Stage 5 proof, axiom, and
operational-bridge checks are therefore not applicable.

I treated the mounted Stage 1/2/3/4 content, including prior logs and reviews,
as evidence rather than authority.  I did not use the prior PASS or Stage 3
rationales as a premise.  The classification below comes from the frozen
`verification.k`, source solution, problem statement, and supplied operational
semantics.

## Frozen input and recorded-hash verification

The schema-4 audit-input contract verified successfully, including the
canonical resolved-input digest
`68cc4e635d084180e9380f13d03344bdfaf0f482200e150f9d3b42d455b835b4`.
Independent recomputation produced:

| Artifact | Recomputed and recorded SHA-256 |
|---|---|
| Stage 1 workspace, pipeline tree hash | `d5560e80277bc5a95486899e1e6e6e540117bf9bfe32c3218265ec6f9ee75420` |
| Stage 1 deterministic-export tree | `736587e98e48bf5aa67dcfbcf72cc629bb3e0cfc2170f41058e9a821795bce4a` |
| Selected Stage 2 audit tree | `143f293ca0e4a877721e2dac641e6bd018e34be4fed792f78c2924249ab5572c` |
| Protected Stage 3 manifest file | `6ed8dcd9320f47ec397f62eeb1df28919ebdaba21d325456eec9beabc38f3e50` |
| Selected Stage 4 generation tree | `a8c79a8cd1760192369e65a8ae9758bf14d52260774f43f0778073e738ed75ca` |
| Generation-time producer-source tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |
| Generated Lean project, exporter tree hash | `da8f8241e20c81098d66f1657cd8ec83f6b86d42e61511c1be28a5778ec6bb3d` |

All 774 Stage 1 regular-file hashes were also recomputed: the observed and
recorded path sets are identical, with no missing, extra, or mismatched entry.
The selected Stage 2 tree was hash-checked but its earlier verdict was not
trusted or reused.

## Generation-time producer identity

I performed this gate before accepting any Stage 4 conclusion.

- `/reference/generation-tools/klean_export.py` hashes to
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`.
- `/reference/generation-tools/klean.py` hashes to
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`.
- Both hashes exactly match the three-file `source-manifest.json` and the
  `exporter_sha256`/`klean_py_sha256` fields of `generator-manifest.json`.
- The source manifest and generator provenance both name immutable image
  `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
  The producer path recorded in `/audit-input.json` ends in that exact image
  digest, and its complete mounted tree has the recorded producer-tree hash
  above.
- The producer bundle contains exactly `klean_export.py`, `klean.py`, and
  `source-manifest.json`.

There is no missing or mismatched producer source, so the infrastructure
`AUDIT_ERROR` condition does not arise.

## Rule-inventory reconstruction and Stage 3 bijection

I ran the trusted `tools.k_rule_inventory.inventory_verification` against
`/reference/k-proof`.  It selected `VERIFICATION`, the main module named by
`prove.sh`.  The local closure contains only that locally declared module:
`MPY` is supplied semantics and is not a module declaration inside
`verification.k`.

The reconstruction found 37 rules in source order.  It independently recovered
every source span, normalized text hash, and
`source_rule_id = "rule-" + normalized_sha256`.  The frozen file hash is
`a615cf0e8fd1c0c8cf53ccfc5d42ba922ce303bcc79fa58a6e4711500d0ed5c7`;
the canonical whole-inventory hash is
`f6ae86ecd9aba28a5a6fa67cf78bae5b8d0e9e654b6f39f4c9f86485764a27b3`.

The reconstruction compared bijectively with
`/reference/lemma-discovery.json`:

- 37 reconstructed and 37 classified entries;
- identical ordered source-rule ID sequence;
- zero duplicate IDs on either side;
- no omitted, extra, or reordered identity;
- no disagreement in reattached module, span, normalized hash, attributes, or
  text; and
- exact agreement on the whole-inventory hash.

The trusted Stage 3 contract validator independently accepted the same
boundary.

## Independent classification judgment

I classified all 37 entries as `DEFINITION`.  This is not based merely on their
K `[function, total]` declarations.  Each rule is actually an AST macro,
guarded defining case, base equation, wrapper, or tail-decreasing recurrence:

| Inventory entries and frozen spans | Defined role |
|---|---|
| 1–4, lines 8–41 | `loopBody`, `afterLoop`, `solutionBody`, and `solutionModule`: nullary macros expanding to the exact translated AST |
| 5–9, lines 48–56 | `nextDepth` guarded character partition and `scanDepth` base/cons recurrence |
| 10–18, lines 60–81 | `openDeepest`, `delimiterDeepest`, `nextDeepest`, and `scanDeepest` guarded cases and recurrence |
| 19–25, lines 85–101 | `delimiterOutput`, `nextOutput`, and `scanOutput` guarded cases and recurrence |
| 26–27, lines 104–105 | `scanChar` base/cons recurrence for the loop variable |
| 28–30, lines 108–116 | `finishOutput` guarded cases and the initialized `expectedDepths` wrapper |
| 31–37, lines 123–136 | `wellFormedStep` character partition, `wellFormed` recurrence, and initialized `validInput` wrapper |

The exact per-rule ledger, with all 37 full source-rule IDs, spans, classes,
and independent reasons, is in
`evidence/15_independent_classification.md`.

The supplied semantics keeps actual execution in ordinary configuration rules:
`For` lowers to `#loop`; string iteration yields one-character strings;
assignment and augmented assignment update the active scope; `If` uses
truthiness and branches; `ListExpr` allocates a heap list; and `append` mutates
that heap list.  None of the 37 inventory rules matches a `<k>` or other runtime
cell, preempts those rules, or directly observes a runtime configuration.
Consequently none is an `OPERATIONAL_RULE`.

None is a `PROVED_DERIVED_LEMMA`: there is no purported theorem rule whose
legitimacy depends on a prior proof against a module without that rule.  The
Stage 1 loop and final program connection are reachability claims in `spec.k`,
not rules in this inventory.

None is a `DOMAIN_LEMMA`.  The potentially sensitive terms are:

- `expectedDepths`, which merely initializes a structurally defined scan
  summary.  Its rule does not assume that execution returns that summary; the
  `parse-nested-parens` reachability claim must connect fixed execution to it.
- `validInput`, which merely initializes the recursive input-domain predicate.
  Its component equations define the accepted parenthesis/ASCII-space language
  and do not assert a mathematical consequence of that language.

The summaries are relevant to the source program and postcondition: they track
the source variables `depth`, `deepest`, `depths`, and `char`, including
delimiter append/reset and the final append.  Their guarded families are
disjoint and exhaustive, and their sequence recurrences consume the tail.
As finite supporting evidence, an independently written direct operational
model and an independently written recurrence model agreed on all 21,845
strings of lengths 0–7 over `(`, `)`, space, and `x`; an independent domain
predicate also had zero disagreements.  Counterfactual open-increment,
delimiter-append, and final-append changes altered representative results.
These finite checks support the reading of the equations but are not used as a
universal proof.

No inventory entry has a `simplification` attribute.  Thus the requirement that
every simplification be either `DEFINITION` or `DOMAIN_LEMMA` is satisfied
vacuously.

The protected classification—37 `DEFINITION`, zero
`OPERATIONAL_RULE`, zero `PROVED_DERIVED_LEMMA`, and zero `DOMAIN_LEMMA`—is
therefore independently correct.

## Deterministic Stage 4 integrity and mathematical adequacy

The Stage 4 `input-manifest.json` contains exactly the same 37 reconstructed
entries, in the same order and with the same spans, texts, attributes, and
normalized hashes.  Its category counts are 37 definitions and zero entries in
all other categories.

I independently checked the following Stage 4 bindings:

- Stage 1 export, Stage 3 manifest, inventory, and `verification.k` hashes agree
  across the input manifest, generator manifest, export result, audit input,
  and recomputed values.
- `generator-manifest.json` exactly embeds
  `/reference/klean-toolchain.lock.json`.
- `generated/obligation-map.json` hashes to
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
  exactly the generator-manifest value.
- `trust-inventory.json` hashes to
  `3c9919d30067452300fe0c6a9db9a6eddc70e334a589ad04a5449699eb5b1852`,
  exactly the export-result value.
- The input source-rule list, obligation-map source-rule list, obligation list,
  and trust-parameter list are all empty.  Generator and export obligation
  counts are both zero.

Because the independent classification also found a genuinely empty domain
set, this empty source-rule/obligation bijection is mathematically correct.  It
does not omit a domain fact, duplicate a fact, weaken a fact, introduce an
irrelevant fact, or create a vacuous conjunct.

The trusted exporter’s target parser returns `null`.  The generator manifest
and audit input also record `target: null`; `Lemmas.lean` contains no
proposition declaration.  Thus target identity is exact: there is no generated
target at all, as required for a genuine no-obligation result.

## Required generation preflight

I reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
required Stage 1, Stage 3, Stage 4, and toolchain-lock paths.

The first invocation exposed a sandbox-only Lean installation-discovery issue:
Lean attempted `readlink("/proc/8/exe")`, while this execution sandbox exposes
the running executable only through `/proc/self/exe`.  The call failed before
the generated project was built.  I preserved that failure and the diagnostic.
I then used a minimal, source-preserved compatibility preload that redirects
only `/proc/<digits>/exe` reads to the equivalent `/proc/self/exe`.  It does not
rewrite files, Lean sources, arguments, or build output.  With that compatibility
in place, Lean reported the pinned version 4.22.0 and commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

The required trusted preflight then returned successfully:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0, empty output;
- `lake build`: exit 0, complete successful nine-target build output;
- build-output SHA-256
  `4232b458928745b4e3e8c592286f8de2a6d5ef2ce02a5f691a6656160095b388`,
  exactly the previously recorded output hash;
- generated tree
  `da8f8241e20c81098d66f1657cd8ec83f6b86d42e61511c1be28a5778ec6bb3d`;
- obligation count 0; and
- target `null`.

The preflight’s before/after immutable snapshots also passed.  The compatibility
source and both the failed and successful raw invocations are preserved in
`evidence/17b_proc_exe_compat_source.c`,
`evidence/16_rerun_check_generation.txt`, and
`evidence/16b_rerun_check_generation_with_proc_compat.txt`.

## Stage 5 applicability

This is not `CLASSIFICATION_AND_PROOF`.  `/candidate` does not exist, and all
Stage 5 paths/results in the audit input are null.  Since the genuine domain
set is empty and there is no generated target, the required terminal state is
exactly classification-only with no proof candidate.  No `Proof.final`,
candidate target shadowing, candidate trust escape, target parameter, or
operational bridge exists to audit.

## Evidence index

Raw commands and outputs are under `evidence/`.  The central records are:

- `04_reconstructed_rule_inventory.json`: canonical reconstructed inventory;
- `05_frozen_stage1_sources.txt`: frozen verification/spec/source text;
- `09_recomputed_hashes.txt`: audit contract, tree hashes, and all 774 file
  hashes;
- `11_inventory_bijection.txt`: ordered bijection and field comparison;
- `13_relevant_operational_semantics.txt`: fixed semantics used for the
  classification judgment;
- `14_independent_semantic_examples.txt`: adversarial and counterfactual finite
  checks;
- `15_independent_classification.md`: complete 37-rule independent ledger;
- `16b_rerun_check_generation_with_proc_compat.txt`: successful required
  preflight result;
- `21_independent_stage4_checks.txt`: producer, manifest, obligation, and target
  checks; and
- `24_stage4_classified_input_bijection.txt`: exact Stage 4 classified-input
  match.

The Stage 3 classification is complete and correct, the Stage 4 producer and
all provenance bindings are authentic, `KLEAN_NO_OBLIGATIONS` corresponds to a
genuinely empty domain-lemma set, and the absence of a target and Stage 5
candidate is exactly required.

VERDICT: PASS
LEGITIMACY: LEGIT
