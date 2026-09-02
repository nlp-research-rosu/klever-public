# Used-construct map

The submitted `solution.mpy` contains exactly two `FuncDef` statements and uses
the following source constructors. Constructor identity with the proof macros is
checked mechanically in `stage4-constructor-compare.log`.

| Submitted construct | Declaration | Fixed-semantics execution rules |
|---|---|---|
| `Module`, statement list | `semantics/syntax.k:56-61` | `semantics/core.k:124-127` loads and sequences the module |
| `FuncDef`, `Params`, `ParamNames` | `semantics/syntax.k:53-60` | `semantics/functions.k:14-16` installs the exact closure body and defining scope |
| `Name` | `semantics/syntax.k:12` | `semantics/core.k:130-154` performs environment lookup |
| `Int` | `semantics/syntax.k:9` | `semantics/core.k:193-196` produces the integer value |
| `If` | `semantics/syntax.k:49` | strictness plus `semantics/controls.k:51-54` evaluates truth and chooses a branch |
| `Compare`, `CmpOp` (`>=`, `!=`) | `semantics/syntax.k:30-32` | `semantics/operators.k:14-17` evaluates operands and dispatches; `semantics/int.k:22-27` gives integer comparison; `semantics/operators.k:34-42` dereferences heap objects for structural comparison |
| `Subscript` | `semantics/syntax.k:22,38-39` | `semantics/subscript.k:27-41` evaluates object/index, dereferences lists, normalizes negative indices, and selects the element |
| `BinOp` (`+`, `-`) | `semantics/syntax.k:15` | `semantics/operators.k:12` dispatches and `semantics/int.k:9-13` performs integer arithmetic |
| `Call` | `semantics/syntax.k:28` | `semantics/call.k:18-21` evaluates callee then arguments left-to-right through `semantics/core.k:183-191` |
| `len` | name lookup through builtins scope at `semantics/core.k:156-181` | builtin dispatch at `semantics/call.k:31-50`; `semantics/builtins.k:20-26` computes list length via `vsLen` (`semantics/core.k:223-225`) |
| user-function application | `closureVal` at `semantics/core.k:31` | `semantics/call.k:69-74` allocates/binds a frame; `semantics/functions.k:63-66,78-90` binds, returns, restores control/state, and pops |
| `Return` | `semantics/syntax.k:50` | strictness plus `semantics/functions.k:77-90` implements abrupt return and frame restoration |

All material fixed-semantics rules in this map are bypassed after the candidate
proof reaches `#applyK`: `verification.k:73-86` rewrites the two exact closures
directly to the proof-local `#targetCall` machine.

The exhaustive inventory in `static-rule-inventory.md` covers all 26 reviewed K
source files: 695 supplied-semantics rules and 16 proof-local rules, plus every
syntax declaration, context, configuration, import, priority, total/function
attribute, macro, and claim. The supplied semantics contains 22 explicit
`no-evaluators` opaque symbols (the MD5 digest, float operations/conversions,
`sortVS`, and `sortKeyVS`). None is reachable from this submitted program.
