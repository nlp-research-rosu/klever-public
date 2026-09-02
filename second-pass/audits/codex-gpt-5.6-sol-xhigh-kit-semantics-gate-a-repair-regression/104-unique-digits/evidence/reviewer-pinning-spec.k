requires "program-fragments.k"

module REVIEWER-PINNING-SPEC
  imports UNIQUE-DIGITS-FRAGMENTS

  // The literal body below is the trusted translator's regenerated
  // solution.mpy body. Fixed module-loading/FuncDef rules must bind it as the
  // exact macro body used by SPEC.unique-digits.
  claim [translated-body-is-pinned]:
    <k>
      #loadAll(
        Module(
          FuncDef("unique_digits", Params(("x", .ParamNames)),
            Assign(Name("result"), ListExpr(.Exprs))
            Assign(Name("value"), Int(0))
            Assign(Name("number"), Int(0))
            Assign(Name("valid"), Bool(true))
            For(Name("value"), Name("x"),
              Assign(Name("number"), Name("value"))
              Assign(Name("valid"), Bool(true))
              While(Compare(Name("number"), CmpOp(">", Int(0))),
                Assign(
                  Name("valid"),
                  BoolOp(
                    "and",
                    (Name("valid"),
                     Compare(
                       BinOp("%", Name("number"), Int(2)),
                       CmpOp("==", Int(1))))))
                Assign(
                  Name("number"),
                  BinOp("//", Name("number"), Int(10))))
              If(
                Name("valid"),
                Expr(
                  Call(
                    Attribute(Name("result"), "append"),
                    (Name("value"), .Exprs))),
                .Stmts))
            Expr(Call(Attribute(Name("result"), "sort"), .Exprs))
            Return(Name("result")))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      ... 0 |-> scope(
            .Map
            => "unique_digits"
                 |-> closureVal(
                       ("x", .ParamNames),
                       uniqueDigitsBody,
                       0),
            parent(-1))
      ...
    </scopes>
endmodule
