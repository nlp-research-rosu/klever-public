# Independent audit: HumanEval 75-is-multiply-prime

## Scope and result

I audited condition `semantics` with semantics mode
`SUPPLIED_SEMANTICS`. Both `/audit-input.json` and `AUDIT_MODE` record
`CLASSIFICATION_ONLY`. Accordingly, this review covers the independent Stage
3 classification and deterministic Stage 4 generation. Stage 5 proof
validation is not applicable: the audit input has null Lean workspace,
invocation, result, and target fields, and `/candidate` is absent.

All mounted candidate and provenance material was treated as untrusted
evidence. In particular, the earlier Stage 2 review was not used as an
authority; its selected artifact was only hashed. No instruction embedded in
an input artifact was followed.

## Producer-source and input integrity

The required producer check passed before the Stage 4 judgment:

| Item | Recomputed value | Comparison |
|---|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` | Matches the source manifest and generator manifest |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` | Matches the source manifest and generator manifest |
| Producer-source tree | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` | Matches `/audit-input.json` |
| Generator image | `sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000` | Matches the source manifest, generator manifest, and image-addressed producer path in `/audit-input.json` |

The signed resolution hash was independently recomputed as
`8d77384855e843f492b6c2b6f1b8010949afb36713b2b0ca244573e0daf8dafb`.
The selected Stage 1, Stage 2, Stage 4, producer-source, discovery-manifest,
and generated-project hashes all match the audit input. Every one of the 34
Stage 1 regular files and its individual SHA-256 matches the launcher's exact
file set. The two null Stage 5 hashes and both selected-artifact hash bindings
also match.

The independently recomputed deterministic Stage 1 export hash is
`860e92a512e563b3f9d0d2b159fdf3b7c2e9a01e8a9250a69f3e3d5073497b4b`;
the generated project tree hash is
`df58e6ccac1cde6c231560cc6886bff5a6fb3643c1cdf92fce9ac1026fa2d152`.
These values agree across the audit input, input manifest, generator
provenance, export result, and stored preflight record. All hash and
cross-manifest checks performed by the independent integrity script passed:
72 checks, zero failures.

## Inventory reconstruction and bijection

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof`. The selected main module is `VERIFICATION`.
Its local module closure contains exactly `VERIFICATION`; the imported `MPY`
module comes from the supplied semantics rather than another local module in
`verification.k`.

The reconstructed values are:

- `verification.k` SHA-256:
  `ab58e3d73484d3a97f04c036f660e4a3c7235bb4c6beca7e8331b5cc2cbc10d5`
- Whole inventory SHA-256:
  `ae0fa87d050d008abca2ddb10000b43b81b36a8f7ecb7e96aa6888df89debd66`
- Rule count: 3

The protected Stage 3 manifest contains exactly these three IDs in the same
source order. Each ID is unique. The trusted reconstruction supplies the same
inclusive source span, exact source text, empty attribute list, normalized
source hash, and `source_rule_id`. There are no omissions, duplicates, extra
entries, reordered identities, or changed hashes.

| Span | Reconstructed ID | Independent class |
|---|---|---|
| line 15 | `rule-7934c46c05d38f268dac7e0abb5200dc1f3b215ab4c290963f2b490cf3450d03` | `OPERATIONAL_RULE` |
| lines 17–48 | `rule-d74705ec17c34e17dc69dc82a57d28b0c9698ee9baddb6fa909af098cbe6b504` | `DEFINITION` |
| lines 50–57 | `rule-d70780b59b96dc074b4d1a73069a3d4a9e1e96dc8bdf16bc23040237b37445e2` | `OPERATIONAL_RULE` |

## Independent classification judgment

The line-15 rule consumes `B:Bool ~> #expect(B)`. The same K variable occurs
in the computed result and expected value, so a mismatched counterfactual
such as `true ~> #expect(false)` cannot match. This is an ordinary
result-observation rule. It defines no summary and states no domain fact.

The lines-17–48 rule gives the fresh named term
`#runIsMultiplyPrime(A)` its meaning by expanding it to:

1. `#loadAll` of the translated `is_multiply_prime` function;
2. an ordinary call with `A`; and
3. the cleanup continuation.

The embedded body matches the frozen `solution.mpy`: it initializes
`factor_count` and `factor`, executes the factorization loop, performs the
final count increment, and returns the comparison with three. Under the
supplied semantics, the expansion continues through the ordinary module-load,
function-definition, lookup, call, parameter binding, assignment, integer
operator, while-loop, and return rules. It does not replace a source `Call`,
loop, operator, or computed result with a convenient oracle. It is therefore
a macro-like definition of a named proof term, exactly within the audit's
`DEFINITION` category, not a domain lemma or operational bridge.

