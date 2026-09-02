# Adversarial audit: 115-max-fill

## Audit conclusion

The candidate contains a legitimate, result-constraining partial-correctness
proof for the intended HumanEval domain. Fresh builds close the three claims,
the proof constant is pinned to the freshly translated submitted program, the
generated semantics faithfully covers every construct actually used on the
intended domain, and a fresh false postcondition is rejected for the expected
logical reason.

The verdict is `CONCERNS / LEGIT`, rather than an unqualified pass, for two
related scope limitations. The K entry precondition says only `C > 0` and its
typed rows contain arbitrary integers, while the natural contract restricts
cells to 0 or 1. The generated `//` rule uses K `/Int` (truncation toward zero),
so the candidate's prose claim that the proof models arbitrary integer-valued
rows is false as a bridge to Python for negative rows. This cannot affect an
intended 0/1 input. In addition, the proof uses contract-typed `gridVal` and
`rowVal` values; their used operations are fully and faithfully defined, but
the representation relation to ordinary nested Python lists is an audited
informal bridge rather than a separate K theorem.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`. The required boundary is
consistent: `/reference/reference-semantics` does not exist. The only trusted
mounted inputs are regular, non-symlink files:
`/reference/canonical.py`, `/reference/prompt.py`, and
`/reference/py2mpy.py`.

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the 319-line structured JSONL trace only as untrusted
claims. They report a bare/generated run, a prior zero exit, prior `#Top`, three
example runs, and 1,000 random Python checks. None of those results was reused.

The candidate prompt and translator are byte-identical to the trusted mounts:

- Prompt SHA-256:
  `c3a3940108ef0c6a7e15e737fd5d29759d8a27f7cfe7a44411ff3f4b3ff3771b`
  on both files.
- Translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`
  on both files.
- Both `cmp` checks exited 0.

All required candidate source and audit-metadata artifacts are regular,
non-symlink files: the five run/trace records, prompt, translator, solution
sources, `semantic.k`, `solution-program.k`, `solution-token.mpy`,
`verification.k`, `spec.k`, and `prove.sh`. No required artifact is missing,
changed, mistyped, additional, or symlinked. The candidate's `__pycache__`,
`semantic-kompiled`, and `verification-kompiled` are extra generated artifacts;
they were deliberately ignored and never copied into the rebuild.

Evidence: [stage1-integrity.log](evidence/stage1-integrity.log).

## 2. Program fidelity and candidate-versus-canonical checks

The natural-language contract is: for every well/row, count its 1-valued water
cells, divide that count into buckets of positive `capacity`, round that row's
quotient upward, and sum the lowerings across rows. Formally on the intended
domain:

`sum(ceil(sum(row) / capacity) for row in grid)`.

The trusted canonical implementation states exactly that expression. The
candidate implements the equivalent positive-divisor identity
`(sum(row) + capacity - 1) // capacity`, using one structural recursion for a
row and another for the grid. On the documented bounds, each recursion depth is
at most about 100 and there is no mutation or alias-sensitive behavior.

Fresh translation used the trusted mounted translator:

```text
python3 /reference/py2mpy.py /tmp/audit-work/rebuild/solution.py \
  > /tmp/audit-work/rebuild/regenerated-solution.mpy
cmp /candidate/solution.mpy \
    /tmp/audit-work/rebuild/regenerated-solution.mpy
```

The submitted and regenerated files have the same SHA-256,
`7d64ef28ec1ccf1567d62479e28792152036f7818b9985a45e9999c6648b470f`;
`cmp` and `py_compile` both exited 0. The emitted construct census contains only
the constructs covered in Stage 5.

The reviewer-authored differential test imports the trusted canonical entry
point and the scratch copy of the generated entry point independently. It ran
the three documented examples, empty grid and empty row robustness cases,
minimum and maximum capacity boundaries, both cell branches, ceiling values
immediately below/at/above a multiple, 100×100 documented size boundaries, and
200 deterministic generated rectangular 0/1 grids. All 215 cases agreed, with
zero mismatches. The log preserves each complete input and output; the
generation seed is `11520260723`.

