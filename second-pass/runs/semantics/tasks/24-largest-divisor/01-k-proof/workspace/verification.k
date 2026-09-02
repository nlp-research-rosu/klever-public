requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The exact statement body emitted in solution.mpy.  Naming it keeps the
  // reachability claims readable; this equation is only syntactic sharing.
  syntax Stmts ::= largestDivisorBody() [function]
  rule largestDivisorBody()
    => Expr(Str("Return the largest positive divisor of n that is smaller than n."))
       Assign(Name("divisor"), BinOp("-", Name("n"), Int(1)))
       While(
         Compare(
           BinOp("%", Name("n"), Name("divisor")),
           CmpOp("!=", Int(0))),
         AugAssign(Name("divisor"), "-", Int(1)))
       Return(Name("divisor"))

  // Mathematical reference result: scan the positive candidates strictly
  // below N in descending order and select the first divisor.  Thus the
  // result divides N, is below N, and no larger candidate below N divides N.
  syntax Int ::= largestProperDivisor(Int) [function]
               | firstDivisorAtOrBelow(Int, Int) [function]

  rule largestProperDivisor(N:Int)
    => firstDivisorAtOrBelow(N, N -Int 1)

  rule firstDivisorAtOrBelow(N:Int, D:Int) => D
    requires D >Int 0 andBool pyMod(N, D) ==Int 0

  rule firstDivisorAtOrBelow(N:Int, D:Int)
    => firstDivisorAtOrBelow(N, D -Int 1)
    requires D >Int 1 andBool pyMod(N, D) =/=Int 0

  // The symbolic Map backend leaves deletion of a symbolic frame as an
  // update term.  This extensional simplification is the Map fact used by
  // #pop: deleting the fresh key 1 restores the untouched remainder.
  rule
    (1 |-> _S:Scope SC:Map) [1 <- undef] => SC
    requires notBool 1 in_keys(SC)
    [simplification, label(deleteFreshFrame)]
endmodule
