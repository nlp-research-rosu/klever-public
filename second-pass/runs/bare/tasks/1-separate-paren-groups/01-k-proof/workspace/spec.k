requires "verification.k"

module SPEC
  imports MPY-VERIFICATION

  // Inductive loop invariant.  This claim is intentionally phrased over an
  // arbitrary remaining character sequence CS, arbitrary scanner state, and
  // the exact AST loop body emitted in solution.mpy.
  claim [loop-invariant]:
    <mpy>
      <k>
        #loop("ch", CS,
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
      <input> IN </input>
      <env>
        "ch" |-> SVal(LAST)
        "current" |-> SVal(CURRENT)
        "depth" |-> D
        "paren_string" |-> SVal(ALL)
        "result" |-> OutList(OUT)
        => ?FINALENV:Map
      </env>
      <functions> FS </functions>
      <result> _ => OutList(stateOutput(runSpec(CS, D, CURRENT, OUT, LAST))) </result>
    </mpy>

  // End-to-end correctness from the exact constructor tree in solution.mpy.
  // Encoded(CS) ranges over every string made of parentheses and spaces, a
  // strict superset of the prompt's balanced-input domain.
  claim [program-correct]:
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
      <input> Encoded(CS) </input>
      <env> .Map => ?TOPENV:Map </env>
      <functions> .Map => ?TOPFUNS:Map </functions>
      <result> none => OutList(separateSpec(CS)) </result>
    </mpy>

endmodule
