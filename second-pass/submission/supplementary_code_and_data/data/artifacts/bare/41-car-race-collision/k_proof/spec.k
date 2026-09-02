requires "verification.k"

module SPEC
  imports VERIFICATION

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
    <functions> .Map => "car_race_collision" |-> definition("n", Return(BinOp("*", Name("n"), Name("n")))) </functions>
    <environment> .Map => "n" |-> N </environment>
    <result> 0 => N *Int N </result>
    requires N >=Int 0
endmodule
