requires "reference-semantics/semantics.k"

module AUDIT-BODY-MUTANT-SYNTAX
  imports MPY-SYNTAX
  imports MPY-CORE
  imports BOOL
  imports INT

  syntax Expr ::= "AnyIntCall" "(" Val "," Val "," Val ")" [macro]
  rule AnyIntCall(X:Val, Y:Val, Z:Val)
    => Call(Name("any_int"), (X, Y, Z))

  syntax Scope ::= "anyIntModuleScope" [macro]
  rule anyIntModuleScope
    => scope(
         "any_int" |->
           closureVal(
             ("x", "y", "z"),
             Return(
               BoolOp(
                 "and",
                 ( Call(Name("isinstance"), (Name("x"), Name("int")))
                 , Call(Name("isinstance"), (Name("y"), Name("int")))
                 , Call(Name("isinstance"), (Name("z"), Name("int")))
                 , BoolOp(
                     "or",
                     ( Compare(BinOp("+", Name("x"), Name("y")), CmpOp("==", Name("z")))
                     , Compare(BinOp("+", Name("x"), Name("z")), CmpOp("==", Name("y")))
                     , Compare(BinOp("+", Name("y"), Name("z")), CmpOp("==", Name("z")))
                     )
                   )
                 )
               )
             ) .Stmts,
             0
           ),
         parent(-1)
       )
endmodule

module AUDIT-BODY-MUTANT
  imports MPY
  imports AUDIT-BODY-MUTANT-SYNTAX
endmodule
