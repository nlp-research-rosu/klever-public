requires "verification.k"

module SPEC
  imports VERIFICATION

  // Universal functional-correctness claim.  CONT makes the claim usable as
  // the circularity at each recursive call, while ENV checks call restoration.
  claim [how-many-times-correct]:
    <k> invoke(strVal(S), strVal(T)) ~> CONT:K
      => intVal(overlapCount(S, T)) ~> CONT </k>
    <functions>
      "how_many_times" |->
        function(Params("string", "substring"),
          If(Compare(Name("substring"), CmpOp("==", Str(""))),
            Return(BinOp("+", Call(Name("len"), Name("string")), Int(1))),
            .Stmts)
          If(Compare(
              Call(Name("len"), Name("string")),
              CmpOp("<", Call(Name("len"), Name("substring")))),
            Return(Int(0)),
            .Stmts)
          If(Compare(
              Subscript(Name("string"),
                Slice(NoBound,
                  Call(Name("len"), Name("substring")), NoBound)),
              CmpOp("==", Name("substring"))),
            Return(BinOp("+", Int(1),
              Call(Name("how_many_times"),
                Subscript(Name("string"),
                  Slice(Int(1), NoBound, NoBound)),
                Name("substring")))),
            .Stmts)
          Return(Call(Name("how_many_times"),
            Subscript(Name("string"), Slice(Int(1), NoBound, NoBound)),
            Name("substring"))))
    </functions>
    <env> _ENV:Map </env>
endmodule
