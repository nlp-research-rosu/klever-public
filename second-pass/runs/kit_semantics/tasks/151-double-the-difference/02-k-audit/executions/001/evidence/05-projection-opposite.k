requires "verification.k"

module PROJECTION-OPPOSITE
  imports VERIFICATION

  // Deliberately false: on an actual Int, the projection is the Int itself.
  claim [wrong-projection]:
    <k> projectIntTotal(3) => 4 </k>
endmodule
