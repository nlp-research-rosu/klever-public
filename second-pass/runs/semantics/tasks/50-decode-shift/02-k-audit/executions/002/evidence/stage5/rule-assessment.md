# Static rule assessment index

The complete source-level declaration blocks are in `rule-inventory.log`:
708 rules, 235 syntax declarations, 5 contexts, 1 configuration, and 3 claims.
`attributes-and-priorities.txt` separately lists every `total`, opaque
`no-evaluators`, and priority occurrence. This index assigns every block in
that inventory to a reviewed class.

## Supplied semantics

| Source | Rules | Assessment |
|---|---:|---|
| `semantics.k` | 0 | Assembly only; proof module imports `MPY`, runtime imports `MPY-KRUN`. |
| `syntax.k` | 0 | All 16 syntax groups reviewed; strictness gives the used RHS and left-to-right binary evaluation. |
| `core.k` | 46 | Used lookup, sequencing, literal, builtin-scope, argument-evaluation, and sequence-helper rules are faithful on the pinned cells. Other heap/cell/collection helpers are fixed-semantics, unused by the theorem. |
| `iter.k` | 0 | Iterator protocol declarations only. |
| `str.k` | 28 | Used literal, string iteration, concatenation, and sequence rules are faithful for ASCII lowercase input and ASCII literals. Other comparison/membership rules are unused. |
| `controls.k` | 34 | Used assignment, aug-assignment, expression, for-loop, and loop rules preserve the pinned scope and continuation. Remaining branches/import/while/control rules are unused. |
| `functions.k` | 15 | Used closure creation, parameter binding, return, and frame-pop rules match the exact call state. Annotated-closure rules are unused. |
| `call.k` | 21 | Used callee lookup, left-to-right argument evaluation, builtin dispatch, and ordinary closure dispatch match the actual term. Heap/method and annotated-closure cases are unused. |
| `operators.k` | 10 | Used binary dispatch is faithful; reference/deref and comparisons are unused. |
| `int.k` | 16 | Used integer `-`, `+`, `%`, and `pyMod` equations are ordinary integer mathematics with nonzero divisor 26. Other operators are unused. |
| `builtins.k` | 137 | Used `ord` and `chr` rules are exact on one-character lowercase ASCII strings and outputs 97–122. All folds, conversions, eval, md5, and other builtins are unused. |
| `tuple.k` | 21 | Used `#bindTgt(Name,Val)` is the ordinary current-frame update. Tuple construction/unpacking/indexing is unused. |
| `assert.k` | 3 | Runtime smoke-test only; no rule is in the proof definition's target path. |
| `bool.k` | 13 | Unused by the target execution except K's guard evaluation; no BoolOp source construct occurs. |
| `comprehension.k` | 7 | The target `decode_shift` has no comprehension; all rules are unused. (`encode_shift` is not the target binding.) |
| `concrete.k` | 16 | Runtime-only `MPY-KRUN`; none contributes to symbolic closure. |
| `dict.k` | 28 | Unused. |
| `float.k` | 121 | Unused. All 22 float `no-evaluators` symbols are therefore outside the dependency cone. |
| `list.k` | 27 | Unused by target `decode_shift`; the accumulator is a `str`, not a list. |
| `methods.k` | 75 | Unused by target `decode_shift`. |
| `range.k` | 6 | Unused. |
| `set.k` | 12 | Unused. |
| `sort.k` | 19 | Unused. Opaque `sortVS` and `sortKeyVS` cannot influence the theorem. |
| `subscript.k` | 40 | Unused. Its deliberately total out-of-bounds abstraction cannot influence the theorem. |

The supplied semantics is an intentionally partial Python model. Globally
excluded behavior (Unicode string literals, non-ASCII `chr`, unsupported
exceptions/imports, escaping closures, invalid indexes, and unused opaque
float/sort/md5 operations) is not reached from this program under
`lowerCodes`. No supplied-semantics rule in the target dependency cone admits
a false result for that domain.

## Candidate-local verification rules

| Lines | Extension | Class and assessment |
|---|---|---|
| 7–8 | `decodeChar` | Truthful total mathematical definition. |
| 11–16 | `decodeAcc`, `decodeCodes` | Truthful, constructor-complete, structurally descending sequence folds. |
| 18–21 | `loopLast` | Truthful, constructor-complete, structurally descending fold. |
| 23–24 | `encodeChar` | Truthful total mathematical definition. |
| 26–29 | `lowerCodes` | Truthful, constructor-complete lowercase predicate. |
| 32–61 | `decodeStep`, `decodeBody`, `decodeClosure` | Syntax macros. KORE comparison in Stage 4 proves exact identity with the regenerated target closure. |
| 69–102 | `decode-loop-lemma` | Operational bridge. **Unsound over its declared match domain.** The bridge permits arbitrary `BUILTINS:Scope`, while the bridge-free connection claim fixes `builtinsScope`. On input code 97 and `scope(.Map,root)`, it fabricates result code 118; fixed execution is stuck at `#look("chr",-1)`. See `bad-bridge-extended.log` and `bad-bridge-base.log`. |

There are no candidate-local `functional`, `simplification`, `concrete`,
`symbol`, or `no-evaluators` declarations. All six candidate-local `total`
function groups have disjoint constructor equations or a single unconditional
equation, complete coverage for their declared algebraic arguments, and
structural descent where recursive.
