requires "bridge-free-symbolic.k"

module BRIDGE-FREE-CONNECTION-SPEC
  imports BRIDGE-FREE-SYMBOLIC

  claim [real-empty-row]:
    <k> #sumAcc(list(rowVals(.IntSeq)), 0)
      => 0
    </k>

  claim [opaque-empty-row]:
    <k> #sumAcc(list(symRowBF(.IntSeq)), 0)
      => 0
    </k>
endmodule

module BRIDGE-ENABLED-CONNECTION-SPEC
  imports MAX-FILL-VERIFICATION

  claim [bridged-empty-row]:
    <k> #sumAcc(list(symRow(.IntSeq)), 0)
      => 0
    </k>

  // Opposite interpretation for a nonempty row: the bridged semantics should
  // compute 1, so the deliberately wrong result 0 must be rejected.
  claim [bridged-one-row-wrong]:
    <k> #sumAcc(list(symRow(iCons(1, .IntSeq))), 0)
      => 0
    </k>
endmodule
