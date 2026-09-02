# Independent audit: HumanEval `92-any-int`

## Scope and result

This audit covers condition `bare`, semantics mode `GENERATED_SEMANTICS`, and
the launcher-selected mode `CLASSIFICATION_ONLY`. The `AUDIT_MODE` environment
variable and `/audit-input.json` agree. Stage 4 is recorded as
`KLEAN_NO_OBLIGATIONS`; no Stage 5 workspace, invocation, result, target, or
`/candidate` mount exists.

I treated all mounted candidate and provenance prose, logs, comments, and prior
verdicts as untrusted evidence. I did not execute `prove.sh`, prior audit
scripts, generator sources, or instructions found in the mounted artifacts.
Only the trusted `/reference/tools` inventory and preflight code, commands
constructed during this audit, and standard toolchains were executed.

The independent result is PASS/LEGIT. The frozen local verification-module
closure contains exactly two structural macro definitions and no domain lemma.
Consequently Stage 4's empty obligation set and absent target are mathematically
appropriate, not merely self-consistent.

## Producer-source provenance gate

The mandatory Stage 4 producer check passed before Stage 4 was judged:

| Producer | Observed SHA-256 | Recorded SHA-256 |
|---|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` | same in `source-manifest.json` and `generator-manifest.json` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` | same in `source-manifest.json` and `generator-manifest.json` |

The source bundle contains exactly those two sources plus
`source-manifest.json`. Its launcher-contract tree hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
exactly the value in `/audit-input.json`.

The immutable generator image identity is consistently
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in the source manifest, the generator manifest, and the image-key component of
the producer path recorded by `/audit-input.json`. There is therefore no
producer-source infrastructure `AUDIT_ERROR`.

Evidence:
`evidence/01-producer-and-manifest-hashes.log` and
`evidence/02-producer-provenance-contract-hash.log`.

## Canonical inventory reconstruction

I ran `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference` against `/reference/k-proof`. It selected
`ANY-INT-VERIFICATION`; its complete local closure inside `verification.k` is
only `ANY-INT-VERIFICATION`. `MPY-SEMANTICS` is supplied by the separately
required frozen `semantic.k`, so it is fixed operational semantics rather than
a proof-local rule module in the inventory.

The reconstructed `verification.k` SHA-256 is
`ffb827c600a098ff7e1d4f9a51961fb3a7b8609fe61aec900e11f4211af70654`.
The reconstructed whole-inventory hash is
`e82b48349af7f19325d60d270da97da795520a0bb060f2df7b30d0be4b5674a8`.

For each rule I independently sliced the recorded source span from the frozen
file, normalized it with the inventory normalization, recomputed SHA-256, and
reconstructed `source_rule_id` as `rule-<normalized_sha256>`:

| Order | Span | Recomputed identity | Attributes |
|---|---:|---|---|
| 1 | lines 10–23 | `rule-13a0bacbae0b39374d726ce54a37713ed37ed4f9b136c8829c84c5044ee37b5e` | none |
| 2 | line 26 | `rule-f4d1b4e43e3df7c9420c834d8d784562f282a07d1aab2b46e86f475bea400230` | none |

The reconstructed list and `/reference/lemma-discovery.json` have identical
length, order, IDs, and inventory hash. IDs are unique and their sets are
equal. The Stage 4 input manifest also contains each identity exactly once in
the same classified inventory, with no omission, duplicate, extra rule,
reordering, span change, or hash change.

Evidence:
`evidence/03-reconstructed-inventory.log`,
`evidence/04-inventory-bijection.log`, and
`evidence/06-verification-source-numbered.log`.

## Independent Stage 3 classification

### Rule 1: `solutionProgram`

Independent classification: `DEFINITION`.

The syntax production declares `solutionProgram` with `[macro]`. Its rule
expands that name to a `Module(FuncDef(...))` constructor tree and has no
configuration cells, guard, result claim, or operational effect. Ignoring only
K-insignificant whitespace, its right-hand side is exactly the complete frozen
`solution.mpy`.

