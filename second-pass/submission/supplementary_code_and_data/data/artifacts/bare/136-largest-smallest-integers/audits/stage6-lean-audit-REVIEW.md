# Independent audit: `136-largest-smallest-integers`

## Scope and outcome

The launcher-bound mode is `CLASSIFICATION_ONLY`, condition `bare`, with
`GENERATED_SEMANTICS`. `AUDIT_MODE` agrees with `/audit-input.json`.
`/candidate` is absent, and the launcher records no Stage 5 invocation,
workspace, or target. I therefore audited Stage 3 and Stage 4 and did not
perform the proof-mode-only candidate, `Proof.final`, or axiom-dependency
checks.

I did not rely on the selected Stage 2 verdict or its review. The independent
classification finds a genuinely empty `DOMAIN_LEMMA` set. The selected
`KLEAN_NO_OBLIGATIONS` result is consequently legitimate: its obligation map
is empty and it generates no theorem target.

## Bound inputs and producer provenance

The launcher resolution and environment are preserved in
`evidence/01-audit-input.log` and `evidence/02-environment.log`. Independent
hash recomputation in `evidence/15b-hash-bindings-with-toolchain.log` produced:

- Stage 1 pipeline tree:
  `8043e15c6c6f41ca2165223e60059ec04572da90f59a8eed081c559383bc0bd9`
- Stage 1 deterministic-export tree:
  `00b6795e09cda2a090e4e7dab47413920e59489e3e5968bcb50769f4ec1a0c90`
- Stage 2 selected artifact:
  `ac009aa1396e95724a308b6a533ab3d7045703dcc519547b9a942a855ec1e0f6`
- Stage 3 manifest:
  `2b94ff2eebda3d21f8ba4c4f46bf2b58e912c271402b841985b7240e46ec02a3`
- Stage 4 artifact:
  `ed651f3ea12aac3b8acb79a1381adce6391b9c3e0dbe52d2497524930111c72a`
- Generated Lean tree:
  `d3a3a5f900992e805887806c558b10a13b9fb56d388836e69c00172fb1f74765`
- Generation-time producer-source tree:
  `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`
- Resolved audit input:
  `b26a2aaccfe01a03cc74ef2fdfb3963eee984fb65b75ec32e3266207906e4319`

Every value matches `/audit-input.json`. The complete 41-entry Stage 1 file
and hash map also matches exactly, with no missing, extra, or changed file.

Before judging Stage 4, I directly hashed both immutable producer files:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` |

These hashes match both `source-manifest.json` and
`generator-manifest.json`. Both manifests record generator image
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`;
the immutable producer-store path recorded in `/audit-input.json` has the same
digest as its basename. The generator toolchain object exactly equals
`/reference/klean-toolchain.lock.json`. Raw manifests and hashes are in
`evidence/04-producer-and-stage4-manifests.log`.

## Inventory reconstruction and bijection

I ran the trusted `tools.k_rule_inventory.inventory_verification` over the
frozen Stage 1 workspace and separately recomputed every span, whitespace-
normalized SHA-256, and `rule-<sha256>` identity from the physical source
lines. The local module closure is exactly `["VERIFICATION"]`; imported
modules defined outside `verification.k` are not local members of this
closure.

The reconstruction found 11 rules. The frozen `verification.k` hash is
`a54766e74afa56d501e8880c29aacebec2884555ba27c801af7a1bbb614859db`,
and the canonical ordered inventory hash is
`577e90b3e2ba59231529bb8ba7f67b95a7969f86d0f9e22e335605619797a3f9`.
For all 11 entries:

- the inclusive line span reproduces the inventory text exactly;
- the normalized hash and `source_rule_id` recompute exactly;
- identities are unique;
- the Stage 3 manifest has one and only one matching entry;
- manifest order is identical to source inventory order; and
- there are no omissions, additions, duplicates, or unaccounted entries.

The complete reconstruction, texts, hashes, and manifest comparison are in
`evidence/07-inventory-reconstruction.log`.

## Independent Stage 3 classification

The source contract asks for the largest negative integer and the smallest
positive integer, using `None` when either side is absent. The frozen
operational semantics evaluates the translated function normally: it binds
the argument, initializes both accumulators, iterates every `IntSeq` element,
evaluates the integer comparisons, updates the environment, and returns the
tuple. No rule in the verification inventory rewrites `run`, skips a loop
body, fabricates a return, or otherwise preempts that execution.

My classification of the ordered inventory is:

| Lines | Rule head | Reclassification | Judgment |
|---:|---|---|---|
| 15 | `#negFold(nil, N)` | `DEFINITION` | Base equation of the negative-extremum fold. |
| 16–17 | `#negFold(icon(I, IS), N)` | `DEFINITION` | Structural recurrence on the sequence tail. |
| 18 | `#posFold(nil, P)` | `DEFINITION` | Base equation of the positive-extremum fold. |
| 19–20 | `#posFold(icon(I, IS), P)` | `DEFINITION` | Structural recurrence on the sequence tail. |
| 22–26 | `#negStep(I, N)` | `DEFINITION` | Named fold-step equation; negative and nonnegative cases are exhaustive. |
| 27 | `#negCandidate(I, pyNone)` | `DEFINITION` | Constructor equation for an empty optional accumulator. |
| 28–32 | `#negCandidate(I, pyInt(N))` | `DEFINITION` | Constructor equation choosing the greater negative candidate. |
| 34–38 | `#posStep(I, P)` | `DEFINITION` | Named fold-step equation; positive and nonpositive cases are exhaustive. |
| 39 | `#posCandidate(I, pyNone)` | `DEFINITION` | Constructor equation for an empty optional accumulator. |
| 40–44 | `#posCandidate(I, pyInt(P))` | `DEFINITION` | Constructor equation choosing the smaller positive candidate. |
| 47–67 | `solutionProgram` | `DEFINITION` | Macro defining the named proof term as the translated program AST. |

