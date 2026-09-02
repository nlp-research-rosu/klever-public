requires "verification.k"

module SPEC-WITNESSES
  imports VERIFICATION

  claim [empty-valid]:
    <k> validParenInput(strToCodes("")) => true </k>

  claim [empty-result]:
    <k> separateParenGroupsSpec(strToCodes("")) => .ValSeq </k>

  claim [single-valid]:
    <k> validParenInput(strToCodes("()")) => true </k>

  claim [single-result]:
    <k>
      separateParenGroupsSpec(strToCodes("()"))
      => vCons(str(strToCodes("()")), .ValSeq)
    </k>

  claim [prompt-valid]:
    <k>
      validParenInput(strToCodes("( ) (( )) (( )( ))")) => true
    </k>

  claim [prompt-result]:
    <k>
      separateParenGroupsSpec(strToCodes("( ) (( )) (( )( ))"))
      => vCons(
           str(strToCodes("()")),
           vCons(
             str(strToCodes("(())")),
             vCons(str(strToCodes("(()())")), .ValSeq)))
    </k>
endmodule
