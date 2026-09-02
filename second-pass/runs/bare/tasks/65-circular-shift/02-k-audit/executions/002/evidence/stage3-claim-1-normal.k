requires "verification.k"

module AUDIT-CLAIM-1-NORMAL
  imports VERIFICATION

  claim <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(X), VInt(SHIFT)) </args>
          <result> VNone => VString(normalCircularShift(Int2String(X), SHIFT)) </result>
        </mpy>
    requires 0 <=Int SHIFT
     andBool SHIFT <=Int lengthString(Int2String(X))
endmodule
