requires "bridge-base.k"

module BRIDGE-SLICE-SPEC
  imports BRIDGE-BASE

  claim
    <k>
      doSlice(list(VS:ValSeq), noB, noB, someB(-1)) ~> CONT:K
      => list(auditReverseVS(VS)) ~> CONT
    </k>
endmodule
