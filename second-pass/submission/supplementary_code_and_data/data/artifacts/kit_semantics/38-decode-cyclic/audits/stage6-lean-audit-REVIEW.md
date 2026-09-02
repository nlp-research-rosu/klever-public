# Independent audit: `38-decode-cyclic`

## Scope and conclusion

The launcher and `AUDIT_MODE` both record `CLASSIFICATION_ONLY` for condition
`kit-semantics` and semantics mode `SUPPLIED_SEMANTICS`. There is therefore no
Stage 5 proof to audit. I independently reconstructed and classified Stage 3,
then checked the deterministic Stage 4 `KLEAN_NO_OBLIGATIONS` result.

The result is legitimate. The local verification-module closure has exactly 13
rules. Each is a genuine definition of an exact source-syntax macro or a fresh,
structurally recursive execution summary. None is a domain lemma, operational
bridge, or claimed proved-derived lemma. Consequently the true domain-lemma set
is empty, the empty Stage 4 obligation set is correct, and no Lean target or
Stage 5 candidate should exist.

## Input and producer integrity

I treated the mounted artifacts as untrusted evidence and did not rely on the
selected Stage 2 verdict, prior reviews, logs, or comments. The trusted
inventory and preflight code came from `/reference/tools`.

Before judging Stage 4, I hashed the two exact producer files:

| Producer file | Observed SHA-256 | Manifest SHA-256 |
|---|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | same |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | same |

`generator-manifest.json` and `source-manifest.json` record the same immutable
generator image ID,
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
The final component of the producer-source path in `/audit-input.json` records
that same ID. The producer bundle has exactly the two source files and its
source manifest; its pipeline tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
matching the audit input. The producer provenance gate therefore passes; there
is no infrastructure `AUDIT_ERROR`.

I also recomputed every launcher-recorded mounted-input hash. All matched:

| Artifact | Recomputed hash |
|---|---|
| Stage 1 workspace tree | `c8bbd396936ed49aeff26ea34563d23604ef39ee01b66cbb3fa40ccd695d45cf` |
| Stage 1 deterministic export tree | `19080e5a92a93527acf60894cec9c95a68c5317048f79503b8865bb5659cd5a5` |
| Stage 2 audit tree | `4ed998d702168fdf011e6c83dd3ab2f858d63915fd90ef571c50e24a92c666b6` |
| Stage 3 manifest file | `5df6d88302bd02e831f04119a29f6f548ffbbded693cdad9cad916d93b22bf92` |
| Stage 4 generation tree | `21d06a9fbd9bb68fa5c83cfcffb649b90c5eba75de2e6bf19e63a3dab169f612` |
| Generated Lean project tree | `bdc993fde5bb1d397bbf9bb507715bd15a2f62cd30e315d1b927a47bfc0e0938` |

The Stage 1 per-file manifest was also bijective: 769 recorded files, 769
observed files, with no missing, extra, or changed entry. Full results are in
`evidence/17-integrity-check.txt`.

## Inventory reconstruction and bijection

Running `tools.k_rule_inventory.inventory_verification` afresh on
`/reference/k-proof` selected the last verification main module `VERIFICATION`.
Its local module closure is exactly `['VERIFICATION']`. The frozen
`verification.k` SHA-256 is
`07cbc3fc57044faf70fbbe6c0856dcb214633c5746bf13666c513e4efec91a01`.

The trusted scanner reconstructed the following source spans. For every entry,
the text is exactly the indicated source-line slice, the normalized hash
recomputes the `source_rule_id` as `rule-<normalized_sha256>`, and attributes
are empty:

