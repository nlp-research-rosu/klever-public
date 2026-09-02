requires "verification.k"

module GROUND-SUMMARY
  imports VERIFICATION

  claim [summary-direct]:
    <k> cycPattern(strToCodes("hello"), strToCodes("ell")) => true </k>

  claim [summary-false]:
    <k> cycPattern(strToCodes("abcd"), strToCodes("abd")) => false </k>

  claim [summary-rotation]:
    <k> cycPattern(strToCodes("abab"), strToCodes("baa")) => true </k>

  claim [summary-empty]:
    <k> cycPattern(strToCodes("abc"), .IntSeq) => true </k>
endmodule
