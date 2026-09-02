requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false result mutation: for ("aaaa", "aa"), the submitted
  // body and overlapCount both produce 3, whereas this destination requires 4.
  claim [how-many-times-false-off-by-one]:
    <k> invoke(strVal(S), strVal(T)) ~> CONT:K
      => intVal(overlapCount(S, T) +Int 1) ~> CONT </k>
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
