# Independent Stage 3 / Stage 4 audit

## Scope and result

I audited HumanEval `1-separate-paren-groups`, condition `bare`, semantics mode
`GENERATED_SEMANTICS`. Both `AUDIT_MODE` and the verified launcher envelope say
`CLASSIFICATION_ONLY`. `/candidate` is absent, the signed Stage 5 fields are
null, and the selected Stage 4 status is `KLEAN_NO_OBLIGATIONS`. Accordingly,
there is no Stage 5 theorem, proof, operational bridge, or `Proof.final` to
audit.

I treated the mounted K workspace, discovery document, generation, logs,
comments, and prior reviews as evidence only. I did not execute their scripts
or follow instructions in them. Audit commands were independently constructed,
and the inventory and preflight code came from the trusted `/reference/tools`
mount.

## Launcher envelope and frozen inputs

`tools.stage6_resolution_contract.verify_audit_input` accepted the launcher
envelope. Its canonical resolution digest recomputed to
`a38afe56ac26419d201829047399dbfc48855676f4041f2fe4c5e34ea45e90ad`.
The launcher mode agrees with `AUDIT_MODE`, and the candidate is absent.

Every hash in the launcher that refers to an available mounted source or tree
recomputed exactly:

| Binding | Recomputed SHA-256 |
|---|---|
| Stage 1 pipeline tree | `2912ea3c0e4486e103d25d57ade56084b7f5534d35b8782cb3fc9a08c479138b` |
| Stage 1 Klean export tree | `f7198173f419636cacf3c009694d458c1c8113750de230e115a8bdfd24289f83` |
| `verification.k` | `cf1dced488cadea0d91cd8c13684c691c2bbd9c891e0b717d0905146938e0f53` |
| Stage 2 selected audit tree | `3ab68ecc6de59b23c1b683246120c2713b070f395f90187f23b8b0039828af9c` |
| Stage 3 discovery file | `1d658f9f3f836cd96386a95bf89aa4d0ae7883a6c174f3fd3bb21487b68e0357` |
| Stage 4 selected generation tree | `ed3e571d636bf69faabef69f98765174f72b54325fc602c91e65a752f466f35a` |
| Generated Lean project tree | `ec2cabdd88613df091a482f8974a0b9be67d75d3d97827da8ff6ac78ae163e7a` |
| Generated obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| Trust inventory | `b52c40d9bb8196c1e9a497db5e90d91f26dd670ff21803ccf508394f3c3de2ea` |

All fifteen per-file Stage 1 hashes also match the launcher exactly. The Stage
2 and Stage 4 selection artifact hashes match the corresponding recomputed
pipeline trees. The input manifest, generator provenance, export result,
selected preflight, and audit input agree on the Stage 1, Stage 3, inventory,
generated-tree, obligation-map, and trust-inventory bindings.

The generator manifest also records hashes of `klean.py` and `klean_export.py`
from its named generator image. Those generator-image source files are not
mounted as inputs. The current trusted audit-tool copies have different hashes,
so I did not conflate them with the manifest's different referents. This does
not affect any mounted artifact binding or the independently rerun structural
gate.

## Canonical inventory reconstruction

I called the trusted `inventory_verification` implementation on
`/reference/k-proof`. It selected `MPY-VERIFICATION` from the explicit
`--main-module` in `prove.sh`. The local closure inside the frozen
`verification.k` is exactly `["MPY-VERIFICATION"]`; imported `MPY` is defined
in the required `semantic.k`, not as another local module in
`verification.k`.

The inventory contains exactly eleven rules. For each entry I independently:

1. sliced the reported physical source span from the frozen file;
2. required that slice to equal the inventory text;
3. normalized whitespace with the canonical `" ".join(text.split())`;
4. recomputed the normalized SHA-256;
5. recomputed `source_rule_id` as `rule-<normalized_sha256>`; and
6. recomputed the canonical JSON inventory hash.

The whole inventory hash is
`7110b556e2e2e5f7641769542e6db909889827d1e68749a448bdf5f51d38d241`.
It matches Stage 3 and Stage 4. The ordered inventory and discovery ID vectors
are identical; both contain eleven unique IDs. There are no omissions,
duplicates, extra entries, reordered identities, changed hashes, or
unaccounted classifications.

