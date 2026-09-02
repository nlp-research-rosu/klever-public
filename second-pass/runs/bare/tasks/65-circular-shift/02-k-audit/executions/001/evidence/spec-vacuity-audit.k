requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh false mutation of the documented (12, 1) result.
  // The real and canonical result is "21"; this deliberately requires "12".
  claim [false-result-12-1]:
        <mpy>
          <k> solutionProgram => .K </k>
          <entry> "circular_shift" </entry>
          <args> (VInt(12), VInt(1)) </args>
          <result> VNone => VString("12") </result>
        </mpy>
endmodule
