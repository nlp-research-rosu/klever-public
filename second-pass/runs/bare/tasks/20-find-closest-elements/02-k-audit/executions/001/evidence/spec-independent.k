requires "verification.k"

module AUDIT-SPEC-1
  imports MPY-VERIFICATION
  claim
    <mpy>
      <k> run(solution, nums(1, 2, 3, 4, 5, 11 /Rat 5)) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => vtuple(vnum(2), vnum(11 /Rat 5)) </result>
    </mpy>
endmodule

module AUDIT-SPEC-2
  imports MPY-VERIFICATION
  claim
    <mpy>
      <k> run(solution, nums(1, 2, 3, 4, 5, 2)) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => vtuple(vnum(2), vnum(2)) </result>
    </mpy>
endmodule

module AUDIT-SPEC-3
  imports MPY-VERIFICATION
  claim
    <mpy>
      <k> run(solution, nums(A, B)) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => vtuple(vnum(A), vnum(B)) </result>
    </mpy>
    requires A <Rat B andBool notBool (B <Rat A)
endmodule

module AUDIT-SPEC-4
  imports MPY-VERIFICATION
  claim
    <mpy>
      <k> run(solution, nums(A, B)) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => vtuple(vnum(B), vnum(A)) </result>
    </mpy>
    requires B <Rat A andBool notBool (A <Rat B)
endmodule

module AUDIT-SPEC-5
  imports MPY-VERIFICATION
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
endmodule

module AUDIT-SPEC-6
  imports MPY-VERIFICATION
  claim
    <mpy>
      <k> run(solution, nums(-10, -3, -7 /Rat 2, 9)) => .K </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult => vtuple(vnum(-7 /Rat 2), vnum(-3)) </result>
    </mpy>
endmodule
