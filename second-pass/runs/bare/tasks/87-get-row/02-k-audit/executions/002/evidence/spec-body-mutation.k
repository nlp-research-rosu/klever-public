module SPEC-BODY-MUTATION
  imports BODY-MUTATION-VERIFICATION

  // The original program returns [(1,0)] for [[],[0]], x=0.
  claim [detect-row-step-mutation]:
      <k> bodyMutatedProgram ~> start => .K </k>
      <args>
        pyArgs(
          pyList(vcons(pyList(vnil),
            vcons(pyList(vcons(pyInt(0), vnil)), vnil))),
          pyInt(0))
      </args>
      <env> .Map </env>
      <functions> .Map </functions>
      <result>
        noResult
          => returned(pyList(
               vcons(pyTuple(vcons(pyInt(1), vcons(pyInt(0), vnil))), vnil)))
      </result>
endmodule
