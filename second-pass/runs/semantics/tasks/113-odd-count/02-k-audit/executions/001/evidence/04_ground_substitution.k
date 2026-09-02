requires "verification.k"

module ODD-COUNT-GROUND-SUBSTITUTION
  imports ODD-COUNT-VERIFICATION

  claim
    <k>
      oddCountSpec(
        vCons(
          str(iCons(49, .IntSeq)),
          .ValSeq))
      =>
      vCons(
        oddText(1),
        .ValSeq)
    </k>
    [label(formal-ground)]

  claim
    <k>
      oddCountSpec(
        vCons(
          str(iCons(49, .IntSeq)),
          .ValSeq))
      =>
      vCons(
        str(strToCodes(
          "the number of odd elements 1n the str1ng 1 of the 1nput.")),
        .ValSeq)
    </k>
    [label(intent-ground)]
endmodule
