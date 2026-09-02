# Independent adversarial audit: 33-sort-third

The reconstructed proof is legitimate for the exact submitted program on
finite lists of mathematical integers. It is result-constraining,
non-vacuous, and closes from fresh source builds. The qualified verdict is
`CONCERNS / LEGIT`, not `PASS`, because the prompt does not restrict list
elements to integers and because the individually generated semantics has an
audited/tested—but not machine-checked—refinement bridge to Python.

All candidate reports, traces, and compiled files were treated as untrusted.
The audit used K v7.1.293 and operated on source copies under
`/tmp/audit-work/33-sort-third`; no candidate-provided compiled definition was
used. Tool and semantics-boundary evidence is in
[environment.log](/audit-output/evidence/environment.log).

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent:
`/reference/reference-semantics` does not exist and is not a symlink. This is
the required boundary for `GENERATED_SEMANTICS`, so no hidden or inferred
reference semantics was used.

All required candidate artifacts are present as regular, non-symlink files:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`. The structured trace consists of
one regular JSONL file beneath `codex-trace/`. There are no mistyped or
symlinked required artifacts. The candidate also contains the additional
derived directories `verification-kompiled/` and `__pycache__/`; both were
reported and ignored.

The candidate prompt is byte-identical to
[the trusted prompt](/reference/prompt.py:1), with SHA-256
`41c45573886f68a38b5dc46f74ab70ef4cb79656e72bc97a04b861810158fa8c`.
The candidate translator is byte-identical to
[the trusted translator](/reference/py2mpy.py:1), with SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The untrusted metadata says this was problem `33-sort-third`, condition
`bare`, completed without timeout, and claimed all proofs returned `#Top`.
The complete trace was parsed as 142 JSON events; its command history and
agent claims were used only to identify what needed independent checking.
Evidence:

- [stage1_integrity.sh](/audit-output/evidence/stage1_integrity.sh) and
  [stage1-integrity.log](/audit-output/evidence/stage1-integrity.log)
- [inspect_trace.py](/audit-output/evidence/inspect_trace.py) and
  [stage1-trace-summary.log](/audit-output/evidence/stage1-trace-summary.log)

No provenance or infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

The natural-language contract is: return a list of the same length; at every
index not divisible by three, preserve the original element; at indices
`0,3,6,...`, place the original elements from those positions in ascending
sorted order. The input list itself is not changed.

[The trusted canonical implementation](/reference/canonical.py:7) copies the
input, sorts `l[::3]`, assigns that sorted slice back to the same stride, and
returns the copy. [The candidate solution](/candidate/solution.py:1) performs
the same algorithm with `result = l[:]`, followed by
`result[::3] = sorted(result[::3])`.

The trusted translator was rerun in scratch:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp regenerated-solution.mpy solution.mpy
```

Both commands exited 0. Submitted and regenerated files have the same SHA-256,
`ace8d0ababa47c4492504394642a67616547bd2fa7634ee69b908429f9e7f6bb`.
See [stage2-translation.log](/audit-output/evidence/stage2-translation.log).

The independent differential script imports the trusted canonical and copied
candidate entry points separately. It covers:

- both documented examples;
- empty lists and explicit length boundaries through 8;
- ascending, descending, equality, duplicate, negative, and huge-integer
  branch witnesses;
- representative orderable string, float, and tuple lists;
- every list of lengths 0 through 6 over integers `-2..2`;
- 500 deterministic seeded lists of lengths 7 through 60.

All 20,050 cases matched, and neither implementation mutated its input.
The reproducible input scope has seed `330033` and digest
`d3308f2c4d0570f90ed43a44df8baa6a08d58a9ddb55251a3d68f1092e1703d3`.
See [differential_test.py](/audit-output/evidence/differential_test.py) and
[stage2-differential.log](/audit-output/evidence/stage2-differential.log).
This is finite fidelity evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

Only the following source files were copied into scratch:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`,
`prove.sh`, and the trusted prompt, translator, and canonical program.
Neither `/candidate/verification-kompiled` nor any candidate cache was copied
or referenced.

The generated semantics was rebuilt for concrete execution:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition semantic-kompiled
```

It exited 0; see
[stage3-kompile-concrete.log](/audit-output/evidence/stage3-kompile-concrete.log).
Eleven fresh `krun --output json` executions covered empty, lengths 1/2/3,
the first and second stride boundaries, both prompt/ordering directions,
duplicates, negatives, and a 41-digit magnitude. Every K result equaled both
Python results and every `krun` exited 0. See
[stage3_concrete_compare.py](/audit-output/evidence/stage3_concrete_compare.py)
and
[stage3-concrete-compare.log](/audit-output/evidence/stage3-concrete-compare.log).

The proof definition was independently rebuilt:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled-audit
```

It exited 0; see
[stage3-kompile-proof.log](/audit-output/evidence/stage3-kompile-proof.log).
The original spec was then proved without modification:

```text
kprove spec.k --definition verification-kompiled-audit --spec-module SPEC
```

It exited 0 and printed `#Top`; see
[stage3-kprove-all.log](/audit-output/evidence/stage3-kprove-all.log).