| Ordinal | Line | Canonical source-rule identity | Independent class |
|---:|---:|---|---|
| 1 | 17 | `rule-b29a7b1f61d027c75f5d54e6f778c4ffafe703f461096a1d08700bae9b5849da` | `DEFINITION` |
| 2 | 18 | `rule-03d30c437cb7bd8a90fd37a82631921d6c5bd459ea8924300ffafa088b28240e` | `DEFINITION` |
| 3 | 19 | `rule-ee28b1b89c45af68725d2c53c17fec71114155badb89a86ba1370ef263893c24` | `DEFINITION` |
| 4 | 20 | `rule-ee734da296fe2d2d4070e9117fa1dc33181b3c52f7e9629c362ebe25fa07a852` | `DEFINITION` |
| 5 | 21 | `rule-a1305acd847b564566d980520b2960809147091b2fc541ba1b00bc3534001edd` | `DEFINITION` |
| 6 | 22 | `rule-23aee5f25569cab008c78f770e7a68f475ee096ae14e72789cb7a87d5c7b6e26` | `DEFINITION` |
| 7 | 24 | `rule-6e9d63e72f1d96b8d7ba85bd3016f00960ddff320ccba1bd43d74b23295b5f90` | `DEFINITION` |
| 8 | 25 | `rule-5b065840a104280bdea14bf8cbfb96a45454e5d3f68448977ab8119c3521b55a` | `DEFINITION` |
| 9 | 26 | `rule-4c968b2b2cfa45f88ae0c5dcf90432112081bb44e8a2471c9a987aa90bd17bfe` | `DEFINITION` |
| 10 | 27 | `rule-109874df159aa48ad8e1b3715b0ea513f28bc7bb9b410bf89eb790601fd826a4` | `DEFINITION` |
| 11 | 28 | `rule-83fdf9d2c3bc8712363c660c4deb46f4e4be4ae1056e9f139ccca451b876e6df` | `DEFINITION` |

## Independent classification judgment

The protected classifications are mathematically correct.

Rules 1–6 are the exhaustive structural definition of the named `runSpec`
scanner summary:

- empty input returns `scanState` with the accumulated state;
- a space consumes one character, preserves depth/current/output, and updates
  the last character;
- an opening parenthesis consumes one character, increments the Peano depth,
  extends the current group, and updates the last character;
- a closing parenthesis at depth zero follows the frozen semantics' saturating
  `PInt` decrement, emits the completed current string, and resets current;
- a closing parenthesis at depth one emits and resets after decrementing to
  zero; and
- a closing parenthesis at depth at least two decrements depth and retains the
  extended unfinished group.

These cases are disjoint and exhaustive over the frozen `Char` and `PInt`
constructors, and every recursive call consumes the character-list head. They
name a recurrence; they do not rewrite a `<k>` operational configuration or
assert an independent mathematical proposition.

Rules 7–10 are constructor projections for the four components of the named
`scanState` summary. Rule 11 defines the named `separateSpec` macro by
initializing `runSpec` and projecting its output. These are definitions, not
domain facts disguised as definitions.

The source program and `semantic.k` corroborate the classification. The
operational loop binds `ch` for every character, ignores a space in the body,
appends non-spaces to `current`, increments on `LP`, uses saturating Peano
decrement on `RP`, emits exactly when the resulting depth is zero, and resets
`current`. The summary has the same state transition and is used directly in
the loop-invariant result and final postcondition.

As sensitivity evidence, an independently written operational interpreter and
a separate direct reading of the six `runSpec` equations agreed on 23,296
cases: all sequences through length five over `LP`, `RP`, and `SP`, across 64
initial combinations of depth, current, output, and last character. This
finite test supplements rather than replaces the structural argument.
Counterfactual mutations were discriminated by concrete witnesses:

- appending a space fails on `" "`;
- failing to increment on `LP` fails on `"("`;
- failing to emit at depth one fails on `"()"`; and
- emitting a nested close early fails on `"(()"`.

