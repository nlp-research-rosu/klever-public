requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh false mutation: the real result is not one larger.
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
