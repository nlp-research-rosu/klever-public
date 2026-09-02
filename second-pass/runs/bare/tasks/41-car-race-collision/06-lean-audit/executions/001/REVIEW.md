# Independent Stage 3–5 audit: `41-car-race-collision`

## Scope and audit mode

This audit covers condition `bare`, semantics mode
`GENERATED_SEMANTICS`. Both `AUDIT_MODE` and the canonically verified
`/audit-input.json` select `CLASSIFICATION_ONLY`. Stage 4 is recorded as
`KLEAN_NO_OBLIGATIONS`; the audit input has no target, Lean workspace, Lean
invocation, or Stage 5 result, and `/candidate` is absent.

I treated the mounted candidates, manifests, logs, comments, and earlier
reviews only as untrusted evidence. I did not rely on the earlier Stage 2
verdict or execute the supplied `prove.sh`. Commands used in this audit were
chosen independently and are recorded under `evidence/`.

## Frozen-input and producer authentication

The trusted Stage 6 audit-input verifier accepted the document and recomputed
its canonical `resolved_input_sha256` as
`bb493ea78cd2aba73a3c13b13fb43a980defdc61ff96885cfcc7a1acd39614fc`,
exactly the recorded value.

Before judging Stage 4, I hashed both generation-time producer sources:

| Producer | Recomputed SHA-256 | Recorded SHA-256 |
|---|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` | same |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` | same |

Those values match both `generator-manifest.json` and the exact file map in
`source-manifest.json`. The source manifest and generator manifest both bind
the producer to immutable image
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`.
The final component of the launcher-recorded producer-source path is the same
image digest. The recomputed producer bundle tree hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
matching `/audit-input.json`. Producer authentication therefore passes; there
is no infrastructure `AUDIT_ERROR`.

I also recomputed every launcher-recorded frozen tree/file identity. The Stage
1 pipeline tree, Stage 1 deterministic-export tree, Stage 2 selected audit
tree, Stage 3 manifest, Stage 4 generation tree, generated-project tree, and
all eight Stage 1 source-file hashes match `/audit-input.json`. The principal
values are:

| Artifact | Recomputed identity |
|---|---|
| Stage 1 pipeline tree | `466f421e4955133ed76d488ded0f8c1d10dc513c04b492d43d06ecbae7e4f934` |
| Stage 1 export tree | `b44d47270f8fe8fe5651890ff033b9a9f46e2b81ec234640ac6dda9f31383842` |
| Stage 3 manifest | `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3` |
| Stage 4 generation tree | `74e9f67fec01636e003461b081fc8fe9d43f07caf8f8c266598d0c13d44b26b0` |
| Generated project | `2499c45aedf5811bb3c58aecf6a018315def82bce59dea5ff6122620b6d81259` |

## Independent rule-inventory reconstruction

I called the trusted `tools.k_rule_inventory.inventory_verification` on the
frozen `/reference/k-proof`, independently of the Stage 3 document.
`prove.sh` selects main module `VERIFICATION`. The only local module in
`verification.k` reachable from that module is `VERIFICATION` itself. It
imports `SEMANTIC`, but that module is defined in the separately required
`semantic.k`, not in the local `verification.k` source scanned by the required
inventory algorithm.

The frozen `verification.k` has SHA-256
`4d68669eca55334e7ec3686ae3eb2dc6c166a9120d2a5cffe5fb43c16555061f`.
Its `VERIFICATION` module contains no rules, so the reconstructed ordered rule
list is exactly `[]`. Consequently there are no source spans, normalized rule
hashes, or `source_rule_id` values to omit or duplicate. The canonical hash of
that ordered inventory is
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.

`/reference/lemma-discovery.json` has the same inventory hash and the same
empty ordered list. The trusted Stage 3 trust-boundary validator also accepts
the bijection. There are no omitted, duplicated, extra, reordered, rehashed,
or unclassified local rules.

## Independent classification judgment

Because the canonical inventory is empty, the independent counts are:

| Classification | Count |
|---|---:|
| `DEFINITION` | 0 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

This empty classification is mathematically appropriate, rather than merely
structurally self-consistent. The source solution is exactly:

```python
def car_race_collision(n: int):
    return n * n
```

The postcondition requires the result to be `N *Int N` for `N >=Int 0`.
The nine rules in the frozen generated `SEMANTIC` module:

1. register the function body;
2. look up the function and bind its parameter;
3. begin evaluating a returned expression;
4. evaluate an integer literal;
5. read a name from the environment;
6. begin left-to-right multiplication evaluation;
7. continue with the right operand;
8. apply built-in integer multiplication; and
9. store the returned integer in the result cell.

These are ordinary execution/observation rules in the fixed semantics. They
are not local verification extensions, summaries, recurrences, macros, named
proof terms, simplification facts, or domain mathematics. No rule has a
`simplification` attribute. Stage 1 contains no alleged derived lemma and no
two-phase proof in which a rule is first proved absent and then used later.
There is therefore no relevant domain lemma hidden under another label.

As an operational check, I made a fresh copy under `/tmp/audit-work`, compiled
the unchanged frozen sources with K 7.1.293, and explicitly ran the program at
`N = 0, 3, 10, -2`. The final results were `0, 9, 100, 4`, respectively.
An independently invoked `kprove spec.k --definition
verification-kompiled --spec-module SPEC` returned `#Top`. This confirms that
the source/postcondition connection is discharged by ordinary execution and
built-in multiplication, with no domain lemma.

