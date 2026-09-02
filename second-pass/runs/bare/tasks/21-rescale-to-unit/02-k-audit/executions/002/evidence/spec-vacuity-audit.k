// Fresh false result mutation of candidate claim 3: the real result is [0, 1].
requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  claim [false-endpoint]:
    <python>
      <k> verify(solutionProgram, vlist(A, B, .Rats))
           => done(vlist(0, 2, .Rats))
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>
    requires A <Rat B
endmodule
