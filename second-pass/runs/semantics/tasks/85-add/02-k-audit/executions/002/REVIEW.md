# Independent adversarial audit — HumanEval/85 `add`

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program over the material source-contract domain. I
assign `CONCERNS`, rather than `PASS`, because the candidate uses an
operational loop-summary rewrite without a bridge-free universal theorem over
the rewrite's complete continuation and cell match domain. The summary value
is nevertheless independently justified for every finite integer sequence,
and I found no witness on the intended domain for a false conclusion.

The audit used K 7.1.293. All candidate and generation records were treated as
untrusted. All builds and experiments were performed from source copies below
`/tmp/audit-work/85-add`; no candidate-built definition or cache was reused.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `85-add`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`; and
- complete input provenance.

The trusted `/reference/reference-semantics` mount is present, as required for
this mode. There is no mode/mount contradiction and therefore no
infrastructure breach.

I independently checked the following:

- `/audit-campaign-lock.json` is a regular file, has SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  matches the hash recorded by `/audit-input.json`, and is deeply equal to its
  `audit_campaign` object.
- Every launcher-required `legacy-selected-stage1` record is a regular,
  readable, non-symlink file: `/run.json`, `/task.json`,
  `/generation-result.json`, `invocation.json`, `metrics.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`.
- `usage.json` is present and its recorded hash matches. Historical
  `runtime-metrics.json` is absent, which is permitted for this legacy layout.
- All recorded hashes for the campaign lock, run/task/result/invocation
  manifests, metrics, usage, prompt, output, last message, canonical source,
  trusted prompt, and translator match independently computed SHA-256 values.
- The structured trace is one regular JSONL file with 694/694 valid JSON
  records. Its SHA-256
  `3c87d329ca38ce4502ad904f55db051606f500941601e135f773e1e3b4c590b0`
  matches the selected-stage record. The inspection script read all 899,493
  trace bytes and all 1,097,626 bytes of `codex-output.log`; generation claims
  such as prior `#Top` results were not relied on.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- Recursive `diff -qr --no-dereference` between the candidate and trusted
  `reference-semantics/` trees exits 0. Both trees have the same 24 regular
  files and the same per-file hashes. No symlink exists anywhere under the
  candidate or trusted reference mounts.
- Required candidate proof artifacts are regular files:
  `solution.py`, `solution.mpy`, `verification.k`, `spec.k`, and executable
  `prove.sh`.

Evidence:

- [stage1_integrity.sh](/audit-output/evidence/stage1_integrity.sh)
  and [stage1_integrity.log](/audit-output/evidence/stage1_integrity.log)
- [stage1_trace_inspect.py](/audit-output/evidence/stage1_trace_inspect.py)
  and [stage1_trace_inspect.log](/audit-output/evidence/stage1_trace_inspect.log)

Stage 1 result: pass; no audit-infrastructure error.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: for a non-empty list of integers, return the
sum of elements that are both at odd zero-based indices and even. The trusted
canonical implementation expresses this directly as a comprehension over
indices `1, 3, 5, ...`.

The candidate uses a different but equivalent single-pass implementation.
`odd_index` starts false, is toggled once after every element, and gates the
evenness test and addition. Thus it is true exactly at odd indices. K and
Python integers are unbounded on the used path, and `% 2` handles negative
even integers as required.

Trusted regeneration was performed with:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

The command exited 0. `cmp solution.mpy regenerated-solution.mpy` exited 0,
and both files have SHA-256
`17a2689caa9b09f7d9c2d776cba052b70c85fdec5f16fcc1f3bf2ed8ab4fe227`.

The independent differential test imports the trusted canonical and candidate
modules under different names. It checked:

- the documented example;
- empty, singleton, zero, sign, parity, and index-boundary cases;
- every list of length 0 through 5 over
  `[-4,-3,-2,-1,0,1,2,3,4]`;
- 2,500 deterministic generated lists of length 1 through 100; and
- very large positive and negative Python integers.

It performed 68,947 comparisons with zero mismatches. Empty input is outside
the stated non-empty contract but also agrees.

Evidence:

