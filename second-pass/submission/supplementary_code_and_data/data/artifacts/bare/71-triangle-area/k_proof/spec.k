requires "verification.k"

module SPEC
  imports VERIFICATION

  // The prompt's valid example: 6.00 is represented as 600 hundredths.
  claim
    <triangle>
      <k> launch(solutionProgram, Args(VInt(3), VInt(4), VInt(5))) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> NoResult => VRounded(600) </result>
    </triangle>

  // A second exact Heron case exercises the complete valid path.
  claim
    <triangle>
      <k> launch(solutionProgram, Args(VInt(5), VInt(12), VInt(13))) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> NoResult => VRounded(3000) </result>
    </triangle>

  // This case exercises square-root approximation and decimal rounding.
  claim
    <triangle>
      <k> launch(solutionProgram, Args(VInt(2), VInt(2), VInt(2))) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> NoResult => VRounded(173) </result>
    </triangle>

  // For every valid integer triangle, symbolic execution establishes that the
  // implementation returns the rounded square root of Heron's radicand.
  claim
    <triangle>
      <k> launch(solutionProgram, Args(VInt(A), VInt(B), VInt(C))) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result>
        NoResult => VRounded(sqrtHundredths(heronRadicand(A, B, C)))
      </result>
    </triangle>
    requires A +Int B >Int C
     andBool A +Int C >Int B
     andBool B +Int C >Int A

  // Every invalid integer triangle reaches exactly one of these three claims,
  // according to the source program's left-to-right guard order.
  claim
    <triangle>
      <k> launch(solutionProgram, Args(VInt(A), VInt(B), VInt(C))) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> NoResult => VInt(-1) </result>
    </triangle>
    requires A +Int B <=Int C

  claim
    <triangle>
      <k> launch(solutionProgram, Args(VInt(A), VInt(B), VInt(C))) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> NoResult => VInt(-1) </result>
    </triangle>
    requires A +Int B >Int C
     andBool A +Int C <=Int B

  claim
    <triangle>
      <k> launch(solutionProgram, Args(VInt(A), VInt(B), VInt(C))) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> NoResult => VInt(-1) </result>
    </triangle>
    requires A +Int B >Int C
     andBool A +Int C >Int B
     andBool B +Int C <=Int A
endmodule
