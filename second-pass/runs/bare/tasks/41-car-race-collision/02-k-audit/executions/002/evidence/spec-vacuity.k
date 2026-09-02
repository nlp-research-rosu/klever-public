requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh result-obligation mutation. The original submitted program still
  // executes, but its result is falsely required to be one larger. N = 0 is a
  // concrete satisfying input witnessing 0 != 1.
  claim
    <k>
      Module(
        FuncDef(
          "car_race_collision",
          Params("n"),
          Return(BinOp("*", Name("n"), Name("n")))
        )
      ) ~> run("car_race_collision", N)
      => .K
    </k>
    <functions>
      .Map
      => "car_race_collision" |->
           definition("n", Return(BinOp("*", Name("n"), Name("n"))))
    </functions>
    <environment> .Map => "n" |-> N </environment>
    <result> 0 => (N *Int N) +Int 1 </result>
    requires N >=Int 0
endmodule
