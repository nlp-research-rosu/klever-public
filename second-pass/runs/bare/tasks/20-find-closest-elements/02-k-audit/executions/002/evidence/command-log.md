# Bounded audit command log

All mutable commands ran in `/tmp/audit-work/closest-audit`, using source files
copied individually from the read-only mounts. Candidate kompiled directories,
`kore-exec.tar.gz`, bytecode caches, and prior logs were not copied or used.

## Stage 1: provenance

Commands:

```sh
find /candidate /generation-evidence /reference -type l -print
sha256sum /audit-campaign-lock.json /run.json /task.json \
  /generation-result.json /generation-evidence/invocation.json \
  /generation-evidence/metrics.json /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt /reference/canonical.py \
  /reference/prompt.py /reference/py2mpy.py \
  /candidate/prompt.py /candidate/py2mpy.py
cmp -s /candidate/prompt.py /reference/prompt.py
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
```

Relevant result: no symlinks were printed; both `cmp` commands exited 0. Every
single-file digest matched its corresponding `/audit-input.json` record. In
particular:

```text
audit_campaign_lock  ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745
run.json             16ab5496e5b7251ecd747d4b58693a614cb2f6d680317214f597d0437ab39c24
task.json            361985db249bb79e03e5ef2ddc0aa855f13bd0fa1bfa0efb21029e3858fc926c
generation-result    7419c2c430f15778a85fc844a00e69c0ceadf2eb00e3a7f9a64e842ccb1d37f8
invocation           708f5c2b50d7cce25bb6df7c61ffccae898bc37c622d3870e33a3e8784f2bce2
metrics              b41e7d197be61a236cc5e144ddc2defd04d64c2b166a232fe0d858c04809a541
usage                0a265a4a586a85ef2a6859b629d7c819b8c77ce487294faf52ce2c0633664c84
codex-last           ac4b7a8c0fff9c1facfe2dbf6371e896b45456ab180a46b49591ee567418fe1a
codex-output         f710c74029591be84a3564c30a34b7d7c3928ea0cbd425e60e9855156c042c38
generation prompt    4fbd8d83152646045c82c9b1c86a3c0c9bf686de949fcbf8c3eff6755a261d9e
canonical            53c1d15a396d19a289cc058703f79ef628f4fda28f42ee90cb159895cd3931dc
prompt               881d52f394307cce02e432bc6342c93bfe0f6652b203f0bf1a0fc365ed87c594
translator           406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16
```

Campaign comparison:

```sh
python3 -c 'import json,hashlib,pathlib; a=json.loads(pathlib.Path("/audit-input.json").read_text()); l=json.loads(pathlib.Path("/audit-campaign-lock.json").read_text()); print("campaign_object_equal",a["audit_campaign"]==l); print("campaign_lock_sha256",hashlib.sha256(pathlib.Path("/audit-campaign-lock.json").read_bytes()).hexdigest()); print("recorded_lock_sha256",a["hashes"]["audit_campaign_lock_sha256"]); print("record_layout",a["record_layout"]); print("semantics_mode",a["semantics_mode"]); print("mount_reference_semantics",a["mount_reference_semantics"])'
```

Output, exit 0:

```text
campaign_object_equal True
campaign_lock_sha256 ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745
recorded_lock_sha256 ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745
record_layout legacy-selected-stage1
semantics_mode GENERATED_SEMANTICS
mount_reference_semantics False
```

Candidate/trace tree and structured-record checks:

```sh
python3 -c 'import sys; sys.path.insert(0,"/opt/humaneval/tools"); import pipeline_contract as p; from pathlib import Path; print("candidate_sha256_tree="+p.sha256_tree(Path("/candidate"))); print("trace_sha256_tree="+p.sha256_tree(Path("/generation-evidence/codex-trace")))'
sha256sum /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T04-18-22-019f891e-7403-7981-b455-6eb4f3fe6275.jsonl
```

