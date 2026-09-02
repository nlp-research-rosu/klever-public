requires "verification-base.k"

module MUTATION
  imports VERIFICATION-BASE

  // Material mutation: advance i by 2, skipping mirrored pairs.
  syntax Stmts ::= "mutantLoopBody" [macro]
  rule mutantLoopBody
    => If(
         Compare(
           Subscript(Name("arr"), Name("i")),
           CmpOp(
             "!=",
             Subscript(
               Name("arr"),
               BinOp(
                 "-",
                 BinOp("-", Call(Name("len"), Name("arr")), Name("i")),
                 Int(1))))),
         AugAssign(Name("changes"), "+", Int(1)),
         .Stmts)
       AugAssign(Name("i"), "+", Int(2))

  syntax Stmts ::= "mutantBody" [macro]
  rule mutantBody
    => Assign(Name("changes"), Int(0))
       Assign(Name("i"), Int(0))
       While(
         Compare(
           Name("i"),
           CmpOp(
             "<",
             BinOp(
               "//",
               Call(Name("len"), Name("arr")),
               Int(2)))),
         mutantLoopBody)
       Return(Name("changes"))
endmodule
