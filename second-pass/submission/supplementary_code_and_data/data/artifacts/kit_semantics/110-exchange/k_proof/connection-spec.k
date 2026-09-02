requires "verification.k"

module CONNECTION-SPEC
  imports VERIFICATION-BASE

  // These claims deliberately import VERIFICATION-BASE, not VERIFICATION, so
  // the operational parity bridge is unavailable while its value is proved.
  claim [parity-int]:
    <k>
      applyCmp("==", applyBin("%", I:Int, 2), 0)
      => numberEven(I)
      ...
    </k>

  claim [parity-bool]:
    <k>
      applyCmp("==", applyBin("%", B:Bool, 2), 0)
      => numberEven(B)
      ...
    </k>

  claim [parity-float]:
    <k>
      applyCmp("==", applyBin("%", F:Float, 2), 0)
      => numberEven(F)
      ...
    </k>

  // Source-expression execution reaches the same connected value under the
  // bridge-free definition, including literal evaluation and operator routing.
  claim [parity-int-exec]:
    <k>
      Compare(BinOp("%", I:Int, 2), CmpOp("==", Int(0)))
      => numberEven(I)
      ...
    </k>

  claim [parity-bool-exec]:
    <k>
      Compare(BinOp("%", B:Bool, 2), CmpOp("==", Int(0)))
      => numberEven(B)
      ...
    </k>

  claim [parity-float-exec]:
    <k>
      Compare(BinOp("%", F:Float, 2), CmpOp("==", Int(0)))
      => numberEven(F)
      ...
    </k>
endmodule
