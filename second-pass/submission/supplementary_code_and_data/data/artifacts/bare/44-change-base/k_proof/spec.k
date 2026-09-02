requires "verification.k"

module SPEC
  imports VERIFICATION

  // Total functional correctness over the HumanEval input domain.  CONT is
  // universally quantified, so the circularity also applies to recursive
  // calls while their string-concatenation continuation is still pending.
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
      strVal(baseString(X, B)) ~> CONT
    </k>
    requires 0 <=Int X andBool 2 <=Int B andBool B <=Int 9
endmodule
