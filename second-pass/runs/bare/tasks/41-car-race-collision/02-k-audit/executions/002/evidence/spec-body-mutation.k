requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // This changes the constructor term actually executed by the claim from
  // `return n * n` to `return n * 0`, while retaining the original result
  // obligation. It is false, for example, at the satisfying input N = 1.
  claim
    <k>
      Module(
        FuncDef(
          "car_race_collision",
          Params("n"),
          Return(BinOp("*", Name("n"), Int(0)))
        )
      ) ~> run("car_race_collision", N)
      => .K
    </k>
    <functions>
      .Map
      => "car_race_collision" |->
           definition("n", Return(BinOp("*", Name("n"), Int(0))))
    </functions>
    <environment> .Map => "n" |-> N </environment>
    <result> 0 => N *Int N </result>
    requires N >=Int 0
endmodule