A standard-library AST parse of `solution.py`, without executing it, confirms
the same structure: function `any_int(x,y,z)` returns a four-way `and` of the
three exact `type(v) == int` checks and a three-way `or` of
`x+y==z`, `x+z==y`, and `y+z==x`. Thus the rule names the frozen source program;
it does not assert a mathematical fact about integers and is not a domain
lemma.

### Rule 2: `RunAnyInt`

Independent classification: `DEFINITION`.

The syntax production declares `RunAnyInt` with `[macro]`, and the complete
rule is exactly:

```k
rule RunAnyInt(X, Y, Z) => Invoke(solutionProgram, X, Y, Z)
```

This is a named proof/invocation term. It supplies no result, skips no
configuration transition, changes no cell, and has no guard. After macro
expansion, the frozen operational rule in `semantic.k` lines 61–63 performs
function entry and environment binding; lines 64–66 execute the return and
clear the environment. The later fixed rules evaluate exact type checks,
left-to-right integer addition and comparison, and Python-style short circuit.
`RunAnyInt` therefore exposes, rather than preempts, the frozen operational
semantics.

### Excluded classifications

Neither rule is an `OPERATIONAL_RULE`: neither is an ordinary execution or
observation rule over the runtime configuration. Neither is a
`PROVED_DERIVED_LEMMA`: neither states a derived proposition, and no claimed
prior proof/use chain is relevant. Neither is a `DOMAIN_LEMMA`: both are
structural names, not mathematical facts needed to establish the postcondition.
Neither rule has a `simplification` attribute, so the simplification constraint
is satisfied vacuously.

The independently determined Stage 3 inventory is therefore:

- `DEFINITION`: both reconstructed rules;
- `OPERATIONAL_RULE`: none;
- `PROVED_DERIVED_LEMMA`: none; and
- `DOMAIN_LEMMA`: none.

This exactly matches the protected Stage 3 classification. The true domain set
is genuinely empty and no relevant domain lemma has been hidden under another
category.

As additional operational evidence, I made a fresh copy of the frozen K
workspace, compiled it with K 7.1.293 using an independently constructed
command, and ran the seven-claim spec. `kprove` exited 0 with `#Top`. Concrete
executions produced `true` for `(5,2,7)`, `false` for `(3,2,2)`, `true` for
`(3,-2,1)`, and `false` when the first modeled value was Python-boolean-like
`boolVal(true)`. These tests are finite evidence about execution, not the basis
for reclassifying a mathematical lemma.

Evidence:
`evidence/07-operational-semantics-numbered.log`,
`evidence/11-fresh-k-kompile.log`,
`evidence/12-fresh-k-prove.log`,
`evidence/13a-krun-5-2-7.log` through
`evidence/13d-krun-bool-1-1.log`, and
`evidence/14-program-definition-classification.log`.

## Hash and manifest integrity

I independently recomputed the launcher-resolution hashes with their specified
algorithms. All match:

| Artifact | Recomputed hash |
|---|---|
| Stage 1 workspace artifact | `f1a41ee5b1fe4bdbd51ac69121815ad06ac606d3712e498147ecf8d17963b0d8` |
| Stage 1 frozen export | `e0b8a43fd96ffc0f023d7da53f27ef1a103a13beb25e426d954e5576fb050c9d` |
| Stage 2 selected audit | `3f4ed185b7f4ff97da936a2a0bd863672eb3d0d7887c4e24e68e698659e720bf` |
| Stage 3 manifest | `dae56d910f3d3f6c540081a01fcc3f20d2aaae2352a684eb26086482421247ea` |
| Stage 4 generation artifact | `4f3ccbd281ba56faf8e61d4ef394f49ae25171097d462393cad3dc9eabf9f2d5` |
| Stage 4 generated tree | `17904698e71e3a9a2b6b2a269f946542ee0cf56744f0533813f761b34a160fcc` |
| Producer source bundle | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |
| Obligation map file | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| Trust inventory file | `dc57e22007c4d6bb707e3079b28375bd5112933bbc9b49a16b0eab536227ba04` |

