requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: for the prompt input, replace the final 11 with 12.
  claim [label(false-prompt-result)]:
        <py>
          <k> init => .K </k>
          <program> solutionProgram </program>
          <input>
            ListExpr(Int(1), Int(11), Int(-1), Int(-11), Int(-12))
          </input>
          <output>
            NoValue =>
            ListVal(IntVal(-1), IntVal(-11), IntVal(1), IntVal(-12), IntVal(12))
          </output>
        </py>
endmodule
