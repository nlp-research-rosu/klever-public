requires "/tmp/audit-work/source/verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Material body mutation: remove the actual lower() call. For "Aa", this
  // mutated program returns 2, so the original expected result 1 must fail.
  claim
    <k>
      Module(
        FuncDef("count_distinct_characters", Params("string"),
          Return(
            Call(
              Name("len"),
              Call(Name("set"), Name("string"), .Exprs)))))
      => .K
    </k>
    <env> .Map => "string" |-> StrVal("Aa") </env>
    <input> "Aa" </input>
    <result> noResult => IntVal(1) </result>
endmodule