This agrees with all 11 protected classifications.

The six `#...` symbols are freshly declared summary functions. Their rules
define base cases, structural recurrences, and constructor cases rather than
asserting facts about pre-existing operations. `IntSeq` has exactly `nil` and
`icon`; `OptInt` has exactly `pyNone` and `pyInt`; the unconditional step rules
partition integers with `#if`. Thus the `[function, total]` declarations have
truthful, terminating, exhaustive equations for every use in the claims.

The `solutionProgram` symbol is explicitly a macro and its rule names an exact
AST; it is not an operational bridge. Independently expanding both
`solutionProgram` and frozen `solution.mpy` with K produced byte-identical
JSON, each with SHA-256
`7f8f39252dbf5c83a921b51fe778321a6895e22427094b2fb3e854368e614c5d`
(`evidence/18-program-macro-fidelity.log`).

There is no `OPERATIONAL_RULE` in this inventory: the ordinary execution rules
are in frozen `semantic.k`, outside the local `verification.k` rule set. There
is no `PROVED_DERIVED_LEMMA`: `verification.k` contains no prior proof of one
of these exact rules in a module that excludes it and no later proof-use
sequence. There is no `DOMAIN_LEMMA`: none of the rules asserts an independent
mathematical proposition; each gives the defining equation of a fresh summary
or macro. None has a `simplification` attribute, so the simplification
classification restriction is also satisfied.

As corroborating evidence rather than a substitute for source judgment:

- a direct fresh `kompile` plus `kprove` closed with `#Top`
  (`evidence/17-direct-k-rebuild-and-proof.log`);
- operational runs covered empty, zero-only, all-negative, all-positive,
  duplicate/mixed, and large-magnitude inputs and returned the intended
  extrema (`evidence/19-operational-adversarial-cases.log`);
- changing the program macro's positive branch made the proof fail with a
  stuck setup claim (`evidence/20-body-mutation-kprove.log`); and
- weakening the final positive result to unconditional `pyNone` made the
  proof fail with an unmet implication
  (`evidence/21-postcondition-mutation-kprove.log`).

These checks confirm body sensitivity, result constraint, and relevance to
the source postcondition. The source and semantics inspected are preserved in
`evidence/06-frozen-sources.log` and the task contract in
`evidence/22-problem-contract.log`.

## Deterministic Stage 4 judgment

I invoked `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and exactly these semantic inputs:

- `/reference/k-proof`
- `/reference/lemma-discovery.json`
- `/reference/klean-generation`
- `/reference/klean-toolchain.lock.json`

The audit container exposes host PIDs in `/proc` while `getpid()` returns a
container PID. Lean 4.22 consequently failed its
`/proc/<getpid>/exe` installation lookup on the first attempt
(`evidence/09-stage4-preflight-rerun.log` and
`evidence/10-lean-toolchain-diagnosis.log`). I used the narrow compatibility
shim in `evidence/lean_proc_compat.c`, which changes only that numeric
`/proc/.../exe` `readlink` to `/proc/self/exe`. The pinned Lean and Lake
binaries, checker, sources, and project were unchanged. A standalone
`lake clean` and `lake build` then succeeded
(`evidence/12-lean-proc-shim-test.log`).

The mandated checker rerun returned `KLEAN_NO_OBLIGATIONS`, exit success,
zero obligations, `target: null`, zero designated sorries, 47 non-propositional
generated trust declarations, and successful `lake clean`/`lake build`.
Its build-output hashes exactly reproduce the recorded preflight:

- clean output:
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- build output:
  `830e27a137e8df217daf93ff10a991550ab4383fe6af8473b11dcc81c0846668`

The returned evidence is in
`evidence/13-stage4-preflight-rerun-success.log`.

The source-rule/obligation mapping is the exact empty bijection:
`source_rules: []`, `obligations: []`, and `trust_parameters: []`.
`input-manifest.json` likewise has no domain source rules;
`generator-manifest.json` records `obligation_count: 0` and `target: null`;
and generated `Lemmas.lean` contains no proposition or theorem. There is no
vacuous `True` target, empty conjunction theorem, weakened statement,
duplicate obligation, or target substitution. Inspection is recorded in
`evidence/16-generated-project-inspection.log`.

Because the independently classified domain set is genuinely empty, this
absence of obligations is mathematically correct, not merely
self-consistent. The trusted mechanical final gate also passed in
classification-only mode and rebound all launcher inputs without mutation
(`evidence/14-mechanical-final-gate.log`).

## Stage 5 applicability and trust conclusion

Stage 5 is not present and must not be present for this signed mode. There is
no generated target to prove, no `/candidate`, no `Proof.final`, no target
parameter, and no Stage 5 axiom ledger to reconcile. The generated executable
trust declarations cannot prove a missing proposition and are structurally
accounted for by the Stage 4 preflight.

The classifications match the frozen rules and operational meaning; the
domain set is empty for substantive reasons; producer provenance and every
launcher-bound artifact hash match; and Stage 4 contains exactly the empty
obligation mapping with no target. I found no legitimacy defect or residual
concern.

VERDICT: PASS
LEGITIMACY: LEGIT
