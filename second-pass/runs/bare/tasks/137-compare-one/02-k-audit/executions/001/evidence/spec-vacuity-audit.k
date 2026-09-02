module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: for I > J the modeled program returns I, not I + 1.
  claim [false-off-by-one]:
    <k> theSolution ~> invoke(pyInt(I), pyInt(J)) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyInt(I +Int 1) </result>
    requires I >Int J
endmodule