| # | Lines | `source_rule_id` | Independent class | Role |
|---:|---:|---|---|---|
| 1 | 8–24 | `rule-5fadedd1d4c059e5d87c1e443849dc7c59bbb473b8aaa92234cfd709eb0715b6` | `DEFINITION` | Exact `decodeLoopBody` syntax macro. |
| 2 | 27–35 | `rule-5367ffff4eaecfb0f84c53b77dc54d061b07006110880a94d6e194146a40ce02` | `DEFINITION` | Exact `decodeFunctionBody` syntax macro. |
| 3 | 39 | `rule-c4174d53c8a3154eebdb9e22c2b92a55e58050b2e3bff8ae7f82b3e27c28ffd1` | `DEFINITION` | `decodedResult` empty-remainder base case. |
| 4 | 40 | `rule-ffb0732d27afbf362e5e9e9fc010a57098d520ce352d603a3a975a24f8ed22de` | `DEFINITION` | `decodedResult` one-code base case. |
| 5 | 41–44 | `rule-1843eb0bcc3ef5cefdf6645c4f7f131e4c0a1a17c02878b5b5b7d1b5bae0eb4c` | `DEFINITION` | `decodedResult` two-code base case. |
| 6 | 45–52 | `rule-58ccf33b1f5982228861b7117175665717d215e2db7474767affb4f2e1a99294` | `DEFINITION` | `decodedResult` consumes one triple and recurs. |
| 7 | 56 | `rule-48f99ba4e9cf5b2f361e19b875ced9ff0a79d3e558b60b093674a0264a84ab08` | `DEFINITION` | `decodedTail` empty base case. |
| 8 | 57 | `rule-0048c482596ccb952ad0ec9470e8ee307fe5f9d342a83640df98cd2ef84f0d54` | `DEFINITION` | `decodedTail` one-code base case. |
| 9 | 58–59 | `rule-405f2fc1f12cf0c83faacc269a24d82e70b4f1fee61206e5ef7273f5f73a983c` | `DEFINITION` | `decodedTail` two-code base case. |
| 10 | 60–61 | `rule-f70ecf73c4b2aeaeb9064d85808f3afd9764972e7dfef3aeb0fc5bc32d56f84b` | `DEFINITION` | `decodedTail` drops one complete triple and recurs. |
| 11 | 64–65 | `rule-813dfdbb1d8c4c8262f557071f5ddb487fa764c1744a74ef71ad94e9bc4e44d5` | `DEFINITION` | `decodeCodes` composes complete-group result and residual tail. |
| 12 | 70 | `rule-b75007273ddfec4a9357ba26cdca2d47ef06a615dbb678c59ff81151a6f259b4` | `DEFINITION` | `finalLoopChar` empty-iteration base case. |
| 13 | 71–72 | `rule-9d892364275b939a50532c29aa15281c55ccadc0974c27de6d7718ff2195ff25` | `DEFINITION` | `finalLoopChar` records the head character and recurs. |

Canonical hashing of those 13 ordered rule documents gives
`204f58f331c4d67162af18c6fd2169b721f142d31a4e056becaa1424420ddd12`.
That value matches both the reconstructed inventory and
`lemma-discovery.json`. The discovery list has the same 13 identities in the
same order, no duplicate, no omission, and no extra. Every entry has exactly
one recognized classification and a nonempty rationale. See
`evidence/07-reconstructed-inventory.json` and
`evidence/18-inventory-bijection.txt`.

## Independent classification judgment

The first two rules cannot bypass execution. Their left sides are fresh
zero-argument syntax tokens declared with `[macro]`; their right sides are the
translated syntax already present in `solution.mpy`. `decodeLoopBody` is the
exact group append, length-three branch, `group[2] + group[:2]` result append,
and group reset. `decodeFunctionBody` is the exact docstring expression,
initializations, `For` statement using that body, and final return. They are
parse-time names for source syntax and are definitions.

The remaining eleven rules have fresh proof-summary symbols on their left
sides, not operational `<k>` configurations or existing semantics operations.
Their defining patterns are exhaustive and disjoint by `IntSeq` constructor
shape:

- `decodedResult` has length-0, length-1, length-2, and length-at-least-3
  cases. The recursive case reduces the remaining sequence by three and
  appends `C,A,B` for encoded triple `A,B,C`.
- `decodedTail` has the same disjoint shape split. Its recursive case reduces
  by three and its three bases preserve the final incomplete group.
- `decodeCodes` is the named composition of those two summaries.
- `finalLoopChar` splits empty from nonempty input and reduces the latter by
  one while replacing the old loop-target value with the current one-character
  string.

