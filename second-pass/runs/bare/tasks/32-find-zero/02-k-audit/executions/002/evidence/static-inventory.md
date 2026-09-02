# Static declaration and rule inventory

This inventory covers every local declaration in the submitted
`semantic.k`, `verification.k`, and `spec.k`. Built-in `INT`, `BOOL`,
`STRING`, `MAP`, and `LIST` rules are treated as the K trust boundary.

## Syntax, configuration, attributes, and generated evaluation contexts

`SEMANTIC-SYNTAX` declares:

- `Strings = List{String, ","}` and `Params(Strings)`.
- `Exprs = List{Expr, ","}` (declared but unused by this program).
- Expressions `Int`, `Name`, `UnaryOp`, `BinOp`, `Compare`, unary `Call`,
  binary `Call`, and value injection.
- `CmpOp(String, Expr)`.
- `Stmts = List{Stmt, ""}`.
- Statements `FuncDef`, `Assign [strict(2)]`, `Return [strict]`, `For`,
  `While`, and `If`.
- Programs `Module(Stmts)` and `Program ;; Expr`.
- Values `rat(Int,Int)`, `bool(Bool)`, and `list(List)`; all are `KResult`.
- External expression `Invoke(String,Val)`.

`SEMANTIC` declares configuration cells `<k>`, `<env>`, `<functions>`, and
`<stack>`; runtime constructors `function1`, `function2`, `frame`, `exec`,
`cleanup`, `forStart`, `forLoop`, `whileTest`, `ifTest`, `compareLeft`,
`compareRight`, `call1`, `callArg1`, `callArg2`, `invoke1`, and `invoke2`.
It declares three explicit contexts: `UnaryOp` operand, left `BinOp` operand,
then right `BinOp` operand. There are no local priority rules and no opaque
symbols.

The helper symbols `gcdInt`, `makeRat`, `addRat`, `subRat`, `mulRat`,
`divRat`, and `negRat` are all `[function,total]`. Their equations are
`[simplification]`. LLVM compilation reports non-exhaustive coverage for
every one over the declared domain; concrete
witnesses include `addRat(bool(true),rat(1,1))` and `makeRat(1,0)`, both of
which remain residual under Haskell `krun`. The actual five claims only call
these symbols on nonzero-denominator rationals.

`VERIFICATION` declares macro `solution`, functions `polyValue`,
`absRat [total]`, and `leRat [total]`, plus strict expression
`VerifyRoot(List,Expr,Val) [strict(2)]`. The last two total declarations also
cover only `rat` patterns although their argument sort is all `Val`.

`SPEC` adds exactly five unlabeled, ground reachability claims and no local
functions, simplifications, priorities, ordinary rules, or opaque symbols.

## Every rule in `semantic.k`

