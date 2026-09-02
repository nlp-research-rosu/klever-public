requires "verification.k"

module SPEC-PROJECTION-GROUND
  imports VERIFICATION

  claim [projection-three]:
    <k> intProjection(3) => 3 </k>

  claim [projection-four]:
    <k> intProjection(4) => 4 </k>

  claim [opposite-projection-three]:
    <k> intProjection(3) => 4 </k>
endmodule
