requires "semantic.k"

module ANY-INT-VERIFICATION
  imports MPY-SEMANTICS

  // This macro is the exact constructor tree in solution.mpy.  Keeping the
  // program separate from the semantics prevents the operational rules from
  // baking in the answer to the task.
  syntax Program ::= "solutionProgram" [macro]
  rule solutionProgram =>
    Module(
      FuncDef("any_int", Params("x", "y", "z"),
        Return(
          BoolOp(
            "and",
            Compare(Call(Name("type"), Name("x")), CmpOp("==", Name("int"))),
            Compare(Call(Name("type"), Name("y")), CmpOp("==", Name("int"))),
            Compare(Call(Name("type"), Name("z")), CmpOp("==", Name("int"))),
            BoolOp(
              "or",
              Compare(BinOp("+", Name("x"), Name("y")), CmpOp("==", Name("z"))),
              Compare(BinOp("+", Name("x"), Name("z")), CmpOp("==", Name("y"))),
              Compare(BinOp("+", Name("y"), Name("z")), CmpOp("==", Name("x"))))))))

  syntax KItem ::= "RunAnyInt" "(" Val "," Val "," Val ")" [macro]
  rule RunAnyInt(X, Y, Z) => Invoke(solutionProgram, X, Y, Z)
endmodule
