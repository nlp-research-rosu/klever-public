requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Exact loop invariant from the candidate, retained as the entry proof's
  // required circularity.
  claim
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

  // Fresh false mutation: for the satisfying input n = 5, the actual result
  // ends in "5", not "6".
  claim
    <mpy>
      <k> init(targetProgram(), 5) => SVal("0 1 2 3 4 6") </k>
      <env> .Map </env>
      <functions>
        .Map => "string_sequence" |-> targetFunction()
      </functions>
      <stack> .List </stack>
    </mpy>
endmodule
