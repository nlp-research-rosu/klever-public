# Independent Stage 3–5 audit: `5-intersperse`

## Scope and audit mode

The launcher environment and `/audit-input.json` both record
`CLASSIFICATION_ONLY` for condition `kit-semantics` and semantics mode
`SUPPLIED_SEMANTICS`. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`. `/candidate` is absent, and the audit input has null
Stage 5 workspace, invocation, result, and target fields. Stage 5 Lean proof
checks therefore do not apply.

I treated the selected Stage 2 review, all prior logs and comments, the Stage 3
classification, Stage 4 generated content, and their stated conclusions as
untrusted evidence. Classification and target legitimacy below are based on the
frozen Stage 1 source, supplied operational semantics, and fresh trusted-tool
reconstruction.

## Producer provenance gate

I hashed the two mounted generation-time producer sources before judging Stage
4:

| Producer | Actual SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both hashes equal the values in `generator-manifest.json` and
`source-manifest.json`. The source manifest image ID and generator-manifest
image ID are both
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`;
the audit-input producer-source path has that exact image digest as its
basename. The producer bundle tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
equal to the audit input. The bundle has exactly the source manifest and these
two producer files. There is no producer-source infrastructure error.

Evidence: `01_launcher_and_producer_provenance.txt`,
`07_reconstructed_inventory_and_hashes.json`, and
`39_all_recorded_hashes_bijection_target.json`. An early exploratory
comparison retained in `02_producer_crosscheck.txt` used tuple membership
instead of exact path-basename equality; its supersession note records that
diagnostic bug.

## Inventory reconstruction and Stage 3 bijection

I ran the trusted `/reference/tools/k_rule_inventory.py` implementation with
`PYTHONPATH=/reference` against the frozen `/reference/k-proof`. The selected
main module is `VERIFICATION`; its local verification-file import closure is
only `VERIFICATION`. The supplied `MPY` semantics is required from other files
and is not an additional local module in `verification.k`.

The frozen `verification.k` SHA-256 is
`71e427a368736161879f1a56827faf269be02ca732b18c68052ffa31c0fe3f2d`.
The reconstruction found these four rules, in this order:

| Source span | Normalized SHA-256 / `source_rule_id` | Fresh classification |
|---|---|---|
| lines 8–14 | `e28394b585c4090679938a1fc2a49542a90c06f9fd53d8d2ea93cb550aecd2b6` / `rule-e28394b585c4090679938a1fc2a49542a90c06f9fd53d8d2ea93cb550aecd2b6` | `DEFINITION` |
| line 20 | `671fd3686197e0c91cef745f9b7af75d1bd0f7277cabab95a54dc8fbf6e1ef79` / `rule-671fd3686197e0c91cef745f9b7af75d1bd0f7277cabab95a54dc8fbf6e1ef79` | `DEFINITION` |
| lines 22–23 | `386331eb5a2c59cc86798243ff1afd3badb062dc83a886655fce827ef4f75b24` / `rule-386331eb5a2c59cc86798243ff1afd3badb062dc83a886655fce827ef4f75b24` | `DEFINITION` |
| lines 25–32 | `b0a9306232910cc5bd1efab08c4f20853e642eec8176e7d9e7d39d1d46f375cd` / `rule-b0a9306232910cc5bd1efab08c4f20853e642eec8176e7d9e7d39d1d46f375cd` | `DEFINITION` |

For each entry I separately joined the exact source lines, normalized whitespace,
rehashed the normalized text, and reconstructed `rule-<hash>`. Every source
span, text, normalized hash, and ID agrees with the trusted inventory.
Rehashing the ordered rule documents gives the whole-inventory SHA-256
`98d24755c0d3f453b048d563519170cd08da8c9b2f46b3546f105d537cb4fbe9`.

The protected Stage 3 list contains the same four unique IDs in the same order.
There are no omissions, duplicates, extras, reordered identities, or changed
hashes. Trusted `validate_trust_boundary` also accepts the structural
classification contract, but I did not use that acceptance as the semantic
classification judgment.

Evidence: `06_frozen_source_and_discovery.txt` and
`07_reconstructed_inventory_and_hashes.json`.

## Independent classification judgment

All four rules are definitions:

1. Lines 8–14 expand the `INTERSPERSE-BODY` syntax production, declared
   `[macro]`, into the exact two-statement loop body from `solution.mpy`: append
   the delimiter iff `result` is nonempty, then append `number`. It names a
   source-syntax proof term and does not match or short-circuit a runtime
   configuration.
2. Line 20 is the base equation for the newly declared
   `[function, total]` summary `intersperseAcc`: empty remaining input returns
   the accumulator.
3. Lines 22–23 are its empty-accumulator/nonempty-input recursive clause. The
   first element is appended without a delimiter, matching list truthiness.
4. Lines 25–32 are its nonempty-accumulator/nonempty-input recursive clause.
   It appends delimiter then element through the supplied `valSeqConcat`
   definition and recurses on the strict tail of the remaining input.

The three summary clauses are pairwise disjoint and exhaustive because both
`ACC` and `REST` are either `.ValSeq` or `vCons`; every recursive call strictly
shortens `REST`. They therefore define a total structural recurrence rather
than assert a property of an existing symbol.

The supplied semantics supports the classification and meaning:

- `truthy(list(V))` is true exactly when `V` is nonempty;
- `If` branches on that truth value;
- list `append` mutates the heap sequence by
  `valSeqConcat(VS, vCons(V, .ValSeq))`; and
- list iteration yields elements in source order.

