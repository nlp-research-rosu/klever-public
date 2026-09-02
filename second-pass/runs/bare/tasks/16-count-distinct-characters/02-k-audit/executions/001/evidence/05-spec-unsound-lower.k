requires "verification.k"

module SPEC-UNSOUND-LOWER
  imports VERIFICATION

  // Candidate semantics says 2; real Python lower() maps Å to å, so the real
  // submitted program and canonical implementation both return 1.
  claim [latin-uppercase-witness]:
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
    <env> .Map => "string" |-> StrVal("Åå") </env>
    <input> "Åå" </input>
    <result> noResult => IntVal(2) </result>
endmodule
