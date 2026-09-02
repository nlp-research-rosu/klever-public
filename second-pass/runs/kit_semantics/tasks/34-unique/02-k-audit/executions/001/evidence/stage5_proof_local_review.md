# Stage 5 proof-local static review

The immutable supplied semantics are exhaustively enumerated together with
`verification.k` in `stage5_rule_inventory.tsv`. This record gives each
configuration, context, syntax declaration, and rule a stable ID, source line,
attributes, and complete whitespace-normalized text. There are no generated
semantic helper files and no candidate modification to the supplied tree.

The proof-relevant fixed-semantics path is:

| Program construct | Declaration | Operational path and state effect |
|---|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k:53,57,61` | `core.k:124-127` loads/sequences; `functions.k:14-16` binds the exact closure in module scope 0. |
| `Call(Name("unique"), ref(0))` | `syntax.k:12,28` | `core.k:131-154` performs LEGB lookup; `call.k:20-21,69-74` evaluates the callee/argument left-to-right, allocates frame 1, binds `l`, and pushes the exact continuation. |
| docstring `Expr(Str(...))` | `syntax.k:13,52` | `str.k:13-17` constructs the ASCII string; `controls.k:46-48` discards it without state change. |
| `Assign(result, ListExpr())` | `syntax.k:17,41` | `list.k:13-15` evaluates the empty literal and allocates heap 1; `controls.k:9-11` binds `result`. |
| `Assign(x, NoneVal)` | `syntax.k:27,41` | `core.k:193-196` produces `noneV`; `controls.k:9-11` binds `x`. |
| `For(x, l, ...)` | `syntax.k:45` | `controls.k:62-74,104-108`, `iter.k:8`, `list.k:9-10`, and `tuple.k:31-34` dereference the input once, iterate left-to-right, bind target `x`, and retain the loop continuation. |
| `If(x not in result)` | `syntax.k:30,32,49` | `core.k:131-154` resolves names; `operators.k:14-17,38-42`; `list.k:57-67` dereferences the result list and folds membership with structural `==K`; `controls.k:50-54` selects the branch. |
| `result.append(x)` | `syntax.k:28-29,52` | `call.k:16,20-24,52-60` preserves the mutating receiver reference; `list.k:52-55` appends exactly one value in heap 1; `controls.k:46-48` discards `noneV`. |
| `Return(sorted(result))` | `syntax.k:28,50` | `call.k:20-21,38-41` dereferences the argument; `sort.k:18-24,32-56` uses supplied `sortVS` and allocates heap 2; `functions.k:77-90` records the value, pops frame 1, restores env 0, and returns `ref(2)`. |
| Configuration/cells | `core.k:44-60` | The entry claim fixes the real initial environment, builtins scope, fresh locations, empty stack, `noRet`, and `NoExc`; omitted `<exit-code>` remains framed at 0. |

## Candidate proof-local inventory and dispositions

| Lines | Extension | Class and complete-domain review | Disposition |
|---|---|---|---|
| 7 | `memberVS(Val, ValSeq) [function,total]` | Result-bearing definitional summary. The result is fixed by the bridge-free `MEMBER-SPEC` theorem over every `Val`, finite `ValSeq`, and K continuation. | Sound. |
| 8 | empty membership equation | Empty and cons patterns are disjoint. It agrees with fixed `#iterDone ~> #memberCont`. | Sound. |
| 9-11 | unequal-head membership equation, simplification | Guard `notBool (V ==K E)` is complementary to the equal rule; recursion strictly descends on the tail. Symmetry of K equality makes `V ==K E` agree with fixed `E ==K V`. | Sound. |
| 12-14 | equal-head membership equation, simplification | Guard `V ==K E` is complementary; returns the fixed membership result immediately. | Sound. |
| 17 | `appendUnique(ValSeq,Val) [function,total]` | Pure definitional summary; it does not rewrite a source term. | Sound. |
| 18-19 | present-value `appendUnique` equation | Guard is exactly the fixed membership theorem's true result and preserves the accumulator. | Sound. |
| 20-22 | absent-value `appendUnique` equation | Complementary guard; uses supplied `valSeqConcat` to append one value. | Sound. |
| 25 | `dedupFromVS(ValSeq,ValSeq) [function,total]` | Pure first-seen fold used in the invariant and postcondition. | Sound. |
| 26 | empty dedup equation | Returns the accumulator and is disjoint from the cons case. | Sound. |
| 27-28 | cons dedup equation | Strictly descends on the source tail and applies the already reviewed `appendUnique`. | Sound. |
| 31 | `lastFromVS(ValSeq,Val) [function,total]` | Pure summary of the observable loop-target binding. | Sound. |
| 32 | empty last-value equation | Preserves the pre-loop binding, matching zero iterations. | Sound. |
| 33 | cons last-value equation | Strictly descends and retains the last head, matching `#bindTgt` on every iteration. | Sound. |
| 41-43 | membership operational bridge, priority 40 | Complete match domain is `<k> #memberAcc(V,list(VS)) ~> CONT </k>` with all cells framed. `MEMBER-SPEC` proves the identical domain and result under `VERIFICATION-BASE`, which does not import this bridge. Fixed membership reads/writes no other cell. | Sound and non-circular. |
| 52-75 | exact loop operational bridge, priority 40 | Match fixes the generated body, env 1, exact local bindings/parent, result heap location, arbitrary `VS`, `ACC`, `X`, continuation, other scopes, heap entries, and omitted cells. `LOOP-SPEC` proves this exact transition under `VERIFICATION-MEMBER`, without the loop bridge. It changes only `x` and heap 1 and introduces no return/pop/allocation/exception effect. | Sound and context-contained. |

