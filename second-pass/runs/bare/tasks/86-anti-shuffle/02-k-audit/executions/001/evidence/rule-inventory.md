# Exhaustive local K inventory and audit notes

This inventory covers all local declarations in `/candidate/semantic.k`,
`/candidate/verification.k`, and `/candidate/spec.k`. There are no generated
helper K files. Imported K builtins are listed separately as trust boundaries.

## Syntax and configuration

`semantic.k` declares:

1. `Pgm`: `Module(Stmts)`.
2. `Stmts`: separator-free `List{Stmt, ""}`.
3. `Stmt`: `FuncDef(String, Params, Stmts)`, `Return(Expr)`, and
   `If(Expr, Stmts, Stmts)`.
4. `Params`: one-string and three-string forms.
5. `Expr`: `Name`, `Str`, `Int`, `BinOp`, `Compare`, `Subscript`, one-argument
   `Call`, and three-argument `Call`.
6. `CmpOp`: `CmpOp(String, Expr)`.
7. `Index`: an `Expr` or `Slice(Expr, NoBound, NoBound)`.
8. `StrVals`: one-string and three-string argument bundles.
9. `Function`: `fun(Params, Stmts)`.
10. `Function`: `findFun(String, Stmts) [function]`.
11. `Map`: `bindParams(Params, StrVals) [function, total]`.
12. `Stmts`: `appendStmts(Stmts, Stmts) [function]`.
13. `KItem`: `run`, `invoke`, `invokeFound`, `exec`, `eval`, `val`,
    `boolVal`, `restore`, `returnValue`, `ifKont`, `plusLeft`, `plusRight`,
    `indexKont`, `sliceKont`, `compareLeft`, `compareRight`, `callOne`,
    `callSecond`, `callThird`, and `callInvoke`.

The sole configuration is `<python>` with `<k> run($PGM,$INPUT) </k>`,
`<functions> .Stmts </functions>`, `<env> .Map </env>`, and
`<result> "" </result>`. Each cell is read or written. There is no heap, I/O,
exception, object-identity, or global-variable cell; none is needed by this
submitted program for short normal executions. There is also no call-depth or
exception cell. That omission is observable for this recursive implementation:
CPython raises `RecursionError` on the preserved 996-character ASCII witness,
while the model has unbounded semantic call frames.

`verification.k` adds:

1. `solutionProgram : Pgm [function,total]`.
2. `solutionFunctions : Stmts [function,total]`.
3. `refInsert(String,String,String) : String [function]`.
4. `refProcess(String,String,String) : String [function]`.
5. `antiShuffleSpec(String) : String [function,total]`.

There are no local `[functional]`, `[simplification]`, `[concrete]`, priority,
`[owise]`, macro, or explicitly opaque declarations. The only proof-local
symbols that can remain symbolic are the three reference functions; all have
ordinary defining equations below.

## Construct coverage for `solution.mpy`

The submitted term uses every source constructor except no unused expression
form: `Module`; the statement list; `FuncDef`, `If`, `Return`; one- and
three-parameter `Params`; `Name`, `Str`, `Int(0)`, `BinOp("+",...)`,
`Compare` with `==` or `<=`, `Subscript` with index `0` or slice `[1:]`, and
one- or three-argument `Call`. `Int` is used only inside the index/slice
constructs, which consume it directly; a general integer-expression rule is
not needed. Each used form maps to the rules inventoried below.

## All 35 rules in `semantic.k`