- [differential_test.py](/audit-output/evidence/differential_test.py)
- [stage2_fidelity.sh](/audit-output/evidence/stage2_fidelity.sh)
  and [stage2_fidelity.log](/audit-output/evidence/stage2_fidelity.log)

Stage 2 result: pass; no implementation/canonical divergence.

## 3. Clean proof reconstruction

Before building, the scratch directory contained no `runtime-kompiled`,
`verification-kompiled`, or local `.k` cache directory. `kup` is unavailable,
but independently installed `kompile`, `krun`, and `kprove` are present and
all report K 7.1.293.

Fresh concrete definition:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit 0. Fresh execution:

```text
krun concrete-tests.mpy --definition runtime-kompiled --output pretty
```

Exit 0. The final configuration has `.K`, `NoExc`, and exit code `0`.

Fresh proof definition:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition verification-kompiled
```

Exit 0. Each positive target was then selected and run independently:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-invariant-bound --output pretty
```

Output `#Top`, exit 0.

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.add-correct --output pretty
```

Output `#Top`, exit 0.

Warnings concern unused variables and fixed-semantics functions unrelated to
the submitted term; they are not proof failures.

Evidence:

- [stage3_clean_check.log](/audit-output/evidence/stage3_clean_check.log)
- [stage3_toolchain.log](/audit-output/evidence/stage3_toolchain.log)
- [stage3_compile_runtime.log](/audit-output/evidence/stage3_compile_runtime.log)
- [stage3_concrete.log](/audit-output/evidence/stage3_concrete.log)
- [stage3_compile_proof.log](/audit-output/evidence/stage3_compile_proof.log)
- [stage3_prove_loop.log](/audit-output/evidence/stage3_prove_loop.log)
- [stage3_prove_add.log](/audit-output/evidence/stage3_prove_add.log)

Stage 3 result: pass.

## 4. Adequacy and real-program pinning

### Claims in plain language

`loop-invariant-bound` starts at the real loop head with:

- any finite algebraic `IntSeq` input;
- any Boolean phase `ODD`;
- any integer accumulator `ACC`;
- a current frame containing `lst`, `total`, `odd_index`, and integer
  `value`; and
- a non-duplicated current scope location.

If execution reaches loop completion, the post-state's `total` binding is
`addAccSpec(INPUT, ODD, ACC)`. Other local bindings may vary. This is the
standard accumulator/phase invariant for the actual loop body.

`add-correct` starts from the complete initial MPY configuration, loads
`solutionModule`, calls its `add` binding on an arbitrary finite integer
sequence, and constrains the returned `<k>` value to
`addAccSpec(INPUT, false, 0)`. It fixes the initial environment, allocation
counters, empty heap and stack, return state, exception state, and exit code.
Its domain includes the source contract's non-empty lists and additionally the
empty list; it does not narrow the HumanEval domain.

### Satisfiability and ground substitution

A loop precondition witness is `L=1`, `RESTSCOPES=.Map`, parent `parent(0)`,
accumulator 0, phase false, old value 0, and input `[4,2,6,7]`. An entry
precondition witness is the claim's fixed initial configuration with that same
input. A reviewer-authored spec containing both witnesses proves `#Top` with
exit 0.

Ground substitutions give:

| Input | `addAccSpec` | Canonical Python | Candidate Python |
|---|---:|---:|---:|
| `[4,2,6,7]` | 2 | 2 | 2 |
| `[1,-2]` | -2 | -2 | -2 |
| `[-2,-4,-6,-8]` | -12 | -12 | -12 |
| `[1,3,4,-6,8,10]` | 4 | 4 | 4 |

Evidence:

- [spec-witness.k](/audit-output/evidence/spec-witness.k)
  and [stage4_k_witness.log](/audit-output/evidence/stage4_k_witness.log)
- [stage4_witnesses.py](/audit-output/evidence/stage4_witnesses.py)
  and [stage4_witnesses.log](/audit-output/evidence/stage4_witnesses.log)

### Mechanical program identity

The entry claim executes `#loadAll(solutionModule)`. I parsed both the freshly
regenerated `solution.mpy` and the expression `solutionModule` with the fresh
proof definition, expanded macros, emitted KORE, and compared the results:

