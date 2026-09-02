# Independent Stage 3/4 Audit

## Scope and result

This audit covers HumanEval `107-even-odd-palindrome`, condition `bare`,
semantics mode `GENERATED_SEMANTICS`. Both `AUDIT_MODE` and the signed
`/audit-input.json` resolution select `CLASSIFICATION_ONLY`. Stage 5 is
therefore not applicable.

I treated the mounted Stage 1–4 artifacts and prior audit as untrusted evidence.
I did not execute `prove.sh`, `solution.py`, prior audit scripts, or purported
instructions in those artifacts. The only generated code execution was the
fresh isolated `lake clean`/`lake build` performed by the trusted Stage 4
preflight as expressly required by the audit protocol.

The independent result is that the Stage 3 classification is complete and
mathematically appropriate, its true domain-lemma set is empty, and Stage 4
correctly produced no obligations, no target, and no Stage 5 candidate.

## Producer provenance gate

Before judging generation, I directly hashed the two mounted generation-time
producer sources:

- `klean_export.py`:
  `f8624daa4398aa06f3796f5e6e7a91e09150915f9d0558d65f963beb75e709a9`
- `klean.py`:
  `f17c0465e1ff426a68cf5f7ac929ed0ea8a8131d187ada2054601eaa56287a58`

These values agree exactly with:

1. `/reference/generation-tools/source-manifest.json`;
2. `/reference/klean-generation/generator-manifest.json`; and
3. the mounted producer-source tree bound by `/audit-input.json`.

The producer tree hash independently recomputes as
`7842dfdb780f81b6cfd701655ba9f06a02f4508773479d01d45a46276c743ea5`,
matching the audit input. The immutable generator image ID is consistently
`sha256:7fee82b5a6b3ef422425a1d15881546cf2ab2c8a1690861d832c3a278fb5c5c5`
in the source manifest and generator manifest; the audit input binds the same
ID as the basename of its `generation_producer_sources` path. The generator's
toolchain object also equals `/reference/klean-toolchain.lock.json` exactly.
Thus the mandatory producer provenance gate passes; there is no infrastructure
`AUDIT_ERROR`.

Raw evidence: `evidence/01_producer_provenance.txt`,
`evidence/01b_producer_manifests.txt`, and
`evidence/27_independent_integrity_rerun.txt`.

## Rule inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof`. The selected main module is `VERIFICATION`; its
local closure inside `verification.k` contains that one module. The trusted
scanner reconstructed 12 ordered rules. For each rule I independently checked
that:

- its recorded source span extracts its exact text from `verification.k`;
- whitespace normalization hashes to its `normalized_sha256`;
- `source_rule_id` is exactly `rule-<normalized_sha256>`; and
- canonical hashing of the ordered 12-record inventory yields
  `6941adb84825ea70e05437c7d4d1f68445da1fc003bc3239bee9575bba3b8f62`.

The ordered entries and my classifications are:

