# Stage 5 static rule review

## Exhaustive inventory scope and disposition

`stage5-rule-inventory.log` inventories every source-level `configuration`,
`syntax`, `context`, `rule`, and `claim` item in the 24 supplied K files,
`verification.k`, and `spec.k`: 938 items total (701 rules, 229 syntax
declarations, five contexts, one configuration, and two claims). The inventory
records normalized text and exact source location for every item.

The 928 items in `reference-semantics/` are byte-identical to the supplied
trusted tree. Each receives one of these dispositions:

1. Rules and declarations named in the used-path map below are materially
   reachable and were checked for evaluation order, binding, control, cell
   effects, and value behavior.
2. The remaining fixed-semantics items are unreachable from the submitted AST.
   They cannot contribute to either claim's closure and are accepted only as
   the selected supplied-semantics baseline, not as candidate proof
   extensions. This includes every float, sort, MD5, list, tuple, set, dict,
   comprehension, subscript, range, iteration, method, and assertion rule not
   named below. Their presence is not evidence for the theorem, and none
   encodes this task's answer.
3. All eight items in `verification.k` are reviewed individually below.
4. The two `spec.k` claims are reviewed as reachability claims, not semantic
   rules.

The inventory contains 22 supplied `[no-evaluators]` opaque symbols and 45
supplied priority rules (one priority 39, 41 priority 40, and three priority
45). None of the opaque symbols is reachable. The only relevant priority/fall-
through behavior is that cell-reference and heap-reference priority rules have
false guards because this program creates neither cells nor heap objects, while
the generic `[owise]` `Call` route therefore handles `str(i)`. There is no
candidate priority rule or candidate operational bridge.

## Used constructor and rule map

| Submitted construct / effect | Declaration and fixed rules | Review |
|---|---|---|
| `Module` and statement lists | `semantics/syntax.k:56-61`; `semantics/core.k:124-127` | `#loadAll` exposes the exact module statements; list sequencing is left-to-right and consumes `.Stmts`. |
| `FuncDef("string_sequence", Params("n"), BODY)` | `syntax.k:53,57,60`; `functions.k:14-16` | Installs a closure containing the exact body and defining environment 0. No helper substitutes the body. |
| Function call and frame creation | `call.k:20-21,69-74`; `core.k:185-191`; `functions.k:63-66,78-90` | Callee is evaluated first, arguments left-to-right, parameter `n` is bound in fresh scope 1, the body executes, `Return` discards only the remaining callee body, and `#pop` restores every caller/control cell pinned by the entry claim. |
| Name/builtin binding | `core.k:130-181` | Local lookup precedes parent/builtin lookup. `str` resolves to `typeV("str")` in the fixed builtins scope; the task adds no interception. Cell-deref priority rules are inapplicable because no `"$cells"` binding exists. |
| Literals and docstring expression | `syntax.k:9-13,52`; `core.k:194-196`; `str.k:13-17`; `controls.k:48` | Integer and ASCII string literals evaluate directly. The ASCII-only string rule covers every source literal. The docstring is evaluated and discarded without state effects. |
| `if n < 0` | `syntax.k:30,32,49`; `operators.k:15-17`; `int.k:22`; `controls.k:51-54`; `core.k:199-205` | Left and right operands are evaluated before integer `<`; the Boolean result is truthy and selects exactly one branch. |
| Assignments | `syntax.k:41`; strictness-generated RHS evaluation; `controls.k:9-18` | RHS precedes the local scope update. Cell-write priority is inapplicable. Only `result` and `i` change. |
| `while i <= n` | `syntax.k:46`; `controls.k:65-82,85`; `operators.k:15-17`; `int.k:23` | `While` enters the recurring `#while`; each guard is reevaluated, true runs the body then returns to the loop label, and false consumes the loop. There is no `break`, `continue`, exception, or abrupt proof-local rewrite. |
| String concatenation | `syntax.k:15`; `operators.k:12`; `str.k:20-26` | `seqstrict(2,3)` evaluates left then right. `applyBin("+",str,str)` uses the ordinary recursive `seqConcat`, preserving character order. |
| `str(i)` | `syntax.k:28`; `call.k:20-21,32`; `core.k:185-191`; `builtins.k:147-149` | The normal call route evaluates the `str` binding and `i`; the type call renders an integer through fixed K `Int2String` and `strToCodes`. No candidate abstraction supplies the result. |
| `i + 1` | `syntax.k:15`; `operators.k:12`; `int.k:9` | Exact mathematical integer addition; Python and K integers are unbounded on this domain. |
| Negative and normal returns | `syntax.k:50`; `functions.k:78-90` | Negative input returns empty before later assignments. Nonnegative input returns `result`. The entry postcondition fixes the returned value and normal cleanup cells. |

