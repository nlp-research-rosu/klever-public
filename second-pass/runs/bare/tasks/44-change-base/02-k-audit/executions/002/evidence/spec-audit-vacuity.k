requires "verification.k"

module SPEC-AUDIT-VACUITY
  imports VERIFICATION

  // Fresh false-result mutation. Satisfying witness X=8, B=3, CONT=.K:
  // the program returns "22", not baseString(8,3) + "0" = "220".
  claim
    <k>
      call(
        Module(
          FuncDef("change_base", Params("x", "base"),
            If(Compare(Name("x"), CmpOp("<", Name("base"))),
              Return(Call(Name("str"), Name("x"))),
              .Stmts)
            Return(
              BinOp(
                "+",
                Call(
                  Name("change_base"),
                  BinOp("//", Name("x"), Name("base")),
                  Name("base")),
                Call(Name("str"),
                     BinOp("%", Name("x"), Name("base"))))))),
        "change_base", intVal(X), intVal(B))
      ~> CONT:K
    =>
      strVal(baseString(X, B) +String "0") ~> CONT
    </k>
    requires 0 <=Int X andBool 2 <=Int B andBool B <=Int 9
endmodule
