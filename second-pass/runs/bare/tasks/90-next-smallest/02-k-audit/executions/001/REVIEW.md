# Independent adversarial audit: 90-next-smallest

## Executive decision

The candidate contains a legitimate, result-constraining K reachability proof
of the exact submitted `solution.mpy` under its generated semantics. A fresh
source-only Haskell build proved the sole positive target with exit 0 and
`#Top`; a fresh LLVM build executed normal and boundary inputs consistently
with both Python implementations; the submitted `.mpy` is a byte-exact
translation of `solution.py`; and independent false-result and body mutations
both built successfully and were rejected with relevant stuck residuals.

The decision is `CONCERNS / LEGIT`, rather than `PASS`, for two related
adequacy limitations:

1. The symbolic postcondition names exactly the same `uniqueSort`/`lenInt`/
   `itemAt`/`iteVal` term produced by execution. The local ground equations are
   mathematically credible and were exhaustively reviewed, but the K proof does
   not separately prove that `uniqueSort` is the sorted duplicate-free
   permutation of its input. That last connection to “second smallest
   distinct integer” is an audited informal induction plus finite differential
   evidence, not a machine-checked K theorem.
2. The generated conditional semantics evaluates both pure branches and
   totalizes an out-of-range index with `invalidIndex`, unlike Python
   short-circuiting and `IndexError`. A concrete witness exists on the empty
   list. For this exact expression, the final result is nevertheless preserved:
   when the condition is false the sentinel is discarded, and when true the
   index is in range. This is a non-reusable, over-broad abstraction, not a
   false final result for the submitted program.

These limitations are material enough to document, but they do not make the
entry theorem false on its stated domain.

## 1. Input and provenance integrity

### Rendered semantics boundary

The rendered mode is `GENERATED_SEMANTICS`, and
`/reference/reference-semantics` is absent. This is the required mount state;
there is no infrastructure contradiction. The approved `/kit-skills` copies of
`using-kit`, `writing-semantics`, and `validating-proof` were byte-identical to
the installed copies used for this audit. K was independently available as
v7.1.293.

### Required artifacts and types

`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, the
single structured JSONL trace, `prompt.py`, `py2mpy.py`, `solution.py`,
`solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and `prove.sh` are
all regular files. No symlink occurs anywhere in `/candidate`. The candidate
has no additional helper K source file.

The candidate contains extra generated material—`semantic-kompiled/`,
`verification-kompiled/`, `__pycache__/`, and their caches/binaries. Those are
not source integrity failures, but they were treated as untrusted and never
copied into the reconstruction. There is no candidate `spec-vacuity.k`; stage
6 uses a fresh reviewer mutation as required.

The candidate prompt and translator compare byte-for-byte equal to the trusted
mounts:

- prompt SHA-256:
  `c411484e97c83ae8e5869ae414e5687f429deda4f5fb49e367e60c85635fed1e`
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

Those values also equal the untrusted hashes stated in `run-input.json`.
`run-input.json` identifies problem `90-next-smallest`, condition `bare`, and
no supplied semantics; this agrees with the rendered mode. The instruction
prompt hash is only a generation claim because no trusted `bare.md` is among
the authoritative mounts.

`metrics.json`, `codex-last.txt`, `codex-output.log`, and the 195-record JSONL
trace were read only as claims. They claim a successful generation and
eventual `#Top`, while the log also records earlier failed attempts. None was
used as proof evidence. The independent file/type/hash commands and bounded
untrusted-log extracts are preserved in:

- [`evidence/provenance.log`](evidence/provenance.log)
- [`evidence/untrusted-trace-extract.log`](evidence/untrusted-trace-extract.log)
- [`evidence/untrusted-codex-output-extract.log`](evidence/untrusted-codex-output-extract.log)
- [`evidence/untrusted-codex-output-tail.log`](evidence/untrusted-codex-output-tail.log)

No required source artifact is missing, changed relative to its trusted
counterpart where one exists, mistyped, or symlinked.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a finite list of integers, return the second smallest **distinct** integer.
Return `None` when fewer than two distinct integers exist. Distinctness is
confirmed both by the trusted canonical implementation’s `sorted(set(lst))`
and by the documented `[1,1] -> None` example.

