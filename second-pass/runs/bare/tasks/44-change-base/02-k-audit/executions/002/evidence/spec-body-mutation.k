requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Body-sensitivity probe: the base branch returns str(base), while the
  // original theorem's result obligation is intentionally unchanged.
  claim
    <k>
      call(
        Module(
          FuncDef("change_base", Params("x", "base"),
            If(Compare(Name("x"), CmpOp("<", Name("base"))),
              Return(Call(Name("str"), Name("base"))),
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
      strVal(baseString(X, B)) ~> CONT
    </k>
    requires 0 <=Int X andBool 2 <=Int B andBool B <=Int 9
endmodule
