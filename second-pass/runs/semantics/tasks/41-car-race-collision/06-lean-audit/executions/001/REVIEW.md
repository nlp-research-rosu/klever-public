# Independent Stage 3–5 audit: `41-car-race-collision`

## Scope and result

This audit covers condition `semantics` in `SUPPLIED_SEMANTICS` mode. Both
`AUDIT_MODE` and the signed `/audit-input.json` resolution say
`CLASSIFICATION_ONLY`. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`, `/candidate` is absent, and the audit input contains no
Stage 5 result. Stage 5 proof construction, `Proof.final`, axiom printing, and
operational-bridge parameter checks are therefore inapplicable.

I treated the mounted Stage 1–5 artifacts, earlier audit, comments, and logs as
untrusted evidence. The conclusions below come from the frozen source, the
trusted inventory/preflight code in `/reference/tools`, independently
recomputed hashes, and direct inspection of the supplied operational
semantics.

## Producer-source and input integrity

The Stage 4 producer gate passed before any Stage 4 judgment:

| Producer | Recomputed SHA-256 | Recorded result |
|---|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` | Matches `source-manifest.json` and `generator-manifest.json` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` | Matches `source-manifest.json` and `generator-manifest.json` |

The bundle contains exactly those two sources plus `source-manifest.json`.
Its trusted tree hash is
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
matching `/audit-input.json`. The immutable generator image identity is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in the generator manifest, source manifest, and the producer-bundle component
recorded by the audit input.

The signed audit-resolution digest and all mounted hashes checked in
`evidence/04_recorded_hash_checks.log` matched. This includes:

- both recorded Stage 1 tree hashes:
  `954ef328e713bad771e19f1643e762795173089287121f1c0fc54fe392d4c555`
  under the pipeline tree algorithm and
  `96d19aa68e62d3962d6a5ebc67dd655bcfe693a23bc60a0749428a9f32ac0dc6`
  under the Stage 4 export tree algorithm;
- every one of the 34 recorded Stage 1 source-file paths and SHA-256 values;
- the Stage 2 audit tree, Stage 3 manifest, selected Stage 4 tree, and generated
  project tree; and
- the producer-source bundle and signed resolution.

The check reported `TOTAL_CHECKS=50` and `TOTAL_MISMATCHES=0`. No
infrastructure `AUDIT_ERROR` condition was found.

## Canonical rule inventory reconstruction

I ran `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference` against `/reference/k-proof`. The trusted code selected
the `VERIFICATION` main module from `prove.sh`; its local module closure is
exactly `["VERIFICATION"]`. The frozen `verification.k` SHA-256 is
`d12d37f461c934500948acbe2784945c8f09f41e72040506fb70507eb58e591b`.

The canonical inventory contains exactly two rules:

| Order | Source span | Normalized SHA-256 / `source_rule_id` | Attributes |
|---|---:|---|---|
| 1 | lines 8–11 | `9b1cd001fa1574b5d38ed3c286fe702d05d566d93fcf98abd5e049d981abc968` / `rule-9b1cd001fa1574b5d38ed3c286fe702d05d566d93fcf98abd5e049d981abc968` | none |
| 2 | lines 15–17 | `d05c71cafbdcedd65ca2027e7a81d8d6fbdfe3240186222e046807d78f81ff16` / `rule-d05c71cafbdcedd65ca2027e7a81d8d6fbdfe3240186222e046807d78f81ff16` | none |

For each entry, I independently re-extracted the exact physical source span,
normalized it with the inventory contract, recomputed its hash, and recomputed
`source_rule_id` as `rule-<normalized hash>`. The canonical JSON inventory hash
is
`17b0b2820a464c02c248e4ed5da0587b8a5b980b4a4fec3a794289da6137a09f`.

The protected Stage 3 manifest has the same inventory hash and the same two
identities in the same order. Both canonical and manifest identity lists are
unique; there are no omissions, additions, duplicates, or reordered
identities. The independent bijection check reported 13/13 checks passing.

## Independent classification judgment

Both rules are correctly classified as `DEFINITION`.

1. `solutionModule` is introduced by a `[macro]` syntax production and expands
   to the exact `Module(FuncDef(...))` AST in frozen `solution.mpy`. That AST
   corresponds exactly to the source function `return n * n`. The rule defines
   a named macro; it states no independent mathematical fact and does not
   summarize or bypass execution.

2. `#runCarRaceCollision(N)` is a named proof harness. It expands to
   `#loadAll(solutionModule) ~> Call(Name("car_race_collision"), Int(N))`.
   It does not replace the function body with its desired result. After this
   expansion, the supplied semantics performs the ordinary operational steps:
   `#loadAll` exposes the module statements; `FuncDef` binds a closure; `Call`
   resolves the name, evaluates the integer argument, allocates and binds a
   call frame, and executes the body; `Return` evaluates the expression and
   pops the frame; `BinOp("*", ...)` dispatches to `applyBin("*", I1, I2)`,
   whose integer rule yields `I1 *Int I2`. Thus the harness is a named proof
   term, not an operational shortcut or domain equation.

