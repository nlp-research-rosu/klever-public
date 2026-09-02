requires "audit-connection.k"

module SPEC-SLICE-GROUND
  imports AUDIT-CONNECTION

  // "cat"[1:] == "at"
  claim
    <k>
      noB ~> #slStep(
        str(iCons(99, iCons(97, iCons(116, .IntSeq)))),
        someB(1),
        noB) ~> CONT:K
      =>
      str(iCons(97, iCons(116, .IntSeq))) ~> CONT
    </k>

  // "cat"[:2] == "ca"
  claim
    <k>
      noB ~> #slStep(
        str(iCons(99, iCons(97, iCons(116, .IntSeq)))),
        noB,
        someB(2)) ~> CONT:K
      =>
      str(iCons(99, iCons(97, .IntSeq))) ~> CONT
    </k>

  // "cat"[::-1] == "tac"
  claim
    <k>
      someB(-1) ~> #slStep(
        str(iCons(99, iCons(97, iCons(116, .IntSeq)))),
        noB,
        noB) ~> CONT:K
      =>
      str(iCons(116, iCons(97, iCons(99, .IntSeq)))) ~> CONT
    </k>

endmodule
