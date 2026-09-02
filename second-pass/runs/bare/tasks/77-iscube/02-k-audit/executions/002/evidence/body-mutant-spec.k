requires "body-mutant-verification.k"

module BODY-MUTANT-SPEC
  imports BODY-MUTANT-VERIFICATION

  claim [mutated-body-rejects-one]:
    <k>
      iscubeProgramMutated ~> invoke(IntVal(1)) => .K
    </k>
    <funs> .Map => ?_ </funs>
    <env> .Map => ?_ </env>
    <result> .K => BoolVal(true) ~> .K </result>
endmodule
