requires "/tmp/audit-work/source/verification.k"

module WRONG-BRIDGE-SPEC
  imports VERIFICATION-BASE

  claim [wrong-yield]:
    <k>
      #iterNext(list(intListVals(intCons(7, .IntList))))
      => #iterYield(8, list(intListVals(.IntList)))
    </k>
endmodule
