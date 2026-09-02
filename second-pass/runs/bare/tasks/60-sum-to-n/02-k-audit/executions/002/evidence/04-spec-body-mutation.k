requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The executed program body is materially changed from n * (n + 1) // 2
  // to n * (n + 2) // 2, while the original postcondition is retained.
  claim
    <k>
      Module(
        FuncDef("sum_to_n", Params("n"),
          Return(
            BinOp("//",
              BinOp("*", Name("n"), BinOp("+", Name("n"), Int(2))),
              Int(2)))))
      ~> invoke("sum_to_n", N)
      => .K
    </k>
    <result> noResult => sumSpec(N) </result>
    requires N >=Int 0
endmodule
