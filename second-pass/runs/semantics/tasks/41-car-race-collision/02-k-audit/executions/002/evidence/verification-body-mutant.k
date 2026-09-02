requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTANT
  imports MPY

  syntax Module ::= "mutatedSolutionModule" [macro]
  rule mutatedSolutionModule
    => Module(
         FuncDef("car_race_collision", Params("n"),
           Return(BinOp("+", Name("n"), Name("n")))))

  syntax KItem ::= "#runMutatedCarRaceCollision" "(" Int ")"
  rule #runMutatedCarRaceCollision(N:Int)
    => #loadAll(mutatedSolutionModule)
       ~> Call(Name("car_race_collision"), Int(N))
endmodule
