requires "verification.k"

module SPEC-CONNECTION
  imports VERIFICATION-BASE

  // Together these two claims cover exactly numericVal(V): Int or Float.
  // They are proved with a definition that does not import VERIFICATION's
  // guarded dynamic-dispatch simplification rule.
  claim [compare-int-connection]:
    <k>
      Compare(I:Int, CmpOp(">", Float(0.0)))
      => positiveNumeric(I)
      ...
    </k>

  claim [compare-float-connection]:
    <k>
      Compare(F:Float, CmpOp(">", Float(0.0)))
      => positiveNumeric(F)
      ...
    </k>

  claim [applycmp-int-connection]:
    <k>
      applyCmp(">", I:Int, 0.0)
      => positiveNumeric(I)
      ...
    </k>

  claim [applycmp-float-connection]:
    <k>
      applyCmp(">", F:Float, 0.0)
      => positiveNumeric(F)
      ...
    </k>
endmodule