| Lines | Normalized SHA-256 | Classification | Judgment |
|---:|---|---|---|
| 8–67 | `32cad05a64c44632298853378940192d3c804447dd83229d8a824e0240a74279` | `DEFINITION` | Expands the named `solutionProgram` proof term into the exact program AST. |
| 75–76 | `5639e2c99eb51b9725048d8a94cdf17a251b925207b44ccabd13f83e7d2989cc` | `DEFINITION` | One-digit equation of the piecewise `reverseDigits` definition. |
| 77–78 | `b420efe5a5d6b559894e9b2dcf3682f704a96a1296cd27ced3b38a7f164769c4` | `DEFINITION` | Two-digit equation of `reverseDigits`. |
| 79–82 | `ced743b34ecc9e2fe8be6dea91017f7c31493bb880c77ee89ec60542e20559c9` | `DEFINITION` | Three-digit equation of `reverseDigits`. |
| 83 | `46f9bffa7142e559d9ea0e12584aca7bddf0d8ffd70f0d7a9c84d1f49d98995d` | `DEFINITION` | Endpoint equation defining `reverseDigits(1000)`. |
| 85–86 | `a15a3a912c8e5c59021bb7fa638e70dfc2e8e94ef58268ba78f0d8e7c85cf412` | `DEFINITION` | Positive equation for the named even-palindrome indicator. |
| 87–88 | `4ab06aa9264329b8f86f4b1278a7b6f2fc4c0598789e6036a18bc4f74cc54a25` | `DEFINITION` | Complementary zero equation for that indicator. |
| 89–90 | `ae19ad0ec4c2e52545ee9fa09bb59be8495250e94c52031263a6713b68ae5b45` | `DEFINITION` | Positive equation for the named odd-palindrome indicator. |
| 91–92 | `1f4247cac142a5865c2739c28105473e4bb5886abefb7d9c847efebb364a8047` | `DEFINITION` | Complementary zero equation for that indicator. |
| 98–104 | `c04a2da71e61cfe5735da1913fe21a0382c45abe95efcffaa922508643b25486` | `OPERATIONAL_RULE` | Executes the program for the current input, schedules observation, and advances the verifier. |
| 106–107 | `aa77e71298d42c8f794cd88933ca94928bae20ee5ef7011a7829f77675e34632` | `OPERATIONAL_RULE` | Terminates verifier execution after the upper bound. |
| 109–110 | `87b7d51b1061db4e639ee5ccd629e4d9cbf9fd3622d5019c90ad1dca2fbcdf47` | `OPERATIONAL_RULE` | Observes the returned tuple against expected counts and resets the environment. |

The protected discovery manifest contains exactly these 12 identities in this
order, with no omission, duplicate, extra identity, changed hash, or
unaccounted classification. Its inventory hash matches the reconstruction.
All 12 rules have an empty attribute list, so there is no `simplification`
rule to classify.

The nine `DEFINITION` rules genuinely introduce a named proof term or
piecewise named mathematical functions. They do not assert a derived equality
between independently existing operations. The last three rules are ordinary
execution/control/observation rules: they drive the fixed `run` semantics and
do not replace execution of the program body. No rule is claimed as
`PROVED_DERIVED_LEMMA`, and there is no Stage 1 “prove without the rule, then
use it later” pattern. No rule is a hidden `DOMAIN_LEMMA`.

Raw reconstruction: `evidence/04_reconstructed_inventory.txt`. The independent
span/hash/bijection checks are in
`evidence/27_independent_integrity_rerun.txt`.

## Mathematical classification judgment

The definition guards for `reverseDigits` are disjoint and cover the complete
formal input range `1..1000`: one, two, and three decimal digits plus the
endpoint `1000`. The two equations for each parity indicator are complementary
definitions. They directly encode the postcondition's reference counts and are
relevant to the source problem.

Under `semantic.k`, `run` binds `n`, executes the actual AST body through
assignments and conditionals, and returns its evaluated tuple. `verifyRange`
does this for each input from 1 through 1000 and `expect` compares the returned
tuple with cumulative indicator counts. Thus the harness rules are operational;
they do not provide an oracle that bypasses the source body.

As an additional independent adequacy check, I reimplemented the inspected
frozen operational arithmetic and separately constructed a decimal-string
palindrome oracle. For every `n` from 1 through 1000:

- `reverseDigits` matched actual decimal reversal;
- cumulative K even/odd indicators matched the frozen program result; and
- the frozen program result matched the separate palindrome-counting oracle.

All three mismatch counts were zero. Boundary/adversarial samples included
`1, 3, 9, 10, 11, 12, 99, 100, 101, 111, 999, 1000`.
Evidence: `evidence/29_classification_semantics_check_rerun.txt` and its source
`evidence/classification_semantics_check.py`.

This confirms a genuinely empty domain-lemma set:

- `DEFINITION`: 9
- `OPERATIONAL_RULE`: 3
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

## Hash and manifest bindings

An independent implementation of the exact Stage 6 pipeline-tree framing and
Stage 4 export-tree framing reproduced all signed resolution hashes:

- signed resolution:
  `5849d3b50ef8e7315f0a84b0ad5ee53ec8a17b2bc2502c7f29431bfc78f4fa4a`
