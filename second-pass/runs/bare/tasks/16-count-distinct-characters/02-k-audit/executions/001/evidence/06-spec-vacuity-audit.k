requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh reviewer mutation: the satisfying empty-string input really returns
  // 0, so changing only its required result to 1 must leave an unmet result
  // obligation.
  claim [false-empty-result]:
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
    <env> .Map => "string" |-> StrVal("") </env>
    <input> "" </input>
    <result> noResult => IntVal(1) </result>
endmodule
