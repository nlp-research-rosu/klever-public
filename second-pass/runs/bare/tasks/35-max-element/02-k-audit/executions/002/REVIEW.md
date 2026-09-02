# Independent adversarial review: 35-max-element

## Executive conclusion

The reconstructed K proof is machine-closing, non-vacuous, result-constraining,
and pinned to the submitted `solution.mpy` for its formal domain: every finite
non-empty sequence of K integers. The local arithmetic equations are truthful
and no opaque oracle determines the result.

It is not a legitimate proof of the full trusted HumanEval source contract.
`prompt.py` declares `l: list` and says to return the list's maximum; it does
not restrict elements to integers. The trusted canonical program works on
non-empty lists of mutually comparable non-integers. Concrete witnesses
`[1.5, -2.0, 1.5001]` and `["alpha", "zeta", "mu"]` return the same maxima in
both Python implementations, while the K input sort `IntSeq` rejects both.
This is a material source-domain narrowing. Under the benchmark-specific rule,
the otherwise sound-but-limited theorem maps to `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = bare`, and `semantics_mode = GENERATED_SEMANTICS`.

- `/audit-campaign-lock.json` is a real regular file, its JSON object exactly
  equals the `audit_campaign` block, and its SHA-256 is the recorded
  `ad5dfcc0...8d745`.
- The required legacy-selected records were present as non-symlink regular
  files and inspected: `/run.json`, `/task.json`,
  `/generation-result.json`, `invocation.json`, `metrics.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, the structured trace,
  and the present optional `usage.json`. Historical
  `runtime-metrics.json` is absent, which is permitted for this layout.
- Every launcher-recorded single-file hash checked by the reviewer matched.
  The structured trace contains one regular JSONL file with 121 valid JSON
  records. Its per-file hash also matches the generation result.
- An independent reimplementation of the pipeline tree digest gives
  `838fd9ae...27fa` for `/candidate`, exactly the generation workspace hash,
  and `482e7602...1e7` for the trace, exactly `usage.json`'s source-trace hash.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts. No candidate or trace entry is a symlink or special node.
- `/reference/reference-semantics` is absent, as GENERATED_SEMANTICS requires.
  No hidden or inferred reference semantics was used.
- The generation records were treated only as untrusted history. In
  particular, their claimed `#Top` was not reused.

The complete command transcript and per-file manifest are in
[stage1-provenance.log](/audit-output/evidence/stage1-provenance.log), produced
by [stage1-provenance.sh](/audit-output/evidence/stage1-provenance.sh) and
[verify_provenance.py](/audit-output/evidence/verify_provenance.py).

Stage result: integrity gate passes; there is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Trusted contract and implementations

The trusted prompt declares:

```python
def max_element(l: list):
    """Return maximum element in the list."""
```

Its examples return `3` and `123`. The trusted canonical implementation starts
with `l[0]`, scans all elements, replaces the current value on `e > m`, and
returns `m`. Thus a returned maximum is defined for a non-empty list whose
elements support the needed comparison. The empty list has no maximum and the
canonical program raises `IndexError`.

The candidate implements `return max(l)`. For non-empty comparable lists this
is extensionally aligned with the canonical scan. On `[]`, it raises
`ValueError`; that exception-type difference is outside the stated
return-a-maximum behavior because no maximum exists.

### Trusted regeneration

From a scratch copy, the exact command was:

```text
python3 /reference/py2mpy.py /tmp/audit-work/35-max-element/solution.py > /tmp/audit-work/35-max-element/regenerated-solution.mpy
cmp /tmp/audit-work/35-max-element/solution.mpy /tmp/audit-work/35-max-element/regenerated-solution.mpy
```

`cmp` exited 0. Both files have SHA-256
`b040afa3d90d99cfcc4af2a4d930d009cfbf495e7de3998c1d24d2899e6b8791`.
See [stage2-source-fidelity.log](/audit-output/evidence/stage2-source-fidelity.log).

### Independent differential test

[differential_test.py](/audit-output/evidence/differential_test.py) separately
imports `/reference/canonical.py` and the scratch candidate. It exercised:

- the two documented examples;
- 12 singleton, increasing, decreasing, equal, negative, duplicate-maximum,
  and arbitrary-precision integer branch boundaries;
