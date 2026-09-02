requires "audit-identity-verification.k"

module AUDIT-PROGRAM-IDENTITY-MUTATION
  imports AUDIT-IDENTITY-VERIFICATION

  // RHS is generated from regenerated-solution.mpy; its single
  // omitted empty Stmts list is written explicitly as .Stmts.
  claim [solution-program-does-not-expand-to-mutated-file]:
    <mpy>
      <k> auditHold(solutionProgram)
           => auditHold(
                Module(
                  FuncDef("words_in_sentence", Params("sentence"),
                    Assign(Name("result"), Str(""))
                    Assign(Name("word"), Str(""))
                    For(Name("word"), Call(Attribute(Name("sentence"), "split"), Str(" ")),
                      If(Compare(
                        Call(Name("len"), Name("word")),
                        CmpOp(
                          "in",
                          ListExpr(
                            Int(4),
                            Int(3),
                            Int(5),
                            Int(7),
                            Int(11),
                            Int(13),
                            Int(17),
                            Int(19),
                            Int(23),
                            Int(29),
                            Int(31),
                            Int(37),
                            Int(41),
                            Int(43),
                            Int(47),
                            Int(53),
                            Int(59),
                            Int(61),
                            Int(67),
                            Int(71),
                            Int(73),
                            Int(79),
                            Int(83),
                            Int(89),
                            Int(97)))),
                        If(Compare(Name("result"), CmpOp("==", Str(""))),
                          Assign(Name("result"), Name("word")),
                          Assign(
                            Name("result"),
                            BinOp(
                              "+",
                              BinOp("+", Name("result"), Str(" ")),
                              Name("word")))),
                        .Stmts))
                    Return(Name("result"))))
              ) </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> NoneVal </result>
    </mpy>
endmodule
