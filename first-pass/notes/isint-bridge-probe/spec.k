// spec.k — does l[0]+l[1] reduce to an Int under allInt(NUMS)? If the echo in verif.k fires,
// applyBin casts both operands to Int and the sum reduces; the claim closes. If not, it sticks.

requires "verif.k"

module ISINT-PROBE-SPEC
  imports ISINT-PROBE-VERIFICATION

  // Probe: the SUM of two same-list elements is an Int (not a stuck opaque Val).
  claim
    <k> applyBin("+", valSeqAt(NUMS:ValSeq, 0), valSeqAt(NUMS:ValSeq, 1)) => ?_:Int ... </k>
    requires allInt(NUMS) andBool vsLen(NUMS) >=Int 2
    [all-path]
endmodule
