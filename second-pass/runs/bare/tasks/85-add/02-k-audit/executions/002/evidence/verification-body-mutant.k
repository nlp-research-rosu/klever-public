requires "semantic.k"

module VERIFICATION-BODY-MUTANT
  imports MPY

  // The mathematical contract.  The second member of each pair has an odd
  // zero-based index; evenPart keeps that integer exactly when it is even.
  syntax Int ::= oddIndexEvenSum(ISeq) [function]
  rule oddIndexEvenSum(nil) => 0
  rule oddIndexEvenSum(cons(_, nil)) => 0
  rule oddIndexEvenSum(cons(_, cons(ITEM, REST)))
    => evenPart(ITEM) +Int oddIndexEvenSum(REST)

  // This macro is the exact constructor tree generated in solution.mpy.
  syntax Module ::= "solutionProgramMutant" [macro]
  rule solutionProgramMutant =>
    Module(
      FuncDef("add", Params("lst"),
        Return(
          IfExp(
            Compare(Call(Name("len"), Name("lst")), CmpOp("<", Int(2))),
            Int(1),
            BinOp(
              "+",
              IfExp(
                Compare(
                  BinOp("%", Subscript(Name("lst"), Int(1)), Int(2)),
                  CmpOp("==", Int(0))),
                Subscript(Name("lst"), Int(1)),
                Int(0)),
              Call(
                Name("add"),
                Subscript(Name("lst"), Slice(Int(2), NoBound, NoBound))))))))
endmodule