The supplied operational rules independently explain these equations:
`#iterNext` on a string yields one-character strings in order; the `For` rules
bind that yielded value before executing the body; string `+` is `seqConcat`;
`len(str(IS))` is `isLen(IS)`; index 2 returns the third code; slice `[:2]`
returns the first two; and assignment updates the current scope. Therefore an
induction on the input sequence in blocks of three gives exactly the
`decodedResult`/`decodedTail` state, and an induction by one gives
`finalLoopChar`. This is a mathematical justification of the definitions, not
an inference from the prior successful proof.

As finite adversarial support, an independent model checked every sequence of
length 0 through 9 over three distinct integer codes: 29,524 cases and zero
mismatches. Boundary lengths 0–6, repeated and negative codes, and multiple
complete groups plus a tail were included. On witness `[1,2,3]`, identity,
constant-empty, and wrong left-rotation counterfactual definitions all disagree
with the operational result `[3,1,2]`. This finite check supplements, but does
not replace, the constructor/induction argument. See
`evidence/35-summary-semantics-check.txt`.

There are no `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA`
entries. Thus no rule is improperly claiming the special proved-derived-lemma
status, and no unproved domain fact is hidden under another label. The
reconstructed rules have no explicit simplification attributes; in any event,
every macro/function equation is classified `DEFINITION`, satisfying the rule
for simplifiers.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and exactly these inputs:

- frozen input: `/reference/k-proof`;
- discovery: `/reference/lemma-discovery.json`;
- generation: `/reference/klean-generation`;
- toolchain lock: `/reference/klean-toolchain.lock.json`.

The first attempt exposed a sandbox-only toolchain issue: Lean 4.22 requests
`/proc/<numeric-pid>/exe`, which this sandbox hides, while `/proc/self/exe` is
available. A narrow compatibility shim changed only that readlink request to
`/proc/self/exe`. With it, `lean --version` reported the pinned Lean 4.22.0
commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`. The same unmodified trusted
checker then returned exit 0. Its internal `lake clean` and `lake build` both
returned 0, and the build completed all generated modules successfully. The
fresh returned JSON is exactly equal to `resolution.stage4_preflight` in
`/audit-input.json`, including the build-output SHA-256. The initial failure and
successful rerun are preserved in `evidence/19-klean-check-generation.txt` and
`evidence/33-klean-check-generation-rerun.txt`.

Independent structural checks, separate from that preflight, established:

- `input-manifest.json` carries all 13 reconstructed rules, in order, in its
  `definitions` list with exact spans, hashes, IDs, classifications, and
  rationales.
- Its domain `source_rules`, operational rules, proved-derived lemmas, lowered
  structural definitions, and promoted structural definitions are all empty.
- The four summary signatures exactly match the frozen declarations.
- `obligation-map.json` is exactly `{schema_version: 3, source_rules: [],
  obligations: [], trust_parameters: []}`. Thus the source-rule/obligation
  bijection is the empty bijection: no omission, duplicate, or extra exists.
- Its file SHA-256 is
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
  matching `generator-manifest.json`.
- The generator manifest, export result, fresh preflight, launcher selection,
  and independent classification all agree on zero obligations and status
  `KLEAN_NO_OBLIGATIONS`.
- `klean_export.expected_target_definition` and
  `klean_export.target_statement` both return `None`. The generator manifest,
  fresh preflight, and audit input all record `target: null`, and the generated
  Lean sources contain no `final` target declaration. There is therefore no
  weakened, duplicated, irrelevant, changed, or vacuous target/conjunct.
- `/candidate` is absent, and the launcher records null Stage 5 workspace,
  invocation, and result fields, as required in classification-only mode.

The generic generated project contains 41 allowlisted non-propositional hook
declarations and no sorry holes, but with an empty obligation set and no target
they do not support any Stage 5 theorem. No Stage 5 build, `Proof.final`, axiom
accounting, or operational-bridge parameter review applies in this mode.
Complete structural results are in `evidence/37-stage4-structure.txt`.

## Final judgment

Stage 3 is complete, bijective, and semantically correct. The genuine domain
set is empty. Stage 4 deterministically and correctly emits no obligations and
no target, with all source, inventory, manifest, toolchain, and tree bindings
intact. The selected `KLEAN_NO_OBLIGATIONS` result is therefore legitimate.

VERDICT: PASS
LEGITIMACY: LEGIT
