requires "verification-base.k"

module AUDIT-PROJECTION-OPPOSITE
  imports VERIFICATION-BASE

  // Reviewer-authored opposite interpretation. The guarded integer projection
  // must not admit 98 as the result of projecting the represented integer 99.
  claim [wrong-projection]:
    <k> projectIntTotal(99) => 98 </k>
endmodule
