module VERIFICATION
  imports MPY

  syntax Program ::= "chooseNumProgram" [function]
  rule chooseNumProgram
    => Module(
         FuncDef("choose_num", Params("x", "y"),
           Return(
             IfExp(
               Compare(Name("x"), CmpOp(">", Name("y"))),
               UnaryOp("-", Int(1)),
               IfExp(
                 Compare(BinOp("%", Name("y"), Int(2)), CmpOp("==", Int(0))),
                 Name("y"),
                 IfExp(
                   Compare(Name("x"), CmpOp("==", Name("y"))),
                   UnaryOp("-", Int(1)),
                   BinOp("-", Name("y"), Int(2))))))))

  // For integer endpoints, an interval has no even member exactly when it is
  // empty, or when it is a one-element interval containing an odd integer.
  syntax Bool ::= "noEvenInRange" "(" Int "," Int ")" [function]
  rule noEvenInRange(X, Y)
    => X >Int Y
       orBool (X ==Int Y andBool X %Int 2 =/=Int 0)

  // If R is not the sentinel, Y < R+2 says that the next even integer after
  // R is outside the interval; together with evenness and the range bounds,
  // this characterizes the greatest even member of [X,Y].
  syntax Bool ::= "chooseNumContract" "(" Int "," Int "," Int ")" [function]
  rule chooseNumContract(X, Y, R)
    => (R ==Int -1 andBool noEvenInRange(X, Y))
       orBool
       (R =/=Int -1
        andBool X <=Int R
        andBool R <=Int Y
        andBool R %Int 2 ==Int 0
        andBool Y <Int R +Int 2)

  syntax KItem ::= "checkChooseNum" "(" Int "," Int ")"
  rule <k> VInt(R) ~> checkChooseNum(X, Y)
        => VBool(chooseNumContract(X, Y, R)) ... </k>
endmodule
