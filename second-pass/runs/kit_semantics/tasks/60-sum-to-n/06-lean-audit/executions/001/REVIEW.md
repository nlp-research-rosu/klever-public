# Independent audit: HumanEval `60-sum-to-n`

## Scope and result

I audited Stage 3 classification and Stage 4 generation for condition
`kit-semantics` under `SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and
`/audit-input.json` say `CLASSIFICATION_ONLY`; `/candidate` is absent. That is
the required shape for the selected Stage 4 status `KLEAN_NO_OBLIGATIONS`, so
the optional Stage 5 proof, `Proof.final`, candidate target-shadowing scan,
axiom print, and parameter bridge checks are not applicable.

I treated the mounted reports, comments, logs, and classifications only as
evidence. The conclusions below come from the trusted inventory/preflight code,
the frozen K source and supplied semantics, independently recomputed hashes,
and a fresh generated-project build. I did not rely on either earlier PASS.

## Producer-source provenance gate

Before evaluating Stage 4, I hashed the two mounted generation-time producer
sources:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`

Both values match `source-manifest.json` and `generator-manifest.json`. The
image ID in both manifests is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`,
which matches the basename of the producer-source path recorded in
`/audit-input.json`. The bundle contains exactly the two producer files and its
source manifest. Its launcher-style tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
also exactly matching `/audit-input.json`.

The `6b80...` value visible in the first provenance log is the distinct Klean
exporter tree-digest algorithm, not the launcher's pipeline tree-hash
algorithm. The required pipeline hash is recomputed with the trusted
`pipeline_contract.sha256_tree` in evidence 04 and 12 and matches `388c...`.
There is no producer-source infrastructure error.

## Inventory reconstruction and bijection

I ran `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference` against `/reference/k-proof`. The local module closure
is, in order, `VERIFICATION-SYNTAX` and `VERIFICATION`; the syntax module has no
rules. The frozen `verification.k` SHA-256 is
`facb0f5bace95b9bc17419afeceb08226404010079a9cbd3478d8222047b34f0`,
and the canonical whole-inventory hash is
`3017b8701327f8ebc811769d3af6ecf7861928f49d848164daa10a03d34e3d3b`.

The reconstructed inventory is exactly:

| Order | Source span | Normalized hash / `source_rule_id` | Independent class |
|---|---:|---|---|
| 1 | lines 13–14 | `61eabb962d387664fc1888e2526053dbc025e35fe1bb15e488f84221b246fa4e` / `rule-61eabb962d387664fc1888e2526053dbc025e35fe1bb15e488f84221b246fa4e` | `DEFINITION` |
| 2 | lines 15–16 | `dc2a2ab329f437ecc03ad7c3e85423ec0880b778f416b2bf8437887f41d0f999` / `rule-dc2a2ab329f437ecc03ad7c3e85423ec0880b778f416b2bf8437887f41d0f999` | `DEFINITION` |

The protected Stage 3 manifest contains these two IDs exactly once and in this
same order. Its stored inventory hash, each source span, normalized hash, and
classification association match the reconstruction. There are no omissions,
duplicates, extras, reordered identities, or unaccounted entries. The trusted
`validate_trust_boundary` check also succeeds. Neither rule has a
`simplification` attribute; there is therefore no simplification rule assigned
an impermissible class.

## Independent classification judgment

Both rules define the fresh total function symbol `sumToN : Int -> Int`:

1. For `N >= 0`, `sumToN(N)` is defined as `N *Int (N +Int 1) /Int 2`.
2. For `N < 0`, `sumToN(N)` is defined as `0`.

These are genuine definitions, not operational rules or disguised domain
lemmas. Their left sides contain only the named mathematical summary. They do
not match `<k>`, a call, a loop, a continuation, an environment, a scope, or
any observable MPY state. A search of the frozen semantics finds no `sumToN`;
outside its declaration/equations it occurs only in the loop claim's final
accumulator and the positive postcondition. Thus neither rule preempts or
accelerates program execution.

The supplied operational semantics independently gives the relevant behavior:
closure calls bind the parameter and execute the body; `While` evaluates its
guard and either executes the body followed by the next loop head or exits;
integer `AugAssign` updates `total` by addition and `n` by subtraction; and
`Return` restores the call frame with the computed value. Consequently one
positive iteration changes `(total, n)` to `(total + n, n - 1)`. The summary
has base value `sumToN(0) = 0` and, for every positive integer, satisfies
`sumToN(n) = n + sumToN(n - 1)`. The product `n(n+1)` is even, so the `/Int 2`
closed form is exact on this branch. For negative inputs the frozen program's
guard is false immediately and it returns zero, agreeing with the second
definition.

Concrete adversarial witnesses `-100, -3, -1, 0, 1, 2, 5, 10, 30, 100` all
agree with the frozen loop and the two equations; the recurrence check has no
mismatch for `1..1000`. Counterfactual mutations (`total += n + 1` and
`n -= 2`) produce 20 and 9 respectively at input 5 instead of the frozen
summary 15, showing the summary is sensitive to the relevant operational
behavior rather than a constant or identity convenience.

The Stage 1 loop reachability claim is what connects fixed execution to this
named result. The equations themselves merely give the fresh name its
mathematical meaning. There are no `OPERATIONAL_RULE`,
`PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA` inventory entries. In particular,
there is no purported derived lemma for which a prior bridge-free proof would
need to be located, and no relevant domain fact has been hidden in another
category. The independently determined true domain-lemma set is genuinely
empty.

## Stage 4 hashes, source-rule bijection, and target identity

The independent hash audit matched every launcher-recorded hash:

- Stage 1 pipeline tree: `e5d3e652...c8a14c`
- Stage 1 exporter tree: `f83b19cd...71069b`
- Stage 3 manifest: `0735921b...7dee5`
- selected Stage 2 audit tree: `fefbd571...d9b6e5`
- selected Stage 4 generation tree: `a1d6f8c1...071e5`
- producer-source bundle: `388cac39...5f11e`
- generated project: `7df7df1a...1be1f`
- Lean workspace and invocation: both null, as required by this mode.

All 774 individual Stage 1 source-file hashes recorded in `/audit-input.json`
were present and matched, with no missing, extra, or changed entry. Generator
provenance matches the Stage 1 exporter hash, Stage 3 hash, inventory hash, and
pinned toolchain lock.

The Stage 4 input manifest reproduces both definitions exactly and has empty
operational-rule and proved-derived-lemma lists. Because the independent
domain set is empty, the exact expected domain `source_rules` list is empty.
It matches both `input-manifest.json` and `generated/obligation-map.json`.
The obligation map likewise has exactly zero obligations and zero trust
parameters; its hash
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`
matches the generator manifest. Counts and status agree across the generator
manifest, export result, recorded preflight, and independent preflight.