The submitted implementation is:

```python
def next_smallest(lst):
    distinct = sorted(set(lst))
    return distinct[1] if len(distinct) > 1 else None
```

This is algorithmically identical to the trusted canonical body modulo the
temporary `distinct` binding and conditional-expression spelling.

### Trusted regeneration

The trusted translator was run against `/candidate/solution.py`. The regenerated
file has SHA-256
`e63a1fb4ace43a6e28f18d4f978372df2cc093a57b1b01c854ce86266fe0381b`
and is byte-identical to `/candidate/solution.mpy`. The source-only scratch
inventory confirms that no candidate kompiled directory was copied. See
[`evidence/prepare-and-fidelity.log`](evidence/prepare-and-fidelity.log) and
its reviewer script
[`evidence/prepare_and_fidelity.sh`](evidence/prepare_and_fidelity.sh).

### Independent differential test

[`evidence/differential_test.py`](evidence/differential_test.py) imports the
trusted canonical entry point and submitted entry point independently. Its
4,421 inputs comprise:

- all four documented examples;
- 11 named empty/singleton/distinctness/order/negative/large-integer branch
  boundaries;
- every list of length 0 through 5 over `{-2,-1,0,1,2}` (3,906 cases);
- 500 deterministic generated lists of length 0 through 20 over `[-100,100]`.

There were zero value or result-type mismatches. The exact ordered input set
has SHA-256
`bc23732c3255236b64b90d801e7e6fc655f8c5bf7dd18f64c939aae1f46f8289`.
All inputs and per-case results are in
[`evidence/differential-results.json`](evidence/differential-results.json);
the command, scope, status 0, and summary are in
[`evidence/differential-test.log`](evidence/differential-test.log).

This establishes strong finite fidelity evidence over the intended Python
domain; it is not substituted for the K proof.

## 3. Clean proof reconstruction

Only these source artifacts were copied to
`/tmp/audit-work/90-next-smallest/source`: the candidate `.py`, `.mpy`, and K
sources plus the trusted prompt, canonical implementation, and translator.
Fresh output definitions were created under
`/tmp/audit-work/90-next-smallest/rebuild`. Candidate definitions and caches
were neither read by the tools nor placed on their paths.

The concrete build command was:

```text
kompile /tmp/audit-work/90-next-smallest/source/semantic.k \
  --backend llvm --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/90-next-smallest/rebuild/semantic-kompiled
```

It exited 0. The reviewer then ran the regenerated program through this
definition on 10 normal and boundary cases: both documented nonempty examples,
empty, duplicates-only, singleton, two distinct in both orders, negative
duplicates, mixed duplicates, and unbounded-size positive/negative integers.
Every `krun` exited 0, consumed `<k>` to `.K`, and returned exactly the value
from both Python implementations. The complete configurations, commands,
statuses, and comparisons are in
[`evidence/reconstruct.log`](evidence/reconstruct.log) and
[`evidence/concrete-results.json`](evidence/concrete-results.json).

The proof definition was rebuilt with:

```text
kompile /tmp/audit-work/90-next-smallest/source/verification.k \
  --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/90-next-smallest/rebuild/verification-kompiled
```

It exited 0. Static enumeration found exactly one positive entry claim. It was
run explicitly:

```text
kprove /tmp/audit-work/90-next-smallest/source/spec.k \
  --definition /tmp/audit-work/90-next-smallest/rebuild/verification-kompiled \
  --spec-module SPEC --claims next-smallest-correct --output pretty
```

The command exited 0 and printed exactly `#Top`. The reconstruction harness
itself exited 0. Exact output is at
[`evidence/reconstruct.log`](evidence/reconstruct.log); the command driver is
[`evidence/reconstruct.sh`](evidence/reconstruct.sh).

Thus the candidate’s positive proof claim survives a clean reconstruction.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

There is no `requires` condition. The claim starts from:

- the exact constructor term for the submitted module and
  `next_smallest(lst)` body in `<k>`;
- any finite constructor list `L:IntList` in `<input>`;
- `none` in `<distinct>`;
- `noResult` in `<result>`.

It requires a final configuration in which:

