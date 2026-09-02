# Independent adversarial audit: 129-minPath

The candidate is **not a legitimate partial-correctness proof of the submitted
program**. Fresh reconstruction confirms that all six positive claims print
`#Top`, and a fresh false-result mutation is rejected. The decisive defect is
real-program soundness: five proof-local priority rules replace
program-defined helper calls with the very mathematical summaries needed by
the postcondition, without machine-checked connection theorems from fixed
execution of those helper bodies. A fresh body-sensitivity experiment changes
`find_neighbor` to return `999`; fixed Python and K execution then return
`[1,999,1]` on a valid input, while the extended entry proof still prints
`#Top` for the old `[1,2,1]` summary.

This is a candidate failure, not an infrastructure failure. The supplied-mode
mount boundary is consistent, the K tools work, and the isolated retry of one
transient concurrent Java-launch failure succeeds.

## Stage 1 — Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount exists, as required. I did not use
`writing-semantics`, infer a hidden semantics, or modify candidate content.

Integrity results:

- `diff -ruN --no-dereference
  /reference/reference-semantics /candidate/reference-semantics` exits 0 with
  no output. The trees have identical entries and bytes.
- `find /candidate -type l` reports no symlinks. In particular, no supplied
  semantics entry is symlinked.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256 `417c9ed7...adb`).
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (SHA-256 `406485ea...b16`).
- All required source deliverables are present as regular files:
  `solution.py`, `solution.mpy`, `verification.k`, `spec.k`, `prove.sh`, and
  `PROOF.md`. The required provenance files and structured trace are also
  present.
- Candidate-built `runtime-kompiled`, `verification-kompiled`,
  `mutant-kompiled`, `__pycache__`, and all prior proof/log outputs were
  excluded from reconstruction.

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the complete 965-record JSONL trace only as untrusted
claims. They claim six closing proofs, 646 tests, and—importantly—the
candidate's own Gate A failure. None of those claims supplies audit authority.
The full log and trace were structurally read and hashed; bounded summaries are
in [untrusted log summary](evidence/logs/09-untrusted-codex-output-summary.log)
and [trace summary](evidence/logs/07-trace-summary.log).

Evidence:

- [toolchain](evidence/logs/01-toolchain.log)
- [semantics recursive diff](evidence/logs/02-semantics-tree-diff.log)
- [prompt comparison](evidence/logs/03-prompt-cmp.log)
- [translator comparison](evidence/logs/04-translator-cmp.log)
- [symlink check](evidence/logs/05-candidate-symlinks.log)
- [artifact types](evidence/logs/06-artifact-types.log)
- [untrusted metadata](evidence/logs/08-untrusted-metadata.log)
- [source hashes](evidence/logs/10-reference-and-candidate-hashes.log)

No required artifact is missing, changed, extra within the supplied semantics
tree, mistyped, or symlinked. There is no semantics-mode/mount contradiction.

## Stage 2 — Program fidelity and candidate-versus-canonical checks

### Contract

For an `N × N` grid with `N >= 2`, whose cells are exactly the distinct
integers `1..N²`, and a positive integer `k`, return the lexicographically
smallest sequence of values visited by any in-bounds orthogonal walk visiting
exactly `k` cells. Cells may be revisited. The prompt guarantees uniqueness.

The minimum walk must start at the globally minimum cell `1`. Let `m` be the
minimum value among the orthogonal neighbors of that cell. The next value must
be `m`; from `m`, the minimum possible next value is the adjacent `1`.
Repeating gives `[1,m,1,m,...]`. The trusted canonical implementation finds
`m` directly and builds that alternating list.

The submitted implementation uses a different but faithful decomposition:
`find_one` and `locate_one` locate the unique `1`; `scan_row` and
`find_neighbor` compute `m`; `build_path` constructs the alternating sequence.
On the intended domain, initializing the neighbor to `N²` instead of the
canonical `N²+1` is harmless because every actual neighbor is at most `N²`.

### Translation identity

Regenerating with the trusted translator:

```text
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/audit-src/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
```

produces byte-identical output. Both files have SHA-256
`23a07ea3c19d466baa6aff9070656e8477f203ff16585e8fbfce9809c8feaa92`.
See [translation comparison](evidence/logs/11-translate-and-compare.log).

### Independent differential testing

The reviewer-authored [differential script](evidence/differential.py) imports
the trusted canonical module and submitted module independently. It also uses
a definition-level brute-force walk enumerator rather than either
implementation's alternating-path logic.

The final run covers:

- both documented examples;
- every one of the 24 valid `2×2` grids for `k=1..8`;
- corner, edge, interior, and opposite-corner locations of `1` on `3×3`;
- 270 seeded valid grids of sizes 3, 4, 5, and 7 over parity and long-`k`
  boundaries;
