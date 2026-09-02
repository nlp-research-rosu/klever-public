requires "verification.k"

module AUDIT-SPEC-GROUND-SUMMARIES
  imports VERIFICATION

  // Concrete substitutions witnessing every entry-claim precondition.
  claim
    <k> .K </k>
    <arg> 0 </arg>
    <result> strVal(decimalToBinarySpec(0)) => strVal("db0db") </result>

  claim
    <k> .K </k>
    <arg> -1 </arg>
    <result> strVal(decimalToBinarySpec(-1)) => strVal("dbb1db") </result>

  claim
    <k> .K </k>
    <arg> 15 </arg>
    <result> strVal(decimalToBinarySpec(15)) => strVal("db1111db") </result>

  claim
    <k> .K </k>
    <arg> 32 </arg>
    <result> strVal(decimalToBinarySpec(32)) => strVal("db100000db") </result>

  claim
    <k> .K </k>
    <arg> -5 </arg>
    <result> strVal(decimalToBinarySpec(-5)) => strVal("dbb101db") </result>
endmodule
