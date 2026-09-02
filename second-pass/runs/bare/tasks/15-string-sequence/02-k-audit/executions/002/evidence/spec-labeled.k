requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [loop-invariant]:
    <mpy>
      <k> exec(While(loopCondition(), loopBody())) ~> KREST
         => KREST </k>
      <env>
        ( "i"      |-> IVal(I)
          "n"      |-> IVal(N)
          "result" |-> SVal(S)
          REST
        =>
          "i"      |-> IVal(indexAfter(I, N))
          "n"      |-> IVal(N)
          "result" |-> SVal(sequenceFrom(I, N, S))
          REST )
      </env>
      <functions> _FUNCTIONS </functions>
      <stack> _STACK </stack>
    </mpy>
    requires I >=Int 1 andBool N >=Int 0

  claim [entry-general]:
    <mpy>
      <k> init(targetProgram(), N) => SVal(sequence(N)) </k>
      <env> .Map </env>
      <functions>
        .Map => "string_sequence" |-> targetFunction()
      </functions>
      <stack> .List </stack>
    </mpy>

  claim [entry-zero]:
    <mpy>
      <k> init(targetProgram(), 0) => SVal("0") </k>
      <env> .Map </env>
      <functions>
        .Map => "string_sequence" |-> targetFunction()
      </functions>
      <stack> .List </stack>
    </mpy>

  claim [entry-five]:
    <mpy>
      <k> init(targetProgram(), 5) => SVal("0 1 2 3 4 5") </k>
      <env> .Map </env>
      <functions>
        .Map => "string_sequence" |-> targetFunction()
      </functions>
      <stack> .List </stack>
    </mpy>
endmodule
