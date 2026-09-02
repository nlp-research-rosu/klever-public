module AUDITOR-FRESH-NONVACUITY
  imports MPY-VERIFICATION

  // Fresh auditor mutation. The real output for [9, 1] is ["Nine", "One"];
  // this result-constraining destination deliberately reverses those names.
  claim
    <k> init(#solutionProgram) => .K </k>
    <program> #solutionProgram </program>
    <input> pyList(9 :: 1 :: .PyVals) </input>
    <result> noResult => pyList("One" :: "Nine" :: .PyVals) </result>
endmodule
