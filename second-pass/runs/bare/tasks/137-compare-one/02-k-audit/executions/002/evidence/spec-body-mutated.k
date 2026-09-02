module SPEC-BODY-MUTATED
  imports VERIFICATION-BODY-MUTATED

  claim [int-lt-original-obligation]:
    <k> theSolutionBodyMutated ~> invoke(pyInt(I), pyInt(J)) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyInt(J) </result>
    requires I <Int J
endmodule
