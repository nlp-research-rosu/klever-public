requires "verification.k"

module AUDIT-LOOP-SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation of the submitted symbolic loop claim.  The added
  // trailing "X" is false already for S = "", R = "", C = "", M = "",
  // FS = .Map, and RES = noResult.
  claim [false-loop-trailing-x]:
    <k> loopString("char", S, encodeLoopBody()) => .K </k>
    <env>
      "char"    |-> pyStr(C)
      "message" |-> pyStr(M)
      "result"  |-> pyStr(R)
    =>
      "char"    |-> pyStr(?C)
      "message" |-> pyStr(M)
      "result"  |-> pyStr((R +String encodeSpec(S)) +String "X")
    </env>
    <functions> FS </functions>
    <result> RES </result>
endmodule
