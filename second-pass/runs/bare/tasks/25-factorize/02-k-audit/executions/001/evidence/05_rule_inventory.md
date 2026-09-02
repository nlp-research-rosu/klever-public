# Auditor rule and declaration inventory

This inventory was reconstructed from the source files, not from either
candidate `*-kompiled` directory. Line numbers refer to `/candidate`.

## Attribute and extension census

- Imported built-ins: `INT`, `BOOL`, `STRING`, `MAP`, and `LIST`.
- Local `[function]` productions: `Machine`, `collect`, `bind`,
  `bindLists`, `evalBinOp`, `evalCompare`, `SolutionModule`,
  `SolutionFunctions`, `SolutionMachine`, `collectStmts`, `FactorFrom`,
  `FactorizeSpec`, `PrependFactor`, `Product`, `OrderedFrom`,
  `MachineValue`, `HasDivisor`, `IsPrime`, `AllPrime`, and
  `ValidFactorization`.
- Local `[total]`, `[functional]`, `[simplification]`, `[concrete]`,
  `[owise]`, priority, macro, alias, or opaque declarations: none.
- Local claims outside `spec.k`: none.
- Helper K files imported by `semantic.k` or `verification.k`: none.

## Local syntax declarations

| ID | Location | Declaration/productions | Review |
|---|---|---|---|
| SS01 | semantic.k:6 | `Module ::= Module(Stmts)` | Exact translated module wrapper. |
| SS02 | semantic.k:8 | `Stmts ::= List{Stmt,""}` | Matches adjacency in translated statement lists. |
| SS03 | semantic.k:9-12 | `Stmt ::= ImportFrom \| FuncDef \| If \| Return` | Exactly the statement forms used. |
| SS04 | semantic.k:14 | `Params ::= Params(Strings)` | Used by both definitions. |
| SS05 | semantic.k:15 | comma-separated `Strings` | Used for imports and parameters. |
| SS06 | semantic.k:17 | comma-separated `Exprs` | Used for calls and list displays. |
| SS07 | semantic.k:18-23 | `Expr ::= Int \| Name \| BinOp \| Compare \| ListExpr \| Call` | Exactly the expression forms used. |
| SS08 | semantic.k:25 | comma-separated `CmpOps` | Submitted comparisons have one element. |
| SS09 | semantic.k:26 | `CmpOp(String,Expr)` | Used for `<`, `>`, and `==`. |
| SS10 | semantic.k:37-39 | `Val ::= IntVal \| BoolVal \| ListVal` | Sufficient runtime values. |
| SS11 | semantic.k:41 | `Closure(Params,Stmts)` | Function body and formal parameters; no closure environment is needed by this program. |
| SS12 | semantic.k:43 | `Frame(K,Map)` | Saves caller continuation and local environment. |
| SS13 | semantic.k:45-46 | `Result ::= noResult \| Val` | Harness result state. |
| SS14 | semantic.k:53-54 | `Machine(...) [function] \| Halted(...)` | The partial deterministic transition machine is evaluated as a K function. |
| SS15 | semantic.k:55 | `ProofState ::= Run(MachineState)` | Wrapper used only by proof claims. |
| SS16 | semantic.k:68-81 | `KItem ::= Invoke \| Exec \| Eval \| BinLeft \| BinRight \| CompareLeft \| CompareRight \| MakeList \| CallOne \| CallTwoLeft \| CallTwoRight \| Choose \| DoReturn \| Finish` | Explicit evaluation/control continuations. |
| SS17 | semantic.k:168 | `collect(Stmts) [function]` | Module-to-function-map helper. |
| SS18 | semantic.k:174 | `bind(Params,List) [function]` | Call binding helper. |
| SS19 | semantic.k:177 | `bindLists(Strings,List) [function]` | Pairwise binding helper. |
| SS20 | semantic.k:182 | `evalBinOp(String,Val,Val) [function]` | Arithmetic/list primitive dispatcher. |
| SS21 | semantic.k:191 | `evalCompare(String,Val,Val) [function]` | Integer comparison dispatcher. |
| VS01 | verification.k:8 | `SolutionModule() [function]` | Hard-coded copy of the submitted constructor term; does not read `solution.mpy`. |
| VS02 | verification.k:33 | `SolutionFunctions() [function]` | Function-map constant derived from VS01. |
| VS03 | verification.k:36 | `SolutionMachine(Int) [function]` | Direct internal-machine proof entry. |
| VS04 | verification.k:41 | `collectStmts(Module) [function]` | Removes the `Module` wrapper. |
| VS05 | verification.k:51 | `FactorFrom(Int,Int) [function]` | Trial-division summary; unused by all 26 submitted claims. |
| VS06 | verification.k:65 | `FactorizeSpec(Int) [function]` | Starts VS05 at divisor 2; unused by all submitted claims. |
| VS07 | verification.k:68 | `PrependFactor(Int,Val) [function]` | VS05 list helper; unused by submitted claims. |
| VS08 | verification.k:73 | `Product(Val) [function]` | Used by contract claims. |
| VS09 | verification.k:80 | `OrderedFrom(Val,Int) [function]` | Used by contract claims. |
| VS10 | verification.k:85 | `MachineValue(MachineState) [function]` | Extracts a value only after the machine halts. |
| VS11 | verification.k:88 | `HasDivisor(Int,Int) [function]` | Used by primality checks. |
| VS12 | verification.k:96 | `IsPrime(Int) [function]` | Used by contract claims. |
| VS13 | verification.k:99 | `AllPrime(Val) [function]` | Used by contract claims. |
| VS14 | verification.k:104 | `ValidFactorization(Int,Val) [function]` | Product/order/primality conjunction. |
| VS15 | verification.k:110 | `Observation ::= Observe(Bool)` | Non-function wrapper for contract reachability claims. |

