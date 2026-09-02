requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false result mutation of the real example-input claim:
  // the satisfying input "10" returns 10, not 11.
  claim [false-ten-to-eleven]:
    <k> solutionProgram => .K </k>
    <arg> pyStr("10") </arg>
    <env> .Map =>
      ("value" |-> pyStr("10")
       "number" |-> exactNum(10, 1)
       "half" |-> exactNum(5, 10))
    </env>
    <result> noResult => pyInt(11) </result>
endmodule
