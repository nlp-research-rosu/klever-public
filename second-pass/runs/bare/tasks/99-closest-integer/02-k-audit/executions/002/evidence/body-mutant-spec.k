requires "body-mutant-verification.k"

module BODY-MUTANT-SPEC
  imports BODY-MUTANT-VERIFICATION

  claim
    <k> bodyMutantProgram => .K </k>
    <arg> pyStr("14.5") </arg>
    <env> .Map =>
      ("value" |-> pyStr("14.5")
       "number" |-> exactNum(145, 10)
       "half" |-> exactNum(5, 10))
    </env>
    <result> noResult => pyInt(15) </result>
endmodule
