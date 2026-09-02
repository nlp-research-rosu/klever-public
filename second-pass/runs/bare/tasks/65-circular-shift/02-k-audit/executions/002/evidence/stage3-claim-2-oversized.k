requires "verification.k"

module AUDIT-CLAIM-2-OVERSIZED
  imports VERIFICATION

  claim <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(X), VInt(SHIFT)) </args>
          <result> VNone => VString(reverseString(Int2String(X))) </result>
        </mpy>
    requires lengthString(Int2String(X)) <Int SHIFT
endmodule
