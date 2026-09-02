requires "reference-semantics/semantics.k"

module MODP-VERIFICATION-BODY-MUTANT
  imports MPY

  syntax Stmts ::= "modpBodyMutant" [function]
  rule modpBodyMutant
    => Expr(Str("Return 2^n modulo p."))
       Return(BinOp("%", BinOp("**", Int(3), Name("n")), Name("p")))

  syntax Module ::= "modpProgramMutant" [function]
  rule modpProgramMutant
    => Module(
         FuncDef("modp", Params("n", "p"), modpBodyMutant))

  syntax Int ::= specModpMutantBodyTest(Int, Int) [function]
  rule specModpMutantBodyTest(N:Int, P:Int) => pyMod(2 ^Int N, P)
       requires N >=Int 0 andBool P >Int 0
endmodule