- 500 deterministic random non-empty integer lists of lengths 1 through 40;
- five non-integer comparable lists, including floats and strings; and
- the empty error boundary.

Command:

```text
bash -x /audit-output/evidence/stage2-differential.sh
```

Exit was 0 with 519 non-empty cases and zero mismatches. The empty exception
types were recorded separately. Full results are in
[stage2-differential.log](/audit-output/evidence/stage2-differential.log).

Stage result: source-to-MPY fidelity passes and the Python implementation
matches the canonical on all tested non-empty inputs. Testing is finite
evidence, not the K proof.

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/35-max-element`; no
candidate-provided compiled definition or cache was copied or reused.

The concrete definition was freshly built with:

```text
kompile semantic.k --backend llvm --main-module MPY-SEMANTICS --syntax-module MPY-SYNTAX --output-definition audit-semantic-kompiled
```

[concrete_k_compare.py](/audit-output/evidence/concrete_k_compare.py) then ran
34 normal and boundary integer-list executions with exact `krun` argument
vectors recorded in the log. Every run exited 0, ended with `<k> .K </k>`, and
returned the same integer as both Python implementations. This included
singletons, order/equality boundaries, negatives, duplicates, 80-digit
integers, both prompt examples, and 20 deterministic random cases. `[]` was
also attempted and was rejected at parse time with exit 113 because it is not
an `IntSeq`.

The proof definition was freshly built with:

```text
kompile verification.k --backend haskell --main-module MPY-VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled
```

There are exactly three positive claims. They were all run together, as
declared in `SPEC`, with:

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
```

The command exited 0 and its complete output was exactly `#Top`. See
[stage3-fresh-reconstruction.log](/audit-output/evidence/stage3-fresh-reconstruction.log)
and the bounded raw output
[stage3-positive-kprove.raw.log](/audit-output/evidence/stage3-positive-kprove.raw.log).

Stage result: clean reconstruction and every positive target claim pass.

## 4. Adequacy and real-program pinning

### Plain-language claims

The universal entry claim has no separate `requires`; its sort is the
precondition. For every `IS:IntSeq`, meaning every finite non-empty sequence of
mathematical K integers, it starts with:

- `solutionProgram ~> invoke("max_element", IS)` in `<k>`;
- empty function and local-environment maps; and
- `noResult`.

It requires execution to consume the entire computation and end with:

- the exact `max_element` closure installed;
- the local environment exactly `"l" |-> IS`; and
- `result(expectedMaximum(IS))`, where `expectedMaximum(IS)` is exactly
  `maxInts(IS)`.

The other two claims have the same state transformation for the two prompt
examples, with results exactly `3` and `123`. These are equality constraints,
not implications to a free result variable. There are no helper or loop
claims.

### Mechanical program identity

[program_term_compare.py](/audit-output/evidence/program_term_compare.py)
independently parses constructor syntax from both the submitted `solution.mpy`
and the right-hand side of the `solutionProgram` equation. Both normalized
trees have SHA-256
`82b8d781412be2eda02a572798c1d51cd6b507ce43b3f3e533aca161e96abbc3`.
Thus the claim executes the same `Module(FuncDef(...Return(Call(max,l))))`
term, not merely a source filename or external copy. The trusted translator's
documented omission of typing annotations is runtime-inert.

The concrete satisfying entry witness `[2, -5, 2]` starts in the exact empty
maps/no-result state. `maxInts` reduces to `2`; the canonical Python function,
candidate Python function, and fresh K execution all returned `2`.

### Executed-body sensitivity

The auditor changed the `solutionProgram` constructor body actually used by a
separate claim from `Return(Call(Name("max"), Name("l")))` to
`Return(Name("l"))`; it did not merely edit external Python. The mutated
definition compiled successfully. Its proof exited 1 with
`WarnStuckClaimState`, leaving the list value before `doReturn` and
`noResult`. See
[stage4-body-mutation-kprove.raw.log](/audit-output/evidence/stage4-body-mutation-kprove.raw.log)
and [stage4-pinning-and-body-sensitivity.log](/audit-output/evidence/stage4-pinning-and-body-sensitivity.log).

Stage result: the formal theorem is satisfiable, result-constraining, and
pinned to the real submitted MPY body.

