requires "verification-base.k"

module PROJECTION-POSITIVE
  imports VERIFICATION-BASE

  claim [positive-five]:
    <k> projectIntTotal(5) => 5 </k>

  claim [negative-seven]:
    <k> projectIntTotal(-7) => -7 </k>
endmodule