## Configuration and used-construct coverage

The configuration at semantic.k:48-51 has `<k>` for the parsed module,
`<input>` for the integer harness argument, and `<result>` for the returned
value. The actual runtime environment, function map, call stack, and pending
computation are fields of `Machine`.

| Submitted construct | Declaration | Operational coverage |
|---|---|---|
| `Module` entry | SS01 | SR01 collects functions and invokes `factorize`; SR02 exports the halted value. |
| `ImportFrom("typing","List")` | SS03 | SR28 intentionally ignores this annotation-only import. |
| `FuncDef`, `Params`, statement sequence | SS02-SS05 | SR27-SR32 collect closures and bind exact-arity calls; SR04-SR06 execute bodies. |
| `If` | SS03 | SR06-SR08 evaluate the guard then select one branch. |
| `Return` | SS03 | SR05 and SR09 evaluate the expression, discard the current function suffix, pop the caller frame, and restore its locals. |
| `Int`, `Name` | SS07 | SR11-SR12. |
| `ListExpr()` and `ListExpr(E)` | SS07 | SR13-SR15; no multi-element literal is used. |
| `BinOp("*","%","//","+")` | SS07 | SR16-SR18 establish left-to-right order; SR33-SR37 supply exactly the used integer and list operations. |
| `Compare("<",">","==")` with one comparator | SS07-SS09 | SR19-SR21 establish left-to-right order; SR38-SR40 supply the used comparisons. |
| One- and two-argument calls with `Name` callees | SS06-SS07 | SR22-SR26 evaluate arguments left-to-right and SR03 invokes the selected closure. |

## `semantic.k` rule decisions

| ID | Location | Rule | Decision |
|---|---|---|---|
| SR01 | 57-60 | module/harness initialization | Sound task harness: passes `<input>` to the named entry and derives the function map from the parsed module. |
| SR02 | 62-63 | halted machine to `<result>` | Sound final-value export. |
| SR03 | 83-87 | `Invoke` | Sound on exact-arity submitted calls: selected closure, new locals, saved continuation/environment, and pushed stack frame agree with the program. |
| SR04 | 89-90 | empty `Exec` | Sound fall-through. |
| SR05 | 91-92 | `Return` scheduling | Sound; expression evaluation precedes abrupt return. |
| SR06 | 93-96 | `If` scheduling | Sound; guard precedes branch and remaining statements. |
| SR07 | 98-101 | true `Choose` | Sound; guard is `B`. |
| SR08 | 102-105 | false `Choose` | Sound; complementary `notBool B` guard. |
| SR09 | 107-109 | `DoReturn` | Sound for submitted calls: discards the callee suffix, pops one frame, and restores caller locals and continuation. |
| SR10 | 111-112 | `Finish` | Sound on reachable entry executions, where the outer frame has just been popped and the stack is empty. It is syntactically broader (it would also halt with a nonempty stack), but no such state is reachable from SR01 for this program; treated as a narrowness gap, not an unsoundness finding. |
| SR11 | 114-115 | integer literal | Sound. |
| SR12 | 116-118 | local name lookup | Sound for present bindings; missing names visibly stick. |
| SR13 | 120-121 | empty list literal | Sound. |
| SR14 | 122-123 | singleton list evaluation | Sound and sufficient for submitted literals. |
| SR15 | 124-125 | singleton list construction | Sound. |
| SR16 | 127-130 | start binary operator | Sound left-before-right sequencing. |
| SR17 | 131-134 | binary left value | Sound right-operand sequencing. |
| SR18 | 135-137 | dispatch binary result | Sound; retains all machine state. |
| SR19 | 139-142 | start comparison | Sound left-before-right sequencing for the one-comparator subset. |
| SR20 | 143-146 | comparison left value | Sound. |
| SR21 | 147-149 | dispatch comparison result | Sound. |
| SR22 | 151-152 | start one-argument call | Sound for `Name` callees. |
| SR23 | 153-154 | invoke one-argument call | Sound after argument evaluation. |
| SR24 | 155-158 | start two-argument call | Sound first-argument-first sequencing. |
| SR25 | 159-162 | evaluate second argument | Sound. |
| SR26 | 163-166 | invoke two-argument call | Sound and preserves argument order. |
| SR27 | 169 | collect empty module suffix | Sound. |
| SR28 | 170 | ignore import | Sound for the submitted `typing.List` import, which has no runtime use after translation. |
| SR29 | 171-172 | collect function definition | Sound for the submitted unique function names. For duplicate names it would let an earlier definition override a later one, unlike Python; duplicate definitions are absent, so this is an unused-language limitation rather than a false conclusion about the submitted program. |
| SR30 | 175 | unwrap parameters | Sound. |
| SR31 | 178 | empty exact binding | Sound. |
| SR32 | 179-180 | cons binding | Sound; mismatched arity remains partial/stuck and all submitted calls have exact arity. |
| SR33 | 183 | integer addition | Sound via built-in unbounded integer addition. |
| SR34 | 184 | integer multiplication | Sound via built-in unbounded integer multiplication. |
| SR35 | 185 | list concatenation | Sound for Python list `+` over the submitted lists. |
| SR36 | 186-187 | integer remainder | Sound on reachable positive operands; zero is guarded. Negative Python remainder conventions are outside reachable submitted execution. |
| SR37 | 188-189 | integer division | Sound on reachable positive operands; zero is guarded. Python recursion/stack limits are not modeled. |
| SR38 | 192 | integer `<` | Sound. |
| SR39 | 193 | integer `>` | Sound. |
| SR40 | 194 | integer `==` | Sound. |