| ID | Lines | Rule and decision |
|---|---:|---|
| S01 | 42 | `findFun` returns the first same-name definition. Sound for the ordered function list. |
| S02 | 43-44 | `findFun` skips a different name. Guard is disjoint from S01; recursion descends. |
| S03 | 46 | Bind one parameter to one string argument. Sound for the one-argument calls used. |
| S04 | 47-48 | Bind three parameters left-to-right to three string arguments. Sound for the used three-argument calls; submitted names are distinct. |
| S05 | 50 | Append onto an empty statement list. Standard list identity. |
| S06 | 51 | Append onto a nonempty list by structural recursion. Disjoint from S05 and descending. |
| S07 | 82-83 | Install module functions and invoke `anti_shuffle`. Sound for this module-level subset. |
| S08 | 85-86 | Resolve an invocation with `findFun`. Sound for the three unshadowed program-defined function names. |
| S09 | 87-88 | Replace the caller environment with parameter bindings and push `restore(OLD)`. Binding/state restoration is sound for this program's local-only functions, but unbounded K continuation frames do not model CPython's reachable recursion-limit exception. |
| S10 | 89-90 | Restore the exact caller map after a value returns. Sound and preserves the value/continuation. |
| S11 | 92 | A `Return` discards remaining function-body statements and evaluates its expression. Correct abrupt control for the used subset. |
| S12 | 93 | Consume `returnValue` after expression evaluation. Sound. |
| S13 | 94-96 | Evaluate an `If` condition before selecting a branch and retain following statements. Correct ordering. |
| S14 | 97-100 | True branch; guard is exactly `B`. Sound. |
| S15 | 101-104 | False branch; guard is `notBool B`, disjoint from and complete with S14. |
| S16 | 106 | Evaluate a string literal to the same K `String`. Sound at the K byte-string level. |
| S17 | 107-108 | Read a named local string from the environment. Sound for the bound names used. |
| S18 | 110 | Start left-to-right evaluation of string `+`. Sound. |
| S19 | 111 | After the left value, evaluate the right expression while retaining it. Sound. |
| S20 | 112 | Concatenate the two K strings. Matches Python concatenation only when the K/Python string representation bridge is valid. |
| S21 | 114 | Evaluate the base of integer subscripting first. Correct ordering. |
| S22 | 115 | Interpret Python `s[i]` as `substrString(S,I,I+1)`. **Materially invalid for non-Latin-1 Python Unicode strings because K's primitive indexes the underlying byte representation, not Python code points.** |
| S23 | 116-118 | Evaluate the base of the `[i:]` slice first. Correct ordering. |
| S24 | 119-121 | Interpret Python `s[i:]` with `substrString`/`lengthString`. **Materially invalid for multibyte Unicode for the same reason as S22.** |
| S25 | 123-125 | Evaluate the left operand of a comparison first. Correct ordering. |
| S26 | 126-128 | Evaluate the right operand second and retain the left value/operator. Correct ordering. |
| S27 | 129 | K-string equality. Sound for K strings and for Python strings only under a valid representation bridge. |
| S28 | 130 | K-string `<=`. It compares the byte fragments produced by S22; therefore it contributes to the Unicode mismatch even though the K-level primitive application is internally consistent. |
| S29 | 132 | Evaluate the sole call argument before invocation. Sound for the used calls. |
| S30 | 133 | Invoke the named one-argument program function. The direct global-name binding is sound here because the used names are unshadowed and present. |
| S31 | 134-136 | Begin three-argument evaluation with argument 1. Correct Python left-to-right order. |
| S32 | 137-139 | Retain argument 1 and evaluate argument 2. Correct. |
| S33 | 140-142 | Retain arguments 1-2 and evaluate argument 3. Correct. |
| S34 | 143-145 | Invoke with all three values in order. Correct for the used functions/arities. |
| S35 | 147-148 | A top-level returned `val(V)` empties `<k>` and writes `V` to `<result>`. Result-constraining and sound. |

The false-conclusion witness for S22/S24/S28 is preserved in
`krun-unicode-single.log` and `concrete-result-check.log`. The entry state with
input `"Ω"` satisfies `universal-correct`'s unconstrained `S:String`
precondition. Fresh K execution returns `"\xa9\xce"`; both actual Python
implementations return `"Ω"`. The same issue is independently visible for
`"éa Ωβ"` and an emoji case. Thus the rules can conclude an observable result
that is false for the real submitted Python program.

