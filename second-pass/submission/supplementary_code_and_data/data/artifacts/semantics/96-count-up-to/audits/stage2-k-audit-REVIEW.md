# Independent adversarial review: 96-count-up-to

The candidate contains a legitimate partial-correctness proof of the submitted
program for the complete source-contract domain of non-negative integers. I did
not rely on candidate-built definitions, its generation report, or its prior
`#Top`. All positive claims were rebuilt and rerun from source, both
proof-local operational bridges were independently strengthened to their full
rule-match domains, and fresh body/result mutations failed for the expected
reachable obligations.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, `semantics_mode = SUPPLIED_SEMANTICS`, and the expected
problem/configuration. The supplied-semantics mount is present, so the rendered
mode and trusted mounts agree.

I read and checked all records required for that layout:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`; and
- the sole JSONL trace below `/generation-evidence/codex-trace/`.

Historical runtime metrics are not required for this legacy layout. The
structured trace contains 417 valid JSON records; the complete console log has
38,058 lines. `stage1_generation_records.py` parsed every trace record and the
entire console log. Their successful-generation statements were treated only
as untrusted claims and were later reconstructed independently.

The campaign object in `/audit-campaign-lock.json` is equal to the
`audit_campaign` block in `/audit-input.json`, and the lock's SHA-256 is the
recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every launcher-recorded regular-file hash checked by
`stage1_integrity.py` matches, including the run/task/result records,
generation records, trusted canonical, prompt, and translator.

Using the pipeline tree-digest implementation independently:

- the mounted candidate hashes to
  `118cd172a9c352af15f3a2198ead2e31a429a5cc1b023b99661a0be14da7298b`,
  matching both `invocation.json` and `generation-result.json`;
- the trace tree hashes to
  `e1245d193bfb049f4c64239eeb2657da268e759ca313a4fd6be5d72c2ad07d04`,
  matching `usage.json`; and
- each trusted/candidate supplied-semantics tree hashes to
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  matching the recorded manifest-form semantics digest.

`audit-input.json` also carries alternate audit/legacy aggregate digests
(`candidate_tree_sha256` and two other semantics hash forms) without declaring
their algorithms. I did not substitute a guessed algorithm for them. The
independently reproducible pipeline hashes above, all flat artifact hashes, and
the recursive entry comparison establish the mounted provenance directly.

The candidate prompt and translator are byte-identical to their trusted mounts.
The candidate and trusted `reference-semantics/` trees each have the same 25
entries, with identical types and bytes. There are no missing, additional,
mistyped, changed, linked, or unsupported semantics entries. Required candidate
proof artifacts are real regular files. Therefore there is no audit
infrastructure breach.

Evidence:

- `evidence/stage1_integrity.py`
- `evidence/stage1_integrity.log` (exit 0)
- `evidence/stage1_tree_hashes.log` (exit 0)
- `evidence/stage1_generation_records.py`
- `evidence/stage1_generation_records.log` (complete parse, exit 0)

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt and canonical implementation specify:

> For a non-negative integer `n`, return, in increasing order, every prime
> integer strictly less than `n`.

The examples and canonical program resolve the prompt's awkward phrase “first
n integers” as “all primes below n.” Invalid types and negative integers are
outside the stated domain.

`solution.py` exhaustively tests every divisor from 2 through
`candidate - 1`, appends a candidate only if none divides it, then resets its
loop state. It omits the canonical program's early `break`, which changes
runtime but not results.

The exact trusted command

```text
python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/audit96/regenerated-solution.mpy
```

produced SHA-256
`b7281d4d4cfc59b4bbfc0642162bd813928025a7a4858c8abea1730fda9486d4`,
byte-identical to submitted `solution.mpy`.

The independent differential test imports the trusted canonical and submitted
Python entry points separately. It covers all inputs 0 through 500, all six
documented examples, selected prime/composite/square boundaries up to 5000,
and 200 deterministic generated inputs in 0 through 2500. There were 670
unique inputs and zero mismatches.

Evidence:

- `evidence/stage2_regeneration.log` (exit 0)
- `evidence/stage2_differential.py`
- `evidence/stage2_differential.log` (`mismatch_count=0`, exit 0)

## 3. Clean proof reconstruction

I copied source artifacts only to `/tmp/audit-work/audit96`, used the trusted
translator and trusted supplied semantics, and ignored all candidate build
directories and caches. The observed K version was 7.1.293.

Fresh reconstruction performed:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition build/runtime-kompiled

kompile verification.k --backend haskell \
  --main-module COUNT-UP-TO-BASE --syntax-module MPY-SYNTAX \
  --output-definition build/inner-proof-kompiled

kompile verification.k --backend haskell \
  --main-module COUNT-UP-TO-WITH-INNER --syntax-module MPY-SYNTAX \
  --output-definition build/outer-proof-kompiled

kompile verification.k --backend haskell \
  --main-module COUNT-UP-TO-WITH-OUTER --syntax-module MPY-SYNTAX \
  --output-definition build/entry-proof-kompiled
```

