requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports MPY-VERIFICATION

  // Fresh reviewer mutation: the real result is (2, 11/5), not (2, 12/5).
  claim
    <mpy>
      <k> run(solution, nums(1, 2, 3, 4, 5, 11 /Rat 5)) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => vtuple(vnum(2), vnum(12 /Rat 5)) </result>
    </mpy>
endmodule
