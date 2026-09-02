requires "summaries.k"

module VERIFICATION-BASE
  imports PROD-SUMMARIES

  // Typed-sequence iterator bridge, narrowed to a for-loop continuation.
  // CONNECTION-SPEC proves both exhaustive fixed-semantics cases without
  // importing this module.
  rule <k>
         #iterNext(list(intVals(IS:IntSeq)))
         ~> #loopStep(TARGET:Expr, BODY:Stmts)
         ~> CONT:K
         =>
         #typedNext(IS)
         ~> #loopStep(TARGET, BODY)
         ~> CONT
       </k>
       [priority(40)]
endmodule
