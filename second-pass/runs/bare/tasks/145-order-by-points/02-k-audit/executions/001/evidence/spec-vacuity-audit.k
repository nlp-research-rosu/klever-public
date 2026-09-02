requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh false mutation: the final result element is changed from 11 to 12.
  // Satisfying witness input: [1, 11, -1, -11, -12].
  claim <py>
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
