requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // This is the exact Module term generated in solution.mpy.
  syntax Module ::= "solutionModule" [macro]
  rule solutionModule
    => Module(
         FuncDef("car_race_collision", Params("n"),
           Return(BinOp("*", Name("n"), Name("n")))))

  // Load the submitted module, then call its required entry point.
  syntax KItem ::= "#runCarRaceCollision" "(" Int ")"
  rule #runCarRaceCollision(N:Int)
    => #loadAll(solutionModule)
       ~> Call(Name("car_race_collision"), Int(N))
endmodule