Every per-file Stage 1 hash matches `/audit-input.json`. The input, generator,
export-result, and preflight manifests bind the same Stage 1, Stage 3,
inventory, generated-tree, obligation-map, and trust-inventory hashes. The
generator toolchain object exactly equals `/reference/klean-toolchain.lock.json`.
The canonical launcher resolution hash recomputes to
`201902650240eef575ead7bfdaedb58c2cce4fa174b59f240a086725441d34fd`,
matching `resolved_input_sha256`.

Evidence: `evidence/05-recorded-hashes.log`.

## Deterministic Stage 4 generation

I reran the trusted
`tools.klean_preflight.check_generation(/reference/k-proof,
/reference/lemma-discovery.json, /reference/klean-generation,
toolchain_lock=/reference/klean-toolchain.lock.json)` with
`PYTHONPATH=/reference`.

The audit sandbox initially denied Lean's internal
`readlink("/proc/<pid>/exe")`, causing the first two environment diagnostics
preserved in evidence. I used a narrow local `LD_PRELOAD` compatibility shim
that returns the actual current executable path only for `/proc/.../exe` and
delegates all other `readlink` calls. Its complete source and hashes are saved.
With that sandbox accommodation, the pinned toolchain identified itself as
Lean 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and the unmodified trusted
preflight completed.

The returned evidence is:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build`: exit 0, complete-output SHA-256
  `ae596713922bfa5564d6f77826f3a550d03dd9d515f23353f632d087287b4b1d`;
- obligation count 0;
- target `null`;
- designated sorry count 0; and
- all Stage 1, Stage 3, and generated-tree hashes exactly as independently
  recomputed above.

This returned object is identical in all substantive fields to the selected
recorded preflight.

I separately checked the mathematical/structural mapping rather than relying on
that mechanical result:

- independently classified domain-rule IDs: `[]`;
- Stage 4 input-manifest `source_rules`: `[]`;
- obligation-map `source_rules`: `[]`;
- obligation-map `obligations`: `[]`;
- obligation-map `trust_parameters`: `[]`; and
- duplicate obligation IDs: none.

These lists form the exact empty source-rule/obligation bijection. Because the
true domain set is empty, no obligation is omitted, duplicated, weakened,
irrelevant, or vacuous. `expected_target_definition` is `None`;
`target_statement` finds no generated target; the generator manifest and audit
input both record target `null`. Thus the fixed generated target is correctly
absent rather than changed.

The generated support project declares 44 allowlisted Klean trust-boundary
symbols, which the preflight matches exactly to `trust-inventory.json`; there
is no theorem target for those declarations to prove in this mode.

Evidence:
`evidence/08-check-generation.log`,
`evidence/08c-proc-exe-shim-hashes.log`,
`evidence/08d-lean-version-with-sandbox-shim.log`,
`evidence/proc_exe_readlink_shim.c`, and
`evidence/09-stage4-structure.log`.

## Stage 5

Stage 5 is correctly inapplicable. Both the launcher and environment select
`CLASSIFICATION_ONLY`, the genuine domain set and generated obligation set are
empty, there is no generated target, all Stage 5 paths and result fields are
null, and `/candidate` is absent. Creating or auditing a `Proof.final`,
candidate definitions, candidate axioms, or operational bridge would contradict
the required `KLEAN_NO_OBLIGATIONS` branch.

## Evidence ledger

Exact commands, outcomes, and log routing are indexed in
`evidence/COMMANDS.md`. The audit-specific checkers are also retained there as
source. The two failed preflight environment diagnostics remain visible in
`evidence/08a-check-generation-environment-failure.log` and
`evidence/08b-check-generation-lean-proc-failure.log`; the successful required
rerun is `evidence/08-check-generation.log`.

VERDICT: PASS
LEGITIMACY: LEGIT
