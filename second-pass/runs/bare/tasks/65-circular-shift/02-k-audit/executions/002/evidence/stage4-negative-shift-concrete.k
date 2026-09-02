requires "verification.k"

module AUDIT-NEGATIVE-SHIFT-CONCRETE
  imports VERIFICATION

  // This real source-domain input is outside both candidate symbolic claims.
  claim <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(1234), VInt(0 -Int 1)) </args>
          <result> VNone => VString("1234") </result>
        </mpy>
endmodule
