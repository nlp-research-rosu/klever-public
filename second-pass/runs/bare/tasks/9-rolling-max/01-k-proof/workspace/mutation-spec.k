requires "verification.k"

module MUTATION-SPEC
  imports VERIFICATION

  // Mutation: forgetting first = False makes every iteration treat its item
  // as the first one, so [2, 1] incorrectly produces [2, 1]. This claim is
  // intentionally unprovable; prove.sh requires kprove to reject it.
  claim <py>
          <k> VerifyRunList(
               Module(
                 ImportFrom("typing", "List", "Tuple")
                 FuncDef("rolling_max", Params("numbers"),
                   Assign(Name("result"), ListExpr(.Exprs))
                   Assign(Name("first"), Bool(true))
                   Assign(Name("maximum"), Int(0))
                   For(Name("number"), Name("numbers"),
                     If(Name("first"),
                       Assign(Name("maximum"), Name("number")),
                       If(Compare(Name("number"), CmpOp(">", Name("maximum"))),
                         Assign(Name("maximum"), Name("number")),
                         .Stmts))
                     Expr(Call(Attribute(Name("result"), "append"), Name("maximum"))))
                   Return(Name("result")))),
               ListItem(2) ListItem(1))
            => ListVal(ListItem(2) ListItem(2)) ~> .K </k>
          <functions> .Map </functions>
          <env> .Map </env>
          <stack> .List </stack>
        </py>
endmodule
