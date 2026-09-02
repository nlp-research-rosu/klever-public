requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: this input returns -9, not 0.
  claim
    <k> boot(solutionProgram) => .K </k>
    <input> input(1, 2, 2, -4) </input>
    <function> .Function => function("arr", solutionBody) </function>
    <env> .Map =>
      "arr" |-> listVal(1, 2, 2, -4)
      "total" |-> 9
      "sign" |-> -1
      "x" |-> -4
    </env>
    <result> noResult => result(0) </result>
endmodule
