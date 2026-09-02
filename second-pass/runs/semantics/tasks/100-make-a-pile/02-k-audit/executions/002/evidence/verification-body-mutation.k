requires "reference-semantics/semantics.k"

module PILE-VERIFICATION-BODY-MUTATION
  imports MPY

  syntax Expr ::= "pileConditionMut" [macro]
  rule pileConditionMut
    => Compare(Name("i"), CmpOp("<", Name("n")))

  // Material mutation: the executed append expression uses 4*i, while the
  // result summary below deliberately remains the required n+2*i sequence.
  syntax Stmts ::= "pileLoopBodyMut" [macro]
  rule pileLoopBodyMut
    => Expr(
         Call(
           Attribute(Name("stones"), "append"),
           BinOp("+", Name("n"), BinOp("*", Int(4), Name("i")))))
       AugAssign(Name("i"), "+", Int(1))

  syntax Stmts ::= "pileBodyMut" [macro]
  rule pileBodyMut
    => Assign(Name("stones"), ListExpr(.Exprs))
       Assign(Name("i"), Int(0))
       While(pileConditionMut, pileLoopBodyMut)
       Return(Name("stones"))

  syntax Module ::= "pileModuleMut" [macro]
  rule pileModuleMut
    => Module(FuncDef("make_a_pile", Params("n"), pileBodyMut))

  syntax ValSeq ::= pileMut(Int, Int) [function, total]
  rule pileMut(N:Int, I:Int) => .ValSeq
    requires I >=Int N
  rule pileMut(N:Int, I:Int)
    => vCons(N +Int (2 *Int I), pileMut(N, I +Int 1))
    requires I <Int N

  rule valSeqConcat(VS:ValSeq, .ValSeq) => VS [simplification]
  rule valSeqConcat(valSeqConcat(A:ValSeq, B:ValSeq), C:ValSeq)
    => valSeqConcat(A, valSeqConcat(B, C))
    [simplification]
endmodule
