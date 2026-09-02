# Independent Stage 3–5 audit: `90-next-smallest`

## Scope and result

The signed launcher input and `AUDIT_MODE` both select
`CLASSIFICATION_ONLY` for condition `bare` and semantics mode
`GENERATED_SEMANTICS`. Stage 4 is selected as
`KLEAN_NO_OBLIGATIONS`. I treated the mounted Stage 1–5 artifacts, prior
reviews, logs, comments, and rationales as untrusted evidence. The conclusions
below come from fresh hashing, the trusted inventory/preflight code, and an
independent reading of the frozen source and operational K rules.

The protected Stage 3 classification is correct. The sole local verification
rule defines the named postcondition summary; it is not a domain lemma,
operational shortcut, or claimed derived theorem. Therefore the true
domain-lemma set is empty. Stage 4 has an exact empty source-rule/obligation
bijection, generates no target, and correctly has no Stage 5 candidate.

## Producer-source provenance

I hashed the generation-time sources before judging Stage 4:

- `/reference/generation-tools/klean_export.py`:
  `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0`
- `/reference/generation-tools/klean.py`:
  `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13`

Both hashes equal the per-file values in `source-manifest.json` and
`generator-manifest.json`. The bundle contains exactly those two sources and
`source-manifest.json`. Its pipeline tree hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
equal to `/audit-input.json`.

The source manifest and generator manifest both record immutable generator
image
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`.
The producer-source path recorded in `/audit-input.json` has the same digest
as its final path component. There is no missing or mismatched producer source
and hence no producer-provenance infrastructure error.

## Canonical inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against
`/reference/k-proof`. The selected verification module is `VERIFICATION`; its
local import closure inside `verification.k` contains only `VERIFICATION`.
The reconstruction found exactly one rule:

| Field | Reconstructed value |
|---|---|
| Source span | lines 9–12 |
| Normalized SHA-256 | `f5e05fc9a552c9b3fec872a9cab3d805625f03178e4c821cde0d4317e5a023e9` |
| Source rule ID | `rule-f5e05fc9a552c9b3fec872a9cab3d805625f03178e4c821cde0d4317e5a023e9` |
| Attributes | empty |
| Verification file SHA-256 | `67dea9ad08a3283efc112894419499146c7965ad90ad0e0ee45781872989d1fd` |
| Whole inventory SHA-256 | `4bd64b8af2c00bb31447cbf7ac369a13d5dc3fb553e960d449f39dcb9b124483` |

The protected discovery manifest contains exactly that ID, exactly once, in
the canonical order, and records the same inventory hash. The trusted
`validate_trust_boundary` check also accepts the bijection. There are no
omitted, duplicated, extra, reordered, or hash-changed inventory entries.

## Independent classification judgment

The rule is:

```k
rule secondSmallest(L)
  => iteVal(lenInt(uniqueSort(L)) >Int 1,
            itemAt(uniqueSort(L), 1),
            none)
