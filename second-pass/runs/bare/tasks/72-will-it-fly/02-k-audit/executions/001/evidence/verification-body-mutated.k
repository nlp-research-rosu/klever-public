requires "semantic.k"

module HUMAN-EVAL-VERIFICATION-BODY-MUTATED
  imports HUMAN-EVAL-SEMANTICS

  syntax Bool ::= "balancedMut" "(" IntList ")"
                  [function, symbol(balancedMut)]
                | "withinWeightMut" "(" IntList "," Int ")"
                  [function, symbol(withinWeightMut)]
                | "canFlyMut" "(" IntList "," Int ")"
                  [function, symbol(canFlyMut)]

  rule balancedMut(IS) => equalIntLists(IS, reverseInts(IS))
  rule withinWeightMut(IS, W) => sumInts(IS) <=Int W
  rule canFlyMut(IS, W) => balancedMut(IS) andBool withinWeightMut(IS, W)

  // Deliberate source-body mutation: q == q replaces q == q[::-1].
  syntax Pgm ::= "solutionProgramBodyMutated"
                 [macro, symbol(solutionProgramBodyMutated)]
  rule solutionProgramBodyMutated =>
    Module(
      FuncDef("will_it_fly", Params("q", "w"),
        Return(
          BoolOp(
            "and",
            Compare(Name("q"), CmpOp("==", Name("q"))),
            Compare(
              Call(Name("sum"), Name("q")),
              CmpOp("<=", Name("w")))))))
endmodule
