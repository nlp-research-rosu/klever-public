requires "verification.k"

module PINNING-SPEC
  imports VERIFICATION

  claim [submitted-module-loads-exact-closure]:
    <k>
      #loadAll(
        Module(
          ImportFrom("typing", ("List", .ParamNames))
          FuncDef("separate_paren_groups", Params(("paren_string", .ParamNames)),
            Assign(Name("groups"), ListExpr(.Exprs))
            Assign(Name("current"), Str(""))
            Assign(Name("depth"), Int(0))
            For(Name("character"), Name("paren_string"),
              If(Compare(Name("character"), CmpOp("==", Str(" "))),
                Continue .Stmts,
                .Stmts)
              AugAssign(Name("current"), "+", Name("character"))
              If(Compare(Name("character"), CmpOp("==", Str("("))),
                AugAssign(Name("depth"), "+", Int(1)) .Stmts,
                AugAssign(Name("depth"), "-", Int(1)) .Stmts)
              If(Compare(Name("depth"), CmpOp("==", Int(0))),
                Expr(Call(Attribute(Name("groups"), "append"),
                          (Name("current"), .Exprs)))
                Assign(Name("current"), Str(""))
                .Stmts,
                .Stmts)
              .Stmts)
            Return(Name("groups"))
            .Stmts)
          .Stmts)
      )
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      ( -1 |-> builtinsScope
        0 |-> scope(.Map, parent(-1)) )
      =>
      ( -1 |-> builtinsScope
        0 |-> scope("separate_paren_groups" |-> solutionClosure,
                     parent(-1)) )
    </scopes>

endmodule
