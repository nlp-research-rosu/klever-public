requires "verification.k"

module GROUND-WITNESSES
  imports MPY-VERIFICATION

  claim [loop-ground]:
    <mpy>
      <k>
        #loop("ch", LP RP .Chars,
          If(Compare(Name("ch"), CmpOp("!=", Str(" "))),
            AugAssign(Name("current"), "+", Name("ch"))
            If(Compare(Name("ch"), CmpOp("==", Str("("))),
              AugAssign(Name("depth"), "+", Int(1)),
              AugAssign(Name("depth"), "-", Int(1))
              If(Compare(Name("depth"), CmpOp("==", Int(0))),
                Expr(Call(Attribute(Name("result"), "append"), Name("current")))
                Assign(Name("current"), Str("")),
                .Stmts)),
            .Stmts))
        ~> #exec(Return(Name("result")) .Stmts)
        => .K
      </k>
      <input> Encoded(LP RP .Chars) </input>
      <env>
        "ch" |-> SVal(.Chars)
        "current" |-> SVal(.Chars)
        "depth" |-> zero
        "paren_string" |-> SVal(LP RP .Chars)
        "result" |-> OutList(.Outputs)
        => ?FINALENV:Map
      </env>
      <functions> .Map </functions>
      <result> none => OutList(out(LP RP .Chars) .Outputs) </result>
    </mpy>

  claim [program-ground]:
    <mpy>
      <k>
        #boot(
          Module(
            ImportFrom("typing", "List")
            FuncDef("separate_paren_groups", Params("paren_string"),
              Assign(Name("result"), ListExpr())
              Assign(Name("current"), Str(""))
              Assign(Name("depth"), Int(0))
              Assign(Name("ch"), Str(""))
              For(Name("ch"), Name("paren_string"),
                If(Compare(Name("ch"), CmpOp("!=", Str(" "))),
                  AugAssign(Name("current"), "+", Name("ch"))
                  If(Compare(Name("ch"), CmpOp("==", Str("("))),
                    AugAssign(Name("depth"), "+", Int(1)),
                    AugAssign(Name("depth"), "-", Int(1))
                    If(Compare(Name("depth"), CmpOp("==", Int(0))),
                      Expr(Call(Attribute(Name("result"), "append"), Name("current")))
                      Assign(Name("current"), Str("")),
                      .Stmts)),
                  .Stmts))
              Return(Name("result"))))
        )
        => .K
      </k>
      <input> Encoded(LP RP .Chars) </input>
      <env> .Map => ?TOPENV:Map </env>
      <functions> .Map => ?TOPFUNS:Map </functions>
      <result> none => OutList(out(LP RP .Chars) .Outputs) </result>
    </mpy>

endmodule
