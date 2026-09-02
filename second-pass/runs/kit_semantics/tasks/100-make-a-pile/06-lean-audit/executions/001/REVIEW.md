# Independent audit: `100-make-a-pile`

## Scope and result

This audit covers HumanEval problem `100-make-a-pile`, condition
`kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and the
signed `/audit-input.json` resolution say `CLASSIFICATION_ONLY`. The resolution
has no Lean workspace, Lean invocation, Stage 5 result, or target, and
`/candidate` is absent. Stage 5 proof checks are therefore not applicable.

I treated the mounted Stage 1–4 files and prior review as untrusted evidence. I
did not accept a prior verdict or execute any mounted provenance script. The
only mounted code executed for the substantive gates was the trusted inventory
and preflight code under `/reference/tools` (plus the pinned Lean/Lake binaries
invoked by preflight).

## Producer provenance gate

Before judging generated content, I hashed both exact generation-time producer
files:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Those values exactly match `source-manifest.json` and the exporter/klean fields
of `generator-manifest.json`. The generator image ID is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in both manifests, and the immutable producer-bundle component recorded in
`/audit-input.json` is the same digest. The complete mounted producer tree
recomputes to
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
also exactly as recorded. There is no producer-source infrastructure error.

Evidence: `evidence/01_stage4_producer_provenance.txt` and
`evidence/43_hash_and_stage4_audit.json`.

## Frozen inventory reconstruction and Stage 3 bijection

I ran `tools.k_rule_inventory.inventory_verification` independently on
`/reference/k-proof`. The selected main module is `VERIFICATION`, and its local
verification-file closure is `VERIFICATION-SYNTAX`, `VERIFICATION`. Imported
modules supplied from the separate semantics tree are not local modules in
`verification.k`, as intended by the canonical inventory contract.

The frozen `verification.k` SHA-256 is
`995fa13e42ca9b636967e7142a55995e394f75dc0300491f20528ba00a4f48cf`.
The canonical inventory SHA-256 is
`01a612e13f79b9f6a231be1502c29934494444339c9f77c964b5837379e003af`.
Exactly two rules were reconstructed:

| Order | Source span | Normalized SHA-256 / source rule ID | Independent class |
|---:|---:|---|---|
| 1 | 13–14 | `82445bea9adcbbe979699c705f558f66f814a969deb1b899bcc8356b74b84d31` / `rule-82445bea9adcbbe979699c705f558f66f814a969deb1b899bcc8356b74b84d31` | `DEFINITION` |
| 2 | 16–21 | `63431e432f0bf08d6bc0c04732f82fcd4f0d71ba7458f65345b9c101ef3654d8` / `rule-63431e432f0bf08d6bc0c04732f82fcd4f0d71ba7458f65345b9c101ef3654d8` | `DEFINITION` |

For each rule, I independently re-extracted the source span, confirmed that its
text equals those exact physical source lines, normalized whitespace, recomputed
the normalized hash, and reconstructed `source_rule_id` as `rule-<hash>`.
Canonical hashing of the ordered rule documents reproduced the whole inventory
hash.

The protected Stage 3 manifest has these same two unique IDs in the same order.
There are no missing, duplicate, extra, reordered, or unaccounted entries. Its
inventory hash is exact, and trusted contract validation also passes. The
manifest's buckets are two definitions and zero operational rules, proved
derived lemmas, and domain lemmas.

Evidence: `evidence/inventory_audit.py`,
`evidence/04_reconstructed_inventory_and_bijection.json`, and
`evidence/03_frozen_sources_and_discovery.txt`.

## Independent classification judgment

The Python source initializes `pile = []` and `i = 0`; while `i < n`, it appends
`n + 2 * i`, increments `i`, and finally returns the list. The supplied K
semantics lowers `While` to `#while`, executes the condition and body through
ordinary operational rules, implements `list.append(v)` as the heap update
`VS => valSeqConcat(VS, vCons(V, .ValSeq))`, and implements the integer
`AugAssign` by updating the current scope with `applyBin`.

