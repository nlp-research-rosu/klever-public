# Independent audit: HumanEval 159-eat

## Scope and result

The launcher-recorded mode is `CLASSIFICATION_ONLY`, condition `bare`,
semantics mode `GENERATED_SEMANTICS`. I independently audited the frozen
Stage 1 verification-module inventory, the protected Stage 3 classifications,
and the selected deterministic Stage 4 generation. Stage 5 proof checks are
not applicable because the independently confirmed domain-lemma set is empty,
the generated target is absent, the audit input has no Stage 5 workspace or
result, and `/candidate` is absent.

I did not rely on the selected Stage 2 verdict, prior reviews, comments, or
claimed prior success. The decisive evidence is the frozen source, the trusted
inventory/preflight tooling, independently recomputed hashes, and the fresh
preflight result.

## Immutable producer provenance

I hashed both generation-time producer files before judging Stage 4:

- `klean_export.py`:
  `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0`
- `klean.py`:
  `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13`

These exactly equal the respective `exporter_sha256` and `klean_py_sha256`
fields in `generator-manifest.json` and the two entries in
`source-manifest.json`. The producer bundle contains exactly those two sources
and `source-manifest.json`; its contract tree hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
matching `/audit-input.json`.

The immutable generator image ID is
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`.
It agrees between the generator manifest and source manifest, and its digest
component is exactly the terminal component of the producer-source path signed
in `/audit-input.json`. There is no missing or mismatched producer source and
therefore no producer-provenance `AUDIT_ERROR`.

Raw producer evidence is in
[03-generation-producer-hashes.txt](/audit-output/evidence/03-generation-producer-hashes.txt),
[04-generator-manifest.json](/audit-output/evidence/04-generator-manifest.json),
and
[05-generation-source-manifest.json](/audit-output/evidence/05-generation-source-manifest.json).

## Inventory reconstruction and bijection

Using the trusted `tools.k_rule_inventory.inventory_verification` on
`/reference/k-proof`, I reconstructed the local closure selected by the final
`kompile verification.k --main-module VERIFICATION` invocation. The closure is
exactly the local module `VERIFICATION`; its import `SEMANTIC` is external to
`verification.k` and therefore not another local module in this inventory.

The frozen `verification.k` SHA-256 is
`ac0aaae94ce4b73799ab250a0f3dffd3a872315ff2ef74776b15c0d86a544d27`.
The canonical whole-inventory hash is
`eb2cde66dab45012187d6b5094ef5d0dbe44a3e37d4ba20b733c4e4b0707fef2`.
The reconstructed rules, spans, normalized hashes, and IDs are:

| Order | Span | Normalized SHA-256 / source rule ID | Independent class |
|---:|---:|---|---|
| 1 | 7–9 | `91c176911d796fd34a936d1c236eea93108d5f11251e4aa98880886a8e508d37` / `rule-91c176911d796fd34a936d1c236eea93108d5f11251e4aa98880886a8e508d37` | `DEFINITION` |
| 2 | 10–12 | `af091bc1f7e6cc6c775155a69831df12634c5cff689a359e16ff738e658ec166` / `rule-af091bc1f7e6cc6c775155a69831df12634c5cff689a359e16ff738e658ec166` | `DEFINITION` |
| 3 | 14–17 | `93bb107fb1fa39b78b377035f5a623e0f98ed1ccfe394e635a844116bb9a184c` / `rule-93bb107fb1fa39b78b377035f5a623e0f98ed1ccfe394e635a844116bb9a184c` | `DEFINITION` |
| 4 | 20–35 | `0cf88ad480aad3ef8af77efd5071f81c8d4d4e3d955e87f4dcad541462652059` / `rule-0cf88ad480aad3ef8af77efd5071f81c8d4d4e3d955e87f4dcad541462652059` | `DEFINITION` |

The protected Stage 3 manifest has exactly these four IDs in exactly this
order, without omission, duplication, extra identity, changed hash, or
unaccounted classification. Its inventory hash matches the reconstruction.
None of the four rules has a `simplification` attribute.

The complete trusted reconstruction is
[07-reconstructed-rule-inventory.json](/audit-output/evidence/07-reconstructed-rule-inventory.json);
the protected-manifest validation summary is
[12-trust-boundary-validation.json](/audit-output/evidence/12-trust-boundary-validation.json).

## Independent classification judgment

The two `carrotContract` rules are the guarded equations of a named result
summary:

- `NEED <= REMAINING` defines
  `result(NUMBER + NEED, REMAINING - NEED)`.
- `REMAINING < NEED` defines
  `result(NUMBER + REMAINING, 0)`.

Their guards are disjoint and exhaustive over K integers. They are used as the
destination summary in the symbolic claims. They do not rewrite `run`,
`evalStmts`, `evalStmt`, `evalExpr`, a continuation, or a state cell. They are
definitions, not arithmetic domain lemmas or operational shortcuts.

The `validInput` rule is a named predicate macro expanding exactly to the
prompt's three integer range constraints. It appears in claim preconditions
and is a definition rather than a proposition asserted to help close the
program proof.

The `solutionProgram` rule is a named proof term expanding to the exact
constructor tree in `solution.mpy`. An independent Python AST parse confirms
the same `eat(number, need, remaining)` binding, `need <= remaining` branch,
two arithmetic results, empty else-body, and final insufficient-stock return.
After this expansion, the frozen operational rules still match `run` and
execute the function body through `evalStmts`, `evalStmt`, `evalExpr`,
`chooseBranch`, and `resultOf`. Thus it is an exact program-term definition,
not a result-bearing abstraction or execution-skipping operational bridge.

Counterfactuals are discriminating: changing `<=` to `<` breaks the equality
witness `(1,10,10)`; changing the insufficient branch breaks `(2,11,5)`;
changing either arithmetic expression breaks `(5,6,10)` or an
insufficient-stock witness. The definitions are relevant to the exact source
program and postcondition.

No inventory rule was first proved against a module excluding that rule and
then used in a later proof, so there is no `PROVED_DERIVED_LEMMA`. After
identifying the three named summaries/macros/proof term above, no mathematical
fact remains that could be a `DOMAIN_LEMMA`. The independently reconstructed
domain set is genuinely empty.

The rule-by-rule semantic record and witnesses are in
[77-classification-judgment.md](/audit-output/evidence/77-classification-judgment.md);
the independent source AST is in
[75-source-solution-ast.txt](/audit-output/evidence/75-source-solution-ast.txt).

## Recorded hashes and deterministic Stage 4 structure

The signed audit-input envelope verifies with resolved-input digest
`554a86098b503b50709585047c1bbbb60be04ac87536dbad4037ce9cde70a249`.
Independent recomputation also confirmed:

- Stage 1 contract tree:
  `8e2b81ca8c45c781f6b1f62dff963f2b505a92bdfa72f7bd94852f4e7818e281`
- Stage 1 export tree:
  `c84b3342bbab6b15b14ad44c9c423e6dfb9cea9a4d9c74256d4ceca3ffdcb96a`
- Stage 2 selected tree:
  `421bb39dd59f0fe76b1c575f484d7647ec7025d043816f48257dd22d2e55bea2`
- Stage 3 manifest:
  `810be45e450458eafb44fbc61f80e31ce2d55f9b3de8c9ba268c7a0b11e88826`
- Stage 4 selected-generation tree:
  `1a827e1ee8ca23437beff92ffb48b4af51a452c5f27c4de22084f0961b09e0d5`
- Generated project tree:
  `a5d88c1983baac23ad7d45c54b64df11547b5d7003323b6fd59b6b1e17c25cea`
- Obligation map:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`
- Trust inventory:
  `140ec001b6e9c49de87d3099900dc2425eec8cfb9d797d73d67791e12f2a1517`

