module BY-LENGTH-SPEC
  imports MPY-VERIFICATION

  // Symbolic total-correctness claim for every finite array of integers XS.
  // #byLength is the prompt's count/multiplicity characterization: nine down
  // to one, with each name occurring exactly as often as its digit in XS.
  claim
    <k> init(#solutionProgram) => .K </k>
    <program> #solutionProgram </program>
    <input> pyList(XS:PyVals) </input>
    <result> noResult => #byLength(XS) </result>
endmodule
