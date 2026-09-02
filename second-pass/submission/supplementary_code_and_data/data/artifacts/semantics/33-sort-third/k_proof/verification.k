requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  syntax Stmts ::= "sortThirdBody" [function, total]
  rule sortThirdBody
    => If(Compare(BinOp("%", Name("i"), Int(3)),
                  CmpOp("==", Int(0))),
         Expr(
           Call(
             Attribute(Name("result"), "append"),
             Subscript(
               Name("thirds"),
               BinOp("//", Name("i"), Int(3))))),
         Expr(
           Call(
             Attribute(Name("result"), "append"),
             Name("value"))))
       AugAssign(Name("i"), "+", Int(1))
       .Stmts

  syntax Stmts ::= "sortThirdFunctionBody" [function, total]
  rule sortThirdFunctionBody
    => Expr(Str("Sort the elements whose indices are divisible by three."))
       Assign(
         Name("thirds"),
         Call(
           Name("sorted"),
           Subscript(Name("l"), Slice(NoBound, NoBound, Int(3)))))
       Assign(Name("result"), ListExpr(.Exprs))
       Assign(Name("i"), Int(0))
       Assign(Name("value"), NoneVal)
       For(Name("value"), Name("l"), sortThirdBody)
       Return(Name("result"))
       .Stmts

  syntax Val ::= "sortThirdClosure" [function, total]
  rule sortThirdClosure
    => closureVal(("l", .ParamNames), sortThirdFunctionBody, 0)

  // The exact program emitted in solution.mpy, named so that specifications
  // can start from the normal MPY module loader without duplicating the AST.
  syntax Module ::= "sortThirdModule" [function, total]
  rule sortThirdModule
    => Module(
         FuncDef(
           "sort_third",
           Params("l"),
           sortThirdFunctionBody))

  // Mathematical fold describing the loop. SORTED is the trusted ascending
  // sort of the input's every-third slice.  I is the original list index and
  // ACC is the prefix already constructed by the implementation.
  syntax Val ::= thirdValue(Val, ValSeq, Int) [function, total]
  rule thirdValue(_:Val, SORTED:ValSeq, I:Int)
    => valSeqAt(SORTED, (I -Int pyMod(I, 3)) /Int 3)
    requires pyMod(I, 3) ==Int 0
  rule thirdValue(V:Val, _:ValSeq, I:Int) => V
    requires pyMod(I, 3) =/=Int 0

  syntax ValSeq ::= sortThirdAcc(ValSeq, ValSeq, Int, ValSeq)
                    [function, total]
  rule sortThirdAcc(.ValSeq, _:ValSeq, _:Int, ACC:ValSeq) => ACC
  rule sortThirdAcc(vCons(V:Val, REST:ValSeq), SORTED:ValSeq,
                    I:Int, ACC:ValSeq)
    => sortThirdAcc(
         REST,
         SORTED,
         I +Int 1,
         valSeqConcat(
           ACC,
           vCons(thirdValue(V, SORTED, I), .ValSeq)))

  syntax Val ::= lastLoopValue(ValSeq, Val) [function, total]
  rule lastLoopValue(.ValSeq, OLD:Val) => OLD
  rule lastLoopValue(vCons(V:Val, REST:ValSeq), _:Val)
    => lastLoopValue(REST, V)

  syntax ValSeq ::= sortThird(ValSeq) [function, total]
  rule sortThird(INPUT:ValSeq)
    => sortThirdAcc(
         INPUT,
         sortVS(buildVS(INPUT, 0, vsLen(INPUT), 3)),
         0,
         .ValSeq)
endmodule
