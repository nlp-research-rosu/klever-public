requires "bridgefree-verification.k"

module BRIDGEFREE-SPEC
  imports VERIFICATION

  claim [int-int]:
    <k> applyCmp(">", I:Int, J:Int)
      => numericGt(numericView(I), numericView(J)) ... </k>

  claim [int-bool]:
    <k> applyCmp(">", I:Int, B:Bool)
      => numericGt(numericView(I), numericView(B)) ... </k>

  claim [bool-int]:
    <k> applyCmp(">", B:Bool, I:Int)
      => numericGt(numericView(B), numericView(I)) ... </k>

  claim [bool-bool]:
    <k> applyCmp(">", B1:Bool, B2:Bool)
      => numericGt(numericView(B1), numericView(B2)) ... </k>

  claim [float-float]:
    <k> applyCmp(">", F1:Float, F2:Float)
      => numericGt(numericView(F1), numericView(F2)) ... </k>

  claim [int-float]:
    <k> applyCmp(">", I:Int, F:Float)
      => numericGt(numericView(I), numericView(F)) ... </k>

  claim [float-int]:
    <k> applyCmp(">", F:Float, I:Int)
      => numericGt(numericView(F), numericView(I)) ... </k>

  claim [bool-float]:
    <k> applyCmp(">", B:Bool, F:Float)
      => numericGt(numericView(B), numericView(F)) ... </k>

  claim [float-bool]:
    <k> applyCmp(">", F:Float, B:Bool)
      => numericGt(numericView(F), numericView(B)) ... </k>

  claim [str-str]:
    <k> applyCmp(">", S1:Str, S2:Str)
      => strLt(codesOf(S2), codesOf(S1)) ... </k>

endmodule
