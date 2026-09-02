requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation: the real result is forced to carry an extra "!".
  // Witness X = 12, SHIFT = 1 satisfies the precondition; Python and K return
  // "21", while this destination requires "21!".
  claim <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(X), VInt(SHIFT)) </args>
          <result>
            VNone
            => VString(normalCircularShift(Int2String(X), SHIFT) +String "!")
          </result>
        </mpy>
    requires 0 <=Int SHIFT
     andBool SHIFT <=Int lengthString(Int2String(X))
endmodule