- 814 intended-domain comparisons against brute-force enumeration; and
- excluded empty, `k=0`, and malformed-small-grid probes.

Results: 1,614 intended-domain cases, zero canonical/submitted mismatches, and
zero submitted/brute mismatches. Two excluded-domain differences are preserved:
empty grid with `k=2` and `[[]]` with `k=2`; both violate `N >= 2` and the
permutation condition and do not weaken the theorem.

Evidence:

- [final differential log](evidence/logs/37-final-python-differential.log)
- [complete generated inputs/results](evidence/differential-cases.json)
- [excluded-domain results](evidence/logs/38-excluded-domain-results.log)

There is no material implementation divergence on the intended domain.

## Stage 3 — Clean proof reconstruction

All source needed for execution was copied to `/tmp/audit-work`. No candidate
definition or cache was copied or referenced. K version
`v7.1.293` was used.

### Concrete definition

The supplied semantics was freshly compiled with the required concrete module:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled
```

The command exits 0. Its non-exhaustiveness warnings concern unused parts of
the fixed supplied semantics. Reviewer-authored concrete cases translate with
the trusted translator and run to `<k> .K </k>`, empty stack, `noRet`, and:

- documented example 1: `[1,2,1]`;
- documented example 2: `[1]`;
- `[[4,3],[2,1]], k=4`: `[1,2,1,2]`.

See [fresh LLVM build](evidence/logs/15-fresh-llvm-kompile.log),
[concrete source](evidence/concrete_cases.py), and
[fresh `krun`](evidence/logs/16-fresh-concrete-krun.log).

### Proof definition and all positive claims

The proof definition was freshly built:

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
```

It exits 0; see [fresh Haskell build](evidence/logs/17-fresh-haskell-kompile.log).
Each positive target claim was then selected and run separately:

| Claim | Exit | Result |
|---|---:|---|
| `SPEC.find-one-loop` | 0 | `#Top` |
| `SPEC.locate-one-loop` | 0 | `#Top` |
| `SPEC.scan-row-loop` | 0 | `#Top` |
| `SPEC.find-neighbor-loop` | 0 | `#Top` |
| `SPEC.result-loop` | 0 | `#Top` |
| `SPEC.minpath-entry` | 0 | `#Top` |

Logs are
[find-one](evidence/logs/18-prove-find-one-loop.log),
[locate-one](evidence/logs/19-prove-locate-one-loop.log),
[scan-row](evidence/logs/20-prove-scan-row-loop.log),
[find-neighbor retry](evidence/logs/24-prove-find-neighbor-loop-retry.log),
[result](evidence/logs/22-prove-result-loop.log), and
[entry](evidence/logs/23-prove-minpath-entry.log).

The first concurrent `find-neighbor-loop` invocation failed before proof
parsing because the Java launcher transiently reported no detected version
([preserved failure](evidence/logs/21-prove-find-neighbor-loop.log)).
The isolated retry records Java 17, exits 0, and prints `#Top`. This is resolved
infrastructure noise and is not used for the candidate verdict.

Thus the positive proof execution gate passes. `#Top` here establishes closure
only under the supplied semantics plus all rules in `verification.k`; it does
not validate those added rules.

## Stage 4 — Adequacy and real-program pinning

### Claim meanings

- `find-one-loop`: for an integer sequence `VS`, executing the real
  `find_one` loop body consumes it, increments `col_index` by `len(VS)`, leaves
  `value` at the last item (or its old value if empty), and makes `answer` the
  last column containing `1`, falling back to its old value.
- `locate-one-loop`: for integer-list rows `GS`, executing the `locate_one`
  outer loop consumes the rows, advances `row_index`, and updates
  `one_row`/`one_col` to the last row containing `1`. Its caller/module/scope
  freshness constraints pin the `find_one` binding.
- `scan-row-loop`: scanning an integer row consumes it, advances `col_index`,
  and folds the minimum value whose Manhattan distance from
  `(one_row,one_col)` is one.
- `find-neighbor-loop`: scanning integer rows consumes them, advances
  `row_index`, and folds `scanNeighbor` across the grid. It pins the
  `scan_row` binding.
- `result-loop`: for `0 <= I < K`, consuming `range(I,K)` appends the exact
  alternating suffix to the list at heap location `H`, and ends with
  `step=K-1`.
- `minpath-entry`: for `validGrid(GRID)`, integer rows, and `K>0`, applying the
  exact `minPath` closure returns `ref(0)`, allocates at heap 0 the sequence
  `alternatingSeq(0,K,scanGridNeighbor(...))`, advances `heapLoc` to 1, and
  ends with empty call stack and `noRet`.

`validGrid` exactly requires at least two rows, square row lengths, integer
cells in `1..N²`, and pairwise distinct cells. Since there are exactly `N²`
cells and `N²` available values, it is equivalent to the prompt's permutation
condition.

