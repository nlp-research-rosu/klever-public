requires "fixed-only.k"

module FIXED-CONNECTION-SPEC
  imports FIXED-ONLY

  claim [isinstance-int]:
    <k> isIntV(I:Int) => true </k>

  claim [greater-than-int]:
    <k> applyCmp(">", I:Int, J:Int) => I >Int J </k>

  claim [modulo-int]:
    <k> applyBin("%", I:Int, J:Int) => pyMod(I, J) </k>

  claim [multiply-int]:
    <k> applyBin("*", I:Int, J:Int) => I *Int J </k>

  // Bridge-free dynamic-sort formulations of the proof-local derived rules.
  claim [isinstance-dynamic]:
    <k> isIntV(V:Val) => isInt(V) </k>

  claim [greater-than-dynamic]:
    <k>
      applyCmp(">", V:Val, J:Int)
      => {V}:>Int >Int J
    </k>
    requires isInt(V)

  claim [modulo-dynamic]:
    <k>
      applyBin("%", V:Val, J:Int)
      => pyMod({V}:>Int, J)
    </k>
    requires isInt(V)

  claim [multiply-dynamic]:
    <k>
      applyBin("*", V1:Val, V2:Val)
      => {V1}:>Int *Int {V2}:>Int
    </k>
    requires isInt(V1) andBool isInt(V2)
endmodule
