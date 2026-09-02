module MPY-VERIFICATION
  imports MPY-SYNTAX
  imports BOOL
  imports K-EQUAL

  syntax Stmts ::= "solutionBody" [function, total]
  rule solutionBody =>
    If(Compare(Name("s"), CmpOp("==", Str(""))),
       Return(Str("")),
       .Stmts)
    Return(
      BinOp("+",
        Call(Name("chr"),
          BinOp("+",
            BinOp("%",
              BinOp("+",
                BinOp("-",
                  Call(Name("ord"), Subscript(Name("s"), Int(0))),
                  Int(97)),
                Int(4)),
              Int(26)),
            Int(97))),
        Call(Name("encrypt"),
          Subscript(Name("s"), Slice(Int(1), NoBound, NoBound)))))

  syntax String ::= rotate4(String) [function]
  rule rotate4("") => "" [simplification]
  rule rotate4(S) =>
    chrChar(((ordChar(substrString(S, 0, 1)) -Int 97 +Int 4)
             modInt 26) +Int 97)
    +String rotate4(substrString(S, 1, lengthString(S)))
    requires S =/=K "" [simplification]
endmodule
