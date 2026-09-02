requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Body-sensitivity probe: mutated source body returns 0 but retains square postcondition.
  claim
    <k>
      Module(
        FuncDef(
          "car_race_collision",
          Params("n"),
          Return(Int(0))
        )
      ) ~> run("car_race_collision", N)
      => .K
    </k>
    <functions> .Map => "car_race_collision" |-> definition("n", Return(Int(0))) </functions>
    <environment> .Map => "n" |-> N </environment>
    <result> 0 => N *Int N </result>
    requires N >=Int 0
endmodule
