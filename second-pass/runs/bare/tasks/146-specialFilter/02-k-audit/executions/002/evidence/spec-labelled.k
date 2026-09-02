requires "verification.k"

module SPEC-LABELLED
  imports VERIFICATION

  // The two examples in the original HumanEval prompt.
  claim [c01]: <py>
          <k> SFTest(ListExpr(Int(15), Int(-73), Int(14), Int(-15)))
              => intVal(1) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>

  claim [c02]: <py>
          <k> SFTest(ListExpr(Int(33), Int(-2), Int(-3), Int(45), Int(21), Int(109)))
              => intVal(2) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>

  // Empty input and the strict lower boundary (> 10).
  claim [c03]: <py>
          <k> SFTest(ListExpr(.Exprs)) => intVal(0) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>

  claim [c04]: <py>
          <k> SFTest(ListExpr(Int(-999), Int(-11), Int(0), Int(1), Int(9), Int(10)))
              => intVal(0) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>

  // Cover every leading/trailing parity combination and several digit widths.
  claim [c05]: <py>
          <k> SFTest(ListExpr(Int(11), Int(12), Int(21), Int(22),
                              Int(313), Int(314), Int(423), Int(424),
                              Int(50005), Int(70008), Int(80007), Int(90009)))
              => intVal(4) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>

  // Repetition demonstrates that the result is a count, not a set cardinality.
  claim [c06]: <py>
          <k> SFTest(ListExpr(Int(15), Int(15), Int(15), Int(20), Int(20)))
              => intVal(3) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>

  // Symbolic contract checks.  Together these partition every integer up to
  // 99, and the last two claims partition all three-digit positive integers.
  claim [c07]: <py>
          <k> SFTest(ListExpr(Int(N:Int))) => intVal(0) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>
    requires N <=Int 10

  claim [c08]: <py>
          <k> SFTest(ListExpr(Int(N:Int))) => intVal(1) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>
    requires 11 <=Int N andBool N <=Int 99
      andBool N %Int 2 ==Int 1
      andBool (N /Int 10) %Int 2 ==Int 1

  claim [c09]: <py>
          <k> SFTest(ListExpr(Int(N:Int))) => intVal(0) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>
    requires 11 <=Int N andBool N <=Int 99
      andBool notBool (N %Int 2 ==Int 1
        andBool (N /Int 10) %Int 2 ==Int 1)

  claim [c10]: <py>
          <k> SFTest(ListExpr(Int(N:Int))) => intVal(1) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>
    requires 100 <=Int N andBool N <=Int 999
      andBool N %Int 2 ==Int 1
      andBool (N /Int 100) %Int 2 ==Int 1

  claim [c11]: <py>
          <k> SFTest(ListExpr(Int(N:Int))) => intVal(0) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>
    requires 100 <=Int N andBool N <=Int 999
      andBool notBool (N %Int 2 ==Int 1
        andBool (N /Int 100) %Int 2 ==Int 1)
endmodule
