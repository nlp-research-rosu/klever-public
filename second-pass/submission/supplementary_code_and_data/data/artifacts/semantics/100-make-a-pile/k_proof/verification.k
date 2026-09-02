requires "reference-semantics/semantics.k"

module PILE-VERIFICATION
  imports MPY

  syntax Expr ::= "pileCondition" [macro]
  rule pileCondition
    => Compare(Name("i"), CmpOp("<", Name("n")))

  syntax Stmts ::= "pileLoopBody" [macro]
  rule pileLoopBody
    => Expr(
         Call(
           Attribute(Name("stones"), "append"),
           BinOp("+", Name("n"), BinOp("*", Int(2), Name("i")))))
       AugAssign(Name("i"), "+", Int(1))

  syntax Stmts ::= "pileBody" [macro]
  rule pileBody
    => Assign(Name("stones"), ListExpr(.Exprs))
       Assign(Name("i"), Int(0))
       While(pileCondition, pileLoopBody)
       Return(Name("stones"))

  syntax Val ::= "pileClosure" [macro]
  rule pileClosure => closureVal(("n", .ParamNames), pileBody, 0)

  syntax Module ::= "pileModule" [macro]
  rule pileModule
    => Module(FuncDef("make_a_pile", Params("n"), pileBody))

  // pile(N, I) is the mathematical suffix at level index I:
  // [N + 2*I, N + 2*(I+1), ..., N + 2*(N-1)].
  syntax ValSeq ::= pile(Int, Int) [function, total]
  rule pile(N:Int, I:Int) => .ValSeq
    requires I >=Int N
  rule pile(N:Int, I:Int)
    => vCons(N +Int (2 *Int I), pile(N, I +Int 1))
    requires I <Int N

  // Two standard list-concatenation identities orient symbolic accumulators
  // into the same form on successive induction steps.
  rule valSeqConcat(VS:ValSeq, .ValSeq) => VS [simplification]
  rule valSeqConcat(valSeqConcat(A:ValSeq, B:ValSeq), C:ValSeq)
    => valSeqConcat(A, valSeqConcat(B, C))
    [simplification]
endmodule
