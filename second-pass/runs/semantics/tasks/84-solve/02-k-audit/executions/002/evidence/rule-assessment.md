# Rule-by-rule assessment key

This assessment applies to every entry in `rule-inventory.md`.  The inventory
contains the exact source block for all 937 declarations, contexts, rules,
configuration declarations, and claims.  There are 700 `rule` entries: 695 in
the byte-verified supplied semantics and five in `verification.k`.

## Assessment classes

- **FIXED/REACHABLE** — part of the supplied semantics, reached by the submitted
  AST, and checked below against the intended behavior.
- **FIXED/INERT** — part of the supplied semantics but its redex/constructor is
  absent from this program and its proof path.  It cannot affect the returned
  term here.  Its guards/constructor cases were inspected for overlaps; no
  equation equating two distinct values was found.  It is not an extra
  candidate assumption.
- **FIXED/CONCRETE-ONLY** — in `semantics/concrete.k`; used only by the LLVM
  smoke definition and absent from the Haskell proof definition.
- **LOCAL/DEFINITIONAL** — a proof-local mathematical name whose equations are
  true on every use in the entry claim.
- **LOCAL/OPERATIONAL-BRIDGE** — a proof-local rule that preempts fixed
  execution and therefore needs a separate context/value assessment.
- **TARGET** — the single reachability claim, assessed for adequacy and
  non-vacuity rather than as a semantic rule.

Every syntax-only declaration and context in the inventory is assigned the
same class as its containing module below.  Syntax declarations make no
value-level assertion by themselves.  Generated heating/cooling from
`seqstrict`/`strict` was reviewed with its declared argument order.

## Complete file assignment

| Source | Rules | Class | Decision |
|---|---:|---|---|
| `semantics/syntax.k` | 0 | FIXED/REACHABLE declarations | The used constructors are `Module`, `FuncDef`, `Params`, `Assign`, `Name`, `BinOp`, `Int`, `Return`, `Subscript`, `Call`, `Slice`, and `NoBound`. `BinOp` is left-to-right `seqstrict`; `Assign` heats the RHS; `Return` heats its expression. |
| `semantics/core.k` | 46 | mixed FIXED/REACHABLE and FIXED/INERT | Reachable rules are module loading/sequencing (125–127), name lookup/parent traversal (131–154), `builtinsScope` (157–181), left-to-right argument evaluation (189–191), `Int` literals (194), and `appendVal` (213–215). Configuration and these transitions preserve the expected heap, exception, return, and allocation cells. Other redexes are absent. |
| `semantics/operators.k` | 10 | mixed FIXED/REACHABLE and FIXED/INERT | `BinOp` dispatch at line 12 is reached after generated left-to-right heating. No heap references occur. Other operators are absent. |
| `semantics/int.k` | 16 | mixed FIXED/REACHABLE and FIXED/INERT | Integer `+`, `%`, `//`, and `pyMod` (9, 15–20) are reached. All divisors are the positive constants 10, 100, 1000, or 10000, so the floor/mod equations agree with Python and have no zero-divisor path. |
| `semantics/controls.k` | 34 | mixed FIXED/REACHABLE and FIXED/INERT | Plain-name assignment (9–11) is reached and updates only the callee scope. Branches, loops, imports, cell writes, and heap dereferences have no matching term. |
| `semantics/functions.k` | 15 | mixed FIXED/REACHABLE and FIXED/INERT | Plain `FuncDef` (14–16), parameter binding (63–66), `Return` (78–79), and frame pop (85–90) are reached. The call frame is removed, the caller environment and `scopeLoc` are restored, and return control is preserved. Annotated closures are absent. |
| `semantics/call.k` | 21 | mixed FIXED/REACHABLE and FIXED/INERT | Generic callee/argument evaluation (20–21), builtin dispatch (31), and plain closure entry (69–74) are reached. Callee lookup selects the actual module closure or the `bin` binding in `builtinsScope`; no textual-name shortcut occurs. |
| `semantics/builtins.k` | 137 | mixed FIXED/REACHABLE and FIXED/INERT | Only `bin` (108–121) is material: for a nonnegative digit sum it emits codepoints `48,98` followed by the recursively defined binary codes. `binAcc` strictly decreases its positive integer argument. The other builtin symbols/redexes are absent. |
| `semantics/subscript.k` | 40 | mixed FIXED/REACHABLE and FIXED/INERT | The fixed slice path (50–121) is the behavior preempted by the local bridge. It evaluates pure bounds `2,None,None`, uses step 1, and selects indices 2 through length−1 without state changes. Fixed ground execution validates every reachable tail. Other indexing/slice forms are absent. |
| `semantics/str.k` | 28 | FIXED/INERT except value constructors | `str(IntSeq)` carries the `bin` result; no string literal/operator/method redex participates in the symbolic theorem. |
| `semantics/assert.k` | 3 | FIXED/CONCRETE-VALIDATION | Absent from the target claim; exercised only in reviewer LLVM harnesses. |
| `semantics/concrete.k` | 16 | FIXED/CONCRETE-ONLY | Imported by `MPY-KRUN`, not by `VERIFICATION`; none of its sort/deep-equality rules can contribute to `#Top`. |
| `semantics/bool.k` | 13 | FIXED/INERT | No Boolean operator term occurs. |
| `semantics/comprehension.k` | 7 | FIXED/INERT | No comprehension occurs. |
| `semantics/dict.k` | 28 | FIXED/INERT | No dictionary term occurs. |
| `semantics/float.k` | 121 | FIXED/INERT | No float term occurs. All 20 proof-opaque float symbols are absent from the target path and postcondition. |
| `semantics/iter.k` | 0 | FIXED/INERT declarations | No iterator term occurs. |
| `semantics/list.k` | 27 | FIXED/INERT | No list term occurs. |
| `semantics/methods.k` | 75 | FIXED/INERT | No bound-method term occurs. |
| `semantics/range.k` | 6 | FIXED/INERT | No range term occurs. |
| `semantics/set.k` | 12 | FIXED/INERT | No set term occurs. |
| `semantics/sort.k` | 19 | FIXED/INERT | `sortVS` and `sortKeyVS` never occur. |
| `semantics/tuple.k` | 21 | FIXED/INERT | No tuple term occurs. |
| `verification.k` lines 8–12 | 2 | LOCAL/DEFINITIONAL | `decimalDigit(N,1)=N mod 10`; for the only other places (10,100,1000,10000) and `N≥0`, `(N−N mod P)/P mod 10 = floor(N/P) mod 10`. Guards are disjoint. The `[total]` attribute leaves out-of-guard values arbitrary but adds no false equality; all theorem uses reduce under their guards. |
| `verification.k` lines 15–22 | 1 | LOCAL/DEFINITIONAL | Expands to exactly the five decimal places needed for `0≤N≤10000`; the bound excludes any nonzero higher digit. |
| `verification.k` lines 25–26 | 1 | LOCAL/DEFINITIONAL | Names `str(binCodes(N))`, the prefix-free binary numeral already defined by the fixed `bin` semantics. The reached argument is in 0..45. |
| `verification.k` lines 31–38 | 1 | LOCAL/OPERATIONAL-BRIDGE | See the complete bridge assessment below. The equation is mathematically true and result-determining, but the candidate supplies no bridge-free universal connection theorem. |
| `spec.k` lines 6–72 | 1 claim | TARGET | Executes the byte-identical submitted module, calls `solve(N)`, and constrains the final `<k>` value for every integer `0≤N≤10000`; all material cells are pinned. |