### Pinning and result constraint

The macro bodies in `verification.k:6-142` match the regenerated
`solution.mpy` constructor-for-constructor. The entry computation does not
load the `Module(...)` term from the submitted file; it starts directly at an
application of the exact `minPath` closure with an explicitly constructed
module environment containing all exact helper closures. Fixed module loading
would create those same bindings, so this direct-entry representation is a
transparent source bridge by itself.

The result is not a free variable, tautology, or one-way implication. The
claim fixes the returned reference, heap key, complete list formula, heap
allocation counter, stack, and return state. The successful fresh
false-result mutation in Stage 6 confirms this constraint.

However, the entry does **not** execute the actual helper bodies end to end:
five priority rules intercept their calls. The exact bodies are present in the
environment only as guards for those rules. The proof therefore pins the
submitted syntax but assumes the property-bearing effects of that syntax,
rather than proving them from real control flow.

Concrete satisfying states exist. For example,
`GRID=[[1,2],[3,4]], K=3` satisfies every entry guard. Specializing the formal
postcondition gives `[1,2,1]`, equal to both trusted canonical Python and
submitted Python. Two further ground states, including an interior `1`, agree
as recorded in [claim witness](evidence/logs/13-claim-ground-witness.log).
Those comparisons establish satisfiability and finite adequacy, not the
missing universal helper connection.

## Stage 5 — Rule-by-rule static soundness review

The reviewer-authored
[exhaustive inventory](evidence/k-rule-inventory.tsv) contains every local
configuration, context, syntax/function declaration, ordinary rule,
priority rule, simplification rule, opaque function, and claim, with line
locations. The generation command, hash, and totals are in
[inventory log](evidence/logs/35-corrected-k-inventory.log). Detailed
classification and the used-construct map are in
[static rule review](evidence/static-rule-review.md).

### Fixed supplied semantics

There are 928 inventory records outside `verification.k` and `spec.k`. They
are accepted as the fixed supplied semantics because their entire source tree
matches the trusted mount. The used program constructs map to fixed rules for
module/function loading, names, assignment, tuple unpacking, left-to-right
call evaluation, frames and returns, list/range iteration, branching, integer
operators, `len`/`abs`/`min`/`range`, allocation, and `append`.

The inventory identifies two fixed opaque functions:
`md5hexCodes` and `sortKeyVS`. Neither is reachable from this program or proof,
so neither affects control, state, result, or any claim. There are no
proof-local opaque functions.

### Candidate-local rules that are valid

- All 22 macro declaration/expansion records exactly name submitted syntax.
- The 21 proof-local total functions and all their equations are structurally
  recursive, covered, and disjoint on their guards. They faithfully define
  integer-row predicates, row/column scans, neighbor scans, the valid-grid
  predicate, and the alternating sequence.
- The guarded integer equality and `minVals` projections agree with fixed
  semantics. The two associativity simplifications are ordinary integer/list
  associativity.
- The priority-35 `For` normalization is an identity under `isIntList(V)`:
  that guard implies `V=list(rowContents(V))`, so no cell or control effect is
  changed.

No concrete or symbolic false conclusion witness was found for these rules;
they are not labeled unsound.

### Illegitimate result-bearing operational bridges

The rules at `verification.k:183-335` intercept calls to:

```text
find_one, scan_row, locate_one, find_neighbor, build_path
```

They replace fixed helper execution with `foundCol`, `scanNeighbor`,
`locateRow`/`locateCol`, `scanGridNeighbor`, and `alternatingSeq`. Priority 35
makes them preempt the fixed generic call path. Although each pins its expected
binding and macro body, it skips name/argument evaluation, frame allocation,
parameter binding, initialization, the helper body, return, frame pop, and
associated control state. The arbitrary `<k>` suffix and omitted
stack/return/exception/scope-location cells are broader than any auxiliary
claim.

Most importantly, all five are result-bearing. Their values drive branches,
coordinates, the selected neighbor, the returned allocation, and the entry
postcondition. The loop claims begin at `#loop`; none proves an exact
invocation from the intercepted call configuration through body execution and
restored caller state. The same summaries appearing in both execution bridges
and the final postcondition is circular.

I do not claim that these equations happen to return a wrong value for the
unmodified submitted source; testing and manual reasoning support their
numerical truth there. The narrower, decisive defect is that they install
program correctness as proof axioms. Under the required proof-extension
contract, program-derived result abstractions require universal
machine-checked connection theorems, not finite tests or a syntactically pinned
body.

The fresh operational-sensitivity witness makes the consequence concrete:

1. [body mutation diff](evidence/verification-body-witness.diff) changes only
   `FIND-NEIGHBOR-FUNCTION-BODY` to `Return(Int(999))`.
2. On the valid input `[[1,2],[3,4]], k=3`, Python returns `[1,999,1]`
   ([Python log](evidence/logs/27-body-witness-python.log)).