- `<k>` is fully consumed;
- `<input>` remains `L`;
- `<distinct>` is `pyList(uniqueSort(L))`;
- `<result>` is `secondSmallest(L)`.

`secondSmallest` is not free or existential. Its sole unconditional equation
expands it to:

```text
iteVal(
  lenInt(uniqueSort(L)) >Int 1,
  itemAt(uniqueSort(L), 1),
  none)
```

The postcondition is therefore a concrete symbolic result expression, not a
tautological wildcard or one-way implication.

### Program identity

[`evidence/pinning_check.py`](evidence/pinning_check.py) independently extracted
the spec’s starting `<k>` program and compared it with the submitted
`solution.mpy`, ignoring layout only. Both normalized terms have SHA-256
`7c800cc508f76b8a38645105c706ed6fbb1d3fc0bc8f47aecdd974296574097e`.
The check exited 0; see
[`evidence/pinning-check.log`](evidence/pinning-check.log). Every constructor,
identifier, builtin name, literal, comparison operator, and index is pinned.

There are no helper/loop claims and no alternate program body. The only
function-entry harness rule matches the literal name `next_smallest`, parameter
`lst`, and exact single-function module structure.

### Satisfiable preconditions and ground substitutions

The precondition is visibly satisfiable. Two examples are:

- `L = nil`: the claimed result reduces concretely to `none`; canonical Python,
  submitted Python, and K all returned `None`/`none`.
- `L = cons(1,cons(2,nil))`: the claimed result is
  `iteVal(true,2,none)`, concretely 2; both Python functions and K returned 2.

These and further satisfying cases appear in the fresh concrete evidence.

### Body sensitivity

A separate reviewer mutation changed only the executed subscript from index 1
to index 0 while retaining the original second-smallest postcondition on
`[1,2]`. The mutated spec parsed successfully (`--dry-run` exit 0), then the
proof exited 1 with `WarnStuckClaimState` and residual result
`iteVal(true,1,none)`. This shows that the theorem is sensitive to a material
change in the pinned body rather than bypassing execution. See
[`evidence/spec-body-mutation-audit.k`](evidence/spec-body-mutation-audit.k) and
[`evidence/body-sensitivity.log`](evidence/body-sensitivity.log).

## 5. Rule-by-rule static soundness review

The complete declaration-by-declaration and rule-by-rule inventory is
[`evidence/rule-inventory.md`](evidence/rule-inventory.md). The mechanically
line-numbered source and attribute inventory is
[`evidence/static-inventory.log`](evidence/static-inventory.log). It counts 40
rules in `semantic.k`, one rule in `verification.k`, and one claim in `spec.k`.
There are no helper K source files, local simplification rules, priority rules,
`owise` rules, `[functional]` declarations, or local opaque declarations.

### Syntax-to-program coverage

| Submitted construct | Declaration and behavior |
|---|---|
| `Module` and one `FuncDef` | `Program`, `Stmt`, `Params`; exact entry harness at `semantic.k:70-71`. |
| statement sequence | `Stmts`; left-to-right `exec` rules at lines 73-74. |
| `Assign(Name("distinct"),...)` | `Assign`, `Name`; assignment frames and `<distinct>` update at lines 76-79. |
| `Return(...)` | `Return`; value evaluation and `<result>` update at lines 81-83. Return is last, so the semantics’ lack of general abrupt-return unwinding is immaterial here. |
| `Name("lst")`, `Name("distinct")` | Exact lookup rules at lines 85-88. |
| `Int(1)`, `NoneVal` | Literal rules at lines 89-90. |
| calls to `set`, `sorted`, `len` | Call frames and result rules at lines 92-98. |
| single integer `>` comparison | Compare frames and correctly ordered `>Int` rule at lines 100-104. |
| `Subscript(...,Int(1))` | Base-before-index frames and `itemAt` at lines 106-110 and 140-143. |
| conditional expression | Conditional frames at lines 115-121 and concrete selection at lines 152-153. |

Every submitted constructor is declared and reaches a rule. No wildcard
operation fabricates the whole task answer, and no rule rewrites the submitted
module directly to its expected return value.

### Configuration, state, and control

