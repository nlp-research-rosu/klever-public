requires "bridge-base.k"

module BRIDGE-SUM-SPEC
  imports BRIDGE-BASE

  claim
    <k>
      #sumAcc(list(VS:ValSeq), 0) ~> CONT:K
      => auditSumIntVS(VS) ~> CONT
    </k>
    requires auditAllInts(VS)
endmodule
