requires "verification.k"

module SPEC-VACUITY
  imports MPY-VERIFICATION

  // Reviewer-authored copy of the genuine auxiliary invariant.  It is needed
  // to make the end-to-end mutation reach the return obligation.
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

  // Deliberately false: require one additional empty output group.  For the
  // satisfying witness CS = LP RP, the real result is [LP RP], not
  // [LP RP, empty].
  claim [program-correct-false-extra-output]:
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
      <result>
        none
        => OutList(#snocOut(separateSpec(CS), .Chars))
      </result>
    </mpy>

endmodule
