requires "verification.k"

module SPEC-WITNESS
  imports VERIFICATION

  claim [precondition-witness]:
    <k>
      balancedTail(strToCodes("( ) (( )) (( )( ))"), 0)
      andBool parenSpaceOnly(strToCodes("( ) (( )) (( )( ))"))
      => true
    </k>

  claim [summary-substitution]:
    <k>
      scanGroups(
        strToCodes("( ) (( )) (( )( ))"),
        .IntSeq,
        0,
        .ValSeq)
      => vCons(str(strToCodes("()")),
           vCons(str(strToCodes("(())")),
           vCons(str(strToCodes("(()())")), .ValSeq)))
    </k>
endmodule
