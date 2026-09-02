# Exhaustive local K declaration and rule inventory

Scope: the copied candidate sources
`/tmp/audit-work/candidate-src/semantic.k`,
`verification.k`, and `spec.k`. There are no other source helper K files.
Imported K standard-library declarations are outside this local inventory.

## Local syntax declarations

| ID | File:line | Declaration/production | Assessment |
|---|---|---|---|
| S01 | semantic.k:6 | `Program ::= Module(Stmts)` | Honest representation of the translated module. |
| S02 | semantic.k:8 | `Stmts ::= List{Stmt, ""}` | Honest juxtaposed statement-list representation. |
| S03 | semantic.k:9 | `Stmt ::= FuncDef(String, Params, Stmts)` | Covers the submitted function definition. |
| S04 | semantic.k:10 | `Stmt ::= Return(Expr)` | Covers all submitted returns. |
| S05 | semantic.k:11 | `Stmt ::= Assign(Expr, Expr)` | Unused by the submitted AST; harmless syntax. |
| S06 | semantic.k:12 | `Stmt ::= If(Expr, Stmts, Stmts)` | Covers both submitted `if` statements. |
| S07 | semantic.k:14 | `Params ::= Params(StringList)` | Covers `Params("l")`. |
| S08 | semantic.k:15 | `StringList ::= List{String, ","}` | Honest parameter-list representation. |
| S09 | semantic.k:17 | `Expr ::= Bool(Bool)` | Covers literal return values. |
| S10 | semantic.k:18 | `Expr ::= Int(Int)` | Covers the `0` index and `1` slice bound. |
| S11 | semantic.k:19 | `Expr ::= Name(String)` | Covers `l` and the recursive function name. |
| S12 | semantic.k:20 | `Expr ::= UnaryOp(String, Expr)` | Covers unary `not` and unary minus. |
| S13 | semantic.k:21 | `Expr ::= Compare(Expr, CmpOps)` | Covers membership comparison. |
| S14 | semantic.k:22 | `Expr ::= Subscript(Expr, Index)` | Covers `[0]` and `[1:]`. |
| S15 | semantic.k:23 | `Expr ::= Call(Expr, Exprs)` | Covers the one-argument recursive call. |
| S16 | semantic.k:25 | `Exprs ::= List{Expr, ","}` | Honest call-argument list. |
| S17 | semantic.k:26 | `CmpOps ::= List{CmpOp, ","}` | Honest comparison-operator list. |
| S18 | semantic.k:27 | `CmpOp ::= CmpOp(String, Expr)` | Covers `"in"` with its right operand. |
| S19 | semantic.k:28 | `Index ::= Expr` | Covers index `0`. |
| S20 | semantic.k:29 | `Index ::= Slice(Bound, Bound, Bound)` | Covers `[1:]`. |
| S21 | semantic.k:30 | `Bound ::= Expr` | Covers the lower bound `1`. |
| S22 | semantic.k:30 | `Bound ::= NoBound` | Covers omitted upper and step bounds. |
| S23 | semantic.k:40 | `ISeq ::= .ISeq [symbol(seqNil)]` | Empty integer-sequence constructor. |
| S24 | semantic.k:41 | `ISeq ::= Int :: ISeq [symbol(seqCons)]` | Nonempty integer-sequence constructor. |
| S25 | semantic.k:43 | `PyVal ::= pyInt(Int)` | Integer value constructor. |
| S26 | semantic.k:44 | `PyVal ::= pyBool(Bool)` | Boolean result constructor. |
| S27 | semantic.k:45 | `PyVal ::= pyList(ISeq)` | List value constructor. |
| S28 | semantic.k:46 | `PyVal ::= pyNone` | Fall-through value; unreachable in the submitted function. |
| S29 | semantic.k:48 | `KItem ::= run(Program, ISeq)` | Entry/re-entry control item. |
| S30 | semantic.k:49 | `KItem ::= functionEnd` | Fall-through marker; unreachable in the submitted function. |
| S31 | semantic.k:50 | `KItem ::= ifStmt(Bool, Stmts, Stmts)` | Internal branch-selection control item. |

