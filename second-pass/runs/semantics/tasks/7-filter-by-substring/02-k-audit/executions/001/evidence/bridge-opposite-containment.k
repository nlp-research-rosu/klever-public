requires "verification.k"

module BRIDGE-OPPOSITE-CONTAINMENT
  imports FILTER-VERIFICATION

  // Deliberately false: "a" occurs at the start of "abc".
  claim [wrong-false]:
    <k> Compare(
          str(iCons(97, .IntSeq)),
          CmpOp("in", str(iCons(97, iCons(98, iCons(99, .IntSeq))))))
      => false
    </k>
endmodule
