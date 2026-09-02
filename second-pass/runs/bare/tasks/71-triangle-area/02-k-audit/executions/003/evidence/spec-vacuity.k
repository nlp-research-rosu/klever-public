requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the actual result lacks the added one hundredth.
  // (A,B,C)=(3,4,5) satisfies the precondition and yields 600, not 601.
  claim
    <triangle>
      <k> launch(solutionProgram, Args(VInt(A), VInt(B), VInt(C))) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result>
        NoResult =>
          VRounded(sqrtHundredths(heronRadicand(A, B, C)) +Int 1)
      </result>
    </triangle>
    requires A +Int B >Int C
     andBool A +Int C >Int B
     andBool B +Int C >Int A
endmodule
