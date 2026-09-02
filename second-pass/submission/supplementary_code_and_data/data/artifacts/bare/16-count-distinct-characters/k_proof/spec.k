requires "verification.k"

module SPEC
  imports VERIFICATION

  // The translated solution returns the reference count for every input.
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
    <env> .Map => "string" |-> StrVal(S) </env>
    <input> S:String </input>
    <result>
      noResult => IntVal(expectedDistinctCharacters(S))
    </result>

  // Prompt examples are retained as concrete regression claims.
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
    <result> noResult => IntVal(3) </result>

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
    <env> .Map => "string" |-> StrVal("Jerry") </env>
    <input> "Jerry" </input>
    <result> noResult => IntVal(4) </result>

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
    <env> .Map => "string" |-> StrVal("") </env>
    <input> "" </input>
    <result> noResult => IntVal(0) </result>
endmodule
