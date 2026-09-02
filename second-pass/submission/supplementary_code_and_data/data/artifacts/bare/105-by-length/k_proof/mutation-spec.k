module BY-LENGTH-MUTATION-SPEC
  imports MPY-VERIFICATION

  // Deliberately false: by_length([1]) is ["One"], never ["Two"].
  claim
    <k> init(#solutionProgram) => .K </k>
    <program> #solutionProgram </program>
    <input> pyList(1 :: .PyVals) </input>
    <result> noResult => pyList("Two" :: .PyVals) </result>
endmodule
