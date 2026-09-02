module VERIFICATION
  imports MPY-SYNTAX
  imports INT
  imports BOOL

  syntax Stmts ::= "countBody" [macro]
  rule countBody =>
    If(Compare(BinOp("%", Name("value"), Int(2)), CmpOp("==", Int(0))),
       Assign(Name("even"), BinOp("+", Name("even"), Int(1))),
       .Stmts)

  syntax Stmt ::= "solutionProgram" [macro]
  rule solutionProgram =>
    Module(
      FuncDef("exchange", Params("lst1", "lst2"),
        Assign(Name("even"), Int(0))
        For(Name("value"), Name("lst1"), countBody)
        For(Name("value"), Name("lst2"), countBody)
        If(Compare(Name("even"), CmpOp(">=", Call(Name("len"), Name("lst1")))),
           Return(Str("YES")),
           .Stmts)
        Return(Str("NO"))))

  syntax Int ::= evenBit(Int) [function, total]
  rule evenBit(I) => 1 requires I %Int 2 ==Int 0
  rule evenBit(I) => 0 requires notBool (I %Int 2 ==Int 0)

  syntax Int ::= countEven(PyList) [function, total]
  rule countEven(Nil) => 0
  rule countEven(Cons(I, REST)) => evenBit(I) +Int countEven(REST)

  syntax Int ::= lastValue(PyList, Int) [function, total]
  rule lastValue(Nil, DEFAULT) => DEFAULT
  rule lastValue(Cons(I, REST), _) => lastValue(REST, I)
endmodule
