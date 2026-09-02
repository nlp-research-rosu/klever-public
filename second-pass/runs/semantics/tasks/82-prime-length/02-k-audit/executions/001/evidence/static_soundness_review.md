# Exhaustive static soundness ledger

The machine-readable sentence inventory is `13_k_inventory.log`. It contains
1,115 source sentences: 704 rules (595 ordinary, 48 priority, 35 concrete, 26
`owise`), 232 syntax sentences (149 function, 79 ordinary, 4 macro), five
contexts, one configuration, three claims, and module/import/require structure.
There are no `[simplification]` rules, `[functional]` declarations, or aliases.
`27_inventory_by_file.log` gives exact per-file counts and
`28_opaque_inventory.log` lists all 25 explicitly symbolic/opaque declarations.

The following disposition applies to every corresponding inventory row. “Used”
means reachable in the submitted solution/claims. “Unused subset” means the
sentence is disjoint from the program's syntax/value sorts or only appears in
the LLVM smoke harness; no concrete or symbolic false conclusion witness was
found for it on the intended domain. Such a classification is not being used
to excuse a false rule.

| Source | Exhaustive disposition |
|---|---|
| `semantics.k` | Assembly only. `MPY` imports the proof semantics; `MPY-KRUN` additionally imports `MPY-CONCRETE`. Imports and module boundaries are consistent. |
| `syntax.k` | AST declarations and strictness. Every submitted construct is declared. `BinOp` is left-to-right `seqstrict`; `If`, `Assign`, `AugAssign`, and `Return` evaluate the indicated expression first. |
| `core.k` | Used configuration, structural sequences/length, scope lookup, argument evaluation, literals, and dispatch declarations are faithful to the declared MPY subset. Heap/cell/keyword helpers are unused subset rules. Cells/configuration are coherent on the used non-cell path. |
| `iter.k`, `range.k` | Iterator declaration/range equations are unused by the while-based implementation. Guards cover positive/negative nonzero steps. |
| `operators.k` | Used compare and binary dispatch preserve evaluation order. Ref-dereference priority rules are sort-disjoint from the submitted integer/string path. |
| `int.k` | Used integer `<`, `==`, `+`, and `%` equations are ordinary arithmetic. On the proof domain divisors begin at 2 and increase, so `pyMod` is never invoked with zero. |
| `bool.k` | Used Boolean comparisons/truth behavior is ordinary. `BoolOp`/ref cases are unused. Guard pairs are disjoint. |
| `str.k` | `isLen` is actually in `core.k`; string iteration/operators are unused by the proof. Literal conversion is intentionally ASCII-only, a language-subset restriction affecting only concrete literals; symbolic claim inputs are `str(IntSeq)` and the theorem depends only on structural length. |
| `set.k`, `list.k`, `tuple.k`, `dict.k` | Collection, membership, mutation, unpacking, and equality rules are unused subset semantics. Their constructor cases/guards descend structurally; priority rules handle refs and are disjoint from used values. |
| `subscript.k` | Entirely unused. Index/slice rules encode the declared subset. The compiler flags the over-broad `[total]` on `valSeqAt` for empty sequences; this is a trust/evidence gap, not a used-path false conclusion. |
| `comprehension.k` | Unused macros translating comprehensions to closures/loops; no role in proof closure. |
| `methods.k` | Unused string/list method subset. The compiler flags `joinCodes` totality on non-string elements such as internal `cellsMark`; such values are outside declared `join` use and do not influence this proof. |
| `controls.k` | Used assignment, if, and fixed while rules are faithful: `While => #while`, condition evaluated, true executes body followed by loop label, false exits. For/loop-control/import/heap-ref cases are unused. |
| `functions.k` | Used closure definition, parameter binding, `Return`, and frame pop preserve result/control on this non-closure-returning program. The semantics explicitly limits escaping closures; that unused restriction is irrelevant here. |
| `call.k` | Used call flow evaluates callee then arguments, resolves `len` through the builtins frame, constructs a call frame, and routes builtin/closure calls. Method/ref rules are unused and priority-disjoint. |
| `builtins.k` | Used `applyBuiltin("len", str(IS)) => isLen(IS)` is exact. Other folds/conversions/eval/hash rules are unused. `md5hexCodes` is explicitly opaque. The compiler flags `mapStrVS` totality on an internal non-user value; it is unused. |
| `float.k` | Entirely unused. Twenty-two symbolic float declarations form an explicit proof trust boundary backed by `[concrete]` LLVM equations where supplied. Compiler totality warnings for `floorFI`, `toF`, and `ceilF` concern invalid generic `Val` cases and do not influence any claim. |
| `sort.k` | Entirely unused. `sortVS` and `sortKeyVS` are explicit opaque proof boundaries with concrete insertion-sort equations for LLVM where supplied. |
| `assert.k`, `concrete.k` | Not imported by the Haskell proof module. Used only by the reviewer’s LLVM smoke test. False assertions set `AssertionError`/exit code 1; concrete deep-equality/key-sort legs do not enter proof closure. |

