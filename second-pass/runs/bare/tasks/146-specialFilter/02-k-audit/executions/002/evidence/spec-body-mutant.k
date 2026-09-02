requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION-BODY-MUTANT

  claim [body-sensitive]: <py>
          <k> SFTest(ListExpr(Int(15), Int(-73), Int(14), Int(-15)))
              => intVal(1) </k>
          <functions> .Map </functions>
          <env> .Map </env>
        </py>
endmodule