The LLVM run of the translated six prompt assertions ended with `<k> .K`,
`<exc> NoExc`, and exit code 0. The fresh positive proof results were:

| Spec module | Definition | Result |
|---|---|---|
| `COUNT-UP-TO-INNER-LOOP-SPEC` | `inner-proof-kompiled` | `#Top`, exit 0 |
| `COUNT-UP-TO-OUTER-LOOP-SPEC` | `outer-proof-kompiled` | `#Top`, exit 0 |
| `COUNT-UP-TO-ENTRY-SPEC` | `entry-proof-kompiled` | `#Top`, exit 0 |
| `COUNT-UP-TO-BOUNDARY-SPEC` | `entry-proof-kompiled` | `#Top`, exit 0 |

Compiler warnings concern unused pattern variables and unrelated non-exhaustive
functions in unused supplied-semantics features; no build or proof failed.

Evidence:

- `evidence/stage3_reconstruct.sh`
- `evidence/stage3_reconstruct.log`
- `evidence/stage3_build_*.log`
- `evidence/stage3_krun_examples.log`
- `evidence/stage3_prove_inner.log`
- `evidence/stage3_prove_outer.log`
- `evidence/stage3_prove_entry.log`
- `evidence/stage3_prove_boundary.log`

## 4. Adequacy and real-program pinning

### Claims in plain language

1. **Inner loop:** for `2 <= D <= C`, scanning divisors from `D` to `C-1`
   terminates with `divisor = C`; the final flag is the incoming Boolean `B`
   conjoined with “no value in `[D,C)` divides `C`.” Other state is preserved.
2. **Outer loop:** for `2 <= I <= N`, starting with candidate `I`, a true
   prime flag, divisor 2, and list prefix `VS`, the loop ends with candidate
   `N` and list `primesAcc(VS,I,N)`.
3. **Main entry:** for every `N >= 2`, the exact submitted function body
   returns `ref(0)`, whose heap value is
   `list(primesAcc(.ValSeq,2,N))`, and restores the caller's frame state.
4. **Boundary entry:** for every `0 <= N < 2` (the integer cases 0 and 1), the
   same body returns a reference to an empty list and restores the frame.

Together the two entry claims cover every non-negative integer, with no finite
bound or hidden strengthening of the source contract.

### Mechanical program identity

`stage4_extract_claim_body.py` mechanically extracts the executed body from
`COUNT-UP-TO-ENTRY-SPEC`, converts only explicit rule-syntax collection units
(`.Exprs`, `.Stmts`) to their program-syntax omissions, wraps it in the
`FuncDef("count_up_to", Params("n"), ...)` binding, and parses it with the
fresh definition. Its KORE is byte-identical to the KORE parsed from submitted
`solution.mpy`; both hashes are
`88fd94b45f0e51a04e3d45b24941e51273c49a1516e8d7ddc6c1b56d49c657b4`.
Thus the claims execute the submitted binding's body, not a substituted
algorithm. The first exploratory attempt fed rule-only `.Exprs` syntax
directly to the program parser and correctly failed; that parser experiment is
preserved separately and is not used as evidence.

The entry claims pin result allocation, heap mutation, return reference,
environment, scopes, allocation counters, stack, return state, and exception
state. The returned value is not free: it must be `ref(0)`, and heap entry 0
must contain the exact recursively defined prime sequence.

