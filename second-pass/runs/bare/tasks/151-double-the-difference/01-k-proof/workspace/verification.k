requires "semantic.k"

module VERIFICATION
  imports MPY
  imports K-EQUAL

  // Named abbreviations for the exact constructor tree emitted in
  // solution.mpy.  Their equations only expose that tree.
  syntax Stmts ::= "loopBody" [function]
  rule loopBody
    => If(Call(Name("isinstance"), Name("value"), Name("int")),
         If(Compare(Name("value"), CmpOp(">=", Int(0))),
            If(Compare(BinOp("%", Name("value"), Int(2)),
                       CmpOp("==", Int(1))),
               Assign(Name("total"),
                      BinOp("+", Name("total"),
                           BinOp("*", Name("value"), Name("value")))),
               .Stmts),
            .Stmts),
         .Stmts)

  syntax Module ::= "solutionProgram" [function]
  rule solutionProgram
    => Module(
         FuncDef("double_the_difference", Params("lst"),
           Assign(Name("total"), Int(0))
           For(Name("value"), Name("lst"), loopBody)
           Return(Name("total"))))

  // Mathematical contract: a left fold that adds precisely the selected
  // square.  This accumulator form is also the loop invariant.
  syntax Int ::= selectedSquare(Int)
    [function, total,
     smt-hook((ite (and (>= #1 0) (= (mod #1 2) 1)) (* #1 #1) 0))]
  syntax Int ::= oddSquareFold(Vals, Int) [function]

  rule selectedSquare(I) => I *Int I
    requires I >=Int 0 andBool I %Int 2 ==Int 1
  rule selectedSquare(I) => 0
    requires notBool (I >=Int 0 andBool I %Int 2 ==Int 1)

  rule oddSquareFold(nil, ACC) => ACC
  rule oddSquareFold(intCons(I, VS), ACC)
    => oddSquareFold(VS, ACC +Int selectedSquare(I))
  rule oddSquareFold(floatCons(_, VS), ACC)
    => oddSquareFold(VS, ACC)
  rule oddSquareFold(boolCons(true, VS), ACC)
    => oddSquareFold(VS, ACC +Int 1)
  rule oddSquareFold(boolCons(false, VS), ACC)
    => oddSquareFold(VS, ACC)
  rule oddSquareFold(listCons(_, VS), ACC)
    => oddSquareFold(VS, ACC)
endmodule