```

My classification is `DEFINITION`, agreeing with Stage 3.

`secondSmallest` is freshly declared in `verification.k` as a total function.
The rule exhaustively unfolds that named summary for arbitrary `L`; it does not
state a fact about two already defined expressions. The symbol occurs only in
its declaration/equation and as the final `<result>` term in `spec.k`. It
never matches a source-program execution term, so it does not preempt or
accelerate operational execution.

The right-hand side is also the exact frozen operational result:

- `set` followed by `sorted` produces `uniqueSort(L)`;
- assignment stores `pyList(uniqueSort(L))`;
- `len` produces `lenInt(uniqueSort(L))`;
- the comparison is against integer `1`;
- subscript at index `1` produces `itemAt(uniqueSort(L), 1)`;
- Python `None` is modeled by `none`; and
- the modeled conditional result is `iteVal`.

For empty lists and lists with one unique element, the condition is false and
the result is `none`. For lists with at least two unique elements, position
one of the ascending duplicate-free list is returned. This matches both the
frozen source implementation and postcondition. The rule is not a
`DOMAIN_LEMMA`; it merely names this expression. It is not a
`PROVED_DERIVED_LEMMA`, because Stage 1 does not first prove the same rule in a
module that omits it. It is not an `OPERATIONAL_RULE`, because it is not an
execution or observation step.

The rule has no `simplification` attribute. Thus the simplification policy is
satisfied directly, and there are no other entries to check. The independent
classification counts are:

- `DEFINITION`: 1
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

Consequently the true domain-lemma set is genuinely empty.

## Hash and manifest reconciliation

The signed resolution digest
`e9d4ad5c7a70f6e70f410500731f054ea44e2cecfa6d501b8d6de5cb265b0bae`
recomputes correctly. Every regular Stage 1 source file, including the recorded
bytecode file, matches the source-hash map. The two intentionally different
Stage 1 tree schemes both match their recorded fields: the pipeline artifact
tree hash is
`69ce4d6d8781a01b697aefa0f90c41c29975b575695531e6b030819a6eb7013f`,
and the Klean export tree hash is
`09a7d9877d43ad852af7ca88c92153d12140f0d553987d06159585900f0da409`.

The selected K-audit tree, whole Klean-generation tree, discovery file,
producer-source bundle, and generated-project tree all match both the signed
resolution and relevant selection/manifests. The generated tree hash is
`a3b9d2c1f6b0f7ef4b8accfb919a48d7c91faa98f28a55fd3f88f436ff65e293`.
The generator toolchain object exactly equals
`/reference/klean-toolchain.lock.json`. The input manifest, generator
provenance, export result, and recorded preflight all agree on the frozen
Stage 1 hash, Stage 3 manifest hash, inventory hash, and generated-tree hash.
The complete machine-readable reconciliation records every comparison as
passing.

## Stage 4 obligation and target identity

The independently derived domain source-rule list is empty. It agrees exactly
with:

- `input-manifest.json` `source_rules`;
- `generated/obligation-map.json` `source_rules`;
- the obligation list; and
- the trust-parameter list.

All four lists are empty. The generator and export result both record
obligation count zero. The obligation-map file hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest.

With no domain rules, there can be no omitted, duplicated, reordered,
irrelevant, weakened, or vacuous generated conjunct. The trusted expected-target
constructor returns `None`; independent target parsing returns `None`; a raw
scan finds zero `def targetStatement` declarations; and the generator
manifest, recorded preflight, and audit input all have `target: null`. Thus the
fixed generated target is correctly absent rather than changed.

## Fresh mechanical preflight

The first direct preflight attempt exposed a container PID-namespace defect:
Lean 4.22 tried to resolve `/proc/<namespace-pid>/exe`, but the mounted `/proc`
does not expose that namespace-local PID. I recorded the exact initial failure.
I then compiled a narrow local `LD_PRELOAD` shim under `/tmp/audit-work` that
redirects only `/proc/<digits>/exe` reads to the valid `/proc/self/exe`.
It changes no mounted input or generated source. With the shim, the pinned tools
reported Lean 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and Lake 5.0.0.

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and the required Stage 1, discovery, generation, and toolchain-lock paths. The
fresh result is byte-for-data equal to the recorded preflight:

- status: `KLEAN_NO_OBLIGATIONS`
- `lake clean`: exit 0, empty output
- `lake build`: exit 0, all generated modules built
- obligation count: 0
- target: `null`
- designated sorry count: 0
- trust declaration count: 41

The complete returned JSON, including command output and output hashes, is
saved in `evidence/preflight-result.json`.

## Stage 5 applicability

Stage 5 proof auditing is not applicable. The signed mode is
`CLASSIFICATION_ONLY`, the independently established domain set is empty, and
Stage 4 has no target. `/candidate` is absent, the signed Lean workspace and
invocation hashes are null, and `stage5_result` is null. This is exactly the
required no-obligation shape. Running `#print axioms Proof.final` or auditing
target parameters would be inappropriate because neither `Proof.final` nor a
generated target exists.

## Evidence

Raw commands and outputs are under `evidence/`:

- `COMMANDS.md`: exact principal commands
- `producer-provenance.txt`: producer hashes and image identity
- `inventory.json`: fresh canonical inventory
- `classification-judgment.json`: independent per-entry judgment
- `reconciliation.json`: complete hash/manifest/bijection checks
- `preflight-initial-failure.txt`: exact first environment failure
- `lean_proc_exe_shim.c`: exact narrow PID-namespace compatibility source
- `toolchain-shim-check.txt`: pinned Lean/Lake identity
- `preflight-result.json`: fresh returned preflight evidence
- `stage4-structure.txt`: no-obligation, no-target, no-candidate checks
- `symbol-occurrences.txt`: frozen semantic and specification linkage

VERDICT: PASS
LEGITIMACY: LEGIT