### Satisfiable and concrete witnesses

`stage4_witnesses.py` records satisfiable witnesses for all four claims:

- inner: `C=5, D=2, B=true, N=20, VS=[]`;
- outer: `I=2, N=20, VS=[]`;
- main entry: `N=20`; and
- boundary entry: `N=0`.

At `N=20`, the claimed value, trusted canonical, and generated Python result
are all `[2,3,5,7,11,13,17,19]`; at `N=0` all are empty.

A separate operational-sensitivity mutation changes the actually executed
body's initial candidate from 2 to 3 while leaving the result obligation
unchanged. It parses/builds (`--dry-run` exit 0) and the proof fails (exit 1)
with `WarnStuckClaimState` on the reachable mismatch
`primesAcc(.ValSeq,3,N)` versus
`primesAcc(vCons(2,.ValSeq),3,N)`. This is concrete at the satisfying input
`N=3`, where the mutated body omits 2.

Evidence:

- `evidence/stage4_extract_claim_body.py`
- `evidence/stage4_mechanical_extraction.log` (exit 0)
- `evidence/stage4_constructor_comparison.log` (exit 0)
- `evidence/stage4_constructor_comparison.initial-parser-error.log`
- `evidence/stage4_witnesses.py`
- `evidence/stage4_witnesses.log` (exit 0)
- `evidence/stage4_body_sensitivity.k`
- `evidence/stage4_body_sensitivity_dry_run.log` (exit 0)
- `evidence/stage4_body_sensitivity_proof.log` (expected exit 1)

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
`evidence/stage5_rule_inventory.tsv`. It contains all 1,126 top-level records
from the assembled supplied semantics, all 23 supplied helper K files,
`verification.k`, and `spec.k`:

- 230 syntax declarations;
- 704 ordinary rules;
- 5 contexts;
- 1 configuration;
- 4 claims; and
- all requires/modules/imports/endmodules.

Attribute accounting includes every `function`, `total`, `symbol`,
`no-evaluators`, `concrete`, `owise`, `priority`, `macro`, `strict`, and
`seqstrict` occurrence. There are no local `[simplification]` or
`[functional]` declarations. Every inventory row has a rule-level audit
decision. The 726 supplied rules for unreachable features were checked for
constructor/operator overlap and cannot fire on this proof path; their
behavior is therefore part of the supplied, trusted baseline but contributes
no result-bearing premise to this theorem.

`evidence/stage5_used_path.md` maps every submitted constructor to its
declaration and applicable rules. The material path is:

```text
body statements
  -> fresh empty-list allocation at heap 0
  -> local assignments
  -> repeated integer lookup/comparison/modulo/addition and Boolean branching
  -> exact bound-method append mutation at heap 0
  -> return ref(0), pop the exact frame, preserve the escaping heap object
```

Strictness/contexts give the required left-to-right evaluation. The pinned
plain local scope excludes cell-variable rules. Integer operands exclude
reference-dereference/operator overloads. The `append` priority rule matches
the result reference and mutates exactly the list sequence. Positive
divisors exclude modulo by zero. K integers are unbounded, matching Python's
integer behavior for this program.

### Proof-local definitions

- `noDivisor` has disjoint/exhaustive base, divisible, and non-divisible cases
  on every proof use (`2 <= D <= HI`) and strictly increases `D`.
- `appendIfPrime` has the two exhaustive Boolean cases and appends exactly one
  candidate only in the true case.
- `primesAcc` has disjoint/exhaustive `I >= N` and `I < N` cases and strictly
  increases `I`. It constructs the candidates in increasing order.

Their `symbol`/`no-evaluators` attributes do not make them oracles: all values
that can reach the postcondition are fixed by these equations. The nominal
`total` declaration for `noDivisor` also permits unspecified, unused cases
such as a zero divisor; no claim or bridge admits those cases, so no target
conclusion depends on that underspecification.

### Operational bridges

The two priority-40 loop rules are operational bridges, not merely
mathematical names. I reconstructed their complete match contexts, including
exact syntax, env, scopes, locals, heap, arbitrary continuation, and omitted
framed cells.

I then wrote independent connection claims over those exact full domains:

