requires "semantic.k"

module AUDIT-SPEC-VACUITY
  imports MPY

  // Fresh auditor mutation: the real program returns true on "<>", so require
  // the opposite result while leaving the same satisfiable entry state.
  claim [false-pair]: <py>
    <k>
      correctProgram() ~> invoke("correct_bracketing", SVal("<>"))
      => .K
    </k>
    <functions> .Map => ?_FM:Map </functions>
    <env> emptyStore() => ?_ENV:Store </env>
    <result> noResult() => result(BVal(false)) </result>
  </py>
endmodule
