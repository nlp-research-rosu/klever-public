requires "verification-body-mut.k"

module SPEC-BODY-MUT
  imports VERIFICATION-BODY-MUT

  claim
    <py>
      <k>
        solutionProgramMut ~> invokeFruit(A:Int, O:Int, N:Int)
        => VInt(N -Int A -Int O)
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
    </py>
    requires (A >=Int 0) andBool (O >=Int 0) andBool (N >=Int A +Int O)
endmodule
