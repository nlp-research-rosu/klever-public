requires "verification.k"

module MODP-PINNING
  imports MODP-VERIFICATION

  claim
    <k>
      modpProgram
      =>
      Module(
        FuncDef("modp", Params("n", "p"),
          Expr(Str("Return 2^n modulo p."))
          Return(BinOp("%", BinOp("**", Int(2), Name("n")), Name("p")))))
    </k>
endmodule