Because the submitted claims are unlabeled, each was also copied unchanged
into its own audit module and run separately. Each command exited 0 and printed
`#Top`:

- General symbolic claim:
  [spec-claim-general.k](/audit-output/evidence/spec-claim-general.k) and
  [stage3-kprove-general.log](/audit-output/evidence/stage3-kprove-general.log)
- Seven-element example:
  [spec-claim-example-seven.k](/audit-output/evidence/spec-claim-example-seven.k)
  and
  [stage3-kprove-example-seven.log](/audit-output/evidence/stage3-kprove-example-seven.log)
- Three-element example:
  [spec-claim-example-three.k](/audit-output/evidence/spec-claim-example-three.k)
  and
  [stage3-kprove-example-three.log](/audit-output/evidence/stage3-kprove-example-three.log)

Thus every positive target claim closes independently under a fresh definition.

## 4. Adequacy and real-program pinning

The general entry claim has no `requires` clause. Its precondition is the exact
submitted module term in `<k>`, any finite K integer sequence
`IS:Ints` wrapped as `<input> VList(IS) </input>`, and an initially empty
`<result> .K </result>`. Its postcondition consumes the program and sets
`<result>` to `contractResult(IS)`.

The other two claims have the same program and empty result precondition, with
fixed inputs and fixed output lists:

- `[5,6,3,4,8,9,2]` must return `[2,6,3,4,8,9,5]`;
- `[1,2,3]` must return `[1,2,3]`.

All three `<k>` programs, after removing only insignificant whitespace, have
the same SHA-256 as submitted `solution.mpy`,
`2c517fb234e374c4fdf10006b2f03989cd31fa9b4e198fd0a4ea380dc8ba7816`.
There is no substituted program. See
[stage4_adequacy.py](/audit-output/evidence/stage4_adequacy.py) and
[stage4-adequacy.log](/audit-output/evidence/stage4-adequacy.log).

There are no helper/loop claims. The module rule enters the actual function
body; the two assignments and return are interpreted in sequence. The
postcondition is not a free variable, existential, implication, or tautology:
it fixes the result to a deterministic function of the original input.

Satisfiable entry states were exhibited for `[]`, both fixed examples, and
`[-1,7,8,-3,9,10,-2]`. Ground substitution into the claimed contract produced,
respectively:

```text
[]
[2,6,3,4,8,9,5]
[1,2,3]
[-3,7,8,-2,9,10,-1]
```

Every value matched both Python implementations. The same starts were
successfully executed by the rebuilt K semantics in Stage 3.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is preserved in
[stage5-rule-inventory.md](/audit-output/evidence/stage5-rule-inventory.md),
with extraction evidence in
[stage5-inventory-extraction.log](/audit-output/evidence/stage5-inventory-extraction.log).
It covers every local declaration and rule:

- 16 local syntax declaration statements/groups, including all alternatives;
- the three-cell configuration;
- 11 `[function]` symbols;
- 26 rules in `semantic.k`;
- one definitional rule in `verification.k`;
- all three reachability claims in `spec.k`.

There are no local `[total]` or `[functional]` declarations, opaque/fresh
result-bearing symbols, simplification rules, priority rules, or `owise`
rules. There are no generated helper K files beyond `semantic.k` and
`verification.k`.

Every construct in `solution.mpy` is mapped to syntax and rules:

```text
Module/FuncDef/Params
  -> entry binding
  -> name assignment with full slice
  -> stride-three slice assignment
  -> sorted call and recursive integer insertion sort
  -> return and result delivery
```

The configuration preserves the input cell. Environments are explicit K maps.
The RHS of the stride assignment is evaluated against the old environment
before the result binding is updated. Return discards its suffix. List
recursions decrease a finite list; countdown recursions use reachable values
2, 1, and 0. Empty/nonempty patterns and the integer guards `I <= J` versus
`I > J` make the potentially competing helper rules disjoint and exhaustive
on their used domains.

`thirds` extracts positions `0,3,6,...`; `sortInts` is a structurally
recursive insertion sort with truthful, disjoint comparison branches;
`replaceThirdInts` weaves a same-length replacement sequence back at those
positions. `contractResult` transparently composes those operations:

```text
VList(replaceThirdInts(0 ; IS ; sortInts(thirds(IS))))
```

It is a definitional mathematical summary, not an operational bridge: it
does not rewrite the submitted program or suppress its body. Although the
semantics and contract deliberately share the fully defined `sortInts`
operation, it is not an unconstrained oracle.

The generated semantics is intentionally not a reusable full Python
semantics. The static audit found these narrower limitations:

- The full-slice rule returns the same modeled value for any expression.
  On the exact path that value is a `VList`, and immutable K value data makes
  it observationally equivalent to a fresh Python copy. Off-path,
  `Subscript(Int(1), full-slice)` would incorrectly yield `VInt(1)` instead of
  Python's `TypeError`. This is an over-broad rule outside the submitted
  program, not a false-conclusion witness for any exact-program state with a
  satisfying `VList` input.
- `sorted` is selected textually and global/builtin rebinding is not modeled.
  The submitted function does not shadow it and the HumanEval harness assumes
  standard builtins.