An independent executable comparison covered 520 accumulator/rest cases,
including empty, singleton, and multi-element states, and found zero
differences between the recurrence and the operational loop continuation.
Concrete witnesses include `[]/[1,2,3]/4`, producing
`[1,4,2,4,3]`, and `[8,7]/[1]/4`, producing `[8,7,4,1]`.
Constant, identity, delimiter-omitting, always-delimiter, and reordered
counterfactuals all produced distinguishing failures.

None of the four rules has a `simplification` attribute. None rewrites a
runtime `<k>` configuration, so none is an `OPERATIONAL_RULE`. None is claimed
or evidenced as an exact rule first proved in a module that omitted it, so
none is a `PROVED_DERIVED_LEMMA`. Most importantly, none states a mathematical
property of a pre-existing operation: the three `intersperseAcc` equations are
the defining clauses of a fresh summary, and the other rule is a syntax macro.
Thus no rule is a hidden or relevant `DOMAIN_LEMMA`.

The independently reclassified domain-lemma set is genuinely empty.

Evidence: `08_operational_semantics_context.txt` and
`36_semantic_recurrence_and_mutations.json`.

## Hash integrity

I independently verified:

- all 769 recorded Stage 1 per-file hashes, with no missing or extra files;
- Stage 1 full tree
  `b1720199b015372df65aac0f4384f09902e6859d532e89bf5c3763a75dc5ca5a`;
- Stage 1 deterministic-export tree
  `192f41973c8305ed710ee4466f7403d9bce3173185acc4eb6781046c8b2206f9`;
- selected Stage 2 tree
  `1f0bddf173617e964a93f1f8849ffce3505d8bdfb7af2cb57ac44687278d46c1`;
- Stage 3 file
  `b74d25b235900363090e2cde6e8ccebdf548eb5b78e9acd3926e369cb98043c3`;
- selected Stage 4 tree
  `b62e8d36a3d61078c973b2eb9b14ff0023e8122e1cde9efbd8a6608d316f7189`;
- generated project tree
  `9742d548236b3793caa9ac16149bef6f6cd393062ead87d886b8325f242e6488`;
- obligation map
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- trust inventory
  `8ef13f36856959bf9c59db40c1c87eeeb307b2c58d67b321b675604fc9f944ee`;
  and
- the signed resolution digest
  `75ec29c80ac5678c9e0d737c6d9eaf0b7d3d2b5fb8487494f37d16799f7aa24b`.

Every corresponding hash field in the audit input, input manifest, generator
manifest, export result, preflight, source manifest, and obligation entries
agrees. The generator toolchain object equals the trusted
`klean-toolchain.lock.json`.

Evidence: `39_all_recorded_hashes_bijection_target.json`.

## Required preflight and deterministic Stage 4 judgment

I invoked `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, `/reference/k-proof`,
`/reference/lemma-discovery.json`,
`/reference/klean-generation`, and the trusted toolchain lock.

The first ambient attempts failed at `lake clean` because this audit
container's namespace PID is not mounted at `/proc/<namespace-pid>`, while Lean
4.22 discovers its executable using that numeric path. The evidence shows
`/proc/self/exe` works but `/proc/2/exe` does not. I used a narrow local
`LD_PRELOAD` shim that changes only numeric `/proc/*/exe` `readlink` requests
to `/proc/self/exe`. Its retained source SHA-256 is
`6262e6e32fa6ef0b4d6ca89fd2f66dc9ccab49667b3993ba7da02d6f6a844152`.
It does not alter Lean, generated sources, declarations, or theorem content.

With the pinned Lean 4.22 installation, the required check returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean` exit 0;
- `lake build` exit 0;
- build output SHA-256
  `91b9f4eb6db9019c40c3cc6094f35a2fd48dcd18a18ac48e8b379671be8e7a1a`;
- zero obligations;
- null target;
- zero designated sorries; and
- 41 generated trust declarations.

The complete successful build output exactly reproduces the preflight object
recorded in both Stage 4 and `/audit-input.json`. The generated tree was
rehashed after all diagnostics and remained exactly
`9742d548236b3793caa9ac16149bef6f6cd393062ead87d886b8325f242e6488`.
The 41 declarations are executable collection-hook values, are all present in
`trust-inventory.json`, and are not propositions or proofs; the trusted
preflight's independent proposition-trust gate accepts them.

Evidence: `09_required_check_generation.txt`,
`11_required_check_generation_rerun.txt`,
`32_pid_namespace_mismatch.txt`, `33_lean_shim_validation.txt`,
`34_required_check_generation_success.txt`, and `lean_app_path_shim.c`.

## Obligation bijection and target identity

The independently classified domain set is empty. Consistently:

- `input-manifest.json` has `source_rules: []`;
- `obligation-map.json` has `source_rules: []`, `obligations: []`, and
  `trust_parameters: []`;
- every recorded obligation count is zero; and
- the ordered source-rule/obligation ID lists are equal and duplicate-free.

There are consequently no omitted, duplicated, irrelevant, weakened, or
vacuous conjuncts. The trusted target parser returns null, the expected target
definition is null, the generator manifest target is null, the preflight target
is null, and the audit-input target is null. The generated `Lemmas.lean`
contains only an empty namespace, and an independent declaration scan finds no
generated proposition or theorem target.

This is a genuine `KLEAN_NO_OBLIGATIONS` case, not a nonempty domain-lemma set
hidden behind self-consistent manifests. There is no Stage 5 candidate.

Evidence: `35_obligation_map_target_and_trust.txt` and
`39_all_recorded_hashes_bijection_target.json`.

## Conclusion

Stage 3 is bijective and correctly classifies all four local verification
rules as definitions. The true domain-lemma set is empty. Stage 4 preserves all
frozen identities and hashes, maps that empty set to exactly zero obligations,
generates no target, and reproduces its clean build. The classification-only
shape correctly excludes Stage 5.

VERDICT: PASS
LEGITIMACY: LEGIT
