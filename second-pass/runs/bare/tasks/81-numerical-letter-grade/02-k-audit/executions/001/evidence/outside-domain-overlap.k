requires "verification.k"

module OUTSIDE-DOMAIN-OVERLAP
  imports VERIFICATION

  // Q = -1 is deliberately outside every candidate entry precondition.
  // Both expectedGrade equations' guards are true at P = 0, Q = -1.
  claim [to-a]:
    <k> expectedGrade(0, -1) => str("A") </k>

  claim [to-e]:
    <k> expectedGrade(0, -1) => str("E") </k>
endmodule