- Invalid extended-slice replacement lengths and unsupported types get stuck
  instead of entering an exception state. The exact RHS
  `sortInts(thirds(IS))` always has the required length.
- List object identity and aliasing are absent. The exact function observes
  only list values, creates a result copy, and does not expose identity.

Under the requested witness standard, none of these limitations enables a
false conclusion for the exact submitted program on its formal integer-list
domain. They do limit reuse and contribute to the qualified verdict.

A separate body-sensitivity probe changed only the final statement to
`Return(Name("l"))` while retaining the true seven-element postcondition. It
built, executed the mutated body, and failed with a stuck state whose actual
result was the untouched input. See
[spec-body-sensitivity.k](/audit-output/evidence/spec-body-sensitivity.k) and
[stage5-body-sensitivity.log](/audit-output/evidence/stage5-body-sensitivity.log).
This shows the proof does not bypass or ignore the function body.

## 6. Fresh non-vacuity test

No candidate mutation artifact was relied on. The reviewer-authored
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k) keeps the real program
and satisfiable documented input `[5,6,3,4,8,9,2]`, but changes the
result-constraining postcondition's final element from the true `5` to false
`6`.

The mutation dry-run exited 0, proving it parsed and built:

```text
kprove spec-vacuity.k --definition verification-kompiled-audit \
  --spec-module SPEC-VACUITY --dry-run
```

See
[stage6-vacuity-dry-run.log](/audit-output/evidence/stage6-vacuity-dry-run.log).
Both Python implementations return `[2,6,3,4,8,9,5]`, making the mutation
demonstrably false; see
[stage6-vacuity-witness.log](/audit-output/evidence/stage6-vacuity-witness.log).

The actual proof command exited 1 with `WarnStuckClaimState`. Its residual had
empty `<k>` and actual
`<result> VList(2,6,3,4,8,9,5) </result>`, which could not unify with the
mutated destination ending in `6`. This is the expected unmet obligation,
not a parser error, missing import, timeout, or unrelated crash. See
[stage6-vacuity-proof.log](/audit-output/evidence/stage6-vacuity-proof.log).

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the submitted generated K semantics, for every finite sequence of
mathematical integers `IS`, executing the exact submitted `solution.mpy` from
the configured entry state is partially correct with respect to:

```text
result =
  VList(replaceThirdInts(0 ; IS ; sortInts(thirds(IS))))
```

The proof also establishes the two fixed examples. It executes the real body,
preserves the configured input, and constrains the returned result. As a
partial-correctness theorem, it does not by itself make a general claim about
all Python executions or all possible input types.

### Trust and assumption ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| K `INT`, `MAP`, builtin list productions, parser, Haskell/LLVM backends | Integer comparison/countdown, binding lookup/update, sequence representation, and all proof/execution results | Acceptable low-level K/toolchain trust boundary. Fresh builds and both backends were exercised. |
| Trusted `py2mpy.py` | Connects `solution.py` syntax to `solution.mpy` | Acceptable trusted input. Fresh translation is byte-identical; it does not prove semantic equivalence by itself. |
| Generated entry/name/assignment/slice/return rules | Connect the MPY constructors to the modeled Python subset | Audited rule-by-rule and exercised concretely. No separate machine-checked refinement theorem to CPython exists, so conclusions about Python remain conditional on this bridge. |
| `eval(Call(Name("sorted"), E)) -> sortedValue(...)` | Determines the result-bearing builtin sort | Acceptable for the standard unshadowed builtin and integer lists. `sortInts` is fully defined by truthful insertion-sort equations; 11 K/Python cases and the broad Python differential support, but do not universally prove, the Python bridge. |
| Immutable `VList` value model | Omits Python object identity and mutation aliasing | Acceptable for this exact value-only function; concerning for semantics reuse. |
| Finite integer-list precondition | Determines the universal theorem's input domain | Material limitation. The prompt says only `list`; the canonical/candidate Python functions also agree on tested strings, floats, and tuples, none of which the K theorem covers. |
| Ordinary mathematical interpretation of `thirds`, insertion sort, and weaving | Connects `contractResult` to the English phrases “indices divisible by three” and “sorted” | The equations are transparent and were statically checked; their human-facing interpretation is an informal inductive argument plus finite evidence, not a separate K property theorem. |

There are no opaque values, empirical oracles, proof-local simplification
axioms, totality declarations, or operational proof bridges. Differential
testing supports only program/semantics fidelity on the recorded cases; it
was not used as a replacement for `kprove`.

### Decision

This is not `FAIL`: fresh builds and every claim close; the claim pins the
submitted translated program; the result is constrained; body and
postcondition mutations are rejected for the expected reasons; and no rule
was found that can enable a false result on the satisfying formal domain.

It is not an unqualified `PASS`: the formal domain is narrower than the
prompt's unqualified Python `list`, the generated-semantics-to-Python bridge
is not machine-checked, and one used semantic rule is over-broad outside the
exact list-valued path. These are documented adequacy/trust limitations, not
illegitimacy of the reconstructed integer-list proof.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
