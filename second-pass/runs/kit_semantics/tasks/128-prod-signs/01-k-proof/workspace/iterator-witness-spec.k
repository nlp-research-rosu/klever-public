requires "verification-base.k"

module ITERATOR-WITNESS-SPEC
  imports VERIFICATION-BASE

  claim [typed-iterator-positive-value]:
    <k>
      #iterNext(list(intVals(iCons(4, .IntSeq))))
      ~> #loopStep(TARGET:Expr, BODY:Stmts)
      ~> CONT:K
      =>
      #iterYield(4, list(intVals(.IntSeq)))
      ~> #loopStep(TARGET, BODY)
      ~> CONT
    </k>

  claim [typed-iterator-negative-value]:
    <k>
      #iterNext(list(intVals(iCons(-2, .IntSeq))))
      ~> #loopStep(TARGET:Expr, BODY:Stmts)
      ~> CONT:K
      =>
      #iterYield(-2, list(intVals(.IntSeq)))
      ~> #loopStep(TARGET, BODY)
      ~> CONT
    </k>
endmodule
