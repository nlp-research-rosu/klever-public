requires "verification.k"

module AUDITOR-WRONG-ITERATOR
  imports VERIFICATION

  // Opposite interpretation probe for the result-bearing iterator bridge.
  claim [a-is-not-empty]:
    <k>
      #iterNext(
        list(
          vCons(
            str(strToCodes("a")),
            .ValSeq)))
      ~> CONT:K
      =>
      #iterYield(
        str(.IntSeq),
        list(.ValSeq))
      ~> CONT
    </k>
endmodule
