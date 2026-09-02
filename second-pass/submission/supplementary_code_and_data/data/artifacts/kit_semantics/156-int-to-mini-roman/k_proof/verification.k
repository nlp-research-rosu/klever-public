requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Parse-time aliases for the exact py2mpy translation and a call harness.
  // Macro expansion happens before execution; it adds no operational rule.
  syntax Stmts ::= "intToMiniRomanBody" [macro]
  syntax Module ::= "solutionModule" [macro]
                  | "solutionCall" "(" Int ")" [macro]

  rule intToMiniRomanBody
    => Assign(
         Name("hundreds"),
         Subscript(
           TupleExpr(
             Str(""), Str("c"), Str("cc"), Str("ccc"), Str("cd"),
             Str("d"), Str("dc"), Str("dcc"), Str("dccc"), Str("cm")),
           BinOp("//", BinOp("%", Name("number"), Int(1000)), Int(100))))
       Assign(
         Name("tens"),
         Subscript(
           TupleExpr(
             Str(""), Str("x"), Str("xx"), Str("xxx"), Str("xl"),
             Str("l"), Str("lx"), Str("lxx"), Str("lxxx"), Str("xc")),
           BinOp("//", BinOp("%", Name("number"), Int(100)), Int(10))))
       Assign(
         Name("ones"),
         Subscript(
           TupleExpr(
             Str(""), Str("i"), Str("ii"), Str("iii"), Str("iv"),
             Str("v"), Str("vi"), Str("vii"), Str("viii"), Str("ix")),
           BinOp("%", Name("number"), Int(10))))
       If(Compare(Name("number"), CmpOp("==", Int(1000))),
         Return(Str("m")),
         .Stmts)
       Return(
         BinOp(
           "+",
           BinOp("+", Name("hundreds"), Name("tens")),
           Name("ones")))

  rule solutionModule
    => Module(
         FuncDef("int_to_mini_roman", Params("number"),
           intToMiniRomanBody))

  rule solutionCall(N:Int)
    => Module(
         FuncDef("int_to_mini_roman", Params("number"),
           intToMiniRomanBody)
         Assign(Name("__result"),
           Call(Name("int_to_mini_roman"), Int(N))))
endmodule
