requires "base-verification.k"

module CONNECTION-SPEC
  imports VERIFICATION-BASE

  claim [cmp-int]:
    <k> applyCmp("<", I:Int, T:Int) => numericLt(I, T) </k>

  claim [cmp-bool]:
    <k> applyCmp("<", B:Bool, T:Int) => numericLt(B, T) </k>

  claim [cmp-float]:
    <k> applyCmp("<", F:Float, T:Int) => numericLt(F, T) </k>
endmodule
