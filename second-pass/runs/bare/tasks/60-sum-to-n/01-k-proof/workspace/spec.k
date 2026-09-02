requires "verification.k"

module SPEC
  imports VERIFICATION

  claim
    <k>
      Module(
        FuncDef("sum_to_n", Params("n"),
          Return(
            BinOp("//",
              BinOp("*", Name("n"), BinOp("+", Name("n"), Int(1))),
              Int(2)))))
      ~> invoke("sum_to_n", N)
      => .K
    </k>
    <result> noResult => sumSpec(N) </result>
    requires N >=Int 0
endmodule
