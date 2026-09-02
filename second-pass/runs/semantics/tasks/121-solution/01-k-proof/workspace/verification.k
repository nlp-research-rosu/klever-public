requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // These macros are the exact constructor terms emitted in solution.mpy.
  syntax Stmts ::= "solutionLoopBody" [macro]
  rule solutionLoopBody
    => If(
         Name("even_position"),
         Assign(
           Name("total"),
           BinOp(
             "+",
             Name("total"),
             BinOp(
               "*",
               Name("value"),
               BinOp("%", Name("value"), Int(2)))))
         .Stmts,
         .Stmts)
       Assign(
         Name("even_position"),
         UnaryOp("not", Name("even_position")))
       .Stmts

  syntax Stmts ::= "solutionBody" [macro]
  rule solutionBody
    => Assign(Name("total"), Int(0))
       Assign(Name("even_position"), Bool(true))
       Assign(Name("value"), Int(0))
       For(Name("value"), Name("lst"), solutionLoopBody)
       Return(Name("total"))
       .Stmts

  syntax Val ::= "solutionClosure" [macro]
  rule solutionClosure
    => closureVal(("lst", .ParamNames), solutionBody, 0)

  // Mathematical contract.  The boolean says whether the next element is at
  // an even zero-based position.  Only odd integers at such positions add in.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(V:Val, R:ValSeq)) => isInt(V) andBool allInts(R)

  // The Haskell backend retains an allInts-constrained element at sort Val.
  // This projection and the two guarded rules express the corresponding
  // subsort fact without changing behavior for any concrete Python integer.
  syntax Int ::= intProjection(Val) [function, total]
  rule intProjection(I:Int) => I

  rule <k> BinOp("%", V:Val, I:Int) => pyMod(intProjection(V), I) ... </k>
    requires isInt(V)
    [priority(40)]
  rule <k> BinOp("+", I:Int, V:Val) => I +Int intProjection(V) ... </k>
    requires isInt(V)
    [priority(40)]
  rule <k> BinOp("*", V:Val, I:Int) => intProjection(V) *Int I ... </k>
    requires isInt(V)
    [priority(40)]

  syntax Int ::= oddAtEvenPositions(ValSeq, Bool) [function]
               | oddAtEvenAcc(ValSeq, Bool, Int) [function]
  rule oddAtEvenPositions(VS:ValSeq, B:Bool)
    => oddAtEvenAcc(VS, B, 0)
  rule oddAtEvenAcc(.ValSeq, _:Bool, ACC:Int) => ACC
  rule oddAtEvenAcc(vCons(V:Val, R:ValSeq), true, ACC:Int)
    => oddAtEvenAcc(
         R,
         false,
         ACC +Int intProjection(V) *Int pyMod(intProjection(V), 2))
  rule oddAtEvenAcc(vCons(_:Val, R:ValSeq), false, ACC:Int)
    => oddAtEvenAcc(R, true, ACC)
endmodule
