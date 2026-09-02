# Independent Stage 3–4 Audit: HumanEval `131-digits`

## Result

The protected Stage 3 classification is correct, and the selected Stage 4
`KLEAN_NO_OBLIGATIONS` result is legitimate. The independently reconstructed
domain-lemma set is genuinely empty. Consequently, the deterministic
generation must have no proof obligation, no generated target, and no Stage 5
candidate; all three conditions hold.

The signed launcher mode is `CLASSIFICATION_ONLY` in `/audit-input.json`, and
`AUDIT_MODE=CLASSIFICATION_ONLY` agrees. The semantics mode is
`GENERATED_SEMANTICS`. `/candidate` is absent, while the signed Stage 5 result,
Lean workspace hash, and Lean invocation hash are all null. I did not rely on
the earlier Stage 2 review or any prior verdict.

## Producer provenance and immutable inputs

I hashed the two mounted generation-time producer sources before making the
Stage 4 judgment:

| Producer | Observed SHA-256 | Bound SHA-256 |
|---|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` | same in `source-manifest.json` and `generator-manifest.json` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` | same in `source-manifest.json` and `generator-manifest.json` |

The source manifest and generator manifest both identify the immutable
generator image as
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`.
The final component of the launcher-bound producer-source path in
`/audit-input.json` is the same image digest. The complete mounted producer
tree hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
also exactly matching the audit input.

Using the trusted pipeline and exporter hash implementations, I recomputed all
launcher-bound artifact hashes:

| Artifact | Recomputed hash |
|---|---|
| Full frozen K workspace | `f9e51c3c3cc86687275131d5fd51a2b0d3cce3eecf3e867bb78131cf3a353e15` |
| Frozen Stage 1 export | `81e476f29f2f78a72b787099e97b29bacd35bfa05e36a9e19bfa5c035ec18623` |
| Stage 2 K audit tree | `4a82645c71c8d4285f4dabac95c437c6853829382d41847d814491e9e8104a67` |
| Stage 3 manifest | `96b52a33ed75249e3c8782ac0bdd5b558b974c514a64f752ecbfc45aadae62c7` |
| Complete Stage 4 generation | `39e0f497ab670266f07a6ff9412119f652c0e80471d490c6e318f8329badd85b` |
| Generated Lean project | `3d317fb5fad8b7bc0f6564dcef49428019eb862d3cdcc6cff57145a4ea563f2d` |

These equal every corresponding hash in the audit input and the two selection
records. All nine per-file Stage 1 source hashes also match exactly, including
`verification.k` at
`d7de1ea00a4fd0346df61d2ea7e5e55540093568f2314fbaa377a919e8e7e2ba`.
The signed resolution digest independently verifies as
`5e582d89828e7ef50de516337672e21348715f21137704f5de81a79ab75bf840`.
The generator toolchain object is exactly equal as structured JSON to the
trusted toolchain lock.

## Canonical inventory reconstruction

I called the trusted `inventory_verification` implementation on the frozen
workspace and independently rechecked every returned span against the
corresponding physical source lines. For each entry I normalized the source as
one whitespace-separated string, recomputed its SHA-256, and required
`source_rule_id` to be exactly `rule-<normalized SHA-256>`.

The selected local verification module is `VERIFICATION`. Its local module
closure inside `verification.k` contains only `VERIFICATION`; imported
`MPY-SEMANTICS` and `BOOL` are external to that file. The reconstruction has
12 rules and whole-inventory hash
`213abec6453da6d80e355466d7711c50d96f53815539caa490ba371a6491b303`.

The protected Stage 3 manifest has exactly the same 12 identities in the same
order. All are unique. There are no omissions, duplicates, extras, reordered
identities, changed normalized hashes, or unclassified entries. The trusted
Stage 3 boundary validator also passes.

## Independent classification

Every inventory rule was classified from its frozen text, declarations, use in
`spec.k`, the source solution, and the operational rules in `semantic.k`:

| Lines | Root symbol / role | Normalized SHA-256 | Independent class |
|---:|---|---|---|
| 12–13 | `digitsCond`, named condition AST | `bb601208edb1e96080955b1328dafddf878fccfb2dce6832f739299c2b3238de` | `DEFINITION` |
| 16–25 | `digitsLoopBody`, named body AST | `211588c9e5b79676333afd044a4f025ce5a926e434e042c16ba8ff965176dff5` | `DEFINITION` |
| 30–35 | `SolutionProgram`, closed program macro | `72490e5f66a388ba81e28c7d33d85162be231d30fbfc42ada45ce48e94f1b47a` | `DEFINITION` |
| 39 | structural `CheckProgram(P,P)` observation | `1b6dfc30f83e14335a83a1746f3105c6dee0842578ac512515f9f976bcf8c44d` | `OPERATIONAL_RULE` |
| 44–45 | `addOddDigit`, even branch | `5d78af83c186109d1745d13d0f1814d6752c84c8c9c47e209a5c7dcadafd402f` | `DEFINITION` |
| 46–47 | `addOddDigit`, first odd branch | `437c4b2500798a57406f8d142559444c31e2437b03b5fe055671c6b689e3540e` | `DEFINITION` |
| 48–49 | `addOddDigit`, later odd branch | `89daad84beeed92afb1ee55504d822d521105908ea9806147e9d9e3147290ec9` | `DEFINITION` |
| 53–54 | `oddProductFrom`, base equation | `e11ad215fdd840b01bcd1242471ce6eec8653123658ff8b63379ca602d63489b` | `DEFINITION` |
| 55–57 | `oddProductFrom`, recursive equation | `6f05f0cf15dc24aba0468572926489fbee6552fbb026dbafa4cc55d063dd2200` | `DEFINITION` |
| 60 | `oddProduct`, initialized wrapper | `ac1c567b0b62d1c41908cf0eddc4e86fd1188c897da6982587d3b155b82122df` | `DEFINITION` |
| 65–66 | `finalScratchDigit`, base equation | `c69abfdd9a91259eebdc62439ad213ee855f4b5c17687e0e4e0d421e2057e987` | `DEFINITION` |
| 67–69 | `finalScratchDigit`, recursive equation | `bd4d10518278875bfc2e732411dd8f7adf6cfa7803bd88a85b0e94d0afaeab06` | `DEFINITION` |

The first three entries name exact syntax trees. The remaining eight
definitional entries introduce the accumulator and scratch summaries used by the loop
invariant and postcondition. They are definitions because their left-hand
sides are the newly declared summary symbols and their equations give the
symbols' cases or recurrence; they do not assert a mathematical fact between
pre-existing symbols. `CheckProgram(P,P) => ProgramsMatch` is instead an
ordinary observation rewrite and is correctly operational.

The `addOddDigit` guards partition even digits, odd digits with a zero
accumulator, and odd digits with a nonzero accumulator. The recurrence guards
for `oddProductFrom` and `finalScratchDigit` partition `N <= 0` and `N > 0`.
For positive `N`, the operational semantics writes `N %Int 10`, applies the
same accumulator cases, then replaces `N` by `N /Int 10`; the quotient is
smaller and the scratch recurrence records exactly that digit. Although the
source condition tests `digit % 2 == 1` while the helper uses nonzero parity,
the operational digit is `N % 10` for positive `N`, hence lies in `0..9` and
the tests agree.

As finite adversarial support for this semantic reading, an independently
implemented operational loop and the two summaries agreed on 150,015 states:
all `N` from 0 through 10,000, five initial accumulators, and three initial
scratch values. Representative results include `235 -> (15,2)`,
`2468 -> (0,2)`, `10203 -> (3,1)`, and `13579 -> (945,1)`, where each pair is
the final accumulator and scratch digit. Constant-zero, constant-one,
identity, and scratch-identity counterfactuals fail on `1`, `4`, or `235`.
These ground checks support but do not replace the direct recurrence analysis.

No rule has a `simplification` attribute. No rule meets the
`PROVED_DERIVED_LEMMA` criterion, and none is claimed as such; Stage 1 does not
first prove any inventory rule in a module omitting it and later reuse it.
Most importantly, no inventory entry is a standalone, source-relevant
mathematical `DOMAIN_LEMMA`. The independently determined true domain set is
therefore empty.

## Deterministic Stage 4 generation

With `PYTHONPATH=/reference`, I reran
`tools.klean_preflight.check_generation` on exactly:

```text
/reference/k-proof
/reference/lemma-discovery.json
/reference/klean-generation
```

The returned status is `KLEAN_NO_OBLIGATIONS`. `lake clean` and `lake build`
both exit 0. The direct required rerun reproduced the launcher-recorded build
output and its SHA-256
`53f73505601c9318b842251d70c719cfffb493b33d3b43389073ea62012cab61`.
The trusted final mechanical gate also passes; its separate parallel build
occasionally swaps the displayed `Func`/`Lemmas` completion order, without
changing any generated input or output hash.

The validated Stage 3 classification arrays in `input-manifest.json` are exact
matches for the independently reconstructed entries. The domain
`source_rules` list is empty in both the input manifest and
`obligation-map.json`. The obligation map, whose bound hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
contains exactly:

```json
{
  "obligations": [],
  "schema_version": 3,
  "source_rules": [],
  "trust_parameters": []
}
```

Thus the source-rule/obligation mapping is the exact empty bijection: there is
no omission, duplicate, irrelevant obligation, weakened conjunct, or vacuous
conjunct. `expected_target_definition` and `target_statement` both return
null. The generator manifest, audit input, and preflight evidence all bind a
null target, and generated `Lemmas.lean` contains only an empty namespace.

The generated project contains 46 allowlisted executable/data trust
declarations and no proposition trust, proof hole, `admit`, or `unsafe`;
preflight reconciled them exactly with `trust-inventory.json`. Because there
is no proposition target, they are not dependencies of a purported proof.

## Stage 5 applicability and trust accounting

Stage 5 proof checks are not applicable in `CLASSIFICATION_ONLY` mode. There
is no generated theorem to prove, no target parameter requiring an
operational-bridge implementation, no `Proof.final`, and no candidate axiom
list to reconcile. The required absence of `/candidate` is confirmed. The
trusted final gate reports mode `CLASSIFICATION_ONLY`, target null,
candidate hash null, and used axioms `[]`.

## Audit-environment note

The first clean preflight attempt exposed an audit-container PID/proc mismatch:
the process-visible PID did not exist in the mounted `/proc`, so Lean could not
resolve its hard-coded `/proc/<pid>/exe` path. This was not an input or
producer mismatch. I preserved the failure, then used a small audit-local
`LD_PRELOAD` shim that redirects only `/proc/*/exe` `readlink` requests to
`/proc/self/exe`. With the shim, the pinned Lean reports version 4.22.0 and
commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and both required trusted
checks pass. Input snapshots before and after the builds are identical. The
shim source, hash, compilation command, initial failure, and successful runs
are all retained in evidence.

## Evidence index

Exact commands are in `set -x` scripts beside their complete captured output:

- `evidence/01_capture_inputs.{sh,log}` — mode, producer hashes, manifests,
  audit input, and candidate absence.
- `evidence/02_inventory_audit.{py,sh,log}` — canonical reconstruction,
  line spans, ordered bijection, and frozen K/source text.
- `evidence/03_hashes_and_preflight.{py,sh,log}` — all launcher hash
  recomputations and the required returned preflight evidence.
- `evidence/03_hashes_and_preflight.initial-failure.log`,
  `evidence/03a_lean_environment_fix.{sh,log}`, and
  `evidence/lean_app_path_shim.c` — diagnosed environment failure and narrow
  compatibility fix.
- `evidence/04_independent_classification.{py,sh,log}` — per-rule independent
  classes, semantic witnesses, counterfactuals, and candidate absence.
- `evidence/05_mechanical_gate.{sh,log,json}` — trusted classification-only
  final gate and a second clean preflight.

VERDICT: PASS
LEGITIMACY: LEGIT
