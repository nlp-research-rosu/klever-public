requires "verification.k"

module SPEC
  imports VERIFICATION

  // Every valid fruit description is represented by VFruits(A, O).  The
  // implementation must return the unallocated fruit count for arbitrary
  // nonnegative counts whose sum does not exceed the basket total.
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

  claim
    <py>
      <k> solutionProgram ~> invokeString("5 apples and 6 oranges", 19) => VInt(8) </k>
      <functions> .Map </functions>
      <env> .Map </env>
    </py>

  claim
    <py>
      <k> solutionProgram ~> invokeString("0 apples and 1 oranges", 3) => VInt(2) </k>
      <functions> .Map </functions>
      <env> .Map </env>
    </py>

  claim
    <py>
      <k> solutionProgram ~> invokeString("2 apples and 3 oranges", 100) => VInt(95) </k>
      <functions> .Map </functions>
      <env> .Map </env>
    </py>

  claim
    <py>
      <k> solutionProgram ~> invokeString("100 apples and 1 oranges", 120) => VInt(19) </k>
      <functions> .Map </functions>
      <env> .Map </env>
    </py>
endmodule