## Stage 4 manifest, obligation, and target audit

I reran the required
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, the
frozen Stage 1 workspace, protected Stage 3 manifest, selected Stage 4
generation, and trusted toolchain lock.

The first call exposed an audit-sandbox issue: Lean 4.22 could not read
`/proc/<pid>/exe`, which its `IO.appPath` implementation requires. This
prevented `lake clean` before any project compilation. I recorded that failure
and used a narrow `LD_PRELOAD` compatibility shim which substitutes only that
denied procfs read with Linux `AT_EXECFN`; all other `readlink` calls pass
through unchanged. With the shim, the immutable compiler identifies itself as
Lean 4.22.0, commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly the pinned lock.

The unchanged trusted preflight then returned:

- `lake clean`: exit 0, empty output;
- `lake build`: exit 0, all nine build tasks successful;
- status: `KLEAN_NO_OBLIGATIONS`;
- obligation count: 0;
- target: `null`;
- generated tree:
  `2499c45aedf5811bb3c58aecf6a018315def82bce59dea5ff6122620b6d81259`;
- Stage 1 export tree:
  `b44d47270f8fe8fe5651890ff033b9a9f46e2b81ec234640ac6dda9f31383842`;
- Stage 3 manifest:
  `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3`.

The clean/build output hashes exactly equal the original recorded preflight,
including build-output hash
`e355af8679b31264a5179b1a67e619758a1ac779d22fbdbf211163bf43c26682`.

I separately checked the manifest graph rather than treating preflight as a
mathematical verdict:

- `input-manifest.json`, `generator-manifest.json`, `export-result.json`,
  `preflight.json`, and `/audit-input.json` all bind the same frozen Stage 1,
  Stage 3, inventory, and generated-tree identities.
- `generator-manifest.json` exactly equals the trusted toolchain lock in its
  toolchain field.
- The generated `obligation-map.json` byte hash is
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
  exactly the generator-manifest value.
- The trust-inventory byte hash is
  `858bcd964f61e9a911b04dd117fcbbe6ef7455bd82db8e619318068925a9bb0b`,
  exactly the export-result value.
- The independently reclassified domain source-rule list is `[]`;
  `input-manifest.json` has `source_rules: []`; and
  `obligation-map.json` has `source_rules: []`, `obligations: []`, and
  `trust_parameters: []`. Thus the ordered source-rule/obligation mapping is a
  genuine empty bijection, with no omission or duplicate.
- The trusted target-construction function computes no target definition from
  the empty obligation map. The trusted target parser finds no generated
  target. The generator manifest, recorded preflight, and audit input all
  record `target: null`.
- `Lemmas.lean` contains only its namespace and no proposition or proof.
  Hence there is no irrelevant, weakened, duplicated, vacuous, or changed
  conjunct: there are no conjuncts and no target.

The generated base contains 44 allowlisted executable-data axioms for generic
K hooks. The trusted preflight independently reconstructed exactly those 44
declarations, rejected proposition-shaped trust, found no `sorry`, `admit`, or
`unsafe`, and built the project. Because there is no generated proposition or
Stage 5 proof, these base declarations are not being used to discharge a
target.

The Stage 4 `KLEAN_NO_OBLIGATIONS` status is therefore correct for a genuinely
empty independently classified domain set.

## Stage 5 applicability

Stage 5 proof checks do not apply in `CLASSIFICATION_ONLY` mode. Consistently:

- no generated target exists;
- `/candidate` is absent;
- the audit input records no Stage 5 result, Lean workspace, or invocation; and
- there are no target parameters or candidate bridge definitions to audit.

Accordingly, a candidate clean build, `#print axioms Proof.final`, candidate
forbidden-token scan, proof identity check, and operational-bridge adversarial
tests are neither possible nor required. Their absence is the required state
for this valid `KLEAN_NO_OBLIGATIONS` selection.

## Evidence

Key raw commands and results are in:

- [Producer authentication](</audit-output/evidence/01_producer_authentication.txt>)
- [Frozen K sources and protected Stage 3 manifest](</audit-output/evidence/02_frozen_sources_and_stage3.txt>)
- [Independent hash and inventory recomputation](</audit-output/evidence/03_integrity_and_inventory.txt>)
- [Initial preflight failure](</audit-output/evidence/04_recomputed_preflight.txt>)
- [Toolchain and sandbox diagnosis](</audit-output/evidence/05_toolchain_diagnosis.txt>)
- [Sandbox compatibility source](</audit-output/evidence/proc_exe_compat.c>)
- [Pinned Lean identity under the compatibility shim](</audit-output/evidence/13_proc_exe_compat_build_and_test.txt>)
- [Successful required preflight rerun](</audit-output/evidence/14_recomputed_preflight_success.txt>)
- [Generated sidecars and Lean sources](</audit-output/evidence/15_stage4_artifacts.txt>)
- [Empty obligation map, absent target, and absent candidate](</audit-output/evidence/16_zero_obligations_and_no_candidate.txt>)
- [Independent Stage 4 hash/bijection/target checks](</audit-output/evidence/17_stage4_bijection_and_target.txt>)
- [Fresh K operational runs and proof](</audit-output/evidence/18_fresh_k_operational_runs.txt>)

VERDICT: PASS
LEGITIMACY: LEGIT
