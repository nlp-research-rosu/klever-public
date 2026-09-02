requires "fixed-audit.k"

module ITER-BRIDGE-CONNECTION
  imports FIXED-AUDIT

  // Fixed-semantics theorem over every integer head, every tail, and every
  // continuation accepted by the candidate's specialized iterator rule.
  claim
    <k> #iterNext(list(vCons(I:Int, REST:ValSeq))) ~> K:K
      => #iterYield(I, list(REST)) ~> K
    </k>
endmodule
