requires "connection.k"

module CONNECTION-SPEC
  imports CONNECTION

  claim [typed-iterator-empty]:
    <k>
      #iterNext(list(intVals(.IntSeq)))
      ~> #loopStep(TARGET:Expr, BODY:Stmts)
      ~> CONT:K
      =>
      #iterDone
      ~> #loopStep(TARGET, BODY)
      ~> CONT
    </k>

  claim [typed-iterator-step]:
    <k>
      #iterNext(list(intVals(iCons(VALUE:Int, REST:IntSeq))))
      ~> #loopStep(TARGET:Expr, BODY:Stmts)
      ~> CONT:K
      =>
      #iterYield(VALUE, list(intVals(REST)))
      ~> #loopStep(TARGET, BODY)
      ~> CONT
    </k>
endmodule
