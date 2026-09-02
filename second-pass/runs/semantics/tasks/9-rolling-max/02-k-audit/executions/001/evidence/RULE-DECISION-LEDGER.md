# Rule-by-rule decision ledger

This ledger is keyed to `K-RULE-INVENTORY.md`. That inventory contains every
top-level `configuration`, `context`, `syntax`, `rule`, and `claim` start in all
24 supplied-semantics source files plus `verification.k` and `spec.k`.

Inventory totals are 957 entries: 713 rules, 236 syntax declarations, five
contexts, one configuration, and two claims. Of these, 928 entries come from
the byte-identical supplied semantics (695 rules, 227 syntax declarations, five
contexts, one configuration), 27 entries come from `verification.k` (18 rules
and nine syntax declarations), and two are the claims in `spec.k`.

## Decision classes for the supplied-semantics complement

The complete supplied tree is the selected, trusted semantics for this audit,
not a candidate-generated proof extension. Every supplied row in
`K-RULE-INVENTORY.md` has one of the following decisions:

- `ACTIVE/REVIEWED`: listed in the used-path table below. Its guards, cells,
  evaluation order, overlaps, and state transition were inspected against the
  concrete program path.
- `INACTIVE/DISJOINT`: every other supplied row. Its top symbol, AST
  constructor, receiver constructor, builtin/method string, or value sort
  cannot match any term on the submitted program's proof path. It therefore
  cannot contribute to either positive claim. This is a rule-by-rule decision
  by set complement against the exhaustive source-located inventory, not a
  claim that unused subset semantics has been validated against full Python.
- `CONCRETE-ONLY`: all rows in `semantics/concrete.k`. `MPY-CONCRETE` is
  imported by `MPY-KRUN` for the LLVM checks but is not imported by
  `VERIFICATION`, which imports `MPY`. These rows cannot close the symbolic
  claims.

No supplied rule outside the active set has a unifiable top symbol and matching
constructor/string guard at an active redex. In particular, the specialized
`Call` rules for math/hash operations do not match `rolling_max`, `max`, or
`append`; other `applyBuiltin` and `applyMethod` equations use disjoint names or
receiver sorts; and other iterator rules use disjoint iterable constructors.

## Used syntax and active supplied rules

| Submitted construct / state effect | Declaration and active supplied rules | Decision |
|---|---|---|
| `Module`, statement sequence | `syntax.k:41,56,61`; `core.k:124-127` | Sound: module load exposes the exact statement list and sequences it left-to-right. |
| `ImportFrom("typing","List")` | `syntax.k:43`; `controls.k:35-44` | Sound on this program: the non-`math` import is a no-op and has no runtime binding used by the function. |
| `FuncDef`, closure installation | `syntax.k:53,57,60`; `functions.k:14-16` | Sound: installs the submitted body and one parameter in module scope 0. |
| Function call and frame | `call.k:19-21,69-74`; `functions.k:63-66,78-90` | Sound: callee and arguments evaluate in order; a fresh local frame is pushed, parameters bind, return sets `retV`, and pop restores the caller while retaining the allocated result. |
| `Expr(Str(...))` docstring | `syntax.k:13,52`; `str.k:13-17`; `controls.k:46-48` | Sound for the submitted ASCII docstring: constructs a string value then discards it without state change. |
| `ListExpr()` and allocation | `syntax.k:17`; `list.k:13-15`; `core.k:117-121,183-191,217-219` | Sound: the empty list is allocated at fresh heap location 0, producing `ref(0)`. |
| `Int`, `Bool`, `Name` | `syntax.k:9-13`; `core.k:130-154,193-196` | Sound on the pinned scopes: literals cool to their values and lookup follows the local/module/builtin chain. |
| Local assignment | `syntax.k:41`; `controls.k:8-18` | Sound: RHS is strict and the ordinary local frame update applies; cell-specific priority rule guards are false for this unannotated function. |
| `For` and loop protocol | `syntax.k:45`; `controls.k:62-74,104-108`; `tuple.k:31-40`; `iter.k:8`; `list.k:9-10` | Sound for concrete lists. The symbolic `intsVS` consumer is separately reviewed as a local bridge below. Target binding updates `number`; each iteration preserves its continuation. |
| `If` | `syntax.k:49`; `controls.k:50-54`; `core.k:199-205` | Sound: `first` is a Boolean, so the guards are exhaustive and disjoint. |
| `max(maximum, number)` | `syntax.k:28`; `call.k:20-21,31-32`; `core.k:156-181,183-191`; `builtins.k:17,97-100` | Sound on two integer arguments: lookup selects builtin `max`, argument order is left-to-right, and `maxVals` returns `maxInt`. Other builtin routes are disjoint. |
| `result.append(maximum)` | `syntax.k:28-29`; `call.k:15-24,52-67`; `list.k:18-20,52-55` | Sound: attribute cooling produces a bound method, `append` is classified as mutating, the receiver reference is preserved, and exactly one value is appended in place. |
| `Return(result)` | `syntax.k:50`; `functions.k:77-90` | Sound: the reference is returned, the suffix is discarded as Python return requires, the local frame is removed, and heap allocation survives. |
| Configuration and state | `core.k:25-60` | Sound for the claim: all observable cells are present; entry starts in the declared initial configuration and ends with empty stack, `noRet`, `NoExc`, and exit code 0. |

All supplied function equations reached above have constructor-complete cases
on the used sorts. The K builtins for mathematical integers, Booleans, maps,
lists, strings, and `maxInt` remain part of the ordinary K trust boundary.

