# Static soundness and adequacy review

This file is the reviewer-authored analysis paired with the exhaustive
machine-generated inventory in `05_rule_inventory.md`.

## Inventory disposition

The inventory contains 937 top-level records: 230 syntax declarations, 700
rules, five contexts, one configuration, and one claim. It marks each
declaration/rule by exact source and line, relevant K attributes, reachability
from `solution.mpy`, and review disposition.

The entire `reference-semantics/` tree is byte-identical to the trusted supplied
tree. Therefore every row from that tree is fixed selected semantics, not a
candidate proof extension. Rows marked "not reached" cannot affect this
program's execution or claim. Rows marked "reachable and path-reviewed" are
reviewed below against the submitted AST. The eight `verification.k` records
and the one `spec.k` record are candidate-local and receive individual
decisions below.

There are no `[simplification]` rules and no `[functional]` declarations. The
22 opaque `[no-evaluators]` declarations are:

- float helpers `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`,
  `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
  `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and `sqrtF`;
- sort helpers `sortVS` and `sortKeyVS`;
- `md5hexCodes`.

None is reachable from this integer/arithmetic/`bin`/slice program. No opaque
value can influence its control flow, returned value, state, or postcondition.

## Construct-to-semantics map

| Submitted construct | Declaration and execution rules | Review |
|---|---|---|
| `Module` and statement sequence | `syntax.k:56,61`; `core.k:124-127` | `#loadAll` exposes the submitted statements and executes them left-to-right. |
| `FuncDef("solve", Params("N"), BODY)` | `syntax.k:53,57,60`; `functions.k:8,14-16` | Installs a closure containing the exact submitted body in module scope 0. |
| Call of `solve` | `call.k:19-21,69-75`; `core.k:185-191`; `functions.k:63-66,78-90` | Resolves the closure, evaluates the one argument, allocates a frame, binds `N`, executes the body, returns, restores the caller, and pops the frame. |
| `Name` lookup | `syntax.k:12`; `core.k:130-154,157-181` | Finds `N`/`digit_sum` in the callee and `bin` through the trusted builtins scope. The claim pins those scopes. |
| `Assign(Name("digit_sum"), RHS)` | `syntax.k:41 [strict(2)]`; `controls.k:9-11` | Evaluates the RHS and updates only the callee scope. That frame is removed on return. |
| `Int` literals | `syntax.k:9`; `core.k:194` | Exact unbounded K integers, matching Python for this domain. |
| `BinOp("+", ...)` | `syntax.k:15 [seqstrict(2,3)]`; `operators.k:12`; `int.k:9` | Left-to-right evaluation and exact integer addition. |
| `BinOp("%", ...)` | same dispatch; `int.k:15,19-20` | `pyMod` matches Python modulo for the positive divisor 10. |
| `BinOp("//", ...)` | same dispatch; `int.k:16,19-20` | `(N-pyMod(N,d))/d` matches Python floor division for positive divisors 10, 100, 1000, 10000. No zero divisor occurs. |
| `Call(Name("bin"), digit_sum)` | call route above; `builtins.k:17,108-121` | For the proved nonnegative digit sum, returns ASCII `0b` followed by the recursively defined binary digits. |
| `Subscript(..., Slice(Int(2), NoBound, NoBound))` | `syntax.k:22,38-39`; fixed rules `subscript.k:27-28,44-121`; candidate bridge `verification.k:31-38` | The bridge is separately reviewed below. |
| `Return` | `syntax.k:50 [strict]`; `functions.k:78-90` | Evaluates the slice, stores that exact value in `<ret>`, pops the frame, and resumes the caller with that value. |
| Configuration/cells | `core.k:49-60` | Entry pins the normal module configuration except that `<exit-code>` is framed. The reachable witness with exit code 0 is concrete; the program never changes it. |

All used arithmetic is exact and terminating on the intended domain. The
program allocates only its call frame; it does not allocate heap objects.
Evaluation order, lookup, call/return control, frame state, and exception state
are all represented in the claim. There are no loops or auxiliary loop claims.

## Candidate-local records, individually decided

1. `verification.k:8`, `decimalDigit(Int,Int) [function,total]`:
   definitional summary. Its used calls have `N` in 0..10000 and place in
   `{1,10,100,1000,10000}`. `[total]` leaves unused, uncovered arguments
   underspecified but supplies no false value used by the theorem.
2. `verification.k:9`, the place-1 equation: `pyMod(N,10)` is the units digit
   for every used nonnegative `N`. It does not overlap the guarded `P>1`
   equation.
3. `verification.k:10-12`, the higher-place equation: for `N>=0,P>1`,
   subtracting `N mod P`, dividing by `P`, and taking modulo 10 gives the digit
   at place `P`. The division is exact and every used `P` is positive.
