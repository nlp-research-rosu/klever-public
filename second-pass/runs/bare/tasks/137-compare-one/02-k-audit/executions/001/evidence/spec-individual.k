module SPEC-01
  imports VERIFICATION
  claim [claim-01]:
    <k> theSolution ~> invoke(pyInt(I), pyInt(J)) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyNone </result>
    requires I ==Int J
endmodule

module SPEC-02
  imports VERIFICATION
  claim [claim-02]:
    <k> theSolution ~> invoke(pyInt(I), pyInt(J)) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyInt(I) </result>
    requires I >Int J
endmodule

module SPEC-03
  imports VERIFICATION
  claim [claim-03]:
    <k> theSolution ~> invoke(pyInt(I), pyInt(J)) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyInt(J) </result>
    requires I <Int J
endmodule

module SPEC-04
  imports VERIFICATION
  claim [claim-04]:
    <k> theSolution ~> invoke(pyFloat(N1, D1), pyFloat(N2, D2)) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyNone </result>
    requires D1 >Int 0 andBool D2 >Int 0
     andBool (N1 *Int D2) ==Int (N2 *Int D1)
endmodule

module SPEC-05
  imports VERIFICATION
  claim [claim-05]:
    <k> theSolution ~> invoke(pyFloat(N1, D1), pyFloat(N2, D2)) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyFloat(N1, D1) </result>
    requires D1 >Int 0 andBool D2 >Int 0
     andBool (N1 *Int D2) >Int (N2 *Int D1)
endmodule

module SPEC-06
  imports VERIFICATION
  claim [claim-06]:
    <k> theSolution ~> invoke(pyFloat(N1, D1), pyFloat(N2, D2)) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyFloat(N2, D2) </result>
    requires D1 >Int 0 andBool D2 >Int 0
     andBool (N1 *Int D2) <Int (N2 *Int D1)
endmodule

module SPEC-07
  imports VERIFICATION
  claim [claim-07]:
    <k> theSolution ~> invoke(pyInt(1), pyFloat(25, 10)) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyFloat(25, 10) </result>
endmodule

module SPEC-08
  imports VERIFICATION
  claim [claim-08]:
    <k> theSolution ~> invoke(pyInt(1), pyStr("2,3")) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyStr("2,3") </result>
endmodule

module SPEC-09
  imports VERIFICATION
  claim [claim-09]:
    <k> theSolution ~> invoke(pyStr("5,1"), pyStr("6")) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyStr("6") </result>
endmodule

module SPEC-10
  imports VERIFICATION
  claim [claim-10]:
    <k> theSolution ~> invoke(pyStr("1"), pyInt(1)) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyNone </result>
endmodule
