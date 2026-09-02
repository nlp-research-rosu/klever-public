requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation of submitted c08: N=11 satisfies the precondition,
  // but specialFilter([11]) returns 1, not the mutated result 0.
  claim [false-result]: <py>
          <k> SFTest(ListExpr(Int(N:Int))) => intVal(0) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>
    requires 11 <=Int N andBool N <=Int 99
      andBool N %Int 2 ==Int 1
      andBool (N /Int 10) %Int 2 ==Int 1
endmodule
