requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation of submitted claim 1: the actual result is 1, not 2.
  claim <py>
          <k> SFTest(ListExpr(Int(15), Int(-73), Int(14), Int(-15)))
              => intVal(2) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>
endmodule
