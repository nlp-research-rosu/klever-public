module SPEC
  imports VERIFICATION

  // For arbitrary integers, equality returns None.
  claim
    <k> theSolution ~> invoke(pyInt(I), pyInt(J)) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyNone </result>
    requires I ==Int J

  // For arbitrary integers, the larger original argument is returned.
  claim
    <k> theSolution ~> invoke(pyInt(I), pyInt(J)) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyInt(I) </result>
    requires I >Int J

  claim
    <k> theSolution ~> invoke(pyInt(I), pyInt(J)) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyInt(J) </result>
    requires I <Int J

  // Floats are modeled exactly as N / D, with positive denominators.
  claim
    <k> theSolution ~> invoke(pyFloat(N1, D1), pyFloat(N2, D2)) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyNone </result>
    requires D1 >Int 0 andBool D2 >Int 0
     andBool (N1 *Int D2) ==Int (N2 *Int D1)

  claim
    <k> theSolution ~> invoke(pyFloat(N1, D1), pyFloat(N2, D2)) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyFloat(N1, D1) </result>
    requires D1 >Int 0 andBool D2 >Int 0
     andBool (N1 *Int D2) >Int (N2 *Int D1)

  claim
    <k> theSolution ~> invoke(pyFloat(N1, D1), pyFloat(N2, D2)) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyFloat(N2, D2) </result>
    requires D1 >Int 0 andBool D2 >Int 0
     andBool (N1 *Int D2) <Int (N2 *Int D1)

  // Original prompt examples, including comma-decimal normalization.
  claim
    <k> theSolution ~> invoke(pyInt(1), pyFloat(25, 10)) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyFloat(25, 10) </result>

  claim
    <k> theSolution ~> invoke(pyInt(1), pyStr("2,3")) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyStr("2,3") </result>

  claim
    <k> theSolution ~> invoke(pyStr("5,1"), pyStr("6")) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyStr("6") </result>

  claim
    <k> theSolution ~> invoke(pyStr("1"), pyInt(1)) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyNone </result>
endmodule
