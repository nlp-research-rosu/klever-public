requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: the real program returns 2 for this satisfiable
  // documented example, while this mutation requires 3.
  claim [false-example-one-result]:
        <k> boot => .K </k>
        <program> searchProgram </program>
        <input> VList(cons(4, cons(1, cons(2, cons(2, cons(3, cons(1, .Ints))))))) </input>
        <env> .Map </env>
        <result> noResult => VInt(3) </result>
endmodule
