requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: same_chars("", "") returns true, not false.
  claim [false-empty-empty]:
    <k> solutionProgram => .K </k>
    <s0> "" </s0>
    <s1> "" </s1>
    <env>
      .Map
      => ("s0" |-> stringValue("")) ("s1" |-> stringValue(""))
    </env>
    <result>
      noResult => result(boolValue(false))
    </result>
endmodule
