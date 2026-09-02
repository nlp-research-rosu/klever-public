requires "verification.k"

module SPEC-GENERAL-ONLY
  imports VERIFICATION

  claim
    <py>
      <k>
        solutionProgram ~> invokeFruit(A:Int, O:Int, N:Int)
        => VInt(N -Int A -Int O)
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
    </py>
    requires (A >=Int 0) andBool (O >=Int 0) andBool (N >=Int A +Int O)
endmodule