```text
kast solution.mpy ... --expand-macros --output kore \
  --output-file submitted-program.kore
kast --expression solutionModule ... --expand-macros --output kore \
  --output-file claim-program.kore
cmp submitted-program.kore claim-program.kore
```

`cmp` exits 0; both constructor terms have SHA-256
`d70ea56139c3d89c6426fca3f4001c3ea6f9d5e22aa6760944341019178b5e16`.
This is constructor-level identity, not a textual resemblance argument.

Evidence: [stage4_program_term.log](/audit-output/evidence/stage4_program_term.log).

### Body and bridge sensitivity

I changed the function term actually loaded by the claim: its loop body sets
`total = 1`, while the candidate's original summary bridge was retained and
still matched only `addLoopBody`. The ground input `[4,2]` reaches value `1`
against the original required value `2`; `kprove` reports
`WarnStuckClaimState` and exits 1. Thus changing the executed body is not
masked by a source-only mutation or by the bridge.

Evidence:

- [verification-body-mutant.k](/audit-output/evidence/verification-body-mutant.k)
- [spec-body-mutant.k](/audit-output/evidence/spec-body-mutant.k)
- [stage4_compile_body_mutant.log](/audit-output/evidence/stage4_compile_body_mutant.log)
- [stage4_body_mutant_proof.log](/audit-output/evidence/stage4_body_mutant_proof.log)

### Adequacy limitation

The proof uses a bare read-only `list(intVals(INPUT))` value, whereas a
source-level `ListExpr` is heap allocated and passed by reference. The supplied
semantics explicitly permits bare lists as read-only claim inputs, and this
program neither mutates the argument nor observes identity. Concrete LLVM
tests exercise the heap-reference route. This representation difference does
not alter this program's result, but there is no separate universal theorem in
the candidate connecting both representations.

Stage 4 result: the actual submitted function and full material input domain
are pinned; the representation and bridge-justification limitations are
non-fatal concerns.

## 5. Rule-by-rule static soundness review

The source-complete inventory contains every top-level `configuration`,
`syntax`, `context`, `rule`, and `claim` block in all supplied K files plus
`verification.k` and `spec.k`:

- 947 inventory entries;
- 233 syntax declarations;
- 706 rules;
- 5 contexts;
- 1 configuration; and
- 2 claims.

It separately identifies 148 function declarations, 113 `total`
declarations, 48 priority rules, 36 concrete rules, 26 `owise` rules, 22
`no-evaluators` declarations, 6 macros, one recursive macro, zero
`functional` declarations, and zero simplification rules. Every row contains
the complete source block, attributes, origin, proof-path classification, and
review decision.

Evidence:

- [rule_inventory.py](/audit-output/evidence/rule_inventory.py)
- [rule_inventory.md](/audit-output/evidence/rule_inventory.md)
- [stage5_inventory_generation.log](/audit-output/evidence/stage5_inventory_generation.log)

### Used fixed-semantics path

The submitted term maps mechanically to:

- MPY syntax for `Module`, `FuncDef`, `Params`, `Expr(Str)`, `Assign`,
  `Name`, `Int`, `Bool`, `For`, `If`, `Compare`, `CmpOp`, `BinOp`,
  `AugAssign`, `UnaryOp`, and `Return`;
- core configuration, module loading, statement sequencing, name lookup,
  left-to-right argument evaluation, literals, truthiness, and operator
  dispatch;
- function definition, parameter binding, call-frame creation, return, and
  frame pop;
- `For` conversion to `#loop`, iterator consumption, and `#bindTgt`;
- Boolean `not`, integer `+`, `%`, and `==`; and
- the ASCII string-literal rule for the discarded docstring.

The actual control order is: load exact module; resolve the loaded `add`
closure; evaluate its one argument; create and bind a frame; execute the
docstring and three initial assignments; evaluate the iterable once; consume
one integer per loop step; bind `value`; run nested guards and possible
addition; toggle the phase; return; and pop the frame. No used operation is
unmodeled. There is no relevant output, exception, allocation, or argument
mutation skipped by the used fixed rules.