## Proof-local rules, individually

| Rule/declaration | Class and decision |
|---|---|
| `primeLoopBody` declaration/equation | Definitional summary. Constructor-for-constructor identical to the submitted loop body. Truthful and non-operational. |
| `primeBody` declaration/equation | Definitional summary. Constructor-for-constructor identical to regenerated `solution.mpy`. It is manually re-encoded, however; no K connection claim loads the submitted `Module` and derives this closure. |
| `primeLengthClosure` declaration/equation | Definitional summary of a one-parameter closure containing `primeBody`; truthful as a term abbreviation. |
| `#primeLoopEntry`, `#capturePrimeLoopN`, `#capturePrimeLoopD` syntax | Proof-only observation symbols. They are not values of the submitted language and `#primeLoopEntry` is not a Boolean. |
| `While(_C,_B) => Name("n") ~> #capturePrimeLoopN ... [priority(1)]` | Operational bridge; **illegitimate** for a real-program result proof. It preempts every fixed `While` rule, ignores condition/body/binding guards, and admits any continuation. No bridge-free connection theorem exists. |
| `N ~> #capturePrimeLoopN ~> REST => Name("divisor") ~> #capturePrimeLoopD(N) ~> REST [priority(40)]` | Instrumentation continuation. It preserves `REST` at this step but is part of the unvalidated operational bridge chain. |
| `D ~> #capturePrimeLoopD(N) ~> _REST => #primeLoopEntry(N,D)` plus cell resets | Operational bridge; **illegitimate**. It discards arbitrary `_REST`, clears scopes/stack, and resets control cells. The concrete false-conclusion/control witness is in `bridge_witness.md`; fixed LLVM completes all tests, while bridge-enabled execution stops at `#primeLoopEntry(2,2)` (`17_krun_audit_concrete.log` versus `26_krun_bridge_enabled.log`). |
| `noDivisorsFrom(N,D) => true` when `D >= N` | Truthful base case for “no divisor among `D..N-1`.” |
| `noDivisorsFrom(N,D) => false` when `D < N` and `pyMod(N,D)==0` | Truthful composite case on the used `D>=2` domain. |
| Recursive `noDivisorsFrom(N,D+1)` otherwise | Truthful, disjoint from the composite guard, and strictly advances toward the base case. The three guards cover every used state without overlap. |

## Priority, overlap, and state conclusion

The supplied priority rules that can occur on the submitted non-ref path are
ordinary dispatch refinements and preserve state. The proof-local
`priority(1)` bridge intentionally outranks the fixed default-priority
`While => #while` rule. Its match domain strictly exceeds any submitted
justification domain and its final step changes `<k>`, `<env>`, `<scopes>`,
`<scopeLoc>`, `<stack>`, and `<ret>`. This is the only material static
soundness failure found, and it is reached by every intended input with length
at least two.
