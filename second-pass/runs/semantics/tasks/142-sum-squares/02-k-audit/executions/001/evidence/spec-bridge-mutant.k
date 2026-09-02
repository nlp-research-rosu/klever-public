requires "verification-bridge-mutant.k"

module SUM-SQUARES-SPEC-BRIDGE-MUTANT
  imports SUM-SQUARES-VERIFICATION-BRIDGE-MUTANT

  claim [mutated-loop]:
    <k>
      #loop(list(intVals(IS:Ints)), Name("value"), sumSquaresLoopBody)
      ~> (Return(Name("total")) .Stmts)
      ~> #endcall
      ~> KONT:K
    =>
      (Return(Name("total")) .Stmts)
      ~> #endcall
      ~> KONT
    </k>
    <env> L:Int </env>
    <scopes>
      SC:Map
      (L |-> scope(
        "lst"   |-> list(intVals(ORIG:Ints))
        "value" |-> OLD:Int
        "total" |-> ACC:Int
        "index" |-> I:Int,
        P:Parent))
    =>
      SC
      (L |-> scope(
        "lst"   |-> list(intVals(ORIG))
        "value" |-> endValue(IS, OLD)
        "total" |-> sumSquares(IS, I, ACC)
        "index" |-> endIndex(IS, I),
        P))
    </scopes>
endmodule