The symbol `finishPile : ValSeq × Int × Int → ValSeq` is declared as a total K
function. Its two local rules are equations over that named function, not
configuration rewrites:

1. If `I >= N`, `finishPile(A,N,I) = A`. This is the base equation for the
   accumulated result after the loop condition is false.
2. If `I < N`, it appends exactly `N + 2*I` to `A` and recurs at `I + 1`. This
   is the recurrence matching one ordinary loop iteration.

The guards are disjoint and exhaustive over K integers, and the recursive case
strictly decreases the natural gap `N-I`. The equations therefore define the
named summary on every use. They do not match a `<k>` cell, alter heap/scope
state, or preempt any ordinary operational rule. They assert no separate
human-facing property of the result. They are not derived lemmas: Stage 1 did
not first prove either exact rule against a module omitting it. They are also
not domain lemmas; their content is the base/recursive definition itself.

Concrete and counterfactual checks support that reading. From empty `A`,
`finishPile(A,3,0)` unfolds to `[3,5,7]`, while the base case at `I=3` preserves
the accumulated list. Replacing `2*I` by `I` would instead produce `[3,4,5]`,
and changing `I+1` to `I+2` would skip levels; both contradict the source loop.
Changing the base RHS from `A` would discard the executed append effects. Thus
the equations are load-bearing, truthful definitions of the execution summary,
not convenient assumptions of the requested theorem.

Neither inventory entry has a `simplification` rule attribute. Consequently
there is no local simplification rule that could violate the requirement that
such a rule be a `DEFINITION` or `DOMAIN_LEMMA`.

The independent true domain-lemma set is therefore genuinely empty.

Operational evidence: `evidence/05_relevant_operational_semantics_search.txt`.

## Recorded-input hashes

I recomputed both tree-hash schemes used by the trusted contracts and every
individual Stage 1 source hash. The complete set of 779 relative Stage 1 file
names and hashes exactly equals `audit-input.resolution.stage1_source_hashes`.
The signed resolution digest also recomputes exactly.

| Bound input | Recomputed and recorded value |
|---|---|
| Stage 1 pipeline tree | `fb740952960c2e23b6dbe3395a5b503ceef905b9445f1944a5dcd7185d97c60b` |
| Stage 1 deterministic-export tree | `993c3f3f2b0a9c5d03b199bab999022a140acec8328bd5f67faf476ed917501e` |
| Stage 2 audit tree | `7e7749ccbcdd4793ee2d0bff9e4e7a62b1eb4a2e7a2f4f6b5161a13798bb37b7` |
| Stage 3 discovery file | `226fd894aca9ee294871ba0f65eae1543b47bb9bdf8993f20dabad46c35f5537` |
| Stage 4 generation tree | `57ce1e10e02e3db98fdb516bdaebb4e3d9c5cb444dbdfd30f70c1c50389bcdc1` |
| Generated Lean project tree | `ed55291b61e7f18eb240b14df7d3652599ac892e7b35ee15333bbd39aca00e37` |
| Producer-source tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |

The null Lean workspace/invocation hashes also agree with classification-only
mode. Evidence: `evidence/43_hash_and_stage4_audit.json`.

## Deterministic Stage 4 generation

I reran the mandated trusted call to
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, the
frozen Stage 1 workspace, protected Stage 3 manifest, selected Stage 4
generation, and `/reference/klean-toolchain.lock.json`.

