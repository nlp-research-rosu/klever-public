requires "stage4-body-mutant-verification.k"

module AUDIT-BODY-MUTANT-SPEC
  imports AUDIT-BODY-MUTANT-VERIFICATION

  claim <mpy>
          <k> solutionProgramBodyMutant => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(12), VInt(1)) </args>
          <result> VNone => VString("21") </result>
        </mpy>
endmodule
