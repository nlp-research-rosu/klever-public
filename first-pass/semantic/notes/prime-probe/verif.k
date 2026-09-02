// prime-probe — the is_prime core: a SYMBOLIC-bound divisor scan with early exit.
//   for i in [I, N): if N % i == 0 -> "div" (found a divisor, stop); else i+1.
// Tests whether the counter induction (range-loop machinery) + a symbolic `N %Int i ==Int 0`
// case-split + a boolean ∃-summary close. If yes, the primality cluster (31 39 75 82 94 96 ...) is open.
module PRIME
  imports INT
  imports BOOL
  imports K-EQUAL
  syntax KItem ::= scan(Int, Int) | loopLbl(K)
  syntax Res   ::= "noDiv" | "div"
  configuration <k> $PGM:K </k> <res> noDiv </res>

  rule <k> scan(I:Int, N:Int) => .K ... </k> requires notBool (I <Int N)               // range exhausted
  rule <k> scan(I:Int, N:Int) => .K ... </k> <res> _ => div </res>
       requires (I <Int N) andBool (N %Int I ==Int 0)                                   // divisor -> stop
  rule <k> scan(I:Int, N:Int) => loopLbl(scan(I +Int 1, N)) ... </k>
       requires (I <Int N) andBool (N %Int I =/=Int 0)                                  // no divisor -> next
  rule <k> loopLbl(NEXT:K) => NEXT ... </k>

  // summary: hasDiv(I, N) = exists j in [I, N): N mod j == 0  (recurses on the INCREASING i)
  syntax Bool ::= hasDiv(Int, Int) [function]
  rule hasDiv(I:Int, N:Int) => false requires notBool (I <Int N) [simplification]
  rule hasDiv(I:Int, N:Int) => true  requires (I <Int N) andBool (N %Int I ==Int 0) [simplification]
  rule hasDiv(I:Int, N:Int) => hasDiv(I +Int 1, N) requires (I <Int N) andBool (N %Int I =/=Int 0) [simplification]
  rule #Ceil(hasDiv(_:Int, _:Int)) => #Top [simplification]   // full coverage -> defined everywhere
endmodule
