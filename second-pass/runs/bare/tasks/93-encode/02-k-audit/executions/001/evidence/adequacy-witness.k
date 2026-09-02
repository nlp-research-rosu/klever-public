requires "../../tmp/audit-work/93-encode/concrete.k"
requires "../../tmp/audit-work/93-encode/verification.k"

module AUDIT-ADEQUACY-WITNESS
  imports CONCRETE
  imports VERIFICATION

  // A satisfiable ground instance of the submitted symbolic loop claim:
  // S = "ab", R = "P", C = "x", M = "ab", FS = .Map, RES = noResult.
  claim [loop-ground-instance]:
    <k> loopString("char", "ab", encodeLoopBody()) => .K </k>
    <env>
      "char"    |-> pyStr("x")
      "message" |-> pyStr("ab")
      "result"  |-> pyStr("P")
    =>
      "char"    |-> pyStr(?C)
      "message" |-> pyStr("ab")
      "result"  |-> pyStr("PCB")
    </env>
    <functions> .Map </functions>
    <result> noResult </result>
endmodule
