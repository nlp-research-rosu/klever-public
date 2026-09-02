requires "verification.k"

module SPEC
  imports VERIFICATION

  // The two examples in the original HumanEval prompt.
  claim <py>
          <k> SFTest(ListExpr(Int(15), Int(-73), Int(14), Int(-15)))
              => intVal(1) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>

  claim <py>
          <k> SFTest(ListExpr(Int(33), Int(-2), Int(-3), Int(45), Int(21), Int(109)))
              => intVal(2) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>

  // Empty input and the strict lower boundary (> 10).
  claim <py>
          <k> SFTest(ListExpr(.Exprs)) => intVal(0) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>

  claim <py>
          <k> SFTest(ListExpr(Int(-999), Int(-11), Int(0), Int(1), Int(9), Int(10)))
              => intVal(0) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>

  // Cover every leading/trailing parity combination and several digit widths.
  claim <py>
          <k> SFTest(ListExpr(Int(11), Int(12), Int(21), Int(22),
                              Int(313), Int(314), Int(423), Int(424),
                              Int(50005), Int(70008), Int(80007), Int(90009)))
              => intVal(4) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>

  // Repetition demonstrates that the result is a count, not a set cardinality.
  claim <py>
          <k> SFTest(ListExpr(Int(15), Int(15), Int(15), Int(20), Int(20)))
              => intVal(3) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>

  // Symbolic contract checks.  Together these partition every integer up to
  // 99, and the last two claims partition all three-digit positive integers.
  claim <py>
          <k> SFTest(ListExpr(Int(N:Int))) => intVal(0) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>
    requires N <=Int 10

  claim <py>
          <k> SFTest(ListExpr(Int(N:Int))) => intVal(1) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>
    requires 11 <=Int N andBool N <=Int 99
      andBool N %Int 2 ==Int 1
      andBool (N /Int 10) %Int 2 ==Int 1

  claim <py>
          <k> SFTest(ListExpr(Int(N:Int))) => intVal(0) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>
    requires 11 <=Int N andBool N <=Int 99
      andBool notBool (N %Int 2 ==Int 1
        andBool (N /Int 10) %Int 2 ==Int 1)

  claim <py>
          <k> SFTest(ListExpr(Int(N:Int))) => intVal(1) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>
    requires 100 <=Int N andBool N <=Int 999
      andBool N %Int 2 ==Int 1
      andBool (N /Int 100) %Int 2 ==Int 1

  claim <py>
          <k> SFTest(ListExpr(Int(N:Int))) => intVal(0) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>
    requires 100 <=Int N andBool N <=Int 999
      andBool notBool (N %Int 2 ==Int 1
        andBool (N /Int 100) %Int 2 ==Int 1)
endmodule