There can be no omitted, duplicated, weakened, irrelevant, or vacuous domain
conjunct in an exact empty-to-empty bijection. The generated `Func.lean`
faithfully contains the guarded nonnegative formula and guarded negative-zero
branch. `target_statement(generated)` independently returns null;
`generator-manifest.json`, recorded preflight, and `/audit-input.json` also all
record a null target, while `Lemmas.lean` contains no target declaration. Thus
the fixed generated target is consistently absent, exactly as required for a
genuinely empty domain set.

## Independent preflight and clean build

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, the required frozen workspace, protected discovery
manifest, selected generation, and trusted toolchain lock. The successful
returned evidence is:

- status: `KLEAN_NO_OBLIGATIONS`
- `lake clean`: exit 0, empty output
- `lake build`: exit 0, all generated modules built, “Build completed
  successfully.”
- obligation count: 0
- target: null
- generated tree hash: `7df7df1a...1be1f`
- designated sorry count: 0
- generated trust declaration count: 41, exactly reconciled with the generated
  trust inventory; the preflight's independent policy found no proposition
  trust.

The first unmodified invocation was preserved because Lake could not locate
its installation. Diagnosis showed an audit-sandbox PID mapping defect:
`getpid()` returned a namespace PID with no `/proc/<pid>/exe`, although
`/proc/self/exe` existed. Lean 4.22 uses that numeric proc path. I compiled a
narrow `LD_PRELOAD` shim under `/tmp/audit-work` that returns the proc-visible
numeric target of `/proc/self`; with it, the pinned Lean binary reports version
4.22.0 and commit `ba2cbbf...`, and the exact trusted preflight completes. The
shim was applied only to the clean-build process and changes no generated or
mounted source. Final tree-hash recomputation confirms every mounted input
remained unchanged. The independent build-log hash differs from the recorded
build-log hash only because independent module build order differed; generated
source and project hashes are identical.

## Stage 5 applicability

No Stage 5 candidate exists, no generated theorem exists, and no
`target.parameters` exist. Creating `Base`, scanning a candidate, running
`#print axioms Proof.final`, and auditing candidate operational bridges would
invent a proof stage forbidden by this `KLEAN_NO_OBLIGATIONS` classification.
Their omission is therefore required, not a gap.

## Evidence index

- [producer hashes and bundle hash](/audit-output/evidence/01-producer-provenance.txt)
  and [launcher-style producer bundle hash](/audit-output/evidence/04-producer-bundle-tree-hash.txt)
- [canonical reconstructed inventory](/audit-output/evidence/02-reconstructed-rule-inventory.json.log)
- [trusted Stage 3 bijection validation](/audit-output/evidence/03-stage3-bijection-validation.json.log)
- [initial unshimmed preflight failure](/audit-output/evidence/05-independent-stage4-preflight.json.log)
- [successful independent preflight and complete returned diagnostics](/audit-output/evidence/07-independent-stage4-preflight-proc-shim.json.log)
- [complete expanded hash, classification-list, obligation, and target comparisons](/audit-output/evidence/12-expanded-independent-hash-bijection-target-audit.txt)
- [sandbox diagnosis and narrowly scoped Lean workaround](/audit-output/evidence/09-lean-proc-sandbox-workaround.txt)
- [frozen source and relevant operational semantics](/audit-output/evidence/14-frozen-source-and-operational-semantics.txt)
- [summary witnesses and counterfactual mutations](/audit-output/evidence/11-summary-witnesses-and-counterfactuals.txt)
- [Stage 4 manifests, generated definitions, empty obligation map/target, mode, and absent candidate](/audit-output/evidence/13-stage4-manifest-and-generated-target-snapshot.txt)

VERDICT: PASS
LEGITIMACY: LEGIT
