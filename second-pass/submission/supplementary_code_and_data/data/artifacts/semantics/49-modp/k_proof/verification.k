requires "reference-semantics/semantics.k"

module MODP-VERIFICATION
  imports MPY

  // This is the exact Module term generated in solution.mpy.  Giving it a
  // name keeps the reachability claim readable while still executing the
  // translated program through the supplied Python semantics.
  syntax Stmts ::= "modpBody" [function]
  rule modpBody
    => Expr(Str("Return 2^n modulo p."))
       Return(BinOp("%", BinOp("**", Int(2), Name("n")), Name("p")))

  syntax Module ::= "modpProgram" [function]
  rule modpProgram
    => Module(
         FuncDef("modp", Params("n", "p"), modpBody))

  // Mathematical contract for the supported input domain.  pyMod is the
  // supplied semantics' Python (floored) remainder, and ^Int is unbounded
  // integer exponentiation.
  syntax Int ::= specModp(Int, Int) [function]
  rule specModp(N:Int, P:Int) => pyMod(2 ^Int N, P)
       requires N >=Int 0 andBool P >Int 0
endmodule
