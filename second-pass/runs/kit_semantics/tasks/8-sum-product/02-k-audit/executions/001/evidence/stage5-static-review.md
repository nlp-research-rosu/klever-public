# Stage 5 static rule review

This reviewer-authored record is keyed to `stage5-rule-inventory.log`, whose
TSV section enumerates all 949 source declarations, rules, contexts,
configuration declarations, and claims with file/line locations and complete
normalized statements.

## Supplied-semantics inventory decision

The fixed supplied tree contributes 928 inventoried entries: 227 syntax
declarations, 695 rules, five evaluation contexts, and one configuration. It
contains all 45 priority rules in the assembled theory, 145 function
declarations, 107 `total` declarations, and 25 symbol/opaque declarations.
Every entry is byte-identical to the launcher-mounted trusted
`/reference/reference-semantics` tree. Therefore each of these entries follows
the selected `SUPPLIED_SEMANTICS` level by definition; none is a
candidate-authored proof extension. The full per-entry decision is
`ACCEPTED AS FIXED SELECTED SEMANTICS`, not a claim that unused MiniPy behavior
is a complete model of CPython.

No fixed-semantics declaration contains `sum_product`, `sumFrom`,
`productFrom`, `allInts`, or `projectIntTotal`. The only occurrences of
`projectIntTotal` under the trusted tree are explanatory comments in
`sort.k`, not declarations or rules. Thus the baseline does not encode this
task's answer.

The fixed opaque/symbol declarations are:

- `md5hexCodes`
- `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`
- `floorFI`, `toF`, `ceilF`
- `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`
- `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
  `sqrtF`
- `sortVS`, `sortKeyVS`

None is reachable from the submitted integer-list program or its entry claim.
The program uses only the fixed algebraic list, integer, scope, call, loop,
assignment, and tuple legs reviewed below.

## Material constructor and rule map

| Program construct | Declaration and execution rules | Static decision |
|---|---|---|
| `Module`, statement sequencing | `syntax.k:61`; `core.k:124-127` | `#loadAll` exposes every submitted statement in order; no statement is skipped. |
| `ImportFrom("typing",...)` | `syntax.k:43`; `controls.k:35-36` | The supplied semantics intentionally treats non-`math` typing imports as a no-op. This is semantically inert because the import is typing-only. |
| `FuncDef`, `Params`, closure binding | `syntax.k:53,57`; `functions.k:14-16` | The exact body is stored in a `closureVal` in module scope 0. |
| `Call`, callee/argument evaluation | `syntax.k:28`; `call.k:20-21,69-75`; `core.k:183-191` | Name lookup selects the stored closure, arguments evaluate left-to-right, and a new frame is allocated with the exact body and continuation. |
| `Name` lookup | `syntax.k:12`; `core.k:129-154` | Reads follow the current scope/parent chain; the entry theorem pins the selected binding. |
| `Int(0)`, `Int(1)` | `syntax.k:9`; `core.k:193-196` | Literal values are exact mathematical K `Int`s. |
| `Assign` | `syntax.k:41` strict RHS; `controls.k:9-18` | Writes `total` and `product` into the active plain frame. The cell-specific priority rule is inapplicable because the frame has no `$cells`. |
| `For`, loop protocol | `syntax.k:45`; `controls.k:62-74`; `list.k:8-10`; `tuple.k:30-41` | Iterable evaluation happens once; every head binds `number`, both body statements execute, and recursion uses the exact tail. Empty and cons cases are disjoint. |
| Heap-ref versus bare read-only list | `core.k:25-34,62-70`; `controls.k:104-108` | Bare `list(VS)` is an explicitly legal claim input. A fixed-semantics universal connection claim proves that `For(...,ref(H),...)` with `H |-> list(VS)` rewrites to the same bare-list loop state. |
| `AugAssign` `+` then `*` | `syntax.k:44` strict operand; `controls.k:20-31`; fixed equations `int.k:9,14` | The active map is updated in source order. The proof-local guarded twins have the same right-hand sides as these fixed equations. |
| `Return` and frame pop | `syntax.k:50`; `functions.k:77-90` | The tuple value becomes `retV`, the exact saved continuation/environment is restored, and the temporary frame is deallocated. |
| `TupleExpr` | `syntax.k:21`; `tuple.k:13-16`; shared argument loop `core.k:183-191` | `total` then `product` evaluate left-to-right into the exact returned tuple. |

The configuration cells are `k`, `env`, `scopes`, `scopeLoc`, `heap`,
`heapLoc`, `stack`, `ret`, `exc`, and `exit-code` (`core.k:49-60`). The entry
claim pins all ten. The loop claim mentions the exact four-key local frame,
preserves `numbers`, and changes only `number`, `total`, and `product` plus
`k`; omitted cells are framed and preserved. Fixed loop execution does not
allocate, print, mutate the input, alter the call stack, or raise for integer
arithmetic.

## Candidate proof-local entries: exhaustive decisions

The candidate contributes exactly 21 entries: five syntax declarations,
14 rules, and two claims. There are no proof-local priority rules, no
proof-local `<k>` operational rewrite rules, and no claim in
`verification.k`.

