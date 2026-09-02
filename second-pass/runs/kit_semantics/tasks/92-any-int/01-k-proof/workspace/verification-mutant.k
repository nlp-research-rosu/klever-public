requires "reference-semantics/semantics.k"

module VERIFICATION-MUTANT-SYNTAX
  imports MPY-SYNTAX
  imports MPY-CORE

  // Deliberate body mutation: the final disjunct is always false instead of
  // checking y + z == x.
  syntax Expr ::= "AnyIntCallMutant" "(" Val "," Val "," Val ")" [macro]
  rule AnyIntCallMutant(X:Val, Y:Val, Z:Val)
    => Call(Name("any_int"), (X, Y, Z))

  syntax Scope ::= "anyIntMutantModuleScope" [macro]
  rule anyIntMutantModuleScope
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
                     , Bool(false)
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

module VERIFICATION-MUTANT
  imports MPY
  imports VERIFICATION-MUTANT-SYNTAX
endmodule