## Candidate proof-extension inventory

| Location | Class and complete domain | Soundness decision |
|---|---|---|
| `verification.k:8` `sequenceAcc(IntSeq,Int,Int) [function,total]` | Definitional summary over all three argument sorts. | Acceptable. Totality asserts definedness but does not choose an arbitrary value. The guarded equations/fold below constrain every use in the proof. |
| `verification.k:10-12` concrete base | Definition when `I > N`: result is `ACC`. | True and terminating; exactly the loop's false-guard case. |
| `verification.k:14-22` concrete step | Definition when `I <= N`: append space plus decimal `I`, increment `I`, recurse. | True on its full guard. It is the source loop body and counter update. Guard is disjoint from and exhaustive with the base guard. |
| `verification.k:26-28` symbolic base simplification | Same equation and guard as the concrete base. | True; overlap has the identical RHS. |
| `verification.k:30-38` symbolic fold simplification | Rewrites `sequenceAcc(updated(ACC,I),I+1,N)` back to `sequenceAcc(ACC,I,N)` when `I <= N`. | True equality: it is exactly the reverse direction of the guarded defining step. At overlap with the base at `I=N`, both paths equal `updated(ACC,I)`. It changes no operational cell and never matches a program AST or control term. |
| `verification.k:42` `stringSequenceCodes(Int) [function,total]` | Definitional final-result summary over all integers. | Acceptable; the next two disjoint/exhaustive rules fix its value. |
| `verification.k:44-45` negative result | `N < 0` maps to `.IntSeq`. | Matches both implementations' empty `range(n+1)` behavior. |
| `verification.k:47-49` nonnegative result | `N >= 0` starts with code 48 (`"0"`) and folds from 1 through `N`. | Exactly the requested inclusive sequence and the source's initialization/loop. |

There are no candidate opaque symbols, priority rules, ordinary operational
rules, calls/returns, heap/state rewrites, or rules that match source AST.
Accordingly there is no displaced fixed-semantics execution, result-bearing
oracle, fabricated effect, or task-answer operational shortcut.

## Overlap, totality, and descent

- `I > N` and `I <= N`, and `N < 0` and `N >= 0`, are each pairwise disjoint
  and exhaustive over K `Int`.
- Concrete `sequenceAcc` recursion increases `I` by one under `I <= N`; the
  natural measure `N-I+1` decreases until the base guard.
- The symbolic fold is used in the opposite direction solely as a valid
  equation for invariant closure. Its only overlap with the duplicate base
  yields equal values.
- `seqConcat` and `strToCodes(Int2String(I))` are fixed-semantics/K
  operations, not candidate functions.
- `[total]` contributes definedness but no free postcondition value. Ground
  actual-program and loop witnesses at `n=5` independently reduce to the
  literal ASCII codes for `"0 1 2 3 4 5"`.

## Claim review

- `SPEC.loop-invariant` has satisfiable precondition `I >= 1 ∧ N >= 0`; for
  example `ACC="0", I=1, N=5`. It starts at the real recurring `#while`,
  fixes the exact local bindings and function closure, permits only the
  irrelevant final `i` to be existential, and constrains `result` to
  `sequenceAcc(ACC,I,N)`. All omitted cells and the continuation are framed;
  the loop touches only the two local variables and performs no abrupt effect.
- `SPEC.string-sequence` has no `requires` clause and therefore covers every K
  integer. It loads the actual constructor-identical program, invokes the
  selected closure, constrains the returned `str`, and fixes the environment,
  scope/heap allocators, stack, return, exception, and exit-code cells.
- The entry claim depends on the loop claim as a circularity. The loop claim
  closes alone; the entry plus helper close together. Selecting the entry
  while deliberately excluding its helper gets stuck at the first iteration,
  which confirms (rather than hides) this explicit dependency.