All fixed-semantics declarations outside this constructor/guard path are
listed in the inventory as off-path. In particular, all opaque float,
sorting, keyed sorting, MD5, slice/index, dict, set, comprehension, and method
symbols are unreachable from this term and cannot affect its result. No
proof-local opaque symbol influences this theorem.

### Candidate-local extensions

| Extension | Classification and decision |
|---|---|
| `intVals(IntSeq)` | A symbolic algebraic representation of finite integer-valued list contents. It is a constructor, not an unconstrained oracle. |
| Two `#iterNext(list(intVals(...)))` rules | Operational extension, but exact and exhaustive over `.IntSeq`/`iCons`; the cons rule yields exactly the integer head and structurally decreases the tail. The rules do not touch state cells. |
| `scopeMap` and its `[function,total]` equation | Exhaustive over the only `Scope` constructor and mathematically definitional. It is unused by either target claim. |
| `addAccSpec` and four equations | Definitional summary. Empty/false/true-even/true-odd cases are exhaustive. The true guards are disjoint and exhaustive for integer `pyMod(I,2)`. Every recursive call descends to `REST`. |
| `addLoopBody`, `addFunctionBody`, `solutionModule` macros | Syntax-only normalization. Their expanded constructor term is mechanically identical to the regenerated program. |
| Loop-summary rule at `verification.k:57` | Operational bridge. It matches the exact original loop body, exact singleton `Return(Name("total"))` statement suffix, exact `#endcall`, exact initial local bindings, and the same `INPUT` in both `lst` and the iterator. It returns the exhaustive `addAccSpec` value. |

The loop-summary bridge reads `<env>` and the current local `<scopes>` entry;
it changes only `<k>`. The skipped loop would update `total`, `odd_index`, and
`value`, but those locals are discarded by the immediately retained
`#endcall`; the replacement directly returns the proved accumulator value.
On finite integer inputs, modulo and addition cannot raise an exception in
the supplied semantics. Heap, allocation counters, caller scopes, exception,
return, and exit-code cells are preserved.

I compiled a bridge-free copy and independently proved
`loop-invariant-bound` under it: `#Top`, exit 0. I also ran bridge-free full
ground entry claims for empty and `[4,2,6,7]` inputs: `#Top`, exit 0. These
establish that fixed loop execution produces the same ground results and that
the universal loop value is `addAccSpec`; they are not inferred from the
candidate bridge.

Evidence:

- [verification-nobridge.k](/audit-output/evidence/verification-nobridge.k)
- [spec-nobridge.k](/audit-output/evidence/spec-nobridge.k)
- [stage4_compile_nobridge.log](/audit-output/evidence/stage4_compile_nobridge.log)
- [stage4_prove_nobridge_loop.log](/audit-output/evidence/stage4_prove_nobridge_loop.log)
- [spec-witness-nobridge.k](/audit-output/evidence/spec-witness-nobridge.k)
- [stage4_ground_nobridge.log](/audit-output/evidence/stage4_ground_nobridge.log)

The remaining concern is precise: the candidate's bridge-free invariant has
an exact `<k>` cell containing only `#loop`, while the operational bridge
matches that loop followed by `Return(...)` and `#endcall` and omits
`<ret>`, `<stack>`, and other cells from its guard. The candidate supplies no
machine-checked bridge-free theorem quantified over that complete match
domain. A diagnostic attempt to prove both bridge-free universal claims
together was reviewer-interrupted with status 130 after about four minutes
and is not treated as a candidate failure; the selected universal loop theorem
and ground full-entry theorems did close.

I found no false conclusion witness enabled by this bridge on the intended
finite-list-of-integers entry domain. Its continuation is exact rather than an
arbitrary frame, its summary is fully defined, and its reachable entry state
has the valid call frame and `noRet` state. Under the benchmark's required
witness rule, this is therefore an evidence/complete-domain gap, not a finding
of material unsoundness.

Stage 5 result: no task-answer oracle, unconstrained result, overlap, or
on-domain false rewrite found; one operational-bridge validation concern.

## 6. Fresh non-vacuity test

The candidate supplied no trusted non-vacuity evidence. I created a fresh
ground mutation of the real entry claim for `[4,2,6,7]`, changing only the
required result from the true value `2` to false value `3`.

