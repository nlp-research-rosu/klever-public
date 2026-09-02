requires "/tmp/audit-work/reconstruction/reference-semantics/semantics.k"

module BRIDGE-FREE-VERIFICATION
  imports MPY

  syntax Stmts ::= "solutionLoopBodyBF" [macro]
  rule solutionLoopBodyBF
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

  syntax Stmts ::= "solutionBodyBF" [macro]
  rule solutionBodyBF
    => Assign(Name("total"), Int(0))
       Assign(Name("even_position"), Bool(true))
       Assign(Name("value"), Int(0))
       For(Name("value"), Name("lst"), solutionLoopBodyBF)
       Return(Name("total"))
       .Stmts

  syntax Val ::= "solutionClosureBF" [macro]
  rule solutionClosureBF
    => closureVal(("lst", .ParamNames), solutionBodyBF, 0)

  syntax Bool ::= allIntsBF(ValSeq) [function, total]
  rule allIntsBF(.ValSeq) => true
  rule allIntsBF(vCons(V:Val, R:ValSeq)) => isInt(V) andBool allIntsBF(R)

  syntax Int ::= intProjectionBF(Val) [function, total]
  rule intProjectionBF(I:Int) => I

  syntax Int ::= oddAtEvenPositionsBF(ValSeq, Bool) [function]
               | oddAtEvenAccBF(ValSeq, Bool, Int) [function]
  rule oddAtEvenPositionsBF(VS:ValSeq, B:Bool)
    => oddAtEvenAccBF(VS, B, 0)
  rule oddAtEvenAccBF(.ValSeq, _:Bool, ACC:Int) => ACC
  rule oddAtEvenAccBF(vCons(V:Val, R:ValSeq), true, ACC:Int)
    => oddAtEvenAccBF(
         R,
         false,
         ACC +Int intProjectionBF(V) *Int pyMod(intProjectionBF(V), 2))
  rule oddAtEvenAccBF(vCons(_:Val, R:ValSeq), false, ACC:Int)
    => oddAtEvenAccBF(R, true, ACC)
endmodule
