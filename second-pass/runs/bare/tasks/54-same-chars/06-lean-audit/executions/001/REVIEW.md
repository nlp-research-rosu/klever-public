# Independent audit: HumanEval 54-same-chars

## Scope and result

I audited Stage 3 lemma classification and deterministic Stage 4 generation
for problem `54-same-chars`, condition `bare`, semantics mode
`GENERATED_SEMANTICS`. Both `AUDIT_MODE` and the signed resolution in
`/audit-input.json` say `CLASSIFICATION_ONLY`. `/candidate` is absent,
`lean_workspace` and `lean_invocation` are null, and there is no Stage 5
result. Thus no Stage 5 proof, candidate definitions, `Proof.final`, or Lean
axiom accounting is applicable.

I treated all mounted candidate/provenance prose and scripts as untrusted
evidence. I did not execute `prove.sh`, the generation-time producer sources,
or instructions from prior reviews. The mechanical checks used the trusted
`/reference/tools` files. Their eight per-file hashes match
`/opt/humaneval/data/klean-audit-tools.lock.json`, whose SHA-256
`5bb56dc3b85793d8528e3eae842a7345c1fde1df86149695f26c6015396f521d`
matches the launcher record.

## Generator producer provenance

I hashed the two mounted generation-time producer sources before judging
Stage 4:

| File | Observed SHA-256 |
|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` |

Both values exactly match `source-manifest.json` and
`generator-manifest.json`. The generator image ID is consistently
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in the source manifest, generator manifest, and the basename of the producer
bundle path signed into `/audit-input.json`. The independently recomputed
producer-bundle tree hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
also exactly as recorded.

Raw evidence: [01-producer-and-manifests.txt](evidence/01-producer-and-manifests.txt)
and [09-trusted-tool-lock.txt](evidence/09-trusted-tool-lock.txt).

## Inventory reconstruction and bijection with Stage 3

Using the trusted canonical inventory code on the frozen
`/reference/k-proof/verification.k`, I reconstructed the local closure of the
selected `VERIFICATION` module. The closure is exactly `[VERIFICATION]`; its
imported `SOLUTION` module is in another required file and is not a local
module in `verification.k`.

The complete local inventory has one entry:

| Field | Reconstructed value |
|---|---|
| Module | `VERIFICATION` |
| Source span | line 11 through line 11 |
| Source text | `rule sameCharsSpec(S0, S1) => charSet(S0) ==K charSet(S1)` |
| Attributes | none |
| Normalized SHA-256 | `69aad3da8a2a2d3aa2322b5eb4234ecca7aa125148464a5fcdbec3fcfb8ad975` |
| `source_rule_id` | `rule-69aad3da8a2a2d3aa2322b5eb4234ecca7aa125148464a5fcdbec3fcfb8ad975` |
| Independent classification | `DEFINITION` |

The reconstructed `verification.k` hash is
`3bed069e49237c66ff75911310f2be3c326e3fa354e852e8896a5c47ce11888a`
and the canonical whole-inventory hash is
`2dac44933e60d3e140b32217d30c4893744c50c91abdff2a01887f55be01006c`.

The protected Stage 3 manifest contains that same single identity in the same
order and with the same classification. Both sides are unique. There are no
omissions, extras, duplicates, reordered identities, changed hashes, or
unaccounted entries.

Raw evidence: [02-inventory-reconstruction.txt](evidence/02-inventory-reconstruction.txt).

## Independent classification judgment

The source program returns Python-style `set(s0) == set(s1)`. In the frozen K
semantics:

1. `charSet` recursively converts a string into a K set of one-code-point
   substrings;
2. `Call(Name("set"), E)` evaluates `E` and returns
   `setValue(charSet(S))`;
3. comparison evaluates both sides and returns
   `boolValue(CHARS0 ==K CHARS1)`; and
4. the universal postcondition names that same value as
   `sameCharsSpec(S0, S1)`.

The sole verification rule only unfolds that named postcondition summary to
`charSet(S0) ==K charSet(S1)`. It does not rewrite a program execution term,
accelerate or replace an operational transition, or assert an independent
mathematical fact about sets or strings. It therefore satisfies the required
meaning of `DEFINITION`. It is not an `OPERATIONAL_RULE`, a
`PROVED_DERIVED_LEMMA`, or a `DOMAIN_LEMMA`. It has no `simplification`
attribute, so the simplification-class restriction is also satisfied.

Consequently the independently determined true domain-lemma set is genuinely
empty. No relevant source-program or postcondition fact has been hidden under
another classification.

As additional operational evidence, I made a fresh K workspace and explicitly
ran `kompile`, two `krun` executions, and `kprove` without invoking the
untrusted `prove.sh`. The executions returned `true` and `false` on the two
representative branches, and the frozen spec proved with `#Top`. A separate
counterfactual claim requiring `false` for two empty strings exited 1 and
stuck with the actual result `boolValue(true)`. This confirms the result is
constrained and the summary is not vacuous.