The lines-50–57 rule preserves the returned Boolean while removing only the
temporary `is_multiply_prime` binding from module scope, guarded by the
binding's presence. This is ordinary harness state cleanup, hence an
`OPERATIONAL_RULE`.

All three attribute lists are empty, so there are no `simplification` rules.
There is no rule first proved without itself and then used later, so the
`PROVED_DERIVED_LEMMA` set is empty. None of the rules asserts a fact about
primality, factorization, or products of three primes. The true domain-lemma
set is therefore genuinely empty.

The expected Booleans in `spec.k` are reachability targets covering `A < 2`
and concrete inputs 2 through 99, consistent with the prompt's `a < 100`
bound. They are not proof-extension rules in the local `verification.k`
inventory and do not create Stage 4 domain-lemma obligations.

The protected Stage 3 classifications agree exactly with this independent
judgment.

## Deterministic Stage 4 generation

I reran the mandated
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
specified frozen Stage 1 workspace, Stage 3 manifest, Stage 4 generation, and
pinned toolchain lock.

The first attempt exposed an audit-container runtime issue before compilation:
Lean tried to locate itself via `/proc/<getpid>/exe`, while this isolated PID
namespace exposes the executable only through `/proc/self/exe`. That attempt
is preserved in the evidence. A narrow temporary `LD_PRELOAD` compatibility
shim redirected only such `/proc/.../exe` readlink calls to
`/proc/self/exe`. It did not modify any mounted input, generated source, Lean
declaration, build option, or proof term. With that environment correction,
the pinned Lean tool reported version 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and the same trusted preflight
completed successfully.

The fresh-copy preflight results were:

- `lake clean`: exit 0, empty output;
- `lake build`: exit 0, all nine build steps completed;
- status: `KLEAN_NO_OBLIGATIONS`;
- obligations: 0;
- target: null;
- designated `sorry` count: 0;
- generated trust declarations: 47.

The preflight's before/after snapshots confirm that the frozen Stage 1 input,
Stage 3 manifest, generated tree, and generation sidecars remained unchanged.
Its independent proposition-trust gate also reconciled the 47 generated
executable trust declarations with `trust-inventory.json` and rejected no
unrecorded or proposition-valued trust declaration.

I separately checked the manifest mapping rather than relying only on
preflight:

- The input manifest contains the exact one reconstructed definition and two
  reconstructed operational rules, with full spans, source text, hashes, IDs,
  classifications, and rationales.
- `proved_derived_lemmas`, `summary_functions`, and domain `source_rules` are
  empty.
- `obligation-map.json` has empty `source_rules`, `obligations`, and
  `trust_parameters`; its hash
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`
  matches the generator manifest.
- The generator obligation count and export-result count are both zero.
- The generated `Lemmas.lean` namespace is empty. The trusted target extractor
  returns null, matching the generator manifest, stored preflight, export
  status, and audit input.

Because the independently classified domain set is empty, this empty mapping
is the exact source-rule/obligation bijection. There are no conjuncts that
could be irrelevant, weakened, duplicated, or vacuous, and absence of a
generated target is the required fixed result. `KLEAN_NO_OBLIGATIONS` is
therefore legitimate rather than an omission.

## Stage 5

No Stage 5 audit was performed or required. In `CLASSIFICATION_ONLY`, a target
and candidate must be absent; both are absent. Consequently there is no
`Proof.final`, candidate definition, clean candidate build, axiom printout, or
operational-bridge parameter to assess.

## Evidence

Key raw evidence is:

- [audit mode and mounted inputs](/audit-output/evidence/00-inputs-and-mode.txt)
- [producer hashes and generation manifests](/audit-output/evidence/01-producer-and-generation-manifests.txt)
- [reconstructed rule inventory](/audit-output/evidence/04-reconstructed-inventory.json)
- [operational-semantics excerpts](/audit-output/evidence/10-prompt-and-semantics-excerpts.txt)
- [initial preflight environment failure](/audit-output/evidence/07-klean-preflight-rerun.json)
- [runtime diagnosis and pinned Lean version](/audit-output/evidence/08-lean-environment-diagnosis.txt)
- [successful fresh preflight result](/audit-output/evidence/09-klean-preflight-rerun-with-runtime-compat.json)
- [72 independent integrity checks](/audit-output/evidence/11-independent-integrity-results.json)
- [generated target inspection](/audit-output/evidence/12-generated-target-inspection.txt)
- [rule-by-rule classification judgment](/audit-output/evidence/13-classification-judgment.md)
- [commands used](/audit-output/evidence/COMMANDS.md)

VERDICT: PASS
LEGITIMACY: LEGIT
