requires "semantic.k"

module HUMAN-EVAL-VERIFICATION
  imports HUMAN-EVAL-SEMANTICS

  // Mathematical vocabulary for the HumanEval contract.
  syntax Bool ::= "balanced" "(" IntList ")" [function, symbol(balanced)]
                | "withinWeight" "(" IntList "," Int ")"
                  [function, symbol(withinWeight)]
                | "canFly" "(" IntList "," Int ")" [function, symbol(canFly)]

  rule balanced(IS) => equalIntLists(IS, reverseInts(IS))
  rule withinWeight(IS, W) => sumInts(IS) <=Int W
  rule canFly(IS, W) => balanced(IS) andBool withinWeight(IS, W)

  // A compact name for the exact constructor tree generated in solution.mpy.
  syntax Pgm ::= "solutionProgram" [macro, symbol(solutionProgram)]
  rule solutionProgram =>
    Module(
      FuncDef("will_it_fly", Params("q", "w"),
        Return(
          BoolOp(
            "and",
            Compare(
              Name("q"),
              CmpOp(
                "==",
                Subscript(
                  Name("q"),
                  Slice(NoBound, NoBound, UnaryOp("-", Int(1)))))),
            Compare(
              Call(Name("sum"), Name("q")),
              CmpOp("<=", Name("w")))))))
endmodule