The supplied proof definition contains 25 explicitly symbolic/opaque operations:
`absF`, `addF`, `ceilF`, `decStrToF`, `divF`, `divFloatIntV`, `divII`, `eqF`,
`floatLt`, `floatMod`, `floorFI`, `gtF`, `intFloatDiv`, `intToF`,
`md5hexCodes`, `mulF`, `powF`, `roundF`, `roundFN`, `sortKeyVS`, `sortVS`,
`sqrtF`, `subF`, `toF`, and `truncF`. None occurs in the submitted AST,
candidate helpers, claims, residuals, or active rule chain. No opaque value can
influence control or result here.

The candidate proof imports no `[simplification]` or `[functional]` rule.
The supplied inventory also contains no such active rule on this path.

## Exhaustive `verification.k` decisions

| Inventory entry | Class and complete-domain decision | Evidence |
|---|---|---|
| `syntax Stmts ::= rollingMaxLoopBody [macro]`; rule at 10 | Definitional macro; exact submitted loop body. No state is abstracted. | Full expanded-module KORE byte identity and body-sensitivity failure. |
| `syntax Stmts ::= rollingMaxBody [macro]`; rule at 20 | Definitional macro; exact submitted function body and order. | Full expanded-module KORE byte identity. |
| `syntax Module ::= rollingMaxModule [macro]`; rule at 30 | Definitional macro; exact submitted module, import, function name, parameter, and body. | `stage4-expanded-module-identity.log`. |
| `syntax ValSeq ::= intsVS(IntSeq)` | Fresh structural input embedding. It admits only `.IntSeq` and `iCons(Int,IntSeq)` inputs at the source sort. The submitted declaration is not `[function]`; that omission is an evidence/derivation gap, not a false equation witness. | Ordinary bridge-free attempt gets stuck; independent total-function connection theory closes. |
| `intsVS(.IntSeq) => .ValSeq` | Truthful base equation for the embedding. | Constructor case; no overlap with cons equation. |
| `intsVS(iCons(I,R)) => vCons(I,intsVS(R))` | Truthful structurally descending cons equation. | Constructor case; preserves head and tail exactly. |
| Empty `#iterNext(list(intsVS(.IntSeq)))` bridge, priority 40 | Operational bridge. Reads only `<k>`, writes only the leading computation, preserves arbitrary continuation and every framed cell. Result exactly matches evaluating the base embedding then supplied empty-list iterator. | Bridge-free total-function theorem `empty-iterator-connection` closes. |
| Cons `#iterNext(list(intsVS(iCons(I,R))))` bridge, priority 40 | Operational bridge. Same footprint; yields exactly head `I` and the embedded tail, with arbitrary continuation preserved. Empty/cons guards are disjoint. | Bridge-free total-function theorem `cons-iterator-connection` and observable suffix witness close. |
| `syntax Int ::= nextRolling(Bool,Int,Int) [function,total]`; true equation | Definitional mathematical summary. Boolean constructor case returns the first input value; exhaustive with false case. | Ground witness and positive proof. |
| `nextRolling(false,M,I) => maxInt(M,I)` | Definitional mathematical summary. Returns the maximum after a non-first element. Disjoint from true case. | K integer `maxInt`; body mutant exposes mismatch. |
| `syntax ValSeq ::= rollingAcc(...) [function,total]`; empty equation | Definitional result summary. Empty sequence returns the existing accumulator. | Constructor-complete base case. |
| `rollingAcc(iCons(...))` equation | Definitional result summary. Recurses strictly on `R`, updates maximum once, and appends the same updated maximum once. Disjoint from empty case. | Explicit `[3,1,4] -> [3,3,4]`; false `[3,3,5]` mutation rejected. |
| `syntax Bool ::= firstAfter(...) [function,total]`; three equations at 65-67 | Definitional local-state summary. Coverage is complete. Overlaps are benign: `firstAfter(.IntSeq,false)` and `firstAfter(iCons(...),false)` have identical `false` RHS in their overlapping equations. | Ground loop witness ends with `false`. |
| `syntax Int ::= maximumAfter(...) [function,total]`; equations at 70-72 | Definitional local-state summary. Empty/cons cases are disjoint; recursion strictly consumes `R` and uses `nextRolling`. | Ground loop witness ends with 4. |
| `syntax Int ::= numberAfter(...) [function,total]`; equations at 75-76 | Definitional local-state summary. Empty/cons cases are disjoint; cons recursion strictly consumes `R` and retains the last element. | Ground loop witness ends with 4. |

There are no local opaque symbols, simplification rules, `functional`
declarations, unguarded oracles, or program-term-to-summary shortcuts. The only
local priority rules are the two iterator bridges just reviewed.

## Claim decisions

| Claim | Decision |
|---|---|
| `rolling-max-loop` | Satisfiable and control-faithful. It starts at the real `#loop` head, permits an arbitrary continuation, updates exactly the four loop-carried locals and result heap object, and preserves all other state. `numbers` and the closure binding are framed because the body does not read or modify them. |
| `rolling-max-correct` | Satisfiable and result-constraining. It loads the byte-identical submitted module, calls its `rolling_max` closure on an arbitrary finite integer sequence, requires return `ref(0)`, fixes the entire result list to `rollingAcc`, fixes allocation and module scope, and requires clean control/exception cells. |

The explicit ground state in `spec-ground-witness.k` instantiates every variable
and structural precondition needed by both claims. Both ground claims close.
The result mutation in `spec-vacuity.k` builds, reaches the return state, and
gets stuck with actual heap list `[3,3,4]` instead of false `[3,3,5]`.
