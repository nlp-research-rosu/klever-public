requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX
  imports MPY-CORE
  imports BOOL
  imports INT

  // Parse-time abbreviations for the loaded module binding and invocation.
  // They expand before the executable K definition is generated.
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
                     , Compare(BinOp("+", Name("y"), Name("z")), CmpOp("==", Name("x")))
                     )
                   )
                 )
               )
             ) .Stmts,
             0
           ),
         parent(-1)
       )

  // The mathematical predicate named by the HumanEval contract.
  syntax Bool ::= anySum(Int, Int, Int) [function, total]
endmodule

module VERIFICATION
  imports MPY
  imports VERIFICATION-SYNTAX

  // Derived from the two exhaustive fixed-semantics equations
  // boolAsInt(true) = 1 and boolAsInt(false) = 0.
  rule boolAsInt(B:Bool)
    => #if B #then 1 #else 0 #fi
    [simplification]

  rule anySum(X:Int, Y:Int, Z:Int)
    => ((X +Int Y) ==Int Z)
       orBool ((X +Int Z) ==Int Y)
       orBool ((Y +Int Z) ==Int X)
endmodule