The Stage 1 per-file hash map, both selected artifact hashes, generator
toolchain lock, mounted preflight document, export bindings, producer bundle,
and all cross-manifest hash links also match. The independent cross-check
reported no failed check; see
[78-structural-cross-check-final.json](/audit-output/evidence/78-structural-cross-check-final.json).

## Obligation bijection and fixed target

The Stage 4 input manifest's domain `source_rules` is `[]`, matching the
independently classified empty domain set. The generated
`obligation-map.json` contains:

- `source_rules: []`
- `obligations: []`
- `trust_parameters: []`

Thus the exact source-rule/obligation mapping is an empty-to-empty bijection;
there is no omission, duplicate, irrelevant obligation, weakened equation,
or vacuous conjunct. The trusted target parser returns `null`, and the
generator manifest, mounted preflight, and signed audit input all record
`target: null`. The immutable `Lemmas.lean` namespace contains no proposition.
Absence of a target is therefore the fixed generated result, not a target
change.

`KLEAN_NO_OBLIGATIONS` is mathematically correct here because the domain set is
genuinely empty after independent classification. It is not being inferred
merely from self-consistent manifests.

## Fresh Stage 4 preflight

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and the required Stage 1, Stage 3, Stage 4, and
toolchain-lock paths. The audit sandbox initially prevented Lean from resolving
its own executable: the process-visible PID was `3`, while the mounted `/proc`
exposed host PIDs, so Lake failed before reading the project.

To make the required tool run without weakening it, I used a preserved small
behavioral shim that redirects only `readlink` calls shaped as
`/proc/<pid>/exe` to `/proc/self/exe`. It does not alter any source, manifest,
hash computation, Lean declaration, or build result. The trusted preflight's
before/after immutable snapshots remained equal.

The fresh preflight returned:

- status `KLEAN_NO_OBLIGATIONS`
- obligation count `0`
- target `null`
- designated sorry count `0`
- trust declaration count `41`
- `lake clean`: exit `0`, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `lake build`: exit `0`, output SHA-256
  `d60f7f5d0f898537ee3a709a5f5151ff83f8da2bca80c8bf01637578914a0ba1`

These hashes and the complete build output exactly match the immutable
recorded preflight. The fresh returned evidence is
[59-rerun-check-generation-final.json](/audit-output/evidence/59-rerun-check-generation-final.json).
The initial infrastructure failure, diagnosis, shim source, and exact command
ledger are preserved in
[COMMANDS.md](/audit-output/evidence/COMMANDS.md).

The 41 generated trust declarations are the executable Map/List/Set hook
boundary recorded in `trust-inventory.json`; the trusted preflight confirmed
the declarations exactly match the allowlist and rejected proposition trust.
There is no generated proposition or proof depending on them in this
no-obligation result.

## Stage 5 applicability

The signed mode is `CLASSIFICATION_ONLY`; `lean_workspace`,
`lean_invocation`, `stage5_result`, and their hashes are all null. There is no
generated target and `/candidate` does not exist. This is exactly the required
state for a legitimate `KLEAN_NO_OBLIGATIONS` result. Consequently no clean
candidate build, `#print axioms Proof.final`, candidate trust scan, or
operational-bridge parameter audit is applicable.

## Final judgment

The Stage 3 manifest is complete and correctly classifies every local rule.
The true domain-lemma set is empty. Stage 4 is bound to the verified immutable
producer image and sources, every recorded hash and mapping agrees, the fixed
target is correctly absent, and a fresh trusted preflight succeeds. No Stage 5
candidate should exist and none does.

VERDICT: PASS
LEGITIMACY: LEGIT
