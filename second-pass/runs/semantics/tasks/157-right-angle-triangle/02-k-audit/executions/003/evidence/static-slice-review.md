# Static target-slice review

The exhaustive row-by-row inventory is `rule-inventory.md`: 934 declarations
from all 25 imported/source files (230 syntax declarations, one configuration,
five contexts, and 698 rules). Every row has an `ACCEPTED_MATERIAL` or
`ACCEPTED_NONMATERIAL` decision. The latter declarations have rule heads
separated from this target by constructor, value sort, operator literal, or an
unreachable helper continuation. They remain part of the fixed supplied
semantics trust boundary, but none can produce a false conclusion for the
target term.

## Exact target construct map

| Submitted construct | Declaration | Operational path |
|---|---|---|
| `Module` / statement sequence | `syntax.k:61`, `core.k:124-127` | `#loadAll(Module(SS))` executes statements left-to-right. |
| `FuncDef`, `Params`, body | `syntax.k:53,57,60`, `functions.k:14-16` | Installs `closureVal(PNS,BODY,L)` in the current scope. |
| Direct proof call | `verification.k:47-50` | Rewrites only the audit adapter to `Call` with the exact closure. |
| `Call` and arguments | `syntax.k:28`, `call.k:19-21`, `core.k:185-191` | Callee first, then positional arguments left-to-right. |
| Closure invocation | `call.k:69-74` | Allocates a callee scope, pushes the complete continuation and caller environment, then binds parameters and executes the body. |
| Parameter binding | `functions.k:63-66` | Binds `a`, `b`, and `c` in order in the fresh plain frame. |
| `Name` | `syntax.k:12`, `core.k:130-154` | Looks up the callee frame first and follows its parent only on a miss. |
| `Int` / `Bool` | `syntax.k:9-12`, `core.k:194-195` | Produces K unbounded `Int` and `Bool` values. |
| `BinOp("*",...)`, `BinOp("+",...)` | `syntax.k:15`, `operators.k:12`, `int.k:9,14` | `seqstrict(2,3)` evaluates left then right; typed dispatch gives exact K integer addition/multiplication. |
| `Compare("<=",...)`, `Compare("==",...)` | `syntax.k:30,32`, `operators.k:15-17`, `int.k:23,26` | Contexts evaluate left then right; typed dispatch gives exact integer comparison. |
| `If` | `syntax.k:49`, `controls.k:51-54`, `core.k:199-200` | The strict guard evaluates first; Boolean truth selects exactly one branch. |
| `Return` | `syntax.k:50`, `functions.k:78-90` | Evaluates its value, sets `retV`, discards the remaining function body, pops the exact saved frame, and restores caller state. |

## Configuration and control

Each claim starts with module environment `0`, an empty module scope whose
parent is the fixed builtins scope, scope allocator `1`, empty heap and stack,
`noRet`, `NoExc`, and exit code `0`. Closure invocation allocates scope `1`,
pushes `frame(CONT,0,1)`, binds three integer arguments, and performs no heap
allocation or external effect. `Return` restores environment `0`, deletes scope
`1`, restores `scopeLoc=1`, empties the stack, clears `ret`, and yields the
Boolean to the saved continuation. Exception and exit cells are untouched.

The direct-closure adapter omits only module loading/name lookup. Fixed
`FuncDef` semantics creates `closureVal(("a","b","c"),BODY,0)`; the proof-local
closure equation creates that identical value. The submitted body and the
proof RHS parse to byte-identical KORE after replacing rule-language `.Stmts`
with the external program parser's omitted empty `Stmts` production
(`stage4-constructor-comparison.log`). Thus the adapter pins the same binding
and body and does not summarize, oracle-call, return early, or alter any cell.

## Overlap, priority, and equation checks

- `verification.k` contains three declarations and three unconditional rules:
  two nullary definitional equations and one adapter-to-`Call` rewrite. It has
  no `total`, `functional`, `simplification`, `concrete`, `priority`, `owise`,
  or opaque/symbol attribute.
- The two proof-local functions each have one exhaustive nullary equation.
  Their right-hand sides are ground constructor terms, so there is no overlap,
  recursion, guard, or totalization gap.
- `Call`'s fixed `[owise]` route is the only matching call route for a
  `closureVal`. Builtin, method, annotated-closure, heap-reference, and
  proof-local interception heads do not overlap it.
- The higher-priority cell-lookup and cell-parameter rules require a
  `"$cells"` entry. The fresh target frame is `scope(.Map,parent(0))`, so those
  rules are provably inapplicable; the plain lookup/binding rules are selected.
- Heap-reference priority rules cannot match because all operands are integers
  or Booleans and the heap remains empty.
- The generic comparison `[owise]` rule feeds `applyCmp`. For target operands,
  the `Int` equations for literal operators `<=` and `==` are unique. Float,
  Bool, collection, membership, and `None` cases are sort/literal-disjoint.
- Integer `+` and `*` equations are unique for `Int,Int`. Python integers and K
  integers are both unbounded, so there is no overflow discrepancy.
- `appendVal` is the only material `[total]` helper besides the nullary
  `builtinsScope`: its empty/nonempty list equations are disjoint, exhaustive,
  and structurally descending.
- There are no `simplification` or `functional` declarations anywhere in the
  imported theory. The 25 `symbol(...)` declarations (float operations,
  `sortVS`/`sortKeyVS`, and `md5hexCodes`) and all 35 `[concrete]` equations are
  unreachable from the integer-only target proof. `MPY-CONCRETE` is not
  imported by the proof module.

## Static conclusion

No task-answer oracle, unconstrained result, smuggled postcondition, operational
shortcut, fabricated used construct, or false target-domain rule was found.
The only proof-local abstraction expands to the exact submitted constructor
body and then executes the fixed call/control semantics. No inventoried rule
has a concrete or symbolic witness that enables a false theorem conclusion on
the target's integer states.
