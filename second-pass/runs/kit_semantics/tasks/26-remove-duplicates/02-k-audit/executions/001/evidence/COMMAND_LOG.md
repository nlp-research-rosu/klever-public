# Independent audit command log

All build and proof commands were run from `/tmp/audit-work/audit-26`.
Read-only integrity commands were run from `/audit-output`. Outputs below are
bounded to the parts relevant to the audit decision.

## 1. Provenance and supplied-semantics integrity

```bash
sha256sum /audit-campaign-lock.json /reference/canonical.py \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /run.json /task.json /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/runtime-metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/24/rollout-2026-07-24T23-46-27-019f9798-9801-70e0-9f1c-273148e9ebef.jsonl
cmp -s /candidate/prompt.py /reference/prompt.py
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
diff -qr --no-dereference /candidate/reference-semantics \
  /reference/reference-semantics
```

Exit: `0` for both `cmp` commands and `diff`.

Relevant output:

```text
ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745  /audit-campaign-lock.json
0b3dc0edbebd5bb456ef0386a280581e47a0584f3b98153a07b55ef0c80f4241  /reference/canonical.py
7823eea9be9599563c786fa16e792f3da2482016607d75ee06ca40b2d33c7dca  /reference/prompt.py
7823eea9be9599563c786fa16e792f3da2482016607d75ee06ca40b2d33c7dca  /candidate/prompt.py
406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16  /reference/py2mpy.py
406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16  /candidate/py2mpy.py
3b99df09203880c9a59a6dcfed87c41b60e6057ebf8720421e156f1e7517bd73  /run.json
5660ce490916ff9080d312d49a23681dbc154d0a48d6b559af14710d873d383f  /task.json
fee42a560b98d2cea49fff838b849a9c36f5a2037ab64cf04679bff8ed40adaf  /generation-result.json
655bd6d6c35f63d8440b759492903497957f64d2ccdb2440472381bccca92207  /generation-evidence/invocation.json
e8fd45c7ebf7e3ae5fdec26812b3efa43c3ae65cb792cb709b6826261acae51e  /generation-evidence/metrics.json
7da99e17d4508305a3765cd5a3877f140f87bc64d03b8e99fffbca3361583855  /generation-evidence/runtime-metrics.json
09d411b94f74960ba91282ba8162247feff4c6b19544e5f6e661f778b20c502a  /generation-evidence/usage.json
d8d6138894a5c8a465ef82ce7d65d1b27b70500641483bdb3b35db34993f8101  /generation-evidence/codex-last.txt
c9247528f83b1057090dbfd2444a3c059e6127c4db6d93ac4d538686d416840f  /generation-evidence/codex-output.log
c5f7af5f994f1d98d2cb3ab967f88f74a437a6548277cceaf24481aba1cf31e5  /generation-evidence/prompt.txt
7ab788ffdff6d0c0add3cf731aae904d59cfb581bcdf291db2e9fb623889ec31  /generation-evidence/codex-trace/...jsonl
```

The campaign block deep comparison returned `True`. Independent tree
manifests found zero symlinks in `/candidate` and identical content manifests
for candidate/trusted semantics:

```text
candidate entries=783 symlinks=0
candidate semantics manifest_sha256=dd4afae8d7a4e2c1b06b8840d070f4d19aff1ba09e353f19de57e7f9c6af3fe3
trusted semantics manifest_sha256=dd4afae8d7a4e2c1b06b8840d070f4d19aff1ba09e353f19de57e7f9c6af3fe3
```

## 2. Trusted regeneration and differential execution

```bash
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
python3 /audit-output/evidence/independent_differential.py \
  canonical.py solution.py
```

Exit: translator `0`; byte comparison `0`; differential script `0`.

```text
0a1f3742d1a9870e83de95c510044b37d3cf3899be7c16f12e61b33bea7360de  solution.mpy
0a1f3742d1a9870e83de95c510044b37d3cf3899be7c16f12e61b33bea7360de  solution.regenerated.mpy
documented-example: input=[1, 2, 3, 2, 4] canonical=[1, 3, 4] generated=[1, 3, 4] rdAcc=[1, 3, 4]
empty: input=[] canonical=[] generated=[] rdAcc=[]
singleton-append-branch: input=[0] canonical=[0] generated=[0] rdAcc=[0]
pair-skip-boundary: input=[7, 7] canonical=[] generated=[] rdAcc=[]
triple-skip: input=[7, 7, 7] canonical=[] generated=[] rdAcc=[]
named cases: 10
exhaustive cases: 19531
random cases: 3000
total cases: 22541
mismatches: 0
```

## 3. Fresh concrete definition and execution

```bash
python3 py2mpy.py k_smoke.py > k_smoke.mpy
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
krun k_smoke.mpy --definition runtime-audit-kompiled
```

Exit: all three commands `0`.

The LLVM build warned that six unrelated total functions have uncovered
constructors outside their intended subdomains: `mapStrVS`, `floorFI`, `toF`,
`ceilF`, `joinCodes`, and `valSeqAt`. The executed result ended with:

```text
<k> .K </k>
<stack> .List </stack>
<ret> noRet </ret>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

The heap contained the expected outputs for empty, singleton, pair-duplicate,
prompt-example, negative/mixed, and unbounded-large-integer assertions,
including:

```text
list(vCons(1, vCons(3, vCons(4, .ValSeq))))
list(vCons(3, vCons(4, .ValSeq)))
list(vCons(100000000000000000000,
  vCons(-100000000000000000000, vCons(5, .ValSeq))))
```

## 4. Fresh proof definition

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

Exit: `0`. Output contained only four unused-variable warnings in the trusted
`strLt` equations.

## 5. Positive target claims

```bash
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC --claims SPEC.remove-duplicates-loop
```

Exit: `0`.

```text
#Top
```

```bash
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC
```

Exit: `0`.

```text
#Top
```

The unfiltered second command proves both claims jointly, so the entry claim
has the loop claim available as its circularity.

## 6. Mechanical real-program comparison

```bash
python3 /audit-output/evidence/extract_claim_program.py \
  spec.k entry-claim-program.mpy \
  --rule-output entry-claim-program.rule
kast solution.mpy --definition verification-audit-kompiled \
  --sort Module --output json --output-file solution.ast.json
kast entry-claim-program.rule --definition verification-audit-kompiled \
  --input rule --module VERIFICATION --output json \
  --output-file entry-claim.rule.json
python3 /audit-output/evidence/compare_program_ast.py \
  solution.ast.json entry-claim.rule.json
```

Exit: all four commands `0`.

```text
entry #loadAll count: 1
translated root: Module(_)_MPY-SYNTAX_Module_Stmts
claim root: Module(_)_MPY-SYNTAX_Module_Stmts
translated AST sha256: 9795cb92042d4dc5299d1cbba98d933d9e025056ba24e034b3a8e74cb1c86937
claim AST sha256: 9795cb92042d4dc5299d1cbba98d933d9e025056ba24e034b3a8e74cb1c86937
translated/claim module identical: True
```

Two earlier diagnostic attempts treated the K-source spelling `.Exprs` as
program-parser input and exited `113`/`2`; they were discarded. The recorded
comparison uses K's rule parser for the claim spelling and K's program parser
for translator output.

## 7. Fresh false-result mutation

```bash
kprove spec-false-result-audit.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-FALSE-RESULT-AUDIT --dry-run
```

Exit: `0`; output was a complete `kore-exec ... --prove ...` invocation, so
the mutation parsed and built.

```bash
kprove spec-false-result-audit.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-FALSE-RESULT-AUDIT
```

Exit: `1`, expected.

```text
Warning (WarnStuckClaimState):
The configuration's term doesn't unify with the destination's term
...
<k> ref ( 0 ) ~> .K </k>
<heap> 0 |-> list ( vCons ( 1 , .ValSeq ) ) </heap>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
[Error] Prover: backend terminated because the configuration cannot be
rewritten further.
```

The mutation demanded heap value `[99]` for satisfying input `[1]`; the
residual exposes the actual `[1]`.

## 8. Body-sensitivity probe

```bash
kprove spec-body-sensitivity-audit.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-BODY-SENSITIVITY-AUDIT --dry-run
kprove spec-body-sensitivity-audit.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-BODY-SENSITIVITY-AUDIT
```

Exit: dry-run `0`; proof `1`, expected.

The mutation changed the executed loop guard from `count == 1` to
`count == 2` while retaining the original `rdAcc` destination. The residual
contains:

```text
Warning (WarnStuckClaimState):
The configuration's term unifies with the destination's term, but the
implication check between the conditions has failed.
...
{ 1 #Equals cntOccVS ( ALL , V ) }
...
{ rdAcc(valSeqConcat(ACC,vCons(V,.ValSeq)),R,ALL)
  #Equals rdAcc(ACC,R,ALL) }
```

## 9. Exhaustive source inventory

```bash
python3 /audit-output/evidence/k_rule_inventory.py \
  --root /reference/reference-semantics \
  --extra /candidate/verification.k /candidate/spec.k \
  --output /audit-output/evidence/K_RULE_INVENTORY.md
```

Exit: `0`.

```text
files=26
items=1103
kind_counts={'claim': 2, 'configuration': 1, 'context': 5,
  'endmodule': 27, 'imports': 88, 'module': 27, 'requires': 25,
  'rule': 699, 'syntax': 229}
tag_counts={'concrete': 36, 'equational': 461, 'function': 148,
  'macro': 4, 'macro-rec': 1, 'no-evaluators': 22, 'opaque': 22,
  'operational': 238, 'owise': 26, 'priority': 45,
  'seqstrict': 1, 'strict': 2, 'symbol': 25, 'total': 109}
```

## 10. Full generation-record inspection

```bash
python3 /audit-output/evidence/summarize_generation_trace.py \
  /generation-evidence/codex-trace/2026/07/24/rollout-2026-07-24T23-46-27-019f9798-9801-70e0-9f1c-273148e9ebef.jsonl \
  /audit-output/evidence/GENERATION_TRACE_SUMMARY.md
python3 /audit-output/evidence/summarize_generation_output.py \
  /generation-evidence/codex-output.log \
  /audit-output/evidence/GENERATION_OUTPUT_SUMMARY.md
```

Exit: both `0`.

```text
valid_jsonl_records=311
function_calls=51
messages=17
complete_lines_read=21248
event_lines=83
signal_lines=670
```
