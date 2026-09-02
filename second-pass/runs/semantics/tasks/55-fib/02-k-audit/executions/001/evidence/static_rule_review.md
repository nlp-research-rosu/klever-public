# Static rule review ledger

This reviewer-authored disposition accompanies `rule_inventory.txt`, whose
SHA-256 is `a72fa8aee4c471c926b50a99c08246198b1dd3aa79221abaef7a0e1f93c12b91`.
That machine-generated ledger enumerates all 232 `syntax` declarations, the
configuration, five contexts, 701 rules, and two claims in the 26 audited K
sources. The decisions below apply to every item in that inventory; exceptions
and limitations are called out explicitly.

Decision classes:

- `TARGET-SOUND`: reachable from the exact `solution.mpy` entry configuration
  for `N >= 0`, and checked against the Python behavior and the rule's complete
  target-path match domain.
- `PROOF-LOCAL-SOUND`: a candidate-added definition or claim that is
  mathematical/definitional and does not replace fixed execution.
- `INERT-FOR-TARGET`: no constructor at the head of the rule can occur in the
  exact target execution or in a result-bearing proof term.
- `OPAQUE-INERT`: a supplied-semantics opaque primitive whose symbol cannot
  occur on the target path.
- `SUBSET-LIMITATION-INERT`: a broader Python-fidelity or totality limitation
  with no reachable witness in this program on `N >= 0`. This is not labeled a
  target unsoundness.

## Per-source disposition

| Source | Rules | Disposition for every inventoried item |
|---|---:|---|
| `semantics.k` | 0 | Assembly/import declarations only. `MPY` is the proof module; `MPY-KRUN` additionally imports `MPY-CONCRETE`. |
| `semantics/syntax.k` | 0 | Grammar declarations are `TARGET-SOUND` for all constructors in `solution.mpy`; unused grammar is `INERT-FOR-TARGET`. |
| `semantics/core.k` | 46 | Module load/statement sequencing, ordinary name lookup, integer literals, builtins scope, argument evaluation, and the target configuration are `TARGET-SOUND`. Heap/cell/ref and unused truthiness paths are `INERT-FOR-TARGET`. |
| `semantics/iter.k` | 0 | Iterator protocol declarations used by range are `TARGET-SOUND`. |
| `semantics/range.k` | 6 | `inRange` and the two `#iterNext(rangeObj(...))` rules are `TARGET-SOUND` at step 1. `rangeLen` is `INERT-FOR-TARGET`. |
| `semantics/operators.k` | 10 | Generic `BinOp` dispatch is `TARGET-SOUND`; compare/unary/ref paths are `INERT-FOR-TARGET`. |
| `semantics/int.k` | 16 | Integer `+` is `TARGET-SOUND`; every other operator case is `INERT-FOR-TARGET`. |
| `semantics/str.k` | 28 | Ground ASCII docstring conversion and the resulting `str` value are `TARGET-SOUND`; other string operations are `INERT-FOR-TARGET`. |
| `semantics/tuple.k` | 21 | Tuple expression evaluation, pair unpacking, and ordinary-name target binding are `TARGET-SOUND`; all other paths are `INERT-FOR-TARGET`. |
| `semantics/controls.k` | 34 | Plain assignment, expression discard, and for-loop expansion/step/termination are `TARGET-SOUND`; other statements and ref/cell cases are `INERT-FOR-TARGET`. |
| `semantics/functions.k` | 15 | Module-level `FuncDef`, plain parameter binding, return, frame pop, and no-return fallthrough are `TARGET-SOUND`; closure-cell paths are `INERT-FOR-TARGET`. |
| `semantics/call.k` | 21 | Callee/argument evaluation, one-argument `range`, plain closure invocation, frame creation, and dispatch are `TARGET-SOUND`; method/ref/cell paths are `INERT-FOR-TARGET`. |
| `semantics/builtins.k` | 137 | The one-argument `range` rule is `TARGET-SOUND`. All other rules are `INERT-FOR-TARGET`; `md5hexCodes` is additionally `OPAQUE-INERT`. |
| `semantics/assert.k` | 3 | Used only in the reviewer LLVM smoke program; Boolean true assertions are `TARGET-SOUND`. It is not imported specially into the proof path beyond the fixed `MPY` semantics. |
| `semantics/bool.k` | 13 | `INERT-FOR-TARGET` in the proof. Boolean results are used only by reviewer assertions, where the ordinary truth rule is sound. |
| `semantics/comprehension.k` | 7 | `INERT-FOR-TARGET`. |
| `semantics/concrete.k` | 16 | `INERT-FOR-TARGET`; imported only by the LLVM `MPY-KRUN` module, not by the Haskell proof definition. |
| `semantics/dict.k` | 28 | `INERT-FOR-TARGET`. |
| `semantics/float.k` | 121 | `INERT-FOR-TARGET`; its 22 float-related symbolic primitives are `OPAQUE-INERT`. |
| `semantics/list.k` | 27 | `INERT-FOR-TARGET`; the submitted program creates tuples but no list. |
| `semantics/methods.k` | 75 | `INERT-FOR-TARGET`. |
| `semantics/set.k` | 12 | `INERT-FOR-TARGET`. |
| `semantics/sort.k` | 19 | `INERT-FOR-TARGET`; `sortVS` and `sortKeyVS` are `OPAQUE-INERT`. |
| `semantics/subscript.k` | 40 | `INERT-FOR-TARGET`. |
| `verification.k` | 6 | All five declarations and six equations are `PROOF-LOCAL-SOUND`; detailed decisions appear below. |
| `spec.k` | 0 | Both inventoried claims are sound reachability claims; detailed decisions appear below. |

