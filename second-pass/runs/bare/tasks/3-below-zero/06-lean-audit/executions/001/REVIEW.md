# Independent audit: `3-below-zero`, `bare`, `GENERATED_SEMANTICS`

## Outcome

The protected Stage 3 classification is mathematically correct, and its true
domain-lemma set is empty. The selected Stage 4 result therefore legitimately
has no obligations, no generated target, and no Stage 5 candidate. All mounted
artifact, source, manifest, and tree bindings recompute exactly, and the trusted
Stage 4 preflight passes.

There is one non-legitimacy-blocking provenance concern: the generator manifest
identifies an older generator image and records exporter/Klean source hashes
that do not match the currently mounted trusted tool revision. A diagnostic
regeneration with the current revision preserves the empty obligation set and
empty target but does not reproduce the selected generated tree byte-for-byte.
Because there is no theorem or proof candidate in this mode, this does not
weaken or replace any proof obligation, but it prevents an unqualified claim
that the historical generator source was independently reproduced.

## Scope and trust handling

`AUDIT_MODE` and `/audit-input.json` both say `CLASSIFICATION_ONLY`.
`/candidate` is absent, both Lean workspace/invocation hashes are null, the
recorded target is null, and the selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`. Consequently, the conditional Stage 5 clean-build,
`#print axioms Proof.final`, proof-identity, and operational-parameter checks do
not apply.

Candidate and provenance content was read only as evidence. No mounted
candidate/provenance script was executed. The only executable pipeline code was
the trusted code under `/reference/tools`, plus audit-local inspection and
environment-compatibility helpers recorded in
`evidence/COMMANDS.md`.

## Rule-inventory reconstruction

I invoked `tools.k_rule_inventory.inventory_verification` on
`/reference/k-proof` and separately recomputed each returned span slice,
whitespace-normalized text, SHA-256, `source_rule_id`, and canonical JSON
inventory hash. The trusted local closure is exactly module `VERIFICATION`;
the imported `SEMANTIC` module is in the required external `semantic.k`, not a
local module in `verification.k`.

| Order | Span | Normalized SHA-256 / source identity | Attributes |
|---|---:|---|---|
| 1 | 11–11 | `fcdc37ffe1758064b9da7c725e0ad61a78f240a75ea058014581fdc375edabf6` / `rule-fcdc37ffe1758064b9da7c725e0ad61a78f240a75ea058014581fdc375edabf6` | none |
| 2 | 12–16 | `8b7947851f91e86a240db6f33eb6cf303d12fbe3055e203d3b910d4df3445b39` / `rule-8b7947851f91e86a240db6f33eb6cf303d12fbe3055e203d3b910d4df3445b39` | none |

The reconstructed `verification.k` hash is
`2bcf4b98c0ab283190e7f18d67ce40c4995229a5b61c9382dcceef818ea945c8`;
the whole rule inventory hash is
`d5def0ac85eed79dfa1a0f725d488b12243abe197cf40deeb8118eb10add9ab3`.

The protected manifest contains exactly these two identities, exactly once and
in this order. Its inventory hash is exact. There are no omissions,
duplicates, extras, reordered identities, changed rule hashes, unexpected
fields, or unaccounted classifications. The trusted Stage 3 contract validator
also accepts it. Complete reconstruction evidence is in
`evidence/inventory.transcript`.

## Independent classification judgment

The two rules are:

1. `belowZeroFrom(_, .IntList) => false`.
2. On `cons(I, IS)`, test `B +Int I <Int 0`; return `true` if so, otherwise
   recurse as `belowZeroFrom(B +Int I, IS)`.

Both are `DEFINITION`, independently of the protected rationales:

- `belowZeroFrom` is explicitly declared as a total K function. The first rule
  is its empty-list base equation.
- The second rule is its structurally descending recurrence over the tail
  `IS`.
- Together they cover the two constructors of the frozen `IntList` sort and
  define a named execution-summary value. They do not assert an algebraic fact
  about a previously defined function.
- Their left-hand sides are summary-function applications, not program
  configurations or operational terms. They do not preempt or replace ordinary
  execution, so neither is an `OPERATIONAL_RULE`.
- Stage 1 does not first prove either exact rule against a module that omits it.
  They are equations present in `VERIFICATION` during the later claims, so
  neither is a `PROVED_DERIVED_LEMMA`.
- They are not `DOMAIN_LEMMA`s: they introduce the meaning of the named
  summary rather than prove a separate mathematical proposition.

This produces the independent partition:

- `DEFINITION`: 2
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

There are no `simplification` attributes in the inventory, so the restriction
that simplification rules be only definitions or domain lemmas is satisfied.

The definitions are relevant and faithful to the frozen program and
postcondition. Operationally, `semantic.k`:

- updates balance to `B +Int I` before the test;
- tests the strict predicate `<Int 0`;
- returns `true` immediately on the true branch;
- otherwise continues on the tail; and
- after an empty tail executes the post-loop `Return(false)`.

The `loop-correct` postcondition consumes this exact summary at
`BoolV(belowZeroFrom(B, OPS))`. By induction on `OPS`, the empty and cons cases
are precisely the two defining equations above. The source, semantics, and
claim are captured in `evidence/source-semantics.transcript`.

Finite adversarial witnesses in `evidence/semantic-witnesses.transcript`
support the structural argument and distinguish three incorrect mutations:

- `[5, -5]` rejects replacing strict `< 0` with `<= 0`;
- `[-1]` rejects testing before the balance update; and
- `[1, -2, 2]` rejects checking only the final balance instead of every prefix.

