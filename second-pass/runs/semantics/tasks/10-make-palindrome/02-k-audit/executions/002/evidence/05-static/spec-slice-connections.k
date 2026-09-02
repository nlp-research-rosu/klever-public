requires "audit-connection.k"

module SPEC-SLICE-CONNECTIONS
  imports AUDIT-CONNECTION

  claim
    <k>
      noB ~> #slStep(str(S:IntSeq), someB(I:Int), noB) ~> CONT:K
      =>
      str(dropIS(S, I)) ~> CONT
    </k>
    requires 0 <=Int I andBool I <=Int isLen(S)

  claim
    <k>
      noB ~> #slStep(str(S:IntSeq), noB, someB(I:Int)) ~> CONT:K
      =>
      str(auditPrefixIS(S, I)) ~> CONT
    </k>
    requires 0 <=Int I andBool I <=Int isLen(S)

  claim
    <k>
      someB(-1) ~> #slStep(str(S:IntSeq), noB, noB) ~> CONT:K
      =>
      str(revIS(S)) ~> CONT
    </k>

endmodule
