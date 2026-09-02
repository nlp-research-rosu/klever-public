requires "semantic.k"

module SPEC-TOTALITY-PROBE
  imports SEMANTIC

  claim [negative-fib4-is-zero]:
    <fib4>
      <k> .K </k>
      <arg> 0 </arg>
      <env> .Map </env>
      <result> result(fib4Spec(-1)) => result(0) </result>
    </fib4>

  claim [unsupported-eval-is-seven]:
    <fib4>
      <k> .K </k>
      <arg> 0 </arg>
      <env> .Map </env>
      <result>
        result(evalInt(Compare(Int(1), CmpOp("==", Int(1))), .Map))
        => result(7)
      </result>
    </fib4>
endmodule