| Inventory IDs | Extension | Class and complete domain | Overlap/coverage/descent decision | Dependents and decision |
|---|---|---|---|---|
| 929 | `allInts : ValSeq -> Bool [function,total]` | Definitional predicate over every finite `ValSeq`. | Empty/cons constructors are disjoint and exhaustive; cons recursion strictly decreases the sequence. | Both claims. Sound and exactly characterizes lists whose elements inhabit semantic `Int`. |
| 930 | `allInts(.ValSeq) => true` | Empty predicate equation. | Unique empty case. | Sound. |
| 931 | `allInts(vCons(V,VS)) => isInt(V) andBool allInts(VS)` | Cons predicate equation. | Unique cons case; strictly descends. | Sound. |
| 932-933 | `definedProjectInt : Val -> Bool [function,total]`; equation to `isInt` | Definitional alias on all semantic values. | One equation covers the complete domain. | Projection lemmas. Sound. |
| 934 | `projectIntTotal : Val -> Int [function,total,symbol,no-evaluators]` | Guarded totalization of the partial `Val`-to-`Int` sort projection. | It is intentionally unspecified for non-`Int` values. Every result-bearing use in both claims is dominated by `allInts`, and recursion preserves that fact. | Summaries and dispatch twins. Acceptable on the exact intended domain; off-domain values are excluded, not treated as Python results. |
| 935 | `#Ceil({V:Val}:>Int)` characterization | Derived sort-refinement lemma for every `Val`. | Definedness is exactly `definedProjectInt(V)=true`, i.e. `isInt(V)`; `#Ceil(V)` preserves term definedness. | Projection orientation. Sound. |
| 936 | `projectIntTotal(V) => {V}:>Int` when `definedProjectInt(V)` | Derived guarded projection equation. | On its complete guard, `V` is an `Int`; right side is its unique subsort projection. The concrete/simplification priority controls orientation. | All arithmetic summaries. Sound. |
| 937 | `{V}:>Int => projectIntTotal(V)` under the same guard | Reverse symbolic orientation of the same equality. | Overlap with IDs 936/938 agrees on the same `Int`. `symbolic(V)` and simplification attributes prevent an execution rewrite loop. | Symbolic sort refinement. Sound. |
| 938 | `projectIntTotal(I:Int) => I` | Definitional identity over every `Int`. | Where it overlaps ID 936, the cast also equals `I`. | All intended uses. Sound and fixes ground results; the opposite value `2 => 3` is rejected. |
| 939 | Projection idempotence | Ordinary mathematical equality because the inner result has sort `Int`. | Where ID 938 also applies, both normalize to `projectIntTotal(V)`. | Simplification only. Sound. |
| 940 | Guarded `applyBin("+",V,W)` twin | Derived fixed-semantics dispatch lemma on `isInt(V) andBool isInt(W)`. | Fixed `MPY-INT` gives `I +Int J`; guarded projections give the same `I,J`. Overlap with the fixed statically sorted rule agrees. No float/bool/string case satisfies both guards as semantic `Int`. | Loop invariant/entry. Sound; the bridge-free baseline connection claim closes. |
| 941 | Guarded `applyBin("*",V,W)` twin | Same classification for multiplication. | Fixed `MPY-INT` gives `I *Int J`; same overlap argument. | Loop invariant/entry. Sound; the bridge-free baseline connection claim closes. |
| 942-944 | `sumFrom` declaration, empty rule, cons rule | Definitional left fold over every finite sequence; on intended uses every projection is defined. | Empty/cons disjoint and exhaustive; cons strictly decreases the tail. | Invariant and entry postcondition. Sound; does not rewrite program execution. |
| 945-947 | `productFrom` declaration, empty rule, cons rule | Definitional left fold with identity 1. | Same coverage/descent decision. | Invariant and entry postcondition. Sound; does not rewrite program execution. |
| 948 | `loop-invariant` reachability claim | Auxiliary circularity for the exact submitted loop body, any finite integer suffix, any integer accumulators, and the exact four-key plain local frame. | Empty branch reaches unchanged accumulators; cons branch binds the real head, executes `+=` then `*=`, and recurs on the strict tail before reusing the claim. The existential final `number` only forgets an unobservable local. | Entry claim. Sound/productive and independently closes as `#Top`. |
| 949 | `sum-product` entry claim | Target theorem over every finite `ValSeq` satisfying `allInts`. | Pins all configuration cells, exact module/binding/body, and exact tuple result. `VS` occurs on both input and deterministic fold result; no result variable is fresh or unconstrained. | Target. Sound and result-constraining if the extensions above are sound. |

## Operational and value sensitivity

There is no candidate-authored rule that rewrites a `<k>` program term, pops a
frame, changes a continuation, or bypasses `#loadAll`, call, loop, or return.
Accordingly there is no candidate operational bridge with a broader
continuation domain to validate.

The two guarded `applyBin` equations are proof-side derived lemmas over fixed
semantic functions. A separate definition importing only `MPY` proves the
fixed `Int` addition and multiplication equations and the universal
heap-ref-to-bare-list `For` dereference connection. Ground helper claims fix
projection outcomes `2` and `-3` and folds `-1` and `-6`; the opposite
projection interpretation is stuck at `2`. The executed-body mutation changes
the actual loaded body and closure from product identity 1 to 2 and is stuck
at returned `(0,2)` against `(0,1)`.

No inventoried rule supplies a false conclusion witness on the intended
integer-list domain. No rule encodes the final answer independently of the
submitted body, introduces a fresh result oracle on that domain, or silently
models a used construct by fabrication.
