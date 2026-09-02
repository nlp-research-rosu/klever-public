module SPEC-VACUITY
  imports VERIFICATION

  // False for the satisfying input []: the actual return is [], not [(0, 0)].
  claim [false-empty-result]:
      <k> solutionProgram ~> start => .K </k>
      <args> pyArgs(pyList(vnil), pyInt(1)) </args>
      <env> .Map </env>
      <functions> .Map </functions>
      <result>
        noResult
          => returned(pyList(
               vcons(pyTuple(vcons(pyInt(0), vcons(pyInt(0), vnil))), vnil)))
      </result>
endmodule
