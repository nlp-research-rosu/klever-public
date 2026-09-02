requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false result obligation: the actual result is required to be one
  // larger. N = 0 satisfies the precondition and witnesses 0 != 1.
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
