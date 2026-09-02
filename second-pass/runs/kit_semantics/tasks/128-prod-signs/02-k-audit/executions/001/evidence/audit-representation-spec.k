requires "audit-representation.k"

module AUDIT-REPRESENTATION-SPEC
  imports AUDIT-REPRESENTATION

  claim [equational-iterator-empty]:
    <k>
      #iterNext(list(auditIntVals(.IntSeq)))
      ~> #loopStep(TARGET:Expr, BODY:Stmts)
      ~> CONT:K
      =>
      #iterDone
      ~> #loopStep(TARGET, BODY)
      ~> CONT
    </k>

  claim [equational-iterator-step]:
    <k>
      #iterNext(list(auditIntVals(iCons(VALUE:Int, REST:IntSeq))))
      ~> #loopStep(TARGET:Expr, BODY:Stmts)
      ~> CONT:K
      =>
      #iterYield(VALUE, list(auditIntVals(REST)))
      ~> #loopStep(TARGET, BODY)
      ~> CONT
    </k>
endmodule