Output, exit 0:

```text
candidate_sha256_tree=adc52633e57d70e47975c9d0b1ca8f81cecb6bd68fc8f1c041463fb7a4ff0f06
trace_sha256_tree=c76b406b66475ce0c65e2e6cba46037ee7bd4aa0e9bbd89ef3fb9658c90f8994
93b9475722376fc1de9b9727806a9554fd988cde5cfda926c1b9dd21baf95cad  ...jsonl
```

The candidate tree digest equals the `workspace_sha256` in both
`generation-result.json` and `invocation.json`. The trace-tree digest equals
`usage.json`'s `source_trace_sha256`, and the trace file digest equals the
per-file invocation record. A full JSONL read reported:

```text
trace_lines 165
invalid_json []
event_types {'session_meta': 1, 'event_msg': 52, 'response_item': 110, 'world_state': 1, 'turn_context': 1}
last_event_type event_msg
```

The complete generation output was read as strict text:

```text
output_log_chars 487555
output_log_lines 12803
contains_final_marker True
top_mentions 9
kprove_mentions 19
warn_stuck_mentions 1
```

These are provenance observations only, not proof evidence.

## Stage 2: trusted regeneration and differential test

Commands:

```sh
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy submitted-solution.mpy
sha256sum solution.py regenerated-solution.mpy submitted-solution.mpy \
  canonical.py py2mpy.py
python3 /audit-output/evidence/differential_test.py
```

All exited 0. Relevant output:

```text
6a4a805b4d8063f1c394927385520e6e2a8a768dbd773c4fb0f41284ac191c1c  solution.py
b55ed6ed23309810651d2a11ca145e61a0fcffac8d85a3150ccc20345c9f43ab  regenerated-solution.mpy
b55ed6ed23309810651d2a11ca145e61a0fcffac8d85a3150ccc20345c9f43ab  submitted-solution.mpy
53c1d15a396d19a289cc058703f79ef628f4fda28f42ee90cb159895cd3931dc  canonical.py
406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16  py2mpy.py
```

Differential summary:

```text
EXHAUSTIVE_INPUTS=3900
RANDOM_INPUTS=2500
IN_DOMAIN_MISMATCHES=0
OUT_OF_DOMAIN_OBSERVATIONS=[
  ('out_of_domain_empty', canonical returned None, candidate raised IndexError),
  ('out_of_domain_singleton', canonical returned None, candidate raised IndexError)
]
```

The script prints all 14 named cases; these include both prompt examples,
length-two ascending/descending/equal, both outcomes of the later-gap branch,
the inner swap, an equal-gap tie, negatives, signed zero, large magnitudes, and
the two out-of-domain lengths.

## Stage 3: clean rebuild and concrete generated-semantics execution

Tool versions:

```text
K version: v7.1.293
Build date: Fri Oct 03 13:32:35 CDT 2025
```

Commands and statuses:

```sh
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-semantic-llvm-kompiled
# exit 0

krun solution.mpy --definition fresh-semantic-llvm-kompiled --output pretty
# exit 0; <k> .K, empty env, function binding installed, noResult

kompile verification.k --backend llvm \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-VERIFICATION \
  --output-definition fresh-verification-llvm-kompiled
# exit 0
```

Concrete executions:

```sh
krun run-example-1.mpy --definition fresh-verification-llvm-kompiled --output pretty
# exit 0; result vtuple(vnum(2),vnum(11 /Rat 5))

krun run-length2-descending.mpy --definition fresh-verification-llvm-kompiled --output pretty
# exit 0; result vtuple(vnum(1),vnum(2))

krun run-negative-update.mpy --definition fresh-verification-llvm-kompiled --output pretty
# exit 0; result vtuple(vnum(-7 /Rat 2),vnum(-3))

krun run-out-of-domain-empty.mpy --definition fresh-verification-llvm-kompiled --output pretty
# exit 113; residual valueAt(vnil,0)
```

