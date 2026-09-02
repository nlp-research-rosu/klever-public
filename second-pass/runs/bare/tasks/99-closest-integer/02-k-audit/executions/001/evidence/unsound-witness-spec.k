requires "verification.k"

module UNSOUND-WITNESS-SPEC
  imports VERIFICATION

  // K proves the exact-rational result below, but the submitted Python program
  // returns 10000000000000000000000000000 under its default Decimal context.
  claim [positive-context-witness]:
    <k> solutionProgram => .K </k>
    <arg> pyStr("9999999999999999999999999999.4") </arg>
    <env> .Map =>
      ("value" |-> pyStr("9999999999999999999999999999.4")
       "number" |-> exactNum(99999999999999999999999999994, 10)
       "half" |-> exactNum(5, 10))
    </env>
    <result>
      noResult => pyInt(9999999999999999999999999999)
    </result>

  // K proves the symmetric exact-rational result, but Python returns
  // -10000000000000000000000000000.
  claim [negative-context-witness]:
    <k> solutionProgram => .K </k>
    <arg> pyStr("-9999999999999999999999999999.4") </arg>
    <env> .Map =>
      ("value" |-> pyStr("-9999999999999999999999999999.4")
       "number" |-> exactNum(-99999999999999999999999999994, 10)
       "half" |-> exactNum(5, 10))
    </env>
    <result>
      noResult => pyInt(-9999999999999999999999999999)
    </result>
endmodule
