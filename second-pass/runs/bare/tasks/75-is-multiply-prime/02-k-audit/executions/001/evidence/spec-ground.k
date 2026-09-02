requires "verification.k"

module SPEC-GROUND
  imports VERIFICATION

  // Satisfying witness: 30 < 100, empty environment, no initial result.
  claim
    <k> solutionProgram => .K </k>
    <arg> 30 </arg>
    <env> .Map </env>
    <result> noResult => Bool(true) </result>

  // A second satisfying witness exercises the false result.
  claim
    <k> solutionProgram => .K </k>
    <arg> 10 </arg>
    <env> .Map </env>
    <result> noResult => Bool(false) </result>
endmodule