The first call exposed a launcher-specific tool issue: this container puts the
process in a PID namespace while mounting host-PID `/proc`. Lean 4.22 resolves
its executable through `/proc/<getpid()>/exe`, which did not exist, so Lake
could not detect its installation. Evidence includes the namespace/host PID
pair (`NSpid: 1382 6`) and Lean's exact failing lookup implementation. I used an
audit-local preload shim that redirects only that exact `readlink` request to
the equivalent `/proc/self/exe`. The shim source is preserved at
`evidence/lean_proc_self_shim.c`; its SHA-256 is
`61113a0cc06d8049718dc7d182dd83b5f622b87f2d0f2959708a0142247356ec`.
It does not alter the generated project, trusted Python code, Lean declarations,
or pinned toolchain. With it, `lean --version` reported Lean 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly matching the lock.

The real trusted preflight rerun then returned:

- status `KLEAN_NO_OBLIGATIONS`;
- Stage 1 tree `993c3f3f2b0a9c5d03b199bab999022a140acec8328bd5f67faf476ed917501e`;
- Stage 3 hash `226fd894aca9ee294871ba0f65eae1543b47bb9bdf8993f20dabad46c35f5537`;
- generated tree `ed55291b61e7f18eb240b14df7d3652599ac892e7b35ee15333bbd39aca00e37`;
- obligation count zero and target `null`;
- `lake clean` exit 0; and
- `lake build` exit 0, with output SHA-256
  `bb4b1d010e488b02a14e510c3fc413da84b438da71f473ca6f6156d6768149b0`.

That build-output hash exactly reproduces the originally recorded preflight
hash. The trusted gate also reconciled all 43 non-propositional generated trust
declarations with `trust-inventory.json` and found no generated `sorry`.

Full returned evidence is in
`evidence/38_check_generation_successful_rerun.txt`; the diagnosed initial call
is retained in `evidence/06_check_generation_rerun.txt`, with supporting
environment evidence in `evidence/36_pid_namespace_diagnosis.txt` and
`evidence/37_lean_pid_namespace_shim_build_and_test.txt`.

## Obligation bijection and target identity

I did not rely only on preflight's structural result. Starting from the
independently classified inventory, the eligible `DOMAIN_LEMMA` sequence is
empty. Independently applying the producer's source-rule projection gives an
empty sequence. This is exactly equal to all three relevant records:

- `input-manifest.json`: `source_rules = []`;
- `generated/obligation-map.json`: `source_rules = []`, `obligations = []`,
  `trust_parameters = []`; and
- `generator-manifest.json`: `obligation_count = 0`.

The obligation-map file SHA-256 matches the generator manifest. The source-rule
and obligation ID sequences are equal in order and duplicate-free (both empty).
There can be no omitted, duplicated, irrelevant, weakened, or vacuous conjunct
in the empty mapping.

The producer's independent expected-target calculation returns `None`, and its
target parser observes no generated target. The generator manifest, recorded
preflight, rerun preflight, export result, and signed audit input all consistently
record a null target. `Klean100MakeAPile/Lemmas.lean` contains an empty namespace
and no target declaration. Thus the fixed generated target is correctly absent,
not changed or weakened.

Evidence: `evidence/43_hash_and_stage4_audit.json` and
`evidence/45_obligation_map_and_target_absence.txt`.

## Stage 5 disposition

`KLEAN_NO_OBLIGATIONS` is legitimate here because the independently determined
domain-lemma set is genuinely empty. Classification-only mode requires no
generated target and no Stage 5 candidate; both are absent. Consequently there
is no `Proof.final`, target parameter, candidate definition, operational bridge,
or candidate axiom list to inspect. Running the proof-mode-only clean candidate
build and `#print axioms Proof.final` would be inapplicable because neither a
candidate nor `Proof.final` exists.

## Judgment

Stage 3 is complete and correctly classifies both local rules as definitions.
Stage 4 has intact producer/image provenance, exact input/output hashes, an
exact empty domain-rule/obligation bijection, and the required null target. The
selected `KLEAN_NO_OBLIGATIONS` status matches the frozen source program and
operational K semantics, not merely the self-consistent manifests.

VERDICT: PASS
LEGITIMACY: LEGIT
