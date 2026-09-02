requires "reference-semantics/semantics.k"

module ANY-INT-VERIFICATION
  imports MPY

  syntax Stmts ::= "anyIntBody" [function, total]
  rule anyIntBody
    => Return(
         BoolOp(
           "and",
           Call(Name("isinstance"), Name("x"), Name("int")),
           Call(Name("isinstance"), Name("y"), Name("int")),
           Call(Name("isinstance"), Name("z"), Name("int")),
           BoolOp(
             "or",
             Compare(
               BinOp("+", Name("x"), Name("y")),
               CmpOp("==", Name("z"))),
             Compare(
               BinOp("+", Name("x"), Name("z")),
               CmpOp("==", Name("y"))),
             Compare(
               BinOp("+", Name("y"), Name("z")),
               CmpOp("==", Name("x"))))))
       .Stmts

  syntax KItem ::= "#anyInt" "(" Val "," Val "," Val ")"
  rule <k> #anyInt(X:Val, Y:Val, Z:Val)
        => #applyK(
             toCall(closureVal(("x", "y", "z"), anyIntBody, 0)),
             (X, Y, Z, .Vals))
         ... </k>

  syntax Bool ::= sumCondition(Int, Int, Int) [function, total]
  rule sumCondition(X:Int, Y:Int, Z:Int)
    => ((X +Int Y) ==Int Z)
       orBool ((X +Int Z) ==Int Y)
       orBool ((Y +Int Z) ==Int X)
endmodule
