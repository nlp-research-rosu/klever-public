requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTANT
  imports MPY

  syntax Module ::= "mutantSolutionModule" [macro]
  rule mutantSolutionModule
    => Module(
         FuncDef("car_race_collision", Params("n"),
           Return(BinOp("+", Name("n"), Name("n")))))

  syntax KItem ::= "#runMutant" "(" Int ")"
  rule #runMutant(N:Int)
    => #loadAll(mutantSolutionModule)
       ~> Call(Name("car_race_collision"), Int(N))
endmodule