The frozen source postcondition is exactly `N *Int N`, matching execution of
`return n * n`. No algebraic or domain-specific lemma is needed to connect the
program result to that postcondition. There are no
`OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA` entries. Neither
inventory rule has a `simplification` attribute, so the simplification
classification restriction is satisfied vacuously.

The independently reclassified domain-lemma set is genuinely empty.

## Deterministic Stage 4 and mechanical preflight

I reran the required call to `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, the frozen Stage 1 workspace, protected Stage 3
manifest, selected Stage 4 generation, and pinned toolchain lock.

The audit container initially prevented Lean 4.22 from resolving
`/proc/<getpid()>/exe`, even though `/proc/self/exe` was available. This made
the first `lake clean` fail before project inspection. Evidence files 11–15
record the diagnosis. I compiled the documented
`evidence/proc_self_exe_shim.c`, which redirects only numeric
`/proc/<pid>/exe` `readlink` calls to the equivalent `/proc/self/exe` link.
With that narrow PID-namespace compatibility shim, the pinned binaries
reported Lean 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and Lake 5.0.0.
The shim does not alter source files, generated terms, build products, or Lean
logic.

The exact preflight rerun then returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean` exit 0 with empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build` exit 0 with output SHA-256
  `e355af8679b31264a5179b1a67e619758a1ac779d22fbdbf211163bf43c26682`;
- Stage 1 export hash
  `96d19aa68e62d3962d6a5ebc67dd655bcfe693a23bc60a0749428a9f32ac0dc6`;
- Stage 3 manifest hash
  `8da9f2b2dcfda337cef10b6a2bf55e441bd61604c902f6fac8207217f63e2472`;
- generated tree hash
  `54498cf6ca880a8d95bcd9bcdb844b4d502cce93d0b84697a61d35a285c38d29`;
- zero obligations, no target, no designated `sorry`, and 47 generated trust
  declarations matching the generated trust inventory.

These diagnostics and hashes reproduce the recorded preflight.

## Obligation bijection and target identity

The independent Stage 4 cross-check reported 34/34 checks passing:

- independently classified domain source IDs: `[]`;
- `input-manifest.json` domain `source_rules`: `[]`;
- `obligation-map.json` `source_rules`: `[]`;
- generated obligations: `[]`;
- trust parameters: `[]`.

The source-rule/obligation identity lists are therefore exactly bijective,
unique, and order-preserving. Obligation counts are zero in the obligation map,
generator manifest, export result, recorded preflight, rerun preflight, and
audit input. The obligation-map SHA-256 is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest.

For an empty obligation list, the trusted target constructor returns no target
definition. Direct target extraction from the generated Lean project also
returns none. The generator manifest, recorded preflight, and audit input all
record `target: null`; `Lemmas.lean` contains no target declaration. Thus there
is no omitted obligation, duplicate, weakened or vacuous conjunct, changed
target, target statement, or target hash. The absence of `/candidate` is
required and confirmed.

The selected `KLEAN_NO_OBLIGATIONS` result is legitimate because it rests on a
genuinely empty independently classified domain set, not merely on
self-consistent empty manifests.

## Evidence index

- `evidence/00_context_and_files.log`: audit mode and mounted file inventory.
- `evidence/01_manifests_and_producer_hashes.log`: manifests and raw producer
  hashes.
- `evidence/04_recorded_hash_checks.log`: signed input, tree, source, producer,
  and image-ID checks.
- `evidence/05_reconstructed_rule_inventory.json`: trusted canonical inventory.
- `evidence/06_frozen_source_and_relevant_semantics.log`,
  `evidence/07_operational_trace_rules.log`, and
  `evidence/08_function_semantics.log`: frozen source and operational rules used
  in reclassification.
- `evidence/09_inventory_bijection_checks.log`: exact span, hash, identity,
  order, uniqueness, and coverage checks.
- `evidence/10_rerun_klean_preflight.log`: initial environment failure.
- `evidence/11_lean_toolchain_diagnosis.log` through
  `evidence/16_proc_exe_shim_build_and_probe.log`: toolchain diagnosis and the
  narrow PID-namespace compatibility shim.
- `evidence/17_rerun_klean_preflight_with_pid_shim.log`: successful required
  preflight and returned evidence.
- `evidence/18_stage4_bijection_and_target_checks.log`: independent Stage 4
  hash, bucket, bijection, status, and target checks.
- `evidence/19_generated_target_absence.log`: generated target absence,
  obligation map, and candidate absence.

VERDICT: PASS
LEGITIMACY: LEGIT