3. Fresh fixed LLVM semantics executes that exact mutant closure and stores
   `[1,999,1]` ([fixed K log](evidence/logs/29-body-witness-fixed-krun.log)).
4. The correspondingly rebuilt extended theory still proves the general
   `minpath-entry` claim with `#Top`
   ([build](evidence/logs/30-body-witness-kompile.log),
   [proof](evidence/logs/31-body-witness-proof.log)).
5. Specializing its unchanged result summary to the same input gives the false
   conclusion `[1,2,1]`.

This is a satisfying intended-domain false-conclusion witness for the
body-insensitive bridge architecture. It confirms that the required
body-to-summary connection is absent; the operational rules can prove the
summary independently of the displaced computation.

## Stage 6 — Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. Starting from the scratch
copy of `spec.k`, I created
[spec-audit-vacuity.k](evidence/spec-audit-vacuity.k), renamed the module, and
changed only the entry heap result from:

```text
list(alternatingSeq(...))
```

to the false:

```text
list(vCons(0, alternatingSeq(...)))
```

The exact change is in [mutation diff](evidence/spec-audit-vacuity.diff).
`GRID=[[1,2],[3,4]], K=1` satisfies the entry precondition and the real result
is `[1]`, whereas the mutation demands a leading `0`.

The mutation parses/builds successfully under `kprove --dry-run` with exit 0
([dry run](evidence/logs/25-vacuity-dry-run.log)). The actual proof exits 1
with `WarnStuckClaimState`; the residual has actual heap
`list(vCons(1, alternatingSeq(1,K,...)))`, which cannot unify with the mutated
destination. This is the expected unmet result obligation, not a parser error,
timeout, import failure, or unrelated crash
([failure log](evidence/logs/26-vacuity-proof-failure.log)).

The entry claim is therefore non-vacuous and result-constraining. This passes
the discrimination check but cannot repair the real-program connection
failure.

## Stage 7 — Proven versus assumed accounting

### What the successful reachability proof establishes

Under the fixed supplied MPY semantics **augmented by every rule in
`verification.k`**, the six symbolic reachability claims close. In particular,
for every formal valid grid and positive `K`, the direct `minPath` closure
application reaches the constrained alternating list, provided the five
program-defined calls may be replaced by their proof-local summaries. This is
a partial-correctness statement; it does not itself prove termination.

It does not establish that fixed execution of the submitted helper bodies
produces those summaries. Therefore it does not establish the required theorem
about the real generated program.

### Trust ledger

| Boundary / assumption | Effect and dependents | Audit disposition |
|---|---|---|
| Trusted supplied MPY source | Defines all execution; all claims depend on it | Acceptable by rendered `SUPPLIED_SEMANTICS` boundary; exact tree match |
| K v7.1.293 compiler, LLVM/Haskell backends, SMT/Kore execution | Build, concrete execution, proof closure | Ordinary tool trust; fresh successful reconstruction |
| Fixed integer/list/map primitives and used builtins | Values, control, heap, allocation | Acceptable selected-semantics primitives; concretely exercised |
| Fixed `md5hexCodes`, `sortKeyVS` opacity | Would affect digest/sort results | Unused and unreachable; no dependent claim |
| Exact source-body macros and direct-entry environment | Bridges submitted `.mpy` syntax to entry configuration | Byte regeneration plus constructor inspection; adequate syntactic bridge |
| Proof-local pure summaries | Define scans, domain, alternating result | Equationally covered and mathematically justified |
| Five helper-call priority rules | Replace all property-bearing helper execution; outer loops and entry depend on them | **Illegitimate**: no universal connection theorem; fresh false body witness |
| “Minimum walk alternates `1,m`” argument | Connects formal alternating summary to natural-language minimum path | Informal mathematical adequacy bridge; independently supported, not the K proof |
| 1,614 Python differential cases / 814 brute-force cases | Source/canonical and intent evidence over tested inputs | Finite empirical support only; cannot prove helper bridge universally |
| Termination of finite loops | Needed to turn partial correctness into total correctness | Not claimed by reachability; informally evident from finite sequences/range |
| Candidate `PROOF.md`, traces, prior `#Top`, logs | None | Untrusted claims only; excluded from proof authority |

### Decision

The dynamic reconstruction and fresh non-vacuity test show a discriminating
proof under the extended theory. Program fidelity and natural-language
adequacy are also well supported. Nevertheless, Gate A fails before those
facts can yield legitimacy: the proof bypasses real helper execution and
assumes the result-bearing summaries that constitute the central correctness
argument. The fresh body witness demonstrates that the architecture remains
provable when displaced fixed execution produces a conflicting result.

Accordingly, this meets the decision boundary for a substituted/bypassed
program computation and an unproved smuggled correctness conclusion.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