There are no local precedence, associativity, strictness, or priority
declarations. Apart from the two named constructor symbols on `ISeq`, there are
no local `symbol` attributes.

## Local functions, totality, functional, and opaque declarations

| ID | File:line | Declaration | Coverage and assessment |
|---|---|---|---|
| F01 | semantic.k:52 | `eval(Expr, Map):PyVal [function]` | Partial by design; equations cover every expression reached in the submitted AST. |
| F02 | semantic.k:53 | `negVal(PyVal):PyVal [function]` | Covered for `pyInt`, its sole reachable argument. |
| F03 | semantic.k:54 | `atZero(PyVal):PyVal [function]` | Covered for a nonempty `pyList`; emptiness is guarded by the first source `if`. |
| F04 | semantic.k:55 | `tailVal(PyVal):PyVal [function]` | Covered for `pyList`, its sole reachable argument. |
| F05 | semantic.k:56 | `containsVal(PyVal,PyVal):PyVal [function]` | Covered for `(pyInt, pyList)`, the sole reachable pair. |
| F06 | semantic.k:57 | `truth(PyVal):Bool [function]` | Equations cover every `PyVal` except `pyNone`; only `pyBool` and `pyList` are reachable as conditions. |
| F07 | semantic.k:58 | `asList(PyVal):ISeq [function]` | Covered for `pyList`, its sole reachable argument. |
| F08 | semantic.k:60 | `isEmpty(ISeq):Bool [function,total]` | Two disjoint equations exhaust `.ISeq` and `Int :: ISeq`; genuinely total. |
| F09 | semantic.k:61 | `member(Int,ISeq):Bool [function,total]` | Two disjoint, descending equations exhaust `ISeq`; genuinely total. |
| F10 | semantic.k:62 | `hasZeroPair(ISeq):Bool [function,total]` | No equation is in `semantic.k`; fresh concrete compilation warns. In the proof theory, V02/V03 are disjoint, exhaustive, and descending, so the combined proof module is total. It is never used by concrete program execution. |
| F11 | semantic.k:63 | `first(ISeq):Int [function,total]` | The only equation is for `Int :: ISeq`; fresh concrete compilation warns on `.ISeq`. The `[total]` attribute is over-broad. Every submitted-program and proof use is dominated by nonemptiness, so no wrong result is enabled on a reachable submitted state. |
| F12 | semantic.k:64 | `rest(ISeq):ISeq [function,total]` | The only equation is for `Int :: ISeq`; fresh concrete compilation warns on `.ISeq`. The `[total]` attribute is over-broad. Every submitted-program and proof use is dominated by nonemptiness. |

There are no `functional` declarations distinct from the twelve `[function]`
symbols above, no `opaque` attributes, no fresh uninterpreted value used by the
program, and no local axioms other than the listed rules. `hasZeroPair` is not
an oracle: V02/V03 define it, and removing those equations produces the stuck
residual in `05-no-summary-kprove.log`.

## Configuration

`semantic.k:66-71` defines exactly:

- `<k>`: `run($PGM, $INPUT)`, the computation;
- `<program>`: the same `$PGM`, used to pin recursive calls to the loaded
  definition;
- `<env>`: `.Map`, used for the sole parameter binding.

All three cells are read by the submitted execution. There is no heap, output,
exception, allocation, or call-stack cell. The absence of an exception/call
stack is the source of the documented CPython recursion-depth limitation.

## Ordinary semantic rules

