requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh false result obligation: the real program returns 15 on "14.5".
  claim
    <k> solutionProgram => .K </k>
    <arg> pyStr("14.5") </arg>
    <env> .Map =>
      ("value" |-> pyStr("14.5")
       "number" |-> exactNum(145, 10)
       "half" |-> exactNum(5, 10))
    </env>
    <result> noResult => pyInt(14) </result>
endmodule