First:

```text
kprove /audit-output/evidence/spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

The mutation parsed and built successfully, exit 0.

Then:

```text
kprove /audit-output/evidence/spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY --output pretty
```

The prover reaches `<k> 2 ~> .K </k>`, cannot unify it with destination `3`,
prints `WarnStuckClaimState`, and exits 1. This is an expected unmet result
obligation, not a parser error, timeout, unrelated crash, or unreachable
mutation.

Evidence:

- [spec-vacuity.k](/audit-output/evidence/spec-vacuity.k)
- [stage6_vacuity_dry_run.log](/audit-output/evidence/stage6_vacuity_dry_run.log)
- [stage6_vacuity_proof.log](/audit-output/evidence/stage6_vacuity_proof.log)

Stage 6 result: pass; the proof is non-vacuous and result-constraining.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Conditional on the supplied MPY semantics and candidate-local extensions, for
every finite K `IntSeq`:

1. the macro-expanded term loaded by the entry claim is exactly the freshly
   translated submitted `solution.mpy`;
2. execution from the fixed initial MPY configuration returns
   `addAccSpec(INPUT,false,0)` without changing the fixed exception/exit
   obligations; and
3. fixed loop execution from every stated accumulator/phase invariant state
   leaves `total = addAccSpec(INPUT,ODD,ACC)`.

This is a universal finite-sequence theorem, not a finite collection of sizes
or bounded unrolling. The source contract's non-empty integer lists are wholly
included.

The mathematical reading of `addAccSpec` is established by its exhaustive
recursive equations: starting phase false, phase true occurs exactly at odd
indices; only values with Python/K modulo 2 equal to zero are added. Therefore
the summary is the stated sum of even elements at odd indices. This last
human-facing interpretation is a straightforward induction and is also
supported, but not universally proved, by the 68,947-case differential test.

### Trust ledger

| Boundary | Effect and assessment |
|---|---|
| K 7.1.293 parser, compiler, Haskell/LLVM backends, `kore-exec`, SMT reasoning | Standard formal-tool trust boundary; affects all proof results; accepted. |
| Trusted supplied MPY semantics | Exact trusted tree selected by the benchmark; every source block inventoried. Used control/value rules were manually traced. Accepted for this supplied-semantics condition. |
| K built-in `Int`, `Bool`, `Map`, `List`, string, equality, and arithmetic hooks | Low-level mathematical/runtime primitives. Used integer operations have ordinary unbounded-integer meaning; accepted. |
| `intVals` iterator rules | Candidate-local but exhaustive structural equations, no oracle and no hidden state. Accepted. |
| `addAccSpec` | Candidate-local result-bearing summary, but fully defined by disjoint descending equations and independently connected to fixed loop execution by a bridge-free universal proof. Accepted. |
| Loop-summary operational bridge | Value-correct on the intended domain and supported by bridge-free universal loop and ground full-entry proofs. Missing a bridge-free universal theorem over its complete continuation/cell match domain. Non-fatal concern. |
| Bare read-only list value versus heap-referenced source list | The supplied semantics supports both; this program observes neither identity nor mutation. Concrete execution covers the reference route, but no universal representation theorem is supplied. Non-fatal concern. |
| Summary-to-natural-language equivalence | Ordinary induction plus broad differential evidence; not a separate K theorem against `canonical.py`. Non-fatal evidence boundary. |
| Generation logs, prior `#Top`, and final generation report | Assigned no trust and not used to establish the verdict. |

Gate summary:

- Fresh verification: pass.
- Real-program identity and body sensitivity: pass.
- Domain adequacy: pass; no narrowing.
- Result constraint/non-vacuity: pass.
- Proof-extension soundness on the intended entry domain: pass.
- Complete operational-bridge validation over every syntactically admitted
  cell context: limited, producing the `CONCERNS` outcome.

The limitations do not permit a false result for any satisfying source-domain
input found symbolically or concretely, do not substitute another program, and
do not restrict the HumanEval domain. The proof is therefore legitimate but
does not meet the strongest fully validated operational-bridge evidence
standard.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
