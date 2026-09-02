requires "semantic.k"

module MPY-VERIFICATION
  imports MPY

  // Readable names for the exact AST fragments emitted by py2mpy.py. These are
  // macros only: proofs still execute the ordinary rules in semantic.k.
  syntax Stmts ::= "parserBranch" [function, total]
  rule parserBranch =>
    If(Compare(Name("note"), CmpOp("==", Str("o"))),
       Assign(Name("beats"),
              BinOp("+", Name("beats"), ListExpr(Int(4)))),
       If(Compare(Name("note"), CmpOp("==", Str("o|"))),
          Assign(Name("beats"),
                 BinOp("+", Name("beats"), ListExpr(Int(2)))),
          Assign(Name("beats"),
                 BinOp("+", Name("beats"), ListExpr(Int(1))))))

  syntax Stmts ::= "parserFunctionBody" [function, total]
  rule parserFunctionBody =>
    Assign(Name("beats"), ListExpr(.Exprs))
    For(Name("note"),
        Call(Attribute(Name("music_string"), "split"), Str(" ")),
        parserBranch)
    Return(Name("beats"))

  syntax Pgm ::= "theProgram" [function, total]
  rule theProgram =>
    Module(ImportFrom("typing", "List")
           FuncDef("parse_music", Params("music_string"),
                   parserFunctionBody))
endmodule