Evidence:
[stage2-translation.log](evidence/stage2-translation.log),
[differential_test.py](evidence/differential_test.py), and
[stage2-differential.log](evidence/stage2-differential.log).

## 3. Clean proof reconstruction

Every source needed for execution was copied to `/tmp/audit-work/rebuild`;
trusted prompt, canonical, and translator copies came from `/reference`. No
candidate-built definition or cache was copied. The live toolchain is K
v7.1.293; see [toolchain-version.log](evidence/toolchain-version.log).

The concrete and proof definitions were rebuilt from source:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-audit-kompiled

kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

Both commands exited 0. Logs:
[stage3-kompile-concrete.log](evidence/stage3-kompile-concrete.log) and
[stage3-kompile-proof.log](evidence/stage3-kompile-proof.log).

The unmodified candidate `spec.k` was then proved as a whole:

```text
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC
```

It printed `#Top` and exited 0
([stage3-kprove-all.log](evidence/stage3-kprove-all.log)). I also created a
body-identical labeled copy to run each target with exactly its prerequisite
closure:

- Row helper alone: `#Top`, exit 0
  ([stage3-kprove-water.log](evidence/stage3-kprove-water.log)).
- Row helper plus grid helper: `#Top`, exit 0
  ([stage3-kprove-buckets-with-water.log](evidence/stage3-kprove-buckets-with-water.log)).
- Both helpers plus entry: `#Top`, exit 0
  ([stage3-kprove-entry-with-helpers.log](evidence/stage3-kprove-entry-with-helpers.log)).

An additional diagnostic selecting the grid-helper claim while filtering out
its row-helper circularity was reviewer-interrupted after it began unbounded
unrolling (exit 130). That was not a candidate positive target: the valid
dependency-closed grid-helper command above independently closes. The
diagnostic is retained in
[stage3-kprove-buckets.log](evidence/stage3-kprove-buckets.log).

Fresh LLVM execution compared K with both Python implementations on 21 normal
and boundary executions. These included both `gridVal`/`rowVal` proof
representations and ordinary nested `listVal` representations. All 21 passed,
including separate height-100 and width-100 cases and a 30×30 representative
grid:
[k_concrete_compare.py](evidence/k_concrete_compare.py) and
[stage3-concrete-differential-pass.log](evidence/stage3-concrete-differential-pass.log).

A first attempt to parse one combined 100×100 K command-line term was killed in
K's Java parser with exit 137 before execution. The failed run is preserved in
[stage3-concrete-differential.log](evidence/stage3-concrete-differential.log).
This is a bounded tooling-scale limitation, not evidence of a false semantic
result; separate maximum dimensions execute, the intended Python case passes,
and the symbolic claim is size-parametric.

## 4. Adequacy and real-program pinning

### Claim meanings

1. **Row helper claim.** With no explicit precondition, any `ROW:Ints`,
   arbitrary continuation, and arbitrary framed argument/environment/result
   cells, invoking `_water_in(rowVal(ROW))` produces
   `intVal(water(ROW))` before that same continuation. All framed cells are
   preserved.
2. **Grid helper claim.** For any `GRID:Rows` and `C > 0`, invoking
   `_buckets_for(gridVal(GRID), intVal(C))` produces exactly
   `intVal(requiredBuckets(GRID,C))`, again before the same continuation and
   with all other cells preserved.
3. **Entry claim.** For any `GRID:Rows` and `C > 0`, starting from
   `solutionProgram`, the supplied two arguments, empty function/environment
   cells, and `noneVal` result, execution consumes `<k>`, installs exactly the
   submitted functions, and writes exactly
   `intVal(requiredBuckets(GRID,C))`.

The entry's result is an equality-bearing cell rewrite, not a free variable,
tautology, or one-way implication.

### Program identity and control flow

The entry executes a `solutionProgram` constant rather than directly naming the
file token. This bridge is adequately pinned:

- Trusted translation is byte-identical to submitted `solution.mpy` (Stage 2).
- Using the fresh proof definition, depth-one KORE states for `solution.mpy`
  and `solution-token.mpy` have identical SHA-256
  `33b7b763ef5c2a8de49baccd99071e427cc4124b534c0936a15473aa6e47f8e4`;
  `cmp` exited 0
  ([stage4-program-pinning.log](evidence/stage4-program-pinning.log)).
- Concrete depth 11 reaches the exact `_buckets_for` invocation pattern, and
  depth 31 reaches the exact `_water_in` invocation with the real arithmetic,
  recursive-call, environment-restoration, and caller continuation suffix:
  [stage4-control-flow-depths.log](evidence/stage4-control-flow-depths.log) and
  [stage4-helper-invocation-depths.log](evidence/stage4-helper-invocation-depths.log).

Thus the helper circularities summarize real recursive control-flow points;
they do not replace a different or fabricated program.

### Satisfiable witness

One state satisfying every applicable precondition uses
`ROW=(1,0)`, `GRID=(rowVal(1,0),rowVal(1,1))`, and `C=2`, with any framed
continuation for helper claims and the entry's initial cells. Here
`water(ROW)=1` and `requiredBuckets(GRID,2)=ceil(1/2)+ceil(2/2)=2`. Trusted
canonical Python, generated Python, and fresh K execution all return 2:
[stage4-satisfying-witness.log](evidence/stage4-satisfying-witness.log).

The formal entry precondition omits the prompt's upper capacity bound, size,
rectangularity, and 0/1 restrictions. This strengthening is harmless for
nonnegative rows but becomes an overclaim for negative cells because of the
division issue discussed below.

## 5. Rule-by-rule static soundness review

The exhaustive declaration/rule inventory is
[rule-inventory.md](evidence/rule-inventory.md); the mechanical extraction is
[stage5-inventory-extraction.log](evidence/stage5-inventory-extraction.log).
It enumerates:

- every local syntax production and all five configuration cells;
- 13 local `[function]` symbols;
- all 58 `semantic.k` rules, the one program-constant rule, all six
  verification equations, and all three claims;
- the absence of local `[total]`, `[functional]`, `[simplification]`, priority,
  `owise`, `anywhere`, macro, and opaque declarations.

Every translated construct is mapped to a declaration and operational rules:
module/function collection; singleton returns; literals and name lookup;
left-to-right binary, condition, subscript, slice, and call evaluation;
argument binding; environment save/restore; empty-list comparison; recursive
index/drop functions; and final result installation. All local overlaps are
constructor-disjoint, literal-operator-disjoint, sort-disjoint, or guarded by
`0` versus `> 0`. Used recursive functions structurally descend. Exact-arity
calls are the only reachable calls, and unsupported or invalid operations stop
rather than fabricate a value.

The semantics has no heap, allocation, output, exception, or mutation cells
because the submitted pure program uses none. Its only changing interpreter
state is `<env>`, which is explicitly saved and restored on every call.
Arguments are evaluated left-to-right. Direct named-call lookup is faithful for
this program's immutable top-level function targets.

`water` and `requiredBuckets` are definitional mathematical summaries, not
operational bridges. Program-defined bodies still execute. The two helper
reachability claims provide the universal connection from exact invocations to
those summaries, and the entry claim depends on those connections. No fresh,
opaque, or unconstrained value can influence control or the result.
`solutionFunctions` and `solutionProgram` are fully equated exact constants;
neither contains the task answer.

### Narrow division limitation

The single scope concern is:

```text
arithmetic("//", intVal(I), intVal(J)) => intVal(I /Int J)
```

Installed K documentation says `/Int` is t-division rounded toward zero
([stage5-k-int-division-definition.log](evidence/stage5-k-int-division-definition.log)).
Python `//` floors. On every intended input, `J=capacity>0` and
`I=water+capacity-1>=0`, so the values coincide. There is therefore no false
conclusion witness on the intended 0/1 domain, and I do not label the rule
unsound there.