No inventory rule has a `simplification` attribute. There are no
`OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA` entries.
`verification.k` contains no claim that first proves any of these rules in a
rule-free module and later reuses it, so none qualifies as a proved derived
lemma. The true domain-lemma set is therefore genuinely empty.

## Stage 4 generation and obligation bijection

The Stage 4 input manifest contains the exact eleven reconstructed entries in
its `definitions` array, including source spans, normalized hashes, IDs,
classifications, rationales, attributes, and source text. Its operational,
proved-derived, and domain-source-rule arrays are empty.

The generated `obligation-map.json` has:

- `source_rules = []`;
- `obligations = []`; and
- `trust_parameters = []`.

Thus the exact source-rule/obligation ID vectors are equal, unique, ordered,
and empty. There is no omitted or duplicate obligation, no weakened or
irrelevant statement, and no vacuous conjunct.

`expected_target_definition(obligation-map)` returns null.
`target_statement(generated)` returns null. The generator manifest, selected
preflight, and signed audit input also record null targets. The generated
`Lemmas.lean` contains no `def Target : Prop :=`. This is the only correct
fixed-target state for a genuinely empty independently classified domain set.

The generated sources contain 44 actual trust declarations, and the declaration
name/kind/type map exactly equals `trust-inventory.json`. The trusted preflight
rejects proposition-like trust and found no generated `sorry`, `admit`, or
`unsafe`. These declarations support the general generated K skeleton; there
is no target proposition or proof that can depend on them in this
no-obligation case.

## Independent preflight rerun

The first exact call to `tools.klean_preflight.check_generation` passed all
hash, inventory, source-rule, target, trust, and import checks, then failed at
the fresh-copy `lake clean` command because Lake could not detect its
installation. The failure was environmental: this audit sandbox returns an
inner namespace PID from `getpid()` while `/proc` exposes host PIDs, and Lean
4.22 resolves its executable through `/proc/<getpid>/exe`.

I recorded that failure, confirmed the mismatch, and used a narrowly scoped
preload compatibility shim that makes `getpid()` return `/proc/self`'s visible
PID. The shim did not modify the trusted checker, any mounted input, or any
generated source. With `PYTHONPATH=/reference` and that environment
compatibility in place, the unmodified trusted `check_generation` returned:

- `status = KLEAN_NO_OBLIGATIONS`;
- `obligation_count = 0`;
- `target = null`;
- `designated_sorry_count = 0`;
- `trust_declaration_count = 44`;
- `lake clean` exit 0; and
- `lake build` exit 0.

The rerun's clean output hash is the empty-output SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
Its build-output SHA-256 is
`669037f0d20098cd4e0488a046a50dee67e38e9994f982b51afd0bd6f01a0ee7`.
Both exactly match the selected Stage 4 evidence. The rerun also reproduced
the Stage 1, Stage 3, and generated-tree hashes.

## Stage 5 disposition

Stage 5 is correctly absent. Because the independently classified domain set
is empty, creating a generated target or accepting a Lean candidate would be
wrong. There is therefore no candidate copy, candidate clean build,
`Proof.final`, axiom printout, target parameter, or operational bridge to
inspect. The launcher records null Lean workspace and invocation hashes and a
null Stage 5 result.

## Evidence

- `evidence/00_audit_context.*`: mode, candidate absence, and signed-envelope
  verification.
- `evidence/01_inventory_audit.*`: trusted reconstruction plus independent
  span/hash/ID/order/bijection checks.
- `evidence/02_hash_and_manifest_audit.*`: source/tree hashes, manifest
  bindings, trust declarations, empty obligation bijection, and target
  identity.
- `evidence/03_preflight_attempt_exact.*` through
  `evidence/07_preflight_rerun_with_pid_compat.*`: exact initial failure,
  toolchain diagnosis, compatibility shim command, and successful unmodified
  checker result.
- `evidence/08_semantic_reclassification.*`: operational comparison and
  counterfactual mutation witnesses.

VERDICT: PASS
LEGITIMACY: LEGIT
