requires "verification.k"

module PROGRAM-IDENTITY-SPEC
  imports MPY-VERIFICATION

  // The right-hand term is copied from the trusted translator's regenerated
  // solution.mpy. This claim checks the proof-side program macro against it.
  claim
    <mpy>
      <k>
        theProgram
        =>
        Module(
          ImportFrom("typing", "List")
          FuncDef("parse_music", Params("music_string"),
            Assign(Name("beats"), ListExpr(.Exprs))
            For(Name("note"),
                Call(Attribute(Name("music_string"), "split"), Str(" ")),
              If(Compare(Name("note"), CmpOp("==", Str("o"))),
                Assign(
                  Name("beats"),
                  BinOp("+", Name("beats"), ListExpr(Int(4)))),
                If(Compare(Name("note"), CmpOp("==", Str("o|"))),
                  Assign(
                    Name("beats"),
                    BinOp("+", Name("beats"), ListExpr(Int(2)))),
                  Assign(
                    Name("beats"),
                    BinOp("+", Name("beats"), ListExpr(Int(1)))))))
            Return(Name("beats"))))
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </mpy>
endmodule
