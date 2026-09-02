requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The exact function body emitted in solution.mpy.  Naming it lets the
  // specifications call the entry point without adding a test harness to the
  // submitted Python program.
  syntax Stmts ::= "sortArrayBody" [function, total]
  rule sortArrayBody
    => If(
         UnaryOp("not", Name("array")),
         Return(ListExpr(.Exprs)) .Stmts,
         .Stmts)
       If(
         Compare(
           BinOp(
             "%",
             BinOp(
               "+",
               Subscript(Name("array"), Int(0)),
               Subscript(Name("array"), UnaryOp("-", Int(1)))),
             Int(2)),
           CmpOp("==", Int(1))),
         Return(Call(Name("sorted"), (Name("array"), .Exprs))) .Stmts,
         .Stmts)
       Return(
         Call(
           Name("sorted"),
           (Name("array"), KwArg("reverse", Bool(true)), .Exprs)))
       .Stmts

  syntax Val ::= "sortArrayClosure" [function, total]
  rule sortArrayClosure
    => closureVal(("array", .ParamNames), sortArrayBody, 0)

  // Symbolic integer lists used by the quantified middle segment in spec.k.
  syntax ValSeq ::= intsVS(IntSeq) [function, total]
  rule intsVS(.IntSeq) => .ValSeq
  rule intsVS(iCons(I:Int, IS:IntSeq)) => vCons(I, intsVS(IS))

  syntax Bool ::= nonNegativeIS(IntSeq) [function, total]
  rule nonNegativeIS(.IntSeq) => true
  rule nonNegativeIS(iCons(I:Int, IS:IntSeq))
    => I >=Int 0 andBool nonNegativeIS(IS)

  // snocVS(M, L) is M followed by L.  The final rule is a derived
  // negative-index lemma.  It prevents the symbolic rewriter from unfolding
  // an arbitrary-length middle segment merely to establish Python's a[-1].
  syntax ValSeq ::= snocVS(ValSeq, Val)
  rule snocVS(.ValSeq, V:Val) => vCons(V, .ValSeq)
  rule snocVS(vCons(H:Val, T:ValSeq), V:Val)
    => vCons(H, snocVS(T, V))

  rule <k>
         Subscript(
           list(vCons(_F:Int, snocVS(_M:ValSeq, L:Int))),
           UnaryOp("-", Int(1)))
         => L
         ...
       </k>
       [priority(40)]
endmodule