- K workspace tree:
  `ff8e16685621a8cf2585a69304cda4ce958c77e4756f9a7eaa896006834b9d0d`
- Stage 1 export tree:
  `f4df5b29d0b5d0072cb460156fab3683072c20af09a9143f1dbdb9bd64a9fdf3`
- selected K audit tree:
  `5eab0643cbeb714f0d5389154c28b41413ac6b1d964230dfb99c1fb2a315e64c`
- selected Stage 4 generation tree:
  `132657c0b56402d38ec9bccb0de8dee5d150ad385278cd0f155cbd7815229f8f`
- producer-source tree:
  `7842dfdb780f81b6cfd701655ba9f06a02f4508773479d01d45a46276c743ea5`
- generated project tree:
  `94e3d600546dd7ff73fee97b8de56e65c42e107570099391adc917f523e4d475`
- discovery manifest:
  `f430fe0c1991010ec1f9e4171502c49a113e450227242729a25885fd18f6696b`

Every per-file Stage 1 source hash also matched, with no source-manifest
omission or extra file. The selected artifact hashes, input manifest,
generator provenance, export result, historical preflight, obligation-map
hash, and trust-inventory hash all reconcile. The initial independent hash
script used the wrong trusted tree-framing variant and failed visibly in
`evidence/25_independent_integrity.txt`; after inspecting the Stage 6 pipeline
contract, the corrected independent implementation passed in
`evidence/27_independent_integrity_rerun.txt`.

## Stage 4 obligation and target identity

The independently classified `DOMAIN_LEMMA` list is empty. The deterministic
generation records are bijective with that empty set:

- `input-manifest.json.source_rules`: empty;
- `obligation-map.json.source_rules`: empty;
- `obligation-map.json.obligations`: empty;
- `obligation-map.json.trust_parameters`: empty; and
- all generator/export/preflight obligation counts: zero.

There are therefore no omitted, duplicated, irrelevant, weakened, or vacuous
conjuncts. Importantly, Stage 4 did not encode the empty conjunction as `True`:
`generator-manifest.json`, the preflight, and the audit input all record target
`null`, and an independent scan found zero `def targetStatement`
declarations. The fixed generated target is exactly “no target.”

## Fresh mechanical preflight

I invoked `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and the required frozen workspace, discovery manifest,
generation, and pinned toolchain lock.

The first invocation reached `lake clean` but exposed an audit-container
infrastructure quirk: processes reported namespace PID 5 while `/proc/5/exe`
was absent, and Lean's runtime uses `/proc/<pid>/exe` to locate itself. This is
recorded in `evidence/07_fresh_check_generation.txt` and
`evidence/18_proc_pid_resolution.txt`.

I compiled the disclosed audit-local shim
`evidence/proc-self-shim.c`, which redirects only the affected
`/proc/<current-pid>/exe` lookup to `/proc/self/exe`, and reran the unmodified
trusted checker. It returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean` exit 0;
- `lake build` exit 0;
- build output SHA-256
  `b9f5d3be03266da54dd438986e86258090bac7d9202466a56b361e21f568dd9d`;
- generated tree hash
  `94e3d600546dd7ff73fee97b8de56e65c42e107570099391adc917f523e4d475`;
- obligation count 0;
- target `null`; and
- designated sorry count 0.

This exactly matches the recorded Stage 4 preflight. The complete successful
returned evidence is
`evidence/20_fresh_check_generation_with_proc_shim.txt`; the shim build and
direct clean build are in `evidence/19_proc_shim_build_and_test.txt`.

## Stage 5 and final legitimacy

The signed launcher mode is `CLASSIFICATION_ONLY`, and the environment agrees.
The audit input has null Lean workspace, invocation, hashes, target, and Stage 5
result. `/candidate` is absent. This is exactly required for a genuine
`KLEAN_NO_OBLIGATIONS` result, so no Stage 5 clean build, `Proof.final`, axiom
print, proof identity, or operational-bridge parameter audit applies.

The raw command/result index is `evidence/30_evidence_index.txt`.

VERDICT: PASS
LEGITIMACY: LEGIT