Raw evidence:
[08-frozen-source-and-semantics.txt](evidence/08-frozen-source-and-semantics.txt),
[10-fresh-k-operational-recheck.txt](evidence/10-fresh-k-operational-recheck.txt),
and [11-k-false-result-mutation.txt](evidence/11-k-false-result-mutation.txt).

## Recorded hash verification

I independently recomputed every source/tree hash in
`resolution.hashes`. All match:

| Binding | Recomputed value |
|---|---|
| Stage 1 full workspace tree | `018fcb10add2ae00dbb0e2bc6762d07b27d108db105c8665e706ea8305289a23` |
| Stage 1 deterministic-export tree | `0d4f92f6e0f80f3553d28f61e73ae5700abf82df6a3781c841c4b5c684acea5a` |
| Stage 3 discovery manifest | `e83f7ed1e1cf05aa31cceff8c1e41aadc6dbe275dd6bee484647d0a016cca42b` |
| Selected Stage 2 audit tree | `df7fd4c8716e34a789113c5e92c321f4b5f48d8c9a5ddbce4e2ad85f34e0ab8e` |
| Selected Stage 4 generation tree | `3b2ec663a394df4dc620dd3c88c545ef97b5497edc7e4e430a0ae32697c3f252` |
| Producer-source bundle tree | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |
| Generated Lean project tree | `2cb03a3bc41b48bf5b95e51a9193799c859072179809c64145f9181ddaf88763` |
| Lean workspace/invocation | both null, as recorded |

The complete per-file `stage1_source_hashes` dictionary also matches, as do
the selected-artifact hashes. The canonical signed-resolution digest
recomputes to
`b40d7234d5da9d473dd0b895a325cd65fc729bea1d614e1b16753fcf0274dfa5`.
The generator toolchain object exactly equals the pinned toolchain lock.

Raw evidence and the independent check program:
[06-hash-and-structure-results.txt](evidence/06-hash-and-structure-results.txt)
and [hash-and-structure-check.py](evidence/hash-and-structure-check.py).

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and the required Stage 1 workspace, Stage 3 manifest,
Stage 4 generation, and pinned toolchain lock. The successful returned
evidence is:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count 0;
- target null;
- designated sorry count 0;
- 47 generated trust declarations;
- `lake clean` exit 0 with empty output; and
- `lake build` exit 0 with output SHA-256
  `9e8b698d35beea8e497798054831392731be841c5239a29c9d23dfcf864ae2ae`.

This result exactly equals both the selected `preflight.json` and the preflight
object signed into `/audit-input.json`.

The first direct rerun exposed an audit-container PID-namespace defect: Lean's
runtime looked up `/proc/<namespace-pid>/exe`, while the mounted `/proc`
contained host PIDs. A second diagnostic attempt fixed Lake discovery but
showed the same defect in Lean. For the successful rerun, I used the documented
small `LD_PRELOAD` shim in [pid_shim.c](evidence/pid_shim.c), scoped to the
preflight process tree, which returns the numeric host PID exposed by
`/proc/self`. It does not alter any frozen or generated source. The two failed
attempts and the final successful run are preserved rather than hidden:
[03-preflight-rerun.txt](evidence/03-preflight-rerun.txt),
[04-preflight-rerun-pinned-env.txt](evidence/04-preflight-rerun-pinned-env.txt),
and [05-preflight-rerun-success.txt](evidence/05-preflight-rerun-success.txt).

## Obligation bijection and fixed target

The independently classified domain-rule ID sequence is `[]`.
`input-manifest.json` has `source_rules: []`. The generated
`obligation-map.json` has `source_rules: []`, `obligations: []`, and
`trust_parameters: []`. Thus the source-rule/obligation mapping is an exact
empty-to-empty bijection: no omission, duplication, irrelevant obligation,
weakened conjunct, or vacuous conjunct exists.

The obligation-map file hashes to
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. The trusted expected-target computation
returns null, the independent target scanner returns null, every recorded
target is null, and `Lemmas.lean` contains no `targetStatement`, theorem, or
lemma. In particular, the generator did not replace the empty obligation set
with a vacuous `True` target.

This is exactly the permitted `KLEAN_NO_OBLIGATIONS` case: the true domain set
is empty, there is no generated target, and there is no Stage 5 candidate.

Raw evidence: [07-generated-target-scan.txt](evidence/07-generated-target-scan.txt).

## Final judgment

Stage 3 completely and correctly classifies the sole local verification rule
as a definition. Deterministic Stage 4 preserves all provenance and structural
bindings and correctly emits no proof obligation or target. The selected
no-obligations status is mathematically legitimate, not merely
self-consistent.

VERDICT: PASS
LEGITIMACY: LEGIT
