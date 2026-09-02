requires "summaries.k"

module CONNECTION
  imports PROD-SUMMARIES

  // Definitional materialization used only by the bridge-free connection
  // proofs.  After this representation step, MPY-LIST performs iteration.
  rule <k>
         #iterNext(list(intVals(.IntSeq)))
         ~> #loopStep(TARGET:Expr, BODY:Stmts)
         ~> CONT:K
         =>
         #iterNext(list(.ValSeq))
         ~> #loopStep(TARGET, BODY)
         ~> CONT
       </k>

  rule <k>
         #iterNext(list(intVals(iCons(VALUE:Int, REST:IntSeq))))
         ~> #loopStep(TARGET:Expr, BODY:Stmts)
         ~> CONT:K
         =>
         #iterNext(list(vCons(VALUE, intVals(REST))))
         ~> #loopStep(TARGET, BODY)
         ~> CONT
       </k>
endmodule
