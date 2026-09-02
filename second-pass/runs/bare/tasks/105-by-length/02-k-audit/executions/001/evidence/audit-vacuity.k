module AUDIT-VACUITY-SPEC
  imports MPY-VERIFICATION

  // Fresh reviewer mutation.  The real result for [1, 9, 9] is
  // ["Nine", "Nine", "One"]; this false postcondition drops one "Nine".
  claim
    <k> init(#solutionProgram) => .K </k>
    <program> #solutionProgram </program>
    <input> pyList(1 :: 9 :: 9 :: .PyVals) </input>
    <result>
      noResult
      => pyList("Nine" :: "One" :: .PyVals)
    </result>
endmodule
