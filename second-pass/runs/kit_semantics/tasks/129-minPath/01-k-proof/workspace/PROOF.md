Incomplete work

## What is proven

The preserved `solution.py` translates byte-for-byte to `solution.mpy` and
executes to the expected alternating path on two fixed-semantics witnesses
covering odd and even `k` (and one and two loop iterations).  K proves these
auxiliary reachability claims with `#Top`:

- the two inner-scan invariants and two outer-scan invariants together;
- the source-level nested-scan completion claim;
- the exact four-conditional neighbor computation claim; and
- the generalized result-loop claim for a symbolic positive remaining count
  and a symbolic accumulated prefix.

The required `minpath-full-contract` claim over arbitrary `N >= 2`, arbitrary
permutation grids, and arbitrary positive `K` does not close.  No successful
proof of the full HumanEval contract is reported.

## Formal claim

`minpath-full-contract` starts from the exact call to the translated
`minPath` closure.  Its precondition represents every square `N >= 2` grid
whose flattened integer sequence is a permutation of `1..N*N`, and every
`K > 0`.  Its postcondition requires the returned list to satisfy
`finishRel(.ValSeq, OUT, (K - pyMod(K,2))/2, neighborMin(...), K)`, i.e. the
sequence `1, M, 1, M, ...`, truncated to length `K`, where `M` is the minimum
orthogonal neighbor of the unique cell containing `1`.

This sequence is the intended lexicographic minimum: every minimum path must
start at the unique global minimum `1`; its least possible second value is the
least adjacent value `M`; returning to `1` is then least, and the argument
repeats.

## Proof-extension inventory

| Extension | Class and role | Domain / context | Footprint and justification | Dependents |
|---|---|---|---|---|
| `intMember`, `allInRange`, `uniqueInts`, `validPerm` | Definitional summaries | Finite `IntSeq`; `validPerm(P,M)` is a precondition | Total structural equations; no program control | All symbolic claims |
| `gridRows*`, `gridRow*`, `pAtTotal`, `gridAt` | Definitional summaries | Row-major finite sequence representation | Total structural construction and selection | Scan and neighbor claims |
| `findOne`, `oneIndex`, `oneRow`, `oneCol` | Definitional summaries | Valid permutation, `N > 0` in uses | Structural search followed by quotient/remainder; fixes the unique `1` position | Scan, neighbor, target |
| `vsLen`/`valSeqAt` selector rules, `gridAt == 1`, and the guarded `gridAt < N*N+1` rule | Derived functional simplifications | Exactly valid indices under `N >= 2` and `validPerm(P,N*N)` | Simplify stuck data access only; do not bypass evaluation or control. These are downstream Lean obligations, not discharged here | Scan and neighbor claims |
| `chooseMin`, `after*`, `best*`, `neighborMin` | Definitional summaries | Valid cell position; exact four directional guards | `neighborMin` expands to the same four conditional minima executed by the program | Neighbor, result, target |
| `snocVS`, `pairDone`, `oddDone`, `finishRel`, `pathRel` | Definitional result summaries | Finite `ValSeq`; guarded recursion on the remaining pair count | Structural list append and exact even/odd output relation; no program term is rewritten | Result loop and target |
| AST abbreviations such as `outerLoop`, `upIf`, `resultBody`, and `minPathBody` | Syntax macros | Exact translated syntax only | Textual abbreviation; no semantic behavior added | All reachability claims |
| `inner-*`, `outer-*`, `scan-finish`, `neighbor-finish`, `result-loop-tail` | Derived reachability claims | Exact configurations, bindings, continuations, and loop invariants shown in `spec.k` | Execute the supplied semantics and preserve all framed cells; successful commands below | Intended modular target composition |

There is no operational answer-bearing rewrite, arbitrary-continuation bridge,
or rule that skips either loop.  The only modular `--trusted` use in the target
command names auxiliary claims that were first proved independently; that target
command nevertheless fails and is not used as evidence of completion.

## Commands and actual outputs

Translation identity:

```bash
cmp -s solution.mpy <(python3 py2mpy.py solution.py)
```

Actual output: none; exit 0.

Concrete LLVM build:

```bash
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX -o runtime-kompiled
```

Actual output: supplied-semantics non-exhaustive/unused-variable warnings; exit
0.

Concrete executions:

```bash
krun smoke_odd.mpy --definition runtime-kompiled
krun smoke_even.mpy --definition runtime-kompiled
```

Actual outputs: both exit 0 with `.K`, `NoExc`, and exit code 0.  The result
heap entries are respectively
`list(vCons(1,vCons(2,vCons(1,.ValSeq))))` and
`list(vCons(1,vCons(4,vCons(1,vCons(4,.ValSeq)))))`.

Symbolic build:

```bash
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX -o verification-kompiled
```

Actual output: only supplied-semantics unused-variable warnings; exit 0.

Nested scan claims:

```bash
kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.inner-one-ahead,SPEC.inner-no-one,SPEC.outer-one-ahead,SPEC.outer-one-past,SPEC.scan-finish --depth 240
```

Actual output: `#Top`; exit 0.

Neighbor claim:

```bash
kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.neighbor-finish --depth 400
```

Actual output: `#Top`; exit 0.

Generalized result-loop claim:

```bash
kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.result-loop-tail --depth 110
```

Actual output: a low-productivity warning followed by `#Top`; exit 0.

Required modular target attempt:

```bash
kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.scan-finish,SPEC.neighbor-finish,SPEC.result-loop-tail,SPEC.minpath-full-contract --trusted SPEC.scan-finish,SPEC.neighbor-finish,SPEC.result-loop-tail --depth 240
```

Actual output: `WarnStuckClaimState`, `WarnUnexploredBranches` (two branches),
and `Error: backend terminated because the configuration cannot be rewritten
further`; exit 1.  The residual reaches `ref(0)` and the correct two-pair heap,
but fails an implication containing the unreduced three-element-prefix
`snocVS` term.  This is a bounded diagnostic, not a successful target proof.

## Gate results

- Gate A — **FAIL**.  The required positive full-domain target command did not
  print `#Top` or exit 0.  In addition, the guarded functional selector lemmas
  remain downstream Lean obligations.  Supporting `#Top` claims do not replace
  the missing composed proof.
- Gate B — **not reached as a successful proof gate**.  The stated target has
  the full unbounded HumanEval domain and its output relation matches the
  lexicographic-minimum characterization; there is no finite-size restriction.
- Gate C — **not reached**.  Reproducible concrete evidence and the trust ledger
  are recorded, but no validation status is claimed for an unfinished proof.

## Trust boundary

The supplied `reference-semantics/` is treated as fixed.  The only outstanding
proof-local assumptions are the guarded functional selector/range lemmas listed
above, intended for downstream Lean discharge.  No Lean project or recorded
`Proof.final` exists here, and no `native_decide` or `Lean.ofReduceBool` occurs.

## Empirically supported facts

`smoke_odd.mpy` executes `[[1,2],[3,4]], k=3` to `[1,2,1]`.
`smoke_even.mpy` executes `[[5,9,3],[4,1,6],[7,8,2]], k=4` to
`[1,4,1,4]`.  These witnesses confirm the summary head and both parities but
are finite evidence only.

## Excluded behavior

No behavior allowed by the HumanEval input contract is intentionally excluded
from the target statement.  What is excluded from the proof report is the
unclosed symbolic composition for arbitrary result-loop counts; fixed sizes and
the successful loop lemma are supporting progress only.
