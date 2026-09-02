requires "verification.k"

module SPEC-GROUND-EVAL
  imports VERIFICATION

  claim [ground-8-2]:
    <k> simplePower(8, 2) => true ... </k>

  claim [ground-3-2]:
    <k> simplePower(3, 2) => false ... </k>

  claim [ground-neg8-neg2]:
    <k> simplePower(-8, -2) => true ... </k>

  claim [ground-0-0]:
    <k> simplePower(0, 0) => true ... </k>
endmodule
