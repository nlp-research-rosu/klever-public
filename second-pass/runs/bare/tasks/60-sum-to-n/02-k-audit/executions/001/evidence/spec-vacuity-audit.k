requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: at the satisfying witness N = 0, the program returns
  // sumSpec(0) = 0, not sumSpec(0) + 1 = 1.
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
    <result> noResult => sumSpec(N) +Int 1 </result>
    requires N >=Int 0
endmodule
