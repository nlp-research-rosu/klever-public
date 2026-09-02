requires "semantic.k"

module HUMAN-EVAL-VERIFICATION-BODY-MUTANT
  imports HUMAN-EVAL-SEMANTICS

  syntax Bool ::= "mutBalanced" "(" IntList ")" [function, symbol(mutBalanced)]
                | "mutWithinWeight" "(" IntList "," Int ")"
                  [function, symbol(mutWithinWeight)]
                | "mutCanFly" "(" IntList "," Int ")"
                  [function, symbol(mutCanFly)]

  rule mutBalanced(IS) => equalIntLists(IS, reverseInts(IS))
  rule mutWithinWeight(IS, W) => sumInts(IS) <=Int W
  rule mutCanFly(IS, W) => mutBalanced(IS) andBool mutWithinWeight(IS, W)

  // Body mutation: the submitted Name("w") is replaced by Int(0).
  syntax Pgm ::= "mutatedSolutionProgram"
                 [macro, symbol(mutatedSolutionProgram)]
  rule mutatedSolutionProgram =>
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
              CmpOp("<=", Int(0)))))))
endmodule