These tests are finite evidence; the universal correspondence is the
constructor induction described above.

## Recorded-hash reconciliation

Every launcher-recorded hash with a mounted artifact target recomputes exactly:

| Binding | Recomputed SHA-256 |
|---|---|
| Stage 1 pipeline workspace tree | `639f7233b9f8918bec0053d213458ef1f8a66a190c4488c1b19e0914a5bd2f91` |
| Stage 1 export tree | `35f8b4a7665b79e10c58099547dd158321a19689874d8c9c48f1404e6813fa42` |
| Stage 2 selected audit tree | `f9f7ea334caeb7a209c1548fa0783979f556d6aa211f3eaab9ee5bf78da925b9` |
| Stage 3 discovery manifest | `fabd7fe1b139d97c12d50b5f3c99abdc197b5c295867fe6cec8f84d4eb320fdc` |
| Stage 4 selected generation tree | `e1e4ced1a529bdde4d102a6e55e2114976406702c38112548934d17d3bbe0bf1` |
| Stage 4 generated-project tree | `322f088531b9f1e7bddd6b3fa06f63af841d42455cea66d6f0608892a6437245` |

All 240 per-file Stage 1 source hashes match with no missing, extra, or changed
path. The selection artifact hashes match their mounted trees. Lean
workspace/invocation hashes are both correctly null. See
`evidence/hashes.transcript`.

I also independently reconciled every content binding in the Stage 4 sidecars:

- input-manifest Stage 1, discovery, verification, inventory, and all four
  classification partitions;
- generator-manifest generated-tree, obligation-map, toolchain lock, and
  provenance hashes;
- export-result Stage 1, discovery, generated-tree, and trust-inventory hashes;
- recorded preflight Stage 1, discovery, and generated-tree hashes; and
- the exact copy of the preflight document embedded in the audit input.

All these comparisons pass; see
`evidence/stage4-comprehensive.transcript`.

## Stage 4 source/obligation bijection and target identity

The independently classified domain set is genuinely empty. It agrees exactly
with all of:

- `input-manifest.json` `source_rules = []`;
- `obligation-map.json` `source_rules = []`;
- `obligation-map.json` `obligations = []`;
- `obligation-map.json` `trust_parameters = []`;
- both recorded obligation counts being zero; and
- export/preflight status `KLEAN_NO_OBLIGATIONS`.

Thus the source-rule/obligation mapping is a bijection between two empty sets;
there can be no omitted, duplicated, irrelevant, weakened, or vacuous
conjunct. `tools.klean_export.expected_target_definition` returns null,
`tools.klean_export.target_statement` returns null, the generator target is
null, and `Klean3BelowZero/Lemmas.lean` contains no declaration. The fixed
generated target is therefore exactly “no target,” not a changed or weakened
proposition. `/candidate` is absent as required.

The generic generated prelude contains 41 non-propositional trust declarations,
all matched by `trust-inventory.json`; they prove no target because there is no
target. The trusted preflight independently rejects proposition trust and
reported the same count.

## Trusted preflight rerun

The required direct call to `tools.klean_preflight.check_generation` was run
with `PYTHONPATH=/reference` and the three specified frozen inputs. The first
run reached the isolated build but exposed an audit-sandbox incompatibility:
Lean 4.22 constructs `/proc/<getpid()>/exe`, while this PID namespace exposes
the executable only through host-relative `/proc` or `/proc/self`. The exact
failure is retained in `evidence/preflight.transcript`.

The audit-local `evidence/host_pid_shim.c` changes only `getpid()` for the
audited command tree, reporting the host PID read from `/proc/self`. It does
not modify a mounted input, generated source, preflight predicate, build
command, or result. A direct pinned-toolchain clean build with this compatibility
shim succeeded; its complete terminal output is in
`evidence/toolchain-repair.transcript`.

The trusted `check_generation` retry then returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean` exit 0 with empty-output hash
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build` exit 0 with output hash
  `882e1a85708a6f08f9f08dd7511cd843635b7a4db64989e72788d0226167b31a`;
- obligation count 0;
- target null; and
- all frozen-input and generated-tree hashes unchanged.

Those diagnostic hashes exactly reproduce the selected preflight record. The
complete returned evidence is `evidence/preflight-retry.transcript`.

## Provenance concern

The selected manifest records historical generator image
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`,
whereas this audit runs in image
`sha256:38016c41eeac2fcc74430bc6f594c88197f0c9afc0a12a22fea01c83372b7252`.
Correspondingly:

| Tool | Historical recorded hash | Current mounted trusted-tool hash |
|---|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` | `92e9515ae1e4c5275b0cd366e5ff5c16ad35af1afdaf070ef1ae7c0980998964` |

The historical source files themselves are not among the mounted inputs, so
those two historical source hashes cannot be independently rederived from the
current revision. A current-tool regeneration, recorded in
`evidence/regeneration.transcript`, still yields zero obligations, a null
target, the same frozen-input/discovery hashes, and the same trust-inventory
hash. Its generated tree is
`4669f29221c990f95810793f4e74f578c725be3f68604b86609473ba9e5e04e5`
rather than the selected `322f...`; the complete diff in
`evidence/regeneration-diff.transcript` is limited to definition/instance order
and an added Lake resource-argument line.

This is a reproducibility/provenance concern, not an operational-bridge or
proof-trust escape. Independent classification establishes that there is no
domain proposition to generate, and no target or proof candidate exists that
could exploit the revision difference. The selected payload remains exactly
bound to all of its own recorded content hashes and passes the current trusted
mechanical gate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
