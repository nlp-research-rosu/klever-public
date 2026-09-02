requires "/tmp/audit-work/source/verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false postcondition. The unchanged submitted program returns 3 for
  // this satisfiable prompt-example input, so requiring 4 must be rejected.
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
    <env> .Map => "string" |-> StrVal("xyzXYZ") </env>
    <input> "xyzXYZ" </input>
    <result> noResult => IntVal(4) </result>
endmodule
