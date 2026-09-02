module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: get_row([], 1) returns [], not [(0, 0)].
  claim [false-empty-nonempty]:
      <k> solutionProgram ~> start => .K </k>
      <args> pyArgs(pyList(vnil), pyInt(1)) </args>
      <env> .Map </env>
      <functions> .Map </functions>
      <result>
        noResult => returned(pyList(
          vcons(pyTuple(vcons(pyInt(0), vcons(pyInt(0), vnil))), vnil)))
      </result>
endmodule