An independent control/exception witness is in `differential-test.log`.
`"a" * 995` returns normally in both Python implementations in this runtime,
whereas `"a" * 996` returns from the canonical but raises `RecursionError` in
the submitted recursive implementation. The K configuration and S09 have no
corresponding exception or recursion-depth state. This is an implementation
and language-model mismatch on an ASCII input, although the requested proof
discipline is partial correctness and therefore does not itself establish
normal termination.

The `[total]` declaration on `bindParams` is not globally covered: the grammar
also permits `bindParams(Params(P),vals(V1,V2,V3))` and the converse arity
mismatch, but neither has an equation. This is an inaccurate totality
annotation. Those terms do not occur in the submitted program or any claim,
and no false result for an intended execution was found from the annotation
itself, so it is recorded as a narrower static defect rather than a second
material-unsoundness finding.

## All 9 rules in `verification.k`

| ID | Lines | Rule and decision |
|---|---:|---|
| V01 | 10 | `solutionProgram => Module(solutionFunctions)`. Zero-argument total constant; sound. |
| V02 | 11-52 | Expands `solutionFunctions` to the exact submitted constructor tree. The separate identity claim closes and trusted translation is byte-identical. |
| V03 | 58-59 | `refInsert` empty-word case. True K-string equation. |
| V04 | 60-63 | Insert before a nonempty word when the K-string comparison succeeds. Disjoint from V03/V05. |
| V05 | 64-69 | Otherwise consume one K substring unit, extend `BEFORE`, and recurse. Guards are complete/disjoint and byte length descends. |
| V06 | 76-77 | `refProcess` empty-text case. True K-string equation. |
| V07 | 78-84 | On a one-byte ASCII space, emit the completed word and separator, reset word, and recurse. Disjoint from V06/V08. |
| V08 | 85-91 | Otherwise consume one K substring unit and insert it into the current word. Guards are complete/disjoint and byte length descends. |
| V09 | 93 | Defines `antiShuffleSpec(S)` as `refProcess(S,"","")`; total one-equation wrapper. |

V03-V09 are internally truthful definitions of a K byte-string insertion
algorithm; they are not opaque oracles. They deliberately mirror the
operational rules and let the two auxiliary claims summarize exact execution.
However, there is no K theorem that this reference algorithm equals the
trusted canonical `' '.join(''.join(sorted(...)))`, even on ASCII, and on
multibyte Unicode the concrete counterexample proves that it does not.

## All 7 claims in `spec.k`

1. `insert-correct`: for arbitrary K strings `C,W,B`, caller continuation
   `K`, map `ENV`, and current result, invoking the exact `insert_char`
   definition reaches `val(refInsert(C,W,B)) ~> K`, restores `ENV`, and leaves
   result unchanged. No `requires` clause.
2. `process-correct`: analogous exact summary for arbitrary `T,W,R`, using the
   independently closed insertion claim. No `requires` clause.
3. `universal-correct`: for every K `String S`, execute `solutionProgram` from
   the empty initial cells and finish with `antiShuffleSpec(S)`.
4. `example-hi`: fixed input/result `"Hi"`.
5. `example-hello`: fixed input/result `"hello"`/`"ehllo"`.
6. `example-prompt`: fixed prompt example.
7. `spaces-preserved`: fixed leading/repeated/trailing-space example.

The helper claims are exact auxiliary execution summaries, not ordinary
operational bridges. Their arbitrary continuations include the real recursive
call/restore/return frames, and their state footprint explicitly preserves the
function table and result and restores the environment. Each was closed before
being supplied as trusted to a dependent modular proof.

## Imported trust boundary

The proof assumes the K Haskell backend, matching/circularity implementation,
Map and Bool builtins, and the `String`/`Int` hooks (`+String`, `==String`,
`<=String`, `substrString`, `lengthString`, and integer addition). These
low-level primitives are ordinary implementation trust boundaries. The defect
is not that their K behavior is opaque; it is that S22/S24 use byte-indexing
primitives as if they were Python's code-point indexing over the unrestricted
formal string domain.