Machine-root rules are deterministic on the submitted states. Their leading
continuation shapes are disjoint except SR07/SR08, whose boolean guards are
complementary. Literal/call arities and primitive operator/type cases are also
disjoint. Partial cases visibly stick; no production is declared `[total]`.

## `verification.k` rule decisions

| ID | Location | Rule | Decision |
|---|---|---|---|
| VR01 | 9-31 | `SolutionModule` equation | Its current constructor tree matches the submitted `solution.mpy`, but it is an independently hard-coded substitute and has no file-sensitive connection claim. This is the material pinning defect demonstrated in `04_body_sensitivity.log`. |
| VR02 | 34 | `SolutionFunctions` | Truthful derivation from VR01, but inherits VR01's lack of file sensitivity. |
| VR03 | 37-39 | `SolutionMachine` | Truthful direct machine entry for VR02; bypasses the actual `<k> Module(...)` file entry and inherits VR01's pinning defect. |
| VR04 | 42 | `collectStmts` | Sound wrapper elimination. |
| VR05 | 52-53 | `FactorFrom`, `N<2` | Truthful for the conventional `1 -> []` case and for the helper's definition; values below 1 are outside the factorization contract. |
| VR06 | 54-55 | `FactorFrom`, `D^2>N` | Requires an unstated trial invariant if interpreted as a valid-factorization summary. Witness: `N=6,D=3` yields `[6]`, and `ValidFactorization(6,[6])` is false because 6 is composite. The machine-checked witness is `05_factorfrom_witness.log`. This helper is unused by every submitted claim, so it does not cause their closure. |
| VR07 | 56-59 | divisible `FactorFrom` step | Mathematically correct only under the same unstated invariant (in particular, that candidates below `D` have been eliminated); unused by submitted claims. |
| VR08 | 60-63 | non-divisible `FactorFrom` step | Correct trial-candidate advance under its explicit guards; unused by submitted claims. |
| VR09 | 66 | `FactorizeSpec(N)=FactorFrom(N,2)` | Correct starting point for positive mathematical trial division, but unused by submitted claims. |
| VR10 | 69-70 | prepend factor | Sound list construction; unused by submitted claims. |
| VR11 | 74 | empty product | Sound (`1`). |
| VR12 | 75-76 | product cons | Sound on integer-valued lists used by claims. |
| VR13 | 81 | empty ordered list | Sound. |
| VR14 | 82-83 | ordered cons | Sound nondecreasing-order recursion. |
| VR15 | 86 | machine value from `Halted` | Sound and partial; it forces ground machine evaluation before extraction. |
| VR16 | 89-90 | divisor search exhausted | Sound for “has a divisor at or after D”; used from D=2. |
| VR17 | 91-92 | divisor found | Sound; reachable D is nonzero. |
| VR18 | 93-94 | advance divisor search | Sound and descending toward the `D^2>N` base in uses from D=2. |
| VR19 | 97 | primality | Sound mathematical definition for integers using divisor search from 2. |
| VR20 | 100 | all-prime empty list | Sound. |
| VR21 | 101-102 | all-prime cons | Sound on integer-valued lists. |
| VR22 | 105-108 | valid factorization | Sound conjunction of product equality, nondecreasing order from 2, and primality. |

The VR05-VR10 trial-division summary is dead proof code: no submitted claim
mentions `FactorFrom`, `FactorizeSpec`, or `PrependFactor`, and no connection
rule relates it to `SolutionMachine`. The ground claims instead evaluate the
machine and then, for 13 inputs, evaluate VR11-VR22.