`memberVS`, `appendUnique`, `dedupFromVS`, and `lastFromVS` have exhaustive
constructor coverage, disjoint or agreeing guards, and structural descent. No
proof-local declaration is opaque, `[functional]`, `[owise]`, `[concrete]`, or
an unconstrained fresh value. The only proof-local priorities are the two
operational bridges above, and the only simplification attributes are the two
guarded membership cons equations.

## Supplied trust and representation findings

- `sortVS(ValSeq)` (`sort.k:18`) is the supplied result-bearing trusted
  primitive. Symbolic execution leaves it opaque; concrete rules implement
  homogeneous integers, strings, and mixed numeric values. The K proof
  establishes that real source execution returns exactly
  `sortVS(dedupFromVS(INPUT,.ValSeq))`; it does not independently establish the
  ascending-order contract of `sortVS`.
- Symbolic `#memberAcc` (`list.k:61-66`) uses structural `==K`. The supplied
  concrete-only module overrides it with `numOrKEq` (`concrete.k:90-99`) so
  CPython's `True == 1 == 1.0` identification is reproduced by `krun`, but that
  override is intentionally absent from Haskell proof definitions. Thus the
  symbolic theorem maps `[True,1]` to two unique model values, while CPython and
  freshly compiled LLVM execution map it to `[True]`.
- ASCII string encoding and unsupported Python object comparison/exception
  behavior are fixed supplied-model boundaries. They do not arise from a
  candidate rule and do not narrow the theorem, whose `INPUT:ValSeq` is
  unbounded and unconstrained.

No reviewed rule can enable a false conclusion about the selected supplied
model. The only divergence witness is model-versus-CPython numeric
identification above; it is not program-versus-docstring behavior.

Every inventory row has an explicit disposition. Candidate-local rows are
`REVIEWED_SOUND_PROOF_LOCAL`. The supplied `sortVS` declaration, symbolic
membership fold, and concrete equality override are separately tagged as the
documented trust/model boundaries. All remaining supplied rows are tagged
`ACCEPTED_FIXED_SUPPLIED_RULE_OR_DECLARATION`: rules on the mapped execution
path were checked against the complete configuration and source behavior;
rules outside that path do not match a constructor or continuation reachable
from this program and contribute no simplification or bridge to claim closure.
