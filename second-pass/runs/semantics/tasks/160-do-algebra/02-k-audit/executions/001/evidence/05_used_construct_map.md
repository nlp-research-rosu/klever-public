# Used-construct map

This is the manually reviewed reachable slice for `solution.mpy`. Exact full
declaration and rule bodies remain in `05_rule_inventory.{json,txt}`.

| Program construct | Declaration | Rules/control path used |
|---|---|---|
| `Module`, statement sequencing | `semantics/syntax.k:61`, `Stmts` at `:56` | `semantics/core.k:124-127` loads the exact module and sequences statements. |
| `FuncDef`, `Params` | `semantics/syntax.k:53,57` | `semantics/functions.k:14-16` binds closures in module scope. |
| `Name` | `semantics/syntax.k:12` | `semantics/core.k:130-155` performs lexical lookup, including the builtins parent scope. |
| `Int` | `semantics/syntax.k:9` | `semantics/core.k:194` yields the integer value. |
| `Str` | `semantics/syntax.k:13` | `semantics/str.k:13-17` converts the five ASCII operator tokens to code sequences. |
| `Assign` | `semantics/syntax.k:41` (`strict(2)`) | `semantics/controls.k:9-11` evaluates the RHS then writes the active scope. The closure-cell priority rule is unreachable here. |
| `AugAssign` | `semantics/syntax.k:44` (`strict(3)`) | `semantics/controls.k:20-24`, then integer `applyBin` rules in `semantics/int.k:9-17`. |
| `If` | `semantics/syntax.k:49` (`strict(1)`) | `semantics/controls.k:51-55` evaluates `truthy` and selects exactly one branch. |
| `While` | `semantics/syntax.k:46` | `semantics/controls.k:77-84` reevaluates the guard, executes the body, and reinstalls the loop. |
| `Compare`, `CmpOp` | `semantics/syntax.k:30,32` | Evaluation contexts and dispatch at `semantics/operators.k:15-17`; integer comparisons at `semantics/int.k:22-27`; string equality at `semantics/str.k:24-27`. |
| `BinOp` | `semantics/syntax.k:15` (`seqstrict(2,3)`) | Left-to-right evaluation then dispatch at `semantics/operators.k:12`; arithmetic cases at `semantics/int.k:9-20`, including Python floor quotient for nonzero divisors and nonnegative exponents. |
| `Subscript` | `semantics/syntax.k:22` | Object then index contexts at `semantics/subscript.k:27-35`; bare read-only list indexing uses `applyIndex`, `normIdx`, and `valSeqAt` at `:7-18,37-41`. |
| `Call`, argument lists | `semantics/syntax.k:28,37` | Callee then left-to-right arguments at `semantics/call.k:19-21` and `semantics/core.k:184-191`; closure entry/frame handling at `semantics/call.k:69-76`; binding at `semantics/functions.k:63-75`. |
| `len(operator)` | ordinary `Call` | Builtin binding comes from `builtinsScope` at `semantics/core.k:157-181`; call dispatch at `semantics/call.k:31`; length at `semantics/builtins.k:17-26` and `vsLen` at `semantics/core.k:224-226`. |
| `Return` | `semantics/syntax.k:50` (`strict`) | `semantics/functions.k:78-89` stores the exact value, pops one frame, restores the caller continuation/environment, and consumes the call. |
| Bare claim inputs `list(OPS)`/`list(NDS)` | value constructors in `semantics/core.k:14-32` | They are read-only and never allocated or mutated by the submitted program; lookup/subscript/len operate structurally. |

No float, sorting, dictionary, set, tuple, comprehension, method, range,
assertion, import, slice, heap-list mutation, closure-cell, or opaque-symbol
rule is reachable from the submitted program on any of the ten claim inputs.
