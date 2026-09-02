requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTANT
  imports MPY

  syntax Stmts ::= "intToMiniRomanBodyMutant" [macro]
  syntax Module ::= "solutionCallMutant" "(" Int ")" [macro]

  rule intToMiniRomanBodyMutant
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
         Return(Str("x")),
         .Stmts)
       Return(
         BinOp(
           "+",
           BinOp("+", Name("hundreds"), Name("tens")),
           Name("ones")))

  rule solutionCallMutant(N:Int)
    => Module(
         FuncDef("int_to_mini_roman", Params("number"),
           intToMiniRomanBodyMutant)
         Assign(Name("__result"),
           Call(Name("int_to_mini_roman"), Int(N))))
endmodule
