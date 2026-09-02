requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh audit mutation of candidate claim 3.
  // For the satisfying input [0, 2], the real and modeled result is [0, 1],
  // so changing the second component to 0 must leave an unmet obligation.
  claim [false-result]:
    <python>
      <k> verify(solutionProgram, vlist(0, 2, .Rats))
           => done(vlist(0, 0, .Rats))
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>
endmodule
