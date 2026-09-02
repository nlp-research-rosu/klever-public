requires "verification.k"

module BRIDGE-OPPOSITE-ITERATOR
  imports FILTER-VERIFICATION

  // Deliberately false: the one-element list contains "a", not "b".
  claim [wrong-head]:
    <k> #iterNext(
          list(strVals(
            ssCons(iCons(97, .IntSeq), .StrSeq))))
      => #iterYield(
           str(iCons(98, .IntSeq)),
           list(strVals(.StrSeq)))
    </k>
endmodule
