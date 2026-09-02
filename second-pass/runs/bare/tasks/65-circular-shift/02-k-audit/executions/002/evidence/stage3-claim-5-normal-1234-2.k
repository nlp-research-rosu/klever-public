requires "verification.k"

module AUDIT-CLAIM-5-NORMAL-1234-2
  imports VERIFICATION

  claim <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(1234), VInt(2)) </args>
          <result> VNone => VString("3412") </result>
        </mpy>
endmodule
