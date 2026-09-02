requires "verification.k"

module AUDIT-CLAIM-4-EXAMPLE-12-2
  imports VERIFICATION

  claim <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(12), VInt(2)) </args>
          <result> VNone => VString("12") </result>
        </mpy>
endmodule