The configuration has only `<k>`, immutable `<input>`, local `<distinct>`, and
`<result>`. That is sufficient for this exact pure body. Assignment changes
only `<distinct>`; return changes only `<result>`; all other cells are framed.
Call arguments, comparison operands, and subscript base/index are evaluated
left-to-right. The entry binding is pinned by literal function and parameter
names.

This is not a reusable Python language semantics: there is no environment,
heap, exception cell, general call stack, output, or arbitrary return
unwinding. Those omissions do not hide an effect of this submitted body.

### Ground mathematical functions

- `uniqueSort(nil/cons)` covers both list constructors and strictly recurses on
  the tail.
- `insertUnique` covers nil plus the disjoint and exhaustive integer cases
  `<`, `==`, and `>`. It inserts in ascending position, removes equality, and
  strictly descends.
- `lenInt` covers nil/cons and strictly descends.
- `iteVal(true/false)` has disjoint, exhaustive ground-Bool equations.
- `secondSmallest` has one unconditional equation and is total by definition.

No overlap gives conflicting right-hand sides. The `uniqueSort`,
`insertUnique`, `lenInt`, and `itemAt` equations are `[concrete]`, so the
symbolic proof leaves terms over unknown `L` intact, while ground executions
reduce them. Attributes affect rewriting strategy; their mathematical
credibility comes from the reviewed equations, not from the attributes.

### Identified coverage/fidelity limitations and witnesses

1. **Eager conditional abstraction.** Lines 117-121 evaluate the then and else
   expressions regardless of the condition. On the satisfying input `L=nil`,
   depth 21 shows `false` already computed while evaluation enters the
   then-subscript; depth 27 shows `invalidIndex(1)` retained in the untaken
   branch. Python evaluates neither. The exact commands and states are in
   [`evidence/eager-branch-witness.log`](evidence/eager-branch-witness.log).

   This is a concrete witness of unfaithful intermediate evaluation on the
   intended domain. It does not enable a false final entry result here:
   `distinct[1]` and `None` are state-free; if `len(distinct)>1`, index 1 is
   valid and `iteVal(true,T,none)=T`; otherwise
   `iteVal(false,invalidIndex(1),none)=none`. There is no observable cell in
   which the speculative branch can leave an effect. The rule would be
   unacceptable for a branch with effects, divergence, or a result-relevant
   exception.

2. **Index-error sentinel and totality declaration.** `itemAt(nil,N)` returns
   `invalidIndex(N)` instead of modeling Python `IndexError`. In addition,
   `itemAt` is declared `[total]`, but a nonempty list with `N<0` matches
   neither the zero nor positive-index rule. That totality declaration is
   over-broad, and Python negative indexing is absent. The submitted term uses
   only the fixed index 1; when actual Python evaluates it, the preceding
   condition guarantees at least two elements. Thus neither negative indexing
   nor an actual out-of-range exception is on the real execution path.

3. **Symbolic intent connection.** The operational `sorted` rule and the final
   summary both contain the same `uniqueSort(L)` term. The equations are not an
   unconstrained oracle—they completely define every ground constructor list—
   but the positive reachability proof does not use an inductive connection
   theorem that states “the output is ascending and contains exactly the
   distinct input elements.” The name `secondSmallest` alone proves nothing.
   Its intended meaning follows from the reviewed recursive equations and the
   trusted canonical bridge. This is the principal reason for `CONCERNS`.

The first two points are over-broad-but-result-preserving for this exact
program and formal domain. No reviewed local rule enables the entry theorem to
return a wrong integer or `none` for an intended input.

## 6. Fresh non-vacuity test

