requires "verification.k"

module BRIDGE-WITNESS
  imports VERIFICATION

  // Fixed supplied-semantics representation of Python [7, 8].
  claim [fixed-two-element-list-len]:
    <k>
      #applyK(toCall(builtinV("len")),
              (list(vCons(7, vCons(8, .ValSeq))), .Vals))
      =>
      2
    </k>

  // Candidate's stated typed representation of the same integer sequence.
  // Its globally applicable priority bridge returns only the nonempty flag 1.
  claim [candidate-intvals-two-element-len]:
    <k>
      #applyK(toCall(builtinV("len")),
              (list(intVals(iCons(7, iCons(8, .IntSeq)))), .Vals))
      =>
      1
    </k>
endmodule
