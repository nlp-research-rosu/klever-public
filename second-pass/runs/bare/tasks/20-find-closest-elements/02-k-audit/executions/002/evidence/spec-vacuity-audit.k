requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports MPY-VERIFICATION

  // Deliberately false: the satisfying documented input returns (2, 11/5),
  // not (2, 5).  This changes only the result-constraining obligation.
  claim
    <mpy>
      <k> run(solution, nums(1, 2, 3, 4, 5, 11 /Rat 5)) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => vtuple(vnum(2), vnum(5)) </result>
    </mpy>
endmodule
