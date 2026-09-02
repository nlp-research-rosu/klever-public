requires "fixed-verification.k"

module BRIDGE-FREE-COMPARISON-SPEC
  imports FIXED-VERIFICATION

  // Universal connection over all Int-sorted operands, using no candidate
  // intValue or applyCmp extension.
  claim
    <k> Compare(I:Int, CmpOp("<", J:Int)) => I <Int J </k>
    [label(fixed-int-less-than)]
endmodule