The remaining declarations/rules in each mixed module are **FIXED/INERT** by
the class definition. This is an exhaustive assignment: every entry in
`rule-inventory.md` belongs to exactly one source row and therefore one decision.

## Proof-local attribute and overlap review

- There are no local simplification rules, functional claims, opaque
  `no-evaluators` symbols, or fresh result-bearing oracles.
- The three local `[function,total]` symbols have deterministic, non-overlapping
  equations on every reached argument. Their declarations are broader than
  their guarded equations, but arbitrary out-of-domain interpretations cannot
  affect the entry claim.
- The only local priority is the slice bridge at `priority(40)`. It deliberately
  preempts the generic fixed `Subscript` path only for a string whose first two
  codes are `0` and `b` and the exact slice `[2:]`.

## Complete operational-bridge assessment

Matched context:

`Subscript(str(iCons(48,iCons(98,REST))), Slice(Int(2),NoBound,NoBound))`
at the head of an arbitrary `<k>` continuation. It reads no cell other than
`<k>`, returns `str(REST)`, and leaves environment, scopes, heap, allocation
counters, stack, return state, exception state, and exit code untouched.

Fixed behavior:

The fixed rules evaluate the lower bound `Int(2)` to 2, both absent bounds to
`noB`, and the absent step to 1. Python/K slice normalization therefore starts
at index 2 and stops at the string length. Structural `buildIS` returns exactly
`REST`. The bound terms are pure and cannot return, raise, allocate, or mutate;
therefore admitting an arbitrary continuation is context-safe.

Evidence and limitation:

- The main proof without this rule fails specifically at the unreduced
  `buildIS(...binCodes(...))` equality (`stage5-proof-without-bridge.log`).
- A fresh fixed-only universal connection claim was well formed but failed
  because the backend leaves symbolic `isLen/buildIS` opaque
  (`stage5-slice-connection.log`). Thus the candidate has no machine-checked
  universal connection theorem.
- Fixed and bridge-enabled LLVM execution produced byte-identical final
  configurations for all 46 values in the conservative 0..45 range (a superset
  of all sums reachable from this program), with assertion continuations after
  every slice (`stage5-slice-ground-comparison.log`).
- There is no opposite interpretation: the RHS contains the exact structural
  tail variable, not a fresh value. A false conclusion witness for this rule
  does not exist under the algebraic `IntSeq` model. Accordingly this is an
  evidence limitation, not an unsound-rule finding.

## Opaque and trusted symbols

The fixed tree declares 22 `no-evaluators` symbols (19 float/conversion
symbols, `md5hexCodes`, `sortVS`, and `sortKeyVS` counting declarations as
listed in `rule-inventory.md`).
None occurs in `solution.mpy`, the reachable residuals, or the postcondition.
The target therefore has no value, branch, state, or control dependency on an
opaque symbol.
