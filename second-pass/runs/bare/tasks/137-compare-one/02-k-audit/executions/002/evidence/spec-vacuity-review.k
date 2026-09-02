module SPEC-VACUITY-REVIEW
  imports VERIFICATION

  // Reviewer-authored false result mutation of the submitted int-gt claim.
  // Satisfying witness: I = 2, J = 1.  The program returns pyInt(2), not
  // pyInt(3), so this must be rejected after real execution reaches <result>.
  claim [false-int-gt-off-by-one]:
    <k> theSolution ~> invoke(pyInt(I), pyInt(J)) => .K </k>
    <functions> .Map => ?_FINALFUNCTIONS </functions>
    <env> .Map => ?_FINALENV </env>
    <result> pyNone => pyInt(I +Int 1) </result>
    requires I >Int J
endmodule