The broader formal/informal claim is not faithful. Concrete off-domain witness
`grid=[[-4]], capacity=2` satisfies the K claim's explicit `C > 0`
precondition: canonical and generated Python both return `-2`, while fresh K
returns `-1`. Evidence:
[stage5-off-domain-division-witness.log](evidence/stage5-off-domain-division-witness.log).
This refutes the candidate report's assertion that the Python bridge covers
arbitrary integer-valued rows, but it does not refute the requested theorem on
the prompt's intended domain.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to trust. I created a fresh mutation
that leaves both helper obligations unchanged and changes only the entry result
to:

```text
intVal(requiredBuckets(GRID,C) +Int 1)
```

The preserved mutation is
[spec-vacuity.k](evidence/spec-vacuity.k). It is demonstrably false for the
satisfying intended input `GRID=(rowVal(1))`, `C=1`: the real/claimed result is
1 and the mutation demands 2.

The mutation parsed and built successfully with `kprove --dry-run`, exit 0:
[stage6-vacuity-dry-run.log](evidence/stage6-vacuity-dry-run.log). The real
proof command then exited 1 with `WarnStuckClaimState` at the mutated entry
claim. Its residual contains the completed result
`intVal(requiredBuckets(GRID,C))` and the failed obligation equating
`requiredBuckets(GRID,C)+1` with `requiredBuckets(GRID,C)`. This is the expected
unmet result obligation, not a parser error, missing import, timeout, or
unreachable mutation:
[stage6-vacuity-proof.log](evidence/stage6-vacuity-proof.log).

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the freshly built generated K theory, for every finite `GRID:Rows` and
positive K integer `C`, if the modeled execution terminates, the exact
translated recursive program consumes its computation and produces
`requiredBuckets(GRID,C)`. The two helper claims establish the corresponding
row-sum and recursive-grid summaries at exact real invocation states. On the
prompt's 0/1-cell domain, `requiredBuckets` is the sum of per-row ceiling
bucket counts, so this is the requested partial-correctness property.

### Trust and assumption ledger

- **K reachability logic, Haskell/LLVM backends, and builtin Int/Map/list
  hooks:** trusted low-level proof platform. They affect all claims; this is the
  ordinary acceptable K trust boundary.
- **Trusted `py2mpy.py` and deterministic K parsing:** the proof/file identity
  bridge depends on them. Byte identity plus normalized KORE identity is strong
  mechanical evidence and does not encode correctness.
- **Generated semantics:** not assumed wholesale. Every local declaration and
  rule was audited. No local opaque primitive, totality assertion,
  simplification lemma, priority rule, or execution-bypassing bridge remains
  unaccounted for.
- **`gridVal`/`rowVal` representation relation:** fully defined for all
  operations the real program uses, and concretely agrees with ordinary
  `listVal` on the tested cases. A separate universal representation theorem
  is absent; this is a concerning but non-material informal bridge.
- **Mathematical intent bridge:** the identity
  `ceil(s/c)=(s+c-1)//c` for `s>=0,c>0` and the interpretation of row sums as
  water units are ordinary mathematics, not separately proved in K.
  Differential evidence supports this bridge on 215 inputs but is not treated
  as a universal proof.
- **Intended-domain restriction:** prompt cells are 0 or 1 and capacity is
  positive. The K precondition does not encode the cell restriction, making
  the negative-value overclaim visible rather than silently trusted.
- **Canonical and differential executions:** finite intent/representation
  evidence only. They do not substitute for any reachability claim.
- **Termination and concrete frontend scale:** the reported theorem is partial
  correctness. The 100×100 command-line parse kill is excluded from candidate
  soundness and retained as an evidence limitation.

There is no materially unsound rule on an intended input, no substituted
program, no free result, no oracle, and no vacuity. The two documented bridges
and the over-broad prose/formal scope justify concerns but do not invalidate the
proof for the real generated program on its required domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
