requires "verification.k"

module SPEC-VACUITY-REVIEWER
  imports VERIFICATION

  // Reviewer mutation: the destination is deliberately one too large.
  // Ground witness A=5, O=6, N=19 expects actual 8 but mutated destination 9.
  claim
    <py>
      <k>
        solutionProgram ~> invokeFruit(A:Int, O:Int, N:Int)
        => VInt(N -Int A -Int O +Int 1)
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
    </py>
    requires (A >=Int 0) andBool (O >=Int 0) andBool (N >=Int A +Int O)
endmodule
