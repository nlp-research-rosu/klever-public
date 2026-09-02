requires "verification.k"

module SPEC
  imports MPY-VERIFICATION

  // The two examples from the HumanEval contract.
  claim
    <mpy>
      <k> run(solution, nums(1, 2, 3, 4, 5, 11 /Rat 5)) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => vtuple(vnum(2), vnum(11 /Rat 5)) </result>
    </mpy>

  claim
    <mpy>
      <k> run(solution, nums(1, 2, 3, 4, 5, 2)) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => vtuple(vnum(2), vnum(2)) </result>
    </mpy>

  // Symbolic length-two cases prove ordering and duplicate behavior for all
  // exact rational inputs satisfying the stated relation.
  claim
    <mpy>
      <k> run(solution, nums(A, B)) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => vtuple(vnum(A), vnum(B)) </result>
    </mpy>
    requires A <Rat B andBool notBool (B <Rat A)

  claim
    <mpy>
      <k> run(solution, nums(A, B)) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => vtuple(vnum(B), vnum(A)) </result>
    </mpy>
    requires B <Rat A andBool notBool (A <Rat B)

  claim
    <mpy>
      <k> run(solution, nums(A, B)) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => vtuple(vnum(A), vnum(B)) </result>
    </mpy>
    requires A ==Rat B
      andBool notBool (A <Rat B)
      andBool notBool (B <Rat A)

  // A negative-valued concrete case exercises normalization away from the
  // prompt's examples.
  claim
    <mpy>
      <k> run(solution, nums(-10, -3, -7 /Rat 2, 9)) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => vtuple(vnum(-7 /Rat 2), vnum(-3)) </result>
    </mpy>
endmodule
