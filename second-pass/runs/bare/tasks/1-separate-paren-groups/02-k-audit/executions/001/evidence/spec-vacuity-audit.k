requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports MPY-VERIFICATION

  // False mutation of the result obligation. The exact submitted program on
  // the satisfiable input "()" returns one group, but this demands no groups.
  claim [false-empty-result-for-one-group]:
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
      <result> none => OutList(.Outputs) </result>
    </mpy>

endmodule
