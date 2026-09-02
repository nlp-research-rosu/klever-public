requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false result mutation. The satisfying input [1] returns 1, not 2.
  claim [false-result-for-one]: <k> boot => .K </k>
        <program> searchProgram </program>
        <input> VList(cons(1, .Ints)) </input>
        <env> .Map </env>
        <result> noResult => VInt(2) </result>
endmodule