| ID | File:line | Rule effect | Reachability and rule assessment |
|---|---|---|---|
| R01 | semantic.k:74-76 | Enter a one-function, one-argument module; execute its body and bind the input list to its parameter. | Matches the submitted module exactly. The `<program>` cell remains the initially identical program. |
| R02 | semantic.k:79 | Turn a nonempty statement list into head `~>` tail. | Honest left-to-right statement sequencing. |
| R03 | semantic.k:80 | Reduce `.Stmts` to `.K`. | Honest empty-block behavior. |
| R04 | semantic.k:82-83 | Evaluate an assignment RHS and update the named environment entry. | Unused by the submitted AST; correct for the pure expression subset. |
| R05 | semantic.k:85-86 | Evaluate an `If` condition in the current environment and form `ifStmt`. | Used. Atomic evaluation is observationally faithful because all supported expressions are pure. |
| R06 | semantic.k:87 | Select the then branch when `B` is true. | Guard is disjoint from R07 and correct. |
| R07 | semantic.k:88 | Select the else branch when `notBool B` is true. | Guard is disjoint from R06 and exhaustive for `Bool`. |
| R08 | semantic.k:91-95 | For a tail-position call to the exact function stored in `<program>`, evaluate the list argument, clear locals, and re-enter; discard the current return continuation. | Binding and return-control handling are exact for this submitted tail-recursive body. It deliberately models unbounded tail re-entry, not CPython stack growth. Concrete witness: on 1,000 positive ones, K returns `false`, while the actual candidate raises `RecursionError` (`05-recursion-model-witness.log`, `02-python-differential.log`). This is a real-execution adequacy limitation, not a false Boolean result for a normally returning Python execution. |
| R09 | semantic.k:97-98 | Return a Boolean literal, discard the function continuation, and clear locals. | Exact for both literal returns in the submitted body. |
| R10 | semantic.k:99 | Turn fall-through `functionEnd` into `pyNone`. | Unreachable in the submitted function because all paths return. It leaves `<env>` unchanged, unlike Python frame destruction, so it is not a reusable model of arbitrary fall-through functions. No submitted-input false conclusion can use it. |
| R11 | semantic.k:101 | Evaluate `Bool(B)` to `pyBool(B)`. | Correct. |
| R12 | semantic.k:102 | Evaluate `Int(I)` to `pyInt(I)`. | Correct for mathematical/Python arbitrary-precision integers. |
| R13 | semantic.k:103 | Look up a name in the map. | Correct for the uniquely bound parameter; missing-name exceptions are outside the used subset. |
| R14 | semantic.k:104 | Evaluate unary `not` through truthiness. | Correct for the used list operand. |
| R15 | semantic.k:105 | Evaluate unary minus through `negVal`. | Correct for the used integer operand. |
| R16 | semantic.k:106 | Evaluate `[0]` through `atZero`. | Correct on nonempty lists; empty-index exception is unmodeled but the source guard prevents this rule from receiving an empty list. |
| R17 | semantic.k:107-108 | Evaluate `[1:]` through `tailVal`. | Correct. Returning the sequence tail rather than allocating a distinct Python list is unobservable because the program performs no mutation or identity test. |
| R18 | semantic.k:109-110 | Evaluate singleton `"in"` comparison through `containsVal`. | Correct for pure integer/list operands. |
| R19 | semantic.k:112 | `negVal(pyInt(I)) = pyInt(0 -Int I)`. | Correct integer negation. |
| R20 | semantic.k:113 | `atZero(pyList(L)) = pyInt(first(L))`. | Correct on the reachable nonempty domain; see F11 for the excluded empty case. |
| R21 | semantic.k:114 | `tailVal(pyList(L)) = pyList(rest(L))`. | Correct on the reachable list domain; submitted slices are called only on nonempty lists. |
| R22 | semantic.k:115 | Integer membership delegates to `member`. | Correct. |
| R23 | semantic.k:117 | Boolean truthiness returns the Boolean. | Correct. |
| R24 | semantic.k:118 | Integer truthiness is nonzero. | Correct, though unused as an `if` condition here. |
| R25 | semantic.k:119 | List truthiness is nonemptiness. | Correct and used by the first `if`. |
| R26 | semantic.k:120 | Extract an `ISeq` from `pyList`. | Correct and used by R08. |
| R27 | semantic.k:122 | `isEmpty(.ISeq) = true`. | Correct. |
| R28 | semantic.k:123 | `isEmpty(I :: IS) = false`. | Correct; disjoint from R27. |
| R29 | semantic.k:124 | `first(I :: IS) = I`. | Correct on its exact constructor domain. |
| R30 | semantic.k:125 | `rest(I :: IS) = IS`. | Correct on its exact constructor domain. |
| R31 | semantic.k:126 | `member(I, .ISeq) = false`. | Correct. |
| R32 | semantic.k:127 | `member(I, J :: JS) = (I ==Int J) orBool member(I, JS)`. | Correct, descending, and exhaustive with R31. Eager evaluation has no observable difference for finite pure integer lists. |

