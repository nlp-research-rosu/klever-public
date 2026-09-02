requires "verification.k"

module AUDIT-CLAIM-6-OVERSIZED-1234-5
  imports VERIFICATION

  claim <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(1234), VInt(5)) </args>
          <result> VNone => VString("4321") </result>
        </mpy>
endmodule