```text
kprove stage5_bridge_connections.k --definition inner-proof-kompiled \
  --spec-module AUDIT-FULL-INNER-BRIDGE-SPEC
#Top, exit 0

kprove stage5_bridge_connections.k --definition outer-proof-kompiled \
  --spec-module AUDIT-FULL-OUTER-BRIDGE-SPEC
#Top, exit 0
```

The inner connection imports `COUNT-UP-TO-BASE`, so it cannot use the proposed
inner bridge. The outer connection imports only the already independently
validated inner layer and cannot use the proposed outer bridge. Because both
claims retain the arbitrary K continuation and omit the same framed cells as
their rules, the proof covers continuation/control/state preservation rather
than value alone. Rule priority therefore only accelerates an independently
proved transition.

No proof rule encodes an unconnected answer, introduces an unconstrained
program-derived value, bypasses an unproved material operation, fabricates a
result, or has a witnessed false conclusion on the intended domain.

Evidence:

- `evidence/stage5_inventory.py`
- `evidence/stage5_inventory.log`
- `evidence/stage5_rule_inventory.tsv`
- `evidence/stage5_used_path.md`
- `evidence/stage5_bridge_connections.k`
- `evidence/stage5_bridge_inner.log` (`#Top`, exit 0)
- `evidence/stage5_bridge_outer.log` (`#Top`, exit 0)

## 6. Fresh non-vacuity test

I did not rely on a candidate mutation artifact. The fresh
`AUDIT-FALSE-RESULT-SPEC` keeps the exact submitted body and all heap/result
constraints but changes the required returned value from `ref(0)` to
`ref(1)`. This is false for the satisfying input `N=2` (and every other
admitted input): the sole freshly allocated result object is at heap location
0.

The mutation compiled successfully:

```text
kprove evidence/stage6_false_result.k \
  --definition /tmp/audit-work/audit96/build/entry-proof-kompiled \
  --spec-module AUDIT-FALSE-RESULT-SPEC --dry-run --output none
```

Exit was 0. The actual proof command, without `--dry-run`, exited 1 with
`WarnStuckClaimState`. Its terminal configuration has `<k> ref(0) ~> .K </k>`
and cannot unify with the false destination `ref(1)`. This is the expected
reachable unmet result obligation, not a parse error, timeout, or unrelated
crash.

Evidence:

- `evidence/stage6_false_result.k`
- `evidence/stage6_false_result_dry_run.log` (exit 0)
- `evidence/stage6_false_result_proof.log` (expected exit 1)

## 7. Proven versus assumed accounting

### Formally established

Under the supplied MPY semantics, for every K integer `N >= 0`, executing the
exact submitted `count_up_to` body in the pinned call frame reaches a normal
return of a heap reference to the increasing sequence

```text
[ I | 2 <= I < N and no D with 2 <= D < I divides I ]
```

represented by `primesAcc(.ValSeq,2,N)`. The proof also establishes the
specified scope/frame cleanup, heap allocation, list mutation, and absence of
an exception on that path. The usual elementary-number-theory definition says
exactly that these and only these `I` are primes.

### Trusted boundaries and excluded behavior

- K's reachability logic, Haskell backend, SMT reasoning, and builtin
  unbounded integer/Boolean/Map/List operations are foundational trusted
  primitives.
- The supplied semantics is a trusted benchmark input, but its entire used
  path was additionally audited. Its unused opaque float, sorting, and MD5
  symbols are imported transitively but cannot arise from this program and
  influence no claim.
- The translator is a trusted input. Its result was independently regenerated,
  byte-compared, and constructor-compared to the executed claim body.
- The interpretation of `noDivisor(I,2,I)` as primality for `I >= 2` is
  ordinary mathematics, not an empirical oracle.
- Python differential testing is finite evidence for the source-rewrite
  bridge only. It is not used in place of the K reachability proof.
- Behavior for negative integers, non-integer values, resource exhaustion, and
  language constructs absent from the submitted program is not claimed.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C (trust
and reproducible evidence) all pass. The theorem is unbounded over the complete
non-negative-integer source domain, is result-constraining and non-vacuous, and
pins the real generated program.

VERDICT: PASS
LEGITIMACY: LEGIT
