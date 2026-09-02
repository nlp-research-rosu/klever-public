requires "verification-body-mutated.k"

module SPEC-BODY-MUTATED
  imports MPY-VERIFICATION-BODY-MUTATED

  claim
    <mpy>
      <k> run(solution, nums(1, 2, 3, 4, 5, 11 /Rat 5)) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => vtuple(vnum(2), vnum(11 /Rat 5)) </result>
    </mpy>
endmodule
