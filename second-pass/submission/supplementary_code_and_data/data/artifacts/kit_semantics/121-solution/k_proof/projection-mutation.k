requires "verification-base.k"

module PROJECTION-MUTATION
  imports VERIFICATION-BASE

  // Deliberately false opposite interpretation.
  claim [five-is-six]:
    <k> projectIntTotal(5) => 6 </k>
endmodule
