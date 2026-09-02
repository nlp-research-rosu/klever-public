# Exhaustive local rule and declaration inventory

Audited sources: `/candidate/semantic.k`, `/candidate/verification.k`, and
`/candidate/spec.k`. There are no generated helper K files and no
proof-local auxiliary claims.

## Local syntax and attributes

| ID | Location | Declaration | Role / assessment |
|---|---|---|---|
| S1 | `semantic.k:5` | `Expr ::= Int(Int)` | Integer-literal AST constructor; used for base `2`. |
| S2 | `semantic.k:6` | `Expr ::= Name(String)` | Name AST constructor; used for `pow`, `n`, and `p`. |
| S3 | `semantic.k:7` | `Expr ::= Call(Expr,Expr,Expr,Expr)` | Callee plus exactly three arguments; used by three-argument `pow`. |
| S4 | `semantic.k:9` | `Params(String,String)` | Exactly two formal parameter names. |
| S5 | `semantic.k:11` | `Return(Expr)` | One return statement. |
| S6 | `semantic.k:12` | `FuncDef(String,Params,Stmt)` | One two-argument function with one statement. |
| S7 | `semantic.k:14` | `Module(Stmt)` | Single-statement translated module. |
| S8 | `semantic.k:23` | `Formals ::= noFormals` | Initial formal-binding marker. |
| S9 | `semantic.k:23` | `formals(String,String)` | Stores the two selected formal names. |
| S10 | `semantic.k:24` | `Result ::= noResult` | Initial no-result marker. |
| S11 | `semantic.k:24` | `result(Int)` | Returned integer value. |
| S12 | `semantic.k:35` | `evalInt(Expr,String,String,Int,Int) [function]` | Partial, structurally recursive expression evaluator. It is not declared `total`. |
| S13 | `verification.k:7` | `expectedModp(Int,Int) [function]` | Definitional name for K modular power. It is not declared `total`. |

There are no local `total`, `functional`, `opaque`, `strict`, `seqstrict`,
priority, simplification, concrete, macro, or anywhere declarations.

## Configuration

`semantic.k:26-33` declares one `<modp>` top cell containing:

| Cell | Initial content | Read/write footprint |
|---|---|---|
| `<k>` | `$PGM:Program` | R5 replaces the module by its body; R6 consumes the return. |
| `<n>` | `$N:Int` | Read by R6, never written. It is the externally supplied first argument. |
| `<p>` | `$P:Int` | Read by R6, never written. It is the externally supplied second argument. |
| `<formals>` | `noFormals` | R5 writes the two names; R6 reads them. |
| `<result>` | `noResult` | R6 writes exactly one integer result. |

No heap, environment, stack, exception, allocation, I/O, or continuation cell
exists.

## Rules and equations

| ID | Location | Exact domain and effect | Class | Assessment |
|---|---|---|---|---|
| R1 | `semantic.k:37` | Every `evalInt(Int(I),X,Y,N,P)` becomes `I`. | Definitional equation | True literal interpretation. Disjoint from R2-R4. |
| R2 | `semantic.k:38` | `evalInt(Name(X),X,Y,N,P)` becomes `N`. | Definitional equation | Correct first-formal lookup for the submitted distinct formals. |
| R3 | `semantic.k:39-40` | `evalInt(Name(Y),X,Y,N,P)` becomes `P` when `X =/=String Y`. | Definitional equation | Guard makes it disjoint from R2. Correct second-formal lookup for `"n" != "p"`. |
| R4 | `semantic.k:41-44` | Any `evalInt(Call(Name("pow"),BASE,EXP,MOD),X,Y,N,P)` becomes recursively evaluated operands combined by K `^%Int`. No integer-domain or binding guard. | Operational bridge to an external primitive | Sound for the submitted binding on tested `N >= 0, P > 0`, conditional on the K primitive. Globally false as Python semantics: at `N=2,P=-5`, Python `pow(2,2,-5)=-1`, while fresh K execution yields `4`. The bridge also has no exception model for modulus zero. |
| R5 | `semantic.k:46-47` | An entire `<k>` containing `Module(FuncDef(F,Params(X,Y),BODY))` becomes `BODY`; `noFormals` becomes `formals(X,Y)`. | Operational entry-runner rule | It matches no arbitrary continuation and preserves all omitted cells. It deliberately treats the sole definition as the selected entry invocation; it ignores `F`. This is adequate for the exact submitted one-function term but is not ordinary Python module-definition behavior. |
| R6 | `semantic.k:49-53` | An entire `<k>` containing `Return(E)` becomes `.K`; with integer inputs, selected formals, and `noResult`, result becomes `evalInt(E,...)`. | Ordinary operational rule | Exact control context (no `...`), so it introduces no broad return/unwind shortcut. Correct for the submitted single return, provided R1-R4 are correct. |
| R7 | `verification.k:8` | Every `expectedModp(N,P)` becomes `2 ^%Int N P`. | Definitional summary | Truthful as the definition of the K-side expected value. It does not independently prove that K `^%Int` equals Python or canonical behavior. |

R1-R4 are structurally descending on the finite expression tree. R1-R4 have no
constructor overlap; R2/R3 are disjoint because of R3's guard. R5 and R6 match
different statement constructors. There are no priorities or simplification
rules whose interactions need ordering analysis.

## Used-construct coverage

The regenerated program is:

`Module(FuncDef("modp", Params("n","p"), Return(Call(Name("pow"), Int(2), Name("n"), Name("p")))))`.

Mapping: `Module`/`FuncDef`/`Params` use S7/S6/S4 and R5; `Return` uses S5 and
R6; `Call` uses S3 and R4; literal `Int(2)` uses S1/R1; names `"n"` and `"p"`
use S2/R2/R3; textual callee `"pow"` is selected directly by R4. Every used
construct has a declaration and applicable rule. Missing behavior for other AST
constructs is outside this generated semantics' minimal submitted-program scope.

Arguments have no side effects in this syntax, so R4's equational evaluation
does not observably violate Python's left-to-right order for this program.
Bindings are not represented generally: the semantics assumes the textual
callee `"pow"` denotes the builtin and the two stored formal names denote the
two integer input cells. The submitted program satisfies those assumptions,
but R4 is over-broad for programs that shadow `pow`.

## Claims

`spec.k` has six reachability goals and no auxiliary/circularity claims:

1. General: exact submitted constructor term; `N >= 0`, `P > 0`; final result
   is `expectedModp(N,P)`, `<k>` is empty, and formals are `"n","p"`.
2. Ground `(3,5)` with final result `3`.
3. Ground `(1101,101)` with final result `2`.
4. Ground `(0,101)` with final result `1`.
5. Ground `(3,11)` with final result `8`.
6. Ground `(100,101)` with final result `1`.

The general claim closes because R4 and R7 reduce the actual body result and
the required result to the same externally hooked K symbol. Thus it is
result-constraining but conditional on the `INT.powmod` bridge; it does not
derive the mathematical or Python meaning of that primitive.

## Imported trust boundary

`^%Int` is imported from K's `INT` module as a hooked function
`hook(INT.powmod)`. The installed K documentation says
`A ^%Int B C` has the value of `(A ^Int B) %Int C`, with K `%Int` using
truncating-division remainder. For `B >= 0, C > 0`, this matches the intended
integer modular power and the tested Python builtin. It differs from Python's
negative-modulus remainder convention, witnessed above. Other imported
operations (`>=Int`, `>Int`, `andBool`, and `=/=String`) only guard the claim or
select the second formal; their ordinary mathematical meanings are trusted.