4. `verification.k:15`, `decimalDigitSum(Int) [function,total]`: definitional
   summary. Its only equation is guard-covered by the entry precondition.
   Outside 0..10000 it is underspecified, but no such term is used.
5. `verification.k:16-22`, the sum equation: the five listed decimal places
   are all and only the possible places for 0..10000 (the fifth is needed only
   for 10000). Leading zero places add zero. This is exact.
6. `verification.k:25`, `binaryNumeral(Int) [function,total]`: definitional
   summary; the theorem uses it only on the nonnegative digit sum.
7. `verification.k:26`, `binaryNumeral(N) => str(binCodes(N))`: exact for the
   used nonnegative values because supplied `binCodes` is precisely the
   no-prefix binary payload. It does not replace program execution.
8. `verification.k:31-38`, priority-40 slice rule: operational bridge. Its
   complete matched domain is an already evaluated
   `str(iCons(48,iCons(98,REST)))`, exact literal slice `[2:]`, arbitrary K
   continuation, and arbitrary framed values of every non-`<k>` cell. It reads
   and changes only `<k>`. Fixed semantics also reads/changes only `<k>` here,
   evaluates start=2, omitted stop to full length, omitted step to 1, and
   returns precisely `str(REST)`. It introduces no return, exception, frame
   change, allocation, binding choice, or state effect. Priority only preempts
   the longer equivalent slice path.
9. `spec.k:6-72`, the sole claim: result-constraining and adequate. The
   `#loadAll` payload is whitespace-normalized identical to the submitted
   `solution.mpy`; the closure body repeated in the final scope is the same
   body. The RHS fixes the returned string to
   `binaryNumeral(decimalDigitSum(N))`, not a fresh variable, implication, or
   tautology. All material cells are pinned or preserved.

## Slice-bridge validation and narrower evidence gap

For an arbitrary finite `IntSeq REST`, ordinary structural reasoning gives:
the prefixed sequence has length `2+len(REST)`; slice start 2, default stop, and
default step 1 enumerate exactly `REST`. Thus no false conclusion witness exists
for the bridge, and it is not labeled unsound.

Reviewer checks used a Haskell definition importing only `MPY`, so the bridge
was absent:

- Three ground prefix cases with arbitrary `CONT:K` closed.
- All 37 binary payloads reachable from a digit sum 0..36 closed in one
  bridge-free proof, again with arbitrary `CONT:K`. This exhausts the bridge
  values reachable from every intended input.
- A stronger claim quantified over every `REST:IntSeq` did not close. The
  residual was the fixed semantics' recursive `buildIS` identity; it did not
  show a contradictory result. K lacked the structural induction needed to
  rewrite that opaque symbolic tail.

The candidate supplied no bridge-free universal connection theorem, and the
reviewer's stronger universal attempt was inconclusive. This is an auditability
limitation under the validation contract, not evidence that the rule can prove
a false result.

## Overlap, coverage, totality, and priorities

The two `decimalDigit` equations have disjoint place guards. The sole
`decimalDigitSum` equation is fully covered by the claim guard. The sole
`binaryNumeral` equation is deterministic. No candidate equation pair has an
overlap with conflicting right-hand sides, and every recursive supplied helper
used by this proof decreases a nonnegative integer (`binAcc`) or performs a
fixed finite expression.

The only candidate priority rule is the exact slice bridge above. It overlaps
the fixed generic slice path but has the same result and footprint on its match
domain. There are no candidate simplification rules, opaque symbols, fresh
oracles, task-answer axioms, function-call interceptions, or rules that bypass
the `solve` body.

The LLVM compiler warned about incomplete `[total]` coverage in unrelated
supplied helpers (`mapStrVS`, float coercions, `joinCodes`, and `valSeqAt`).
Those are fixed semantics and unreachable here. None can influence target
closure.

## Concrete satisfying states and substitutions

The default configuration with `N=0`, module scope empty, builtins scope
present, empty heap/stack, `noRet`, `NoExc`, and exit code 0 satisfies the entry
precondition. Additional satisfying substitutions:

| N | `decimalDigitSum(N)` | Claimed result | Trusted canonical | Candidate Python |
|---:|---:|---|---|---|
| 0 | 0 | `"0"` | `"0"` | `"0"` |
| 147 | 12 | `"1100"` | `"1100"` | `"1100"` |
| 150 | 6 | `"110"` | `"110"` | `"110"` |
| 1000 | 1 | `"1"` | `"1"` | `"1"` |
| 9999 | 36 | `"100100"` | `"100100"` | `"100100"` |
| 10000 | 1 | `"1"` | `"1"` | `"1"` |

`05_summary_math.log` checks the proof-side digit equations against the
decimal-string oracle for every integer 0..10000 with zero mismatches.
