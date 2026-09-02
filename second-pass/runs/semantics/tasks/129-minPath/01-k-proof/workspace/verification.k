requires "reference-semantics/semantics.k"

module MINPATH-VERIFICATION
  imports MPY

  syntax Stmts ::= "minPathAppendBody" [macro]
  rule minPathAppendBody =>
    If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
       Expr(Call(Attribute(Name("path"), "append"), Int(1))),
       Expr(Call(Attribute(Name("path"), "append"), Name("neighbor"))))

  // The exact translated body from solution.mpy, named once so that the
  // execution claims and the final module closure refer to the same program.
  syntax Stmts ::= "minPathBody" [macro]
  rule minPathBody =>
    Assign(Name("n"), Call(Name("len"), Name("grid")))
    Assign(Name("row"), Int(0))
    Assign(Name("column"), Int(0))
    For(Name("i"), Call(Name("range"), Name("n")),
      For(Name("j"), Call(Name("range"), Name("n")),
        If(Compare(
             Subscript(Subscript(Name("grid"), Name("i")), Name("j")),
             CmpOp("==", Int(1))),
           Assign(Name("row"), Name("i"))
           Assign(Name("column"), Name("j")),
           .Stmts)))
    Assign(Name("neighbor"),
      BinOp("+", BinOp("*", Name("n"), Name("n")), Int(1)))
    If(Compare(Name("row"), CmpOp(">", Int(0))),
       Assign(Name("value"),
         Subscript(
           Subscript(Name("grid"), BinOp("-", Name("row"), Int(1))),
           Name("column")))
       If(Compare(Name("value"), CmpOp("<", Name("neighbor"))),
          Assign(Name("neighbor"), Name("value")),
          .Stmts),
       .Stmts)
    If(Compare(BinOp("+", Name("row"), Int(1)), CmpOp("<", Name("n"))),
       Assign(Name("value"),
         Subscript(
           Subscript(Name("grid"), BinOp("+", Name("row"), Int(1))),
           Name("column")))
       If(Compare(Name("value"), CmpOp("<", Name("neighbor"))),
          Assign(Name("neighbor"), Name("value")),
          .Stmts),
       .Stmts)
    If(Compare(Name("column"), CmpOp(">", Int(0))),
       Assign(Name("value"),
         Subscript(
           Subscript(Name("grid"), Name("row")),
           BinOp("-", Name("column"), Int(1))))
       If(Compare(Name("value"), CmpOp("<", Name("neighbor"))),
          Assign(Name("neighbor"), Name("value")),
          .Stmts),
       .Stmts)
    If(Compare(BinOp("+", Name("column"), Int(1)), CmpOp("<", Name("n"))),
       Assign(Name("value"),
         Subscript(
           Subscript(Name("grid"), Name("row")),
           BinOp("+", Name("column"), Int(1))))
       If(Compare(Name("value"), CmpOp("<", Name("neighbor"))),
          Assign(Name("neighbor"), Name("value")),
          .Stmts),
       .Stmts)
    Assign(Name("path"), ListExpr(.Exprs))
    For(Name("i"), Call(Name("range"), Name("k")),
      minPathAppendBody)
    Return(Name("path"))

  syntax Module ::= "minPathProgram" [macro]
  rule minPathProgram =>
    Module(FuncDef("minPath", Params("grid", "k"), minPathBody))

  syntax Val ::= "minPathClosure" [macro]
  rule minPathClosure =>
    closureVal(("grid", "k", .ParamNames), minPathBody, 0)

  // Mathematical helpers used only in postconditions.
  syntax Int ::= minPathMin(Int, Int) [function, total]
  rule minPathMin(A:Int, B:Int) => A requires A <=Int B
  rule minPathMin(A:Int, B:Int) => B requires A  >Int B

  // On a 2x2 grid, all cells are corners. Under the spec's permutation
  // precondition these four rules select the two neighbors of the unique 1.
  syntax Int ::= minPathNeighbor2(Int, Int, Int, Int) [function, total]
  rule minPathNeighbor2(A:Int, B:Int, C:Int, _D:Int)
    => minPathMin(B, C)
    requires A ==Int 1
  rule minPathNeighbor2(A:Int, B:Int, _C:Int, D:Int)
    => minPathMin(A, D)
    requires A =/=Int 1 andBool B ==Int 1
  rule minPathNeighbor2(A:Int, B:Int, C:Int, D:Int)
    => minPathMin(A, D)
    requires A =/=Int 1 andBool B =/=Int 1 andBool C ==Int 1
  rule minPathNeighbor2(A:Int, B:Int, C:Int, _D:Int)
    => minPathMin(B, C)
    requires A =/=Int 1 andBool B =/=Int 1 andBool C =/=Int 1

  syntax ValSeq ::= minPathFour(Int) [function, total]
  rule minPathFour(M:Int)
    => vCons(1, vCons(M, vCons(1, vCons(M, .ValSeq))))

  // Accumulator specification for the exact append loop. It is deliberately
  // phrased in accumulator form so the symbolic loop and this mathematical
  // function advance in lockstep under circularity.
  syntax ValSeq ::= minPathBuild(ValSeq, Int, Int, Int) [function, total]
  rule minPathBuild(P:ValSeq, I:Int, K:Int, _M:Int) => P
    requires I >=Int K
  rule minPathBuild(P:ValSeq, I:Int, K:Int, M:Int)
    => minPathBuild(
         valSeqConcat(P, vCons(1, .ValSeq)), I +Int 1, K, M)
    requires I <Int K andBool pyMod(I, 2) ==Int 0
  rule minPathBuild(P:ValSeq, I:Int, K:Int, M:Int)
    => minPathBuild(
         valSeqConcat(P, vCons(M, .ValSeq)), I +Int 1, K, M)
    requires I <Int K andBool pyMod(I, 2) =/=Int 0
endmodule
