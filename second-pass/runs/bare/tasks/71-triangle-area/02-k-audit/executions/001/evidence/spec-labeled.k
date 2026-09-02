requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [example-3-4-5]:
    <triangle>
      <k> launch(solutionProgram, Args(VInt(3), VInt(4), VInt(5))) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> NoResult => VRounded(600) </result>
    </triangle>

  claim [example-5-12-13]:
    <triangle>
      <k> launch(solutionProgram, Args(VInt(5), VInt(12), VInt(13))) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> NoResult => VRounded(3000) </result>
    </triangle>

  claim [example-2-2-2]:
    <triangle>
      <k> launch(solutionProgram, Args(VInt(2), VInt(2), VInt(2))) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> NoResult => VRounded(173) </result>
    </triangle>

  claim [valid-universal]:
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

  claim [invalid-first]:
    <triangle>
      <k> launch(solutionProgram, Args(VInt(A), VInt(B), VInt(C))) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> NoResult => VInt(-1) </result>
    </triangle>
    requires A +Int B <=Int C

  claim [invalid-second]:
    <triangle>
      <k> launch(solutionProgram, Args(VInt(A), VInt(B), VInt(C))) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> NoResult => VInt(-1) </result>
    </triangle>
    requires A +Int B >Int C
     andBool A +Int C <=Int B

  claim [invalid-third]:
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
