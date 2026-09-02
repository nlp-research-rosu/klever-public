requires "verification.k"

module AUDIT-SYMBOLIC-MODEL-GAP
  imports VERIFICATION-BASE

  // The bridge-free supplied Haskell semantics uses structural ==K:
  // 1 is not considered a member of [True].
  claim [bool-int-structural]:
    <k>
      #memberAcc(1, list(vCons(true, .ValSeq)))
      => false
    </k>
endmodule

module AUDIT-SYMBOLIC-MODEL-OPPOSITE
  imports VERIFICATION-BASE

  // Deliberately asks for CPython's opposite result. The fixed symbolic model
  // must reject it.
  claim [bool-int-cpython-result]:
    <k>
      #memberAcc(1, list(vCons(true, .ValSeq)))
      => true
    </k>
endmodule

