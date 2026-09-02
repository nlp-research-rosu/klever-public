requires "reference-semantics/semantics.k"

module MODP-VERIFICATION-BODY-MUT
  imports MPY

  syntax Stmts ::= "modpBodyMut" [function]
  rule modpBodyMut
    => Expr(Str("Return 2^n modulo p."))
       Return(BinOp("%", BinOp("**", Int(3), Name("n")), Name("p")))

  syntax Module ::= "modpProgramMut" [function]
  rule modpProgramMut
    => Module(
         FuncDef("modp", Params("n", "p"), modpBodyMut))

  syntax Int ::= specModpMut(Int, Int) [function]
  rule specModpMut(N:Int, P:Int) => pyMod(2 ^Int N, P)
       requires N >=Int 0 andBool P >Int 0
endmodule
