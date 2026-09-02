requires "verification.k"

module GROUND-RESULT-SPEC
  imports VERIFICATION

  claim [empty]:
    <k> bracketResult(.IntSeq, 0) => true </k>

  claim [single-open]:
    <k> bracketResult(iCons(60, .IntSeq), 0) => false </k>

  claim [one-pair]:
    <k> bracketResult(iCons(60, iCons(62, .IntSeq)), 0) => true </k>

  claim [bad-prefix]:
    <k> bracketResult(iCons(62, iCons(60, .IntSeq)), 0) => false </k>
endmodule
