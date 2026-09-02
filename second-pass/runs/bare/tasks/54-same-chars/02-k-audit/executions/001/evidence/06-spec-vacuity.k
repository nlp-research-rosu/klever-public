requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false result mutation: both empty strings have equal character
  // sets, so the submitted program returns true, not false.
  claim [false-empty-result]:
    <k> solutionProgram => .K </k>
    <s0> "" </s0>
    <s1> "" </s1>
    <env> .Map => ("s0" |-> stringValue(""))
                 ("s1" |-> stringValue("")) </env>
    <result> noResult => result(boolValue(false)) </result>
endmodule