## 5. Rule-by-rule static soundness review

The exhaustive declaration inventory is
[RULE_INVENTORY.md](/audit-output/evidence/RULE_INVENTORY.md). It enumerates
all 24 local syntax productions, the configuration, all 15 local rules, all
four `[function,total]` declarations, and the three claims. There are no helper
K files and no local `[functional]`, opaque, priority, simplification,
`concrete`, macro, or `anywhere` rules.

### Syntax, configuration, and used constructs

`solution.mpy` uses exactly `Module`, `FuncDef`, `Params`, `Return`, `Call`,
`Name`, and the statement/expression lists. Runtime inputs additionally use
`IntSeq`, `NonEmptyInts`, and imported `Int`. Every used constructor has a
declaration and an execution path. The four cells are all material:
`<k>`, `<functions>`, `<env>`, and `<result>`. There is no modeled heap, I/O,
allocation, exception, or general call stack because the submitted program
does not use them.

### Local functions and rules

| Rules | Review |
|---|---|
| `maxInts` singleton and recursive equations (semantic.k:45-46) | Disjoint by list length. The recursive call has a strictly shorter non-empty list. Together they cover all `IntSeq` terms. |
| `imax` guarded equations (48-49) | `I >= J` and `I < J` are disjoint and exhaustive over K integers, and each result is the greater integer. |
| module/empty/cons execution (60-62) | Begins module execution and sequences statement lists left-to-right. Empty/non-empty cases are disjoint. |
| function installation (66-67) | Installs exactly the parameter list and body. Omitting captured state is correct for this capture-free submitted definition. |
| invocation (71-75) | Requires the named closure to exist, binds its sole parameter to the `IntSeq`, resets only the local environment, and preserves the remaining cells. This matches the submitted one-argument entry call. |
| return scheduling (77) | Schedules expression evaluation and `doReturn`. It is correct for the submitted sole body statement but is not a general early-return/unwind implementation. |
| name lookup (81-82) | Truthful map lookup. The specialized builtin call handles the actual `l` argument directly, so this general rule is not exercised on the submitted path. |
| builtin `max` bridge (84-88) | Rewrites the exact used call shape to the fully defined `maxInts(IS)`. It reads `<env>`, changes only the front of `<k>`, and preserves the continuation and all other cells. This is a result-bearing external-primitive semantic bridge, not an opaque oracle. |
| result write (90-91) | Consumes `intVal(I) ~> doReturn`, changes `noResult` to `result(I)`, and preserves the suffix. On the submitted path that suffix is only the empty statement tail. |
| `solutionProgram` (verification.k:9-12) | Truthful, total nullary definitional equation; constructor identity was mechanically checked. |
| `expectedMaximum` (verification.k:18) | Truthful total alias of `maxInts`. The elementary induction over the preceding equations supplies its human-facing “maximum” meaning. |

The specialized builtin rule preempts general callee and argument evaluation.
For the actual claim, its complete context has an unshadowed builtin name, a
local `l |-> IS:IntSeq`, and continuation
`doReturn ~> exec(.Stmts) ~> .K`; neither name evaluation has side effects and
the rule preserves that continuation. `maxInts` cannot take an opposite
interpretation because its exhaustive equations fix every ground value.

### Bounded semantic limitations and witnesses

Two declarations are broader than the behavior actually justified:

1. The builtin rule does not check the binding of the name `max`. In
   `shadow-max.mpy`, the parameter itself is named `max`. On `[1,2]`, K
   concludes `result(2)`, while the analogous Python function raises
   `TypeError` because the list is not callable. This is a concrete false
   conclusion witness for reading rule 84-88 as a general Python-call rule.
2. Return does not unwind arbitrary remaining statements.
   `trailing-return.mpy` reaches the second return and becomes stuck after the
   first result is stored, while Python returns immediately from the first.
   This is an incompleteness/control witness, not a false returned conclusion.

Exact commands and outputs are in
[stage5-static-witnesses.log](/audit-output/evidence/stage5-static-witnesses.log).
Neither witness is reachable from the immutable submitted term: its parameter
is `l`, the model's builtin name is unshadowed, and its return is the only body
statement. Under the generated-semantics boundary, minimal coverage of every
construct as actually used is permitted. These limitations are concerning and
prevent treating `semantic.k` as reusable Python semantics, but they do not
make a false result provable for a state satisfying the actual entry claim.

