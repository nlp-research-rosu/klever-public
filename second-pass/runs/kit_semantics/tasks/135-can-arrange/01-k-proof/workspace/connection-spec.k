requires "verification.k"

module CONNECTION-SPEC
  imports VERIFICATION-BASE

  claim [ge-int-int]:
    <k> applyCmp(">=", I:Int, J:Int) => orderGe(I, J) </k>

  claim [ge-bool-bool]:
    <k> applyCmp(">=", B:Bool, C:Bool) => orderGe(B, C) </k>

  claim [ge-bool-int]:
    <k> applyCmp(">=", B:Bool, I:Int) => orderGe(B, I) </k>

  claim [ge-int-bool]:
    <k> applyCmp(">=", I:Int, B:Bool) => orderGe(I, B) </k>

  claim [ge-float-float]:
    <k> applyCmp(">=", F:Float, G:Float) => orderGe(F, G) </k>

  claim [ge-int-float]:
    <k> applyCmp(">=", I:Int, F:Float) => orderGe(I, F) </k>

  claim [ge-float-int]:
    <k> applyCmp(">=", F:Float, I:Int) => orderGe(F, I) </k>

  claim [ge-bool-float]:
    <k> applyCmp(">=", B:Bool, F:Float) => orderGe(B, F) </k>

  claim [ge-float-bool]:
    <k> applyCmp(">=", F:Float, B:Bool) => orderGe(F, B) </k>

  claim [ge-str-str]:
    <k>
      applyCmp(">=", str(A:IntSeq), str(B:IntSeq))
      => orderGe(str(A), str(B))
    </k>
endmodule