## Used-construct closure

| Submitted constructor | Declaration | Rewriting path |
|---|---|---|
| `Module`, statement sequence | `syntax.k:56,61` | `core.k:124-127` |
| `FuncDef`, `Params` | `syntax.k:53,57,60` | `functions.k:14-16`; parameters `functions.k:63-66` |
| `Expr(Str(...))` | `syntax.k:13,52` | `str.k:13-17`; discard `controls.k:48` |
| `Assign(Name(...), Int(...))` | `syntax.k:9,12,41` | literal `core.k:194`; assignment `controls.k:9-11` |
| `Name` | `syntax.k:12` | lookup `core.k:131-154` |
| `Call(Name("range"), Name("n"))` | `syntax.k:28` | `call.k:20-21,31`; args `core.k:189-191`; builtin `builtins.k:177` |
| `For` | `syntax.k:45` | `controls.k:69-74`; protocol `range.k:20-24` |
| `TupleExpr` | `syntax.k:21` | expression `tuple.k:14-16`; assignment/unpack `tuple.k:50-57` |
| `BinOp("+",...)` | `syntax.k:15` | dispatch `operators.k:12`; value `int.k:9` |
| `Return` | `syntax.k:50` | `functions.k:78-90` |

The ordinary frame contains no `"$cells"` key, so the higher-priority cell
lookup/write alternatives are disjoint from the target. The call is neither a
math/MD5 interception nor a method, so the generic `[owise]` call route is the
correct route. Tuple RHS evaluation is left-to-right and completes before
`#unpackSeq` writes `a` then `b`, preserving Python's simultaneous assignment.
The range expression is evaluated once. The loop updates only the current scope;
the heap and allocation counter remain unchanged. Return restores environment,
stack, scope location, return state, and deletes the callee scope.

## Candidate-local equations and claims

- `fibBody`: exact expansion of the submitted translated body. No guard or
  alternative rule exists.
- `fibClosure`: exact fixed-semantics closure value for one parameter `n`, body
  `fibBody`, and definition environment 0.
- `fibProgram`: exact `Module(FuncDef(...))` wrapper. Expansion identity is
  machine-checked by `program_pinning_check.py`.
- `fibRun` base: for `I >= N`, `rangeObj(I,N,1)` is empty and the loop returns
  the current `A`.
- `fibRun` step: for `I < N`, fixed semantics yields `I`, writes `_`, computes
  the tuple `(B,A+B)` before unpacking, and continues at `I+1`; this is exactly
  `fibRun(B,A+B,I+1,N)`.
- The two `fibRun` guards are disjoint and exhaustive on K integers. The
  recursive measure `N-I` strictly decreases on its guarded recursive branch.
- `fibSpec(N) = fibRun(0,1,0,N)` is unconditional and total.
- `fib-loop` is an auxiliary execution theorem/circularity, not an operational
  rewrite. It preserves the continuation and every cell except `a`, `b`, and
  `_` in the active scope; `a` is constrained, while the other two are
  existential because the entry continuation does not observe them.
- `fib-all-natural` executes `#loadAll(fibProgram)` and the ordinary call path.
  It constrains the returned K value to `fibSpec(N)` under `N >= 0` and restores
  all observable cells to their expected post-call values.

There are no proof-local priority, simplification, concrete, functional, or
opaque declarations, and no operational bridge that preempts fixed execution.

## Opaque and totality boundaries

The 25 supplied-semantics `symbol(...)` declarations are listed exactly in
`18_static_attribute_audit.log`: 22 float/conversion symbols, two sort symbols,
and `md5hexCodes`. None is in the syntactic or semantic dependency closure
above. The target result depends only on K's integer arithmetic, maps/lists,
strings for the discarded docstring, and the fully defined `fibRun`/`fibSpec`.

Fresh compilation warned that `mapStrVS`, `floorFI`, `toF`, `ceilF`,
`joinCodes`, and `valSeqAt` are non-exhaustive despite `total` declarations.
Those are `SUBSET-LIMITATION-INERT`: this program never constructs a call to
any of them. Other documented subset limitations (ASCII-only string literals,
restricted imports/exceptions, no escaping plain nested closures, and opaque
sort/float/MD5 behavior) likewise have no reachable target witness. They are
therefore recorded as evidence limitations, not mislabeled as target
unsoundness.

## Body sensitivity

The reviewer changed both real-body occurrences from `a + b` to `a - b` while
leaving `fibRun` unchanged. The mutated definition compiled, but the helper
proof exited 1 with the expected residual
`fibRun(B,A-B,I+1,N) = fibRun(B,A+B,I+1,N)` under `I < N`. This shows the proof
is sensitive to the displaced body computation and is not closing through an
execution-bypassing rule.