Stage result: rule truth and execution fidelity pass for the submitted program
over `IntSeq`; the semantics is intentionally narrow and not sound as a
general interpreter for all terms admitted by its broad constructor grammar.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was relied on. The auditor created
`spec-vacuity-audit.k`, preserving the actual program and initial state but
requiring `result(4)` for the satisfying input `[1,2,3]`.

First, the exact dry-run command:

```text
kprove spec-vacuity-audit.k --definition audit-verification-kompiled --spec-module SPEC-VACUITY-AUDIT --dry-run
```

exited 0 and emitted a valid `kore-exec ... --prove ...` command, establishing
that the mutation parsed and built. The same command without `--dry-run`
exited 1 with `WarnStuckClaimState`. Its residual had `<k> .K </k>` and
`<result> result(3) </result>`, directly exposing the unmet result obligation.

Artifacts:
[spec mutation](/audit-output/evidence/spec-vacuity-audit.k),
[driver log](/audit-output/evidence/stage6-false-mutation.log),
[dry-run log](/audit-output/evidence/stage6-vacuity-dry-run.raw.log), and
[proof residual](/audit-output/evidence/stage6-vacuity-kprove.raw.log).

Stage result: non-vacuity passes.

## 7. Proven versus assumed accounting

### Precisely proven

Conditional on the freshly compiled K definition, the successful universal
reachability claim establishes:

> For every finite non-empty sequence `IS` of arbitrary-precision K integers,
> executing the exact translated `max_element` binding/body from empty module
> and local maps consumes the computation and leaves exactly the installed
> closure, `l |-> IS`, and `result(maxInts(IS))`.

The two source examples are additionally proven as ground instances. The
result is not free, and the false-result mutation is rejected.

### Trust and limitation ledger

| Boundary | Dependents and effect | Assessment |
|---|---|---|
| K `Int`, integer order, `Map`, list, and sequencing primitives | All rules and claims; value, lookup, and control | Acceptable low-level K toolchain trust boundary. |
| Trusted `/reference/py2mpy.py` | Source-to-constructor identity | Acceptable launcher-trusted translator; byte identity was independently re-established. |
| Rule 84-88 as the meaning of unshadowed Python builtin `max` on non-empty integer lists | Determines the executed call's value and hence all claims | Acceptable for the exact state and formal domain, but concerning as an informal source-semantics bridge. It is fully value-defined by R1-R4 and supported by independent differential tests, not by an external K connection theorem. |
| Elementary induction that R1-R4 denote a mathematical maximum | Natural-language interpretation of `expectedMaximum` | Acceptable ordinary mathematics: singleton base; the recursive step chooses the greater of the head and tail maximum. This property is reviewed, not separately stated as membership/order K lemmas. |
| Finite differential and concrete executions | Source-alignment and semantic-bridge evidence on tested inputs | Empirical support only; never used as a universal proof substitute. |
| Partial-correctness interpretation | The theorem speaks about the declared K executions, not all CPython exceptional behavior | Acceptable for non-empty modeled inputs. Empty-list exception behavior is excluded because a maximum does not exist. |
| `IntSeq` instead of the prompt's unrestricted `list` | Excludes floats, strings, and every other comparable non-integer element from the universal theorem | Illegitimate material narrowing of the trusted HumanEval source contract. |

[stage7-domain-gap.log](/audit-output/evidence/stage7-domain-gap.log) records
that the prompt parameter annotation is exactly `list`, both Python programs
return `1.5001` and `"zeta"` on the concrete non-integer witnesses, and fresh K
execution rejects each at parsing with exit 113.

### Gate accounting

- Gate A, real-program soundness over the formal `IntSeq` domain: PASS.
- Gate B, intent/source-contract adequacy: FAIL because the theorem materially
  narrows non-empty comparable lists to integer lists.
- Gate C, trust and evidence auditability: PASS with the explicit narrow
  builtin/semantics limitations above; all cited tests and commands are
  preserved. This does not cure Gate B.

The proof is therefore sound but materially limited. The benchmark prompt
explicitly maps such HumanEval-domain narrowing to the failing candidate
verdict rather than to a legitimate concern-only result.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