The corresponding Python candidate results were `(2.0,2.2)`, `(1.0,2.0)`,
`(-3.5,-3.0)`, and `IndexError`.

Fresh proof:

```sh
kompile verification.k --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-VERIFICATION \
  --output-definition fresh-verification-proof-kompiled
# exit 0

kprove spec.k --definition fresh-verification-proof-kompiled \
  --spec-module SPEC
```

Output and status:

```text
#Top
kprove_all_claims_exit=0
```

The single `kprove` invocation selects the complete `SPEC` module, hence all
six unlabeled positive claims.

## Stage 4: program pinning and body sensitivity

Commands:

```sh
python3 /audit-output/evidence/extract_solution_rhs.py \
  > proof-embedded-solution.mpy
kast regenerated-solution.mpy \
  --definition fresh-verification-proof-kompiled \
  --module MPY-VERIFICATION --sort Program --output kore \
  --output-file regenerated-solution.kore
kast proof-embedded-solution.mpy \
  --definition fresh-verification-proof-kompiled \
  --module MPY-VERIFICATION --sort Program --output kore \
  --output-file proof-embedded-solution.kore
cmp -s regenerated-solution.kore proof-embedded-solution.kore
```

All exited 0:

```text
49688d9f3ee1f5d0191129959613193e441b4c09fddf4b0e0a6d3db493f8d5dd  regenerated-solution.kore
49688d9f3ee1f5d0191129959613193e441b4c09fddf4b0e0a6d3db493f8d5dd  proof-embedded-solution.kore
12835 regenerated-solution.kore
12835 proof-embedded-solution.kore
```

The extractor requires exactly three `.Stmts` units and normalizes those rule
notations to the concrete parser's empty-list spelling before comparison.

```sh
python3 /audit-output/evidence/claim_witnesses.py
# exit 0
```

Output ends with `SATISFYING_WITNESSES=6`; every formal result matched both
Python implementations.

The actual executed program term was then mutated (second initialization index
`1` to `0`):

```sh
kompile verification-body-mutated.k --backend haskell \
  --main-module MPY-VERIFICATION-BODY-MUTATED \
  --syntax-module MPY-VERIFICATION-BODY-MUTATED \
  --output-definition fresh-body-mutated-kompiled
# exit 0
kprove spec-body-mutated.k --definition fresh-body-mutated-kompiled \
  --spec-module SPEC-BODY-MUTATED
# exit 1
```

Relevant residual:

```text
Warning (WarnStuckClaimState)
<result> vtuple ( vnum ( 1 ) , vnum ( 1 ) ) </result>
[Error] Prover: backend terminated because the configuration cannot be rewritten further.
```

## Stage 5: static inventory

Commands:

```sh
rg -n '\[(function|total|functional|simplification|priority|owise|anywhere|macro|alias|strict|seqstrict|heat|cool|concrete)' semantic.k verification.k spec.k
rg -n '^[[:space:]]*(syntax|rule|claim|configuration|imports|requires|module|endmodule)' semantic.k verification.k spec.k
```

The exhaustive result and per-rule decisions are preserved in
`rule-inventory.md`: 51 local semantics rules, 4 verification rules, and 6
claims. No local totality, simplification, priority, opacity, or operational
bridge was found.

## Stage 6: fresh false-result mutation

The false mutation expects `(2,5)` for the first prompt input, whose true result
is `(2,11/5)`.

```sh
kprove spec-vacuity-audit.k \
  --definition fresh-verification-proof-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
# exit 0; emitted a valid kore-exec --prove command

kprove spec-vacuity-audit.k \
  --definition fresh-verification-proof-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
# exit 1
```

Relevant residual:

```text
Warning (WarnStuckClaimState)
<result>
  vtuple ( vnum ( 2 ) , vnum ( 11 /Rat 5 ) )
</result>
[Error] Prover: backend terminated because the configuration cannot be rewritten further.
```