The reviewer-authored
[`evidence/spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k) uses the exact
submitted body and the satisfying input `[1,2]`, but changes the
result-constraining obligation from second-smallest to `none`. The trusted
canonical function independently returns 2 on that input.

The mutation was copied to scratch and first run with `kprove --dry-run`; that
exited 0, establishing successful parsing/spec construction against the fresh
proof definition. The actual proof command then exited 1 with
`WarnStuckClaimState`. Its terminal residual was:

```text
<k> .K </k>
<input> cons(1,cons(2,nil)) </input>
<distinct> pyList(cons(1,cons(2,nil))) </distinct>
<result> iteVal(true,2,none) </result>
```

That residual directly exposes the unmet false result, rather than a parser
error, missing import, timeout, or unrelated crash. The harness recognized the
nonzero proof as expected and exited 0. Exact commands, the dry-run status,
proof status, warning, and residual are in
[`evidence/nonvacuity.log`](evidence/nonvacuity.log); the driver is
[`evidence/run_nonvacuity.sh`](evidence/run_nonvacuity.sh).

The proof is therefore non-vacuous and result-discriminating.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the candidate’s generated K theory, for every finite `IntList` of
mathematical integers, starting from the exact submitted `.mpy` program and
initialized cells, symbolic execution consumes the computation, stores
`pyList(uniqueSort(L))` in `<distinct>`, and stores

```text
iteVal(lenInt(uniqueSort(L)) >Int 1,
       itemAt(uniqueSort(L), 1),
       none)
```

in `<result>` (written through the definitional name `secondSmallest(L)`).
This is a machine-checked reachability/partial-correctness statement under the
rebuilt theory. It is sensitive to both the source index and the demanded
result.

It does not, by itself, prove a theorem in a complete CPython semantics, prove
the recursive sorting invariant in K, model arbitrary exceptions/effects, or
extend to inputs outside finite mathematical-integer lists.

### Trust ledger

| Boundary | Influence and dependents | Accounting |
|---|---|---|
| K v7.1.293 compiler, Haskell/LLVM backends, reachability engine | All builds, executions, and proof closure | Standard unavoidable toolchain trust. Fresh builds avoid candidate binaries. |
| K `Int`/`Bool` primitives and `+Int`, `-Int`, comparisons/equality | Sorting, length, indexing, guard, final branch | Acceptable ordinary mathematical primitives over unbounded integers. |
| Trusted `py2mpy.py` | Identity between Python AST and submitted `.mpy` | Byte-identical trusted translator and regenerated output. |
| Entry harness rather than full Python definition/call semantics | Binding and execution of the sole body | Acceptable for the exact one-function module because literal function/parameter names and the whole AST are pinned; not reusable as general Python. |
| `set`/`sorted`/`len` bridges and `uniqueSort`/`lenInt` equations | Entire returned value | Ground equations are exhaustive, disjoint, descending, and mathematically audited. Ten fresh K/Python comparisons plus 4,421 Python differentials support the bridge. The absence of a machine-checked sorting connection theorem is a documented concern. |
| `itemAt` and `invalidIndex` | Then-branch value | Correct for the fixed in-range index; over-broad totality and exception abstraction are concerning but do not alter the exact entry result. |
| Eager `iteVal` encoding | Branch control and returned value | Ground selector equations are truthful. Contextual equivalence is an informal argument specific to these pure branches, supported by boundary execution; it is not a general operational equivalence theorem. |
| `secondSmallest` proof-local symbol | Final postcondition | Definitional summary, not an oracle: one unconditional equation fixes its value. It does not independently certify the human-facing name. |
| Trusted canonical Python entry point | Natural-language adequacy oracle in finite tests | Strong finite evidence only; not a universal proof and not used in place of `kprove`. |

There are no fresh unconstrained values, proof-local operational rewrites,
priority overrides, simplification axioms, auxiliary circularities, opaque
program-derived results, or omitted helper claims.

### Gate assessment

- **Real-program soundness:** passes for the stated result property and exact
  submitted AST. Pinning, clean execution, body sensitivity, and non-vacuity
  all pass. The eager conditional is a context-specific extensional
  abstraction; its unfaithful intermediate state is explicit and does not
  change any claimed final cell on the formal domain.
- **Intent adequacy:** the formal domain matches finite lists of integers and
  the result expression matches the canonical distinct-second-smallest
  formula. The sorting/conditional connections are audited but informal, so
  this gate carries the concerns described above.
- **Evidence auditability:** passes. Reviewer scripts, complete bounded command
  logs, statuses, test inputs/results, fresh mutations, and exact source
  inventories are preserved under `/audit-output/evidence/`.

The reconstructed proof is therefore legitimate but not strong enough for an
unqualified `PASS`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
