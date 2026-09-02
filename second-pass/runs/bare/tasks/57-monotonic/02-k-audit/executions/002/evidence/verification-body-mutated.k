requires "semantic.k"

module VERIFICATION-BODY-MUTATED
  imports SEMANTIC

  // Reviewer mutation: the second comparison uses ascending sorted(l) too.
  // This changes the program body actually executed by the claim.
  syntax Pgm ::= "bodyMutatedProgram" [function]
  rule bodyMutatedProgram =>
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
              CmpOp("==", Call(Name("sorted"), Name("l"))))))))

  syntax Val ::= #intendedMonotonicSpec(IntList) [function]
  rule #intendedMonotonicSpec(L) =>
    boolVal(
      #eqIntLists(L, #sortInts(L))
      orBool
      #eqIntLists(L, #reverseInts(#sortInts(L))))
endmodule