| ID | Source | Rule and decision |
|---|---:|---|
| S01 | 82 | `gcdInt(A,0) => absInt(A)`: ordinary Euclidean base case; valid. |
| S02 | 83 | `gcdInt(A,B) => gcdInt(B,A modInt B)` for `B != 0`: descending Euclidean step on actual positive-divisor uses; valid there. |
| S03 | 93 | `makeRat(0,D) => rat(0,1)` for `D != 0`: valid. |
| S04 | 95 | Negative-denominator sign normalization: valid and descending. |
| S05 | 97 | Positive-denominator gcd reduction: valid for `N != 0,D > 0`. |
| S06 | 101 | Rational addition by cross multiplication: mathematically valid on nonzero denominators. |
| S07 | 103 | Rational subtraction: mathematically valid on nonzero denominators. |
| S08 | 105 | Rational multiplication: mathematically valid on nonzero denominators. |
| S09 | 107 | Rational division guarded by nonzero divisor numerator: valid on normalized rationals. |
| S10 | 110 | Rational negation: valid as a value equation; it does not itself restore a negative input denominator, an unreachable case for the submitted claims. |
| S11 | 113 | `Module(SS) ;; E` loads statements, evaluates `E`, then cleans up: correct for the submitted module-entry form. |
| S12 | 114 | Empty `exec` consumes: valid. |
| S13 | 115 | Nonempty `exec` sequences head before tail: correct statement order. |
| S14 | 117 | Top-level cleanup retains the value and clears environment/functions when stack is empty: correct for actual top-level completion. |
| S15 | 123 | One-parameter `FuncDef` installs `function1`: correct for `find_zero`. |
| S16 | 125 | Two-parameter `FuncDef` installs `function2`: correct for `evaluate_polynomial`. |
| S17 | 129 | Source `Int(I)` becomes `rat(I,1)`: exact-integer model. |
| S18 | 130 | `Name` reads the local environment: correct for all reached names. |
| S19 | 133 | Unary minus delegates to rational negation: correct on reached rationals. |
| S20 | 134 | Binary `+` delegates to `addRat`: correct in the exact-rational model. |
| S21 | 135 | Binary `-` delegates to `subRat`: correct in the exact-rational model. |
| S22 | 136 | Binary `*` delegates to `mulRat`: correct in the exact-rational model. |
| S23 | 137 | Binary `/` delegates to `divRat`: correct for the program’s nonzero constants, but models exact rational rather than Python float division. |
| S24 | 144 | `Compare` evaluates its left operand first: correct. |
| S25 | 145 | A left value triggers right-operand evaluation while saving the left: correct. |
| S26 | 146 | Cross-multiplied `>` is valid only for positive denominators and exact arithmetic. It is observably unlike Python floats on an intended input; see the witness below. |
| S27 | 150 | Assignment updates the named local after RHS evaluation: correct. |
| S28 | 153 | `For` evaluates its iterable before starting: correct for the list use. |
| S29 | 154 | A list value initializes `forLoop`: correct. |
| S30 | 155 | Empty `forLoop` terminates: correct. |
| S31 | 156 | Each list item binds the loop target, executes the body, then recurs: correct order/state for the actual program. |
| S32 | 159 | `While` evaluates its guard and remembers guard/body: correct. |
| S33 | 160 | True guard executes body then reevaluates: correct. |
| S34 | 162 | False guard exits: correct. |
| S35 | 164 | `If` evaluates its guard: correct. |
| S36 | 165 | True guard selects the yes branch: correct. |
| S37 | 166 | False guard selects the no branch: correct. |
| S38 | 169 | Unary call evaluates its argument before invocation: correct for actual direct-name calls. |
| S39 | 170 | Unary argument value becomes `invoke1`: correct. |
| S40 | 171 | Binary call starts with its first argument: correct left-to-right order. |
| S41 | 172 | First binary argument is saved while the second evaluates: correct. |
| S42 | 173 | Second binary argument completes `invoke2`: correct. |
| S43 | 174 | External `Invoke` becomes `invoke1`: correct entry bridge to the installed function. |
| S44 | 176 | `invoke1` saves the complete caller continuation/environment and installs the one-argument local environment: correct for reached calls. |
| S45 | 181 | `invoke2` analogously saves caller state and binds both arguments: correct for reached calls. |
| S46 | 187 | `Return` discards the callee remainder, restores the saved continuation/environment, and pops one frame: correct return control for the actual program. |

## Every rule in `verification.k`

| ID | Source | Rule and decision |
|---|---:|---|
| V01 | 9 | `solution` expands to the submitted constructor tree. A 435-token constructor comparison and trusted regeneration both match exactly. It is syntax normalization, not an execution-skipping bridge. |
| V02 | 56 | `polyValue(.List,X) => 0`: valid polynomial base case. |
| V03 | 57 | `polyValue(c::rest,x) => c + x*polyValue(rest,x)`: valid Horner recurrence for ascending coefficients. |
| V04 | 60 | Negative-numerator `absRat`: valid on the maintained positive-denominator invariant. On admitted term `rat(1,-1)`, V05 instead returns `rat(1,-1)`, which is not mathematical absolute value. |
| V05 | 62 | Nonnegative-numerator `absRat`: valid only under positive denominators; see V04’s ground representation witness. |
| V06 | 64 | Cross-multiplied `leRat`: valid only under positive denominators. Admitted term `leRat(rat(1,-1),rat(0,1))` yields false although `-1 <= 0`. |
| V07 | 68 | `VerifyRoot` evaluates the real returned root and independently computes whether the exact-rational residual is at most the ground tolerance: result-constraining and correct on normalized rationals. |

## Construct coverage and principal false-conclusion witness

`solution.mpy` uses `Module`, two `FuncDef` arities, `Params`, `Assign`,
`Name`, `Int`, `UnaryOp("-")`, `BinOp("+","-","*","/")`, `For`, `While`,
`Compare/CmpOp(">")`, unary and binary `Call`, `If`, and `Return`. Each maps
to the declarations and rules S11–S46 above. No used construct is silently
fabricated or left unmodeled on the Haskell backend.

The semantics nevertheless models all arithmetic as exact rationals, whereas
the generated Python program uses IEEE-754 binary floats after its first `/`.
For valid coefficients `[9007199254740993,-18014398509481984]`, at
`x = 1/2` Python computes the polynomial as `0.0`, but exact arithmetic gives
`1`. Thus Python takes the false branch of line 20 while S20–S26 take the true
branch. The rebuilt K semantics returns
`17179869185/34359738368`; Python returns
`17179869183/34359738368`. This is a concrete intended-domain observable
false conclusion witness for the claimed Python-language fidelity, preserved
in `stage5-rounding-witness-{krun,python}.log`.
