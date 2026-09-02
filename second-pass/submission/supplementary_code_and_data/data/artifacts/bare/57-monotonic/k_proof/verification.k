requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // This constant is the exact AST emitted in solution.mpy. Keeping the program
  // as syntax makes the proof exercise the evaluator, rather than replacing
  // the implementation with a task-specific execution rule.
  syntax Pgm ::= "solutionProgram" [function]
  rule solutionProgram =>
    Module(
      FuncDef("monotonic", Params("l"),
        Return(
          BoolOp(
            "or",
            Compare(
              Name("l"),
              CmpOp("==", Call(Name("sorted"), Name("l")))),
            Compare(
              Name("l"),
              CmpOp(
                "==",
                Call(
                  Name("sorted"),
                  Name("l"),
                  KwArg("reverse", Bool(true)))))))))

  // Formal contract: equality with the ascending ordering or with its reverse.
  // For finite integer lists this is precisely nondecreasing or nonincreasing.
  syntax Val ::= #monotonicSpec(IntList) [function]
  rule #monotonicSpec(L) =>
    boolVal(
      #eqIntLists(L, #sortInts(L))
      orBool
      #eqIntLists(L, #reverseInts(#sortInts(L))))
endmodule