There are no semantic rule priorities. R06/R07 and R27/R28 have disjoint
constructor/Boolean cases. R31/R32 have disjoint constructors. No ordinary
semantic rule overlaps another at the same control form.

## Proof-local simplification rules

| ID | File:line | Rule | Class, domain, and assessment |
|---|---|---|---|
| V01 | verification.k:6 | `notBool notBool B => B [simplification]` | Derived Boolean lemma, all `B:Bool`; true, unguarded, and no state/control footprint. |
| V02 | verification.k:12-13 | `hasZeroPair(L) => false requires isEmpty(L) [simplification]` | Definitional summary, exactly the empty-list case. |
| V03 | verification.k:14-16 | `hasZeroPair(L) => member(0 -Int first(L), rest(L)) orBool hasZeroPair(rest(L)) requires notBool isEmpty(L) [simplification]` | Definitional summary for nonempty lists. It states the exhaustive mathematical partition: a zero-sum pair uses the head and a later inverse, or lies wholly in the tail. The recursive call descends by one constructor. |

V02 and V03 have disjoint guards. Because every `ISeq` is empty or a
constructor, their guards cover the full domain; R27/R28 decide the guards.
V03 uses `first` and `rest` only under nonemptiness. Neither rule replaces a
program term or touches any configuration cell. The value influences the final
postcondition only, and the main reachability claim is the machine-checked
connection from fixed program execution to this summary. The summary-to-English
existential interpretation is an ordinary induction, not a separate K claim.

## Entry claim

`spec.k:9-47` contains one unlabeled positive claim and no helper claims.
Precondition: any `L:ISeq`, with the exact submitted program in both `run` and
`<program>`, and empty environment. Postcondition: exact `<k>` result
`pyBool(hasZeroPair(L))`, with the program cell unchanged and the environment
empty. There are no right-only variables, ellipses, implications, or
existentials in the result.

The claim itself is the recursion circularity. R08 reaches exactly the same
`run(submitted-program, rest(L))` shape, with the same program cell and empty
environment, so the circularity matches real control flow rather than a
substituted helper.

## Used-construct coverage map

| Submitted AST construct | Declaration(s) | Executing rules/functions |
|---|---|---|
| `Module(FuncDef(...))`, one parameter | S01, S03, S07, S08 | R01 |
| Juxtaposed statement blocks and empty else blocks | S02 | R02, R03 |
| First and second `If` | S06, S31 | R05-R07 |
| `not l` | S11, S12 | R13, R14, R25, R27-R28 |
| Literal `False`/`True` returns | S04, S09 | R09, R11 |
| `-l[0]` | S10-S12, S14, S19 | R12, R13, R15-R16, R19-R20, R29 |
| `l[1:]` | S10, S11, S14, S20-S22 | R12, R13, R17, R21, R30 |
| Membership comparison | S13, S17-S18 | R18, R22, R31-R32 |
| Tail-recursive call | S04, S11, S15-S16 | R08, R13, R17, R21, R26, R30 |
| Semantic integer-list input and Boolean result | S23-S27 | R19-R32 as above |

Every construct in `solution.mpy` is declared and reaches a matching rule.
Unused syntax/rules are S05/R04, S28/S30/R10, and truthiness R23/R24 for operand
types not used as conditions. Missing general Python constructs are not defects
under the generated-semantics minimal-subset boundary.
