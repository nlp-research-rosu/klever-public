requires "/tmp/audit-work/source/verification.k"

module SPEC-UNICODE-WITNESS
  imports VERIFICATION

  // Python's canonical function returns 1 for this input because "Ä".lower()
  // is "ä". The generated semantics instead proves a result of 2.
  claim
    <k>
      Module(
        FuncDef("count_distinct_characters", Params("string"),
          Return(
            Call(
              Name("len"),
              Call(Name("set"),
                Call(Attribute(Name("string"), "lower"), .Exprs))))))
      => .K
    </k>
    <env> .Map => "string" |-> StrVal("Ää") </env>
    <input> "Ää" </input>
    <result> noResult => IntVal(2) </result>
endmodule
