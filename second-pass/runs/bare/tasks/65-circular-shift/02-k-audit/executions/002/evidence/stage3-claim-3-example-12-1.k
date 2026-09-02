requires "verification.k"

module AUDIT-CLAIM-3-EXAMPLE-12-1
  imports VERIFICATION

  claim <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(12), VInt(1)) </args>
          <result> VNone => VString("21") </result>
        </mpy>
endmodule
