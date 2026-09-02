// verif4.k — the round-trip with a STRENGTHENED induction hypothesis. The weak claim
// #intOf(DS, 0) => DS pins the accumulator at 0, so the recursive state #intOf(T, C-48)
// never re-matches and kprove unrolls forever. Generalize the accumulator:
//     #intOf(DS, A)  =>  digitCodes(A) ++ DS         (for A >= 1, DS all digit codes)
// Now the recursive call #intOf(T, A') has A' = A*10+(C-48) >= 1, so the claim re-matches
// as its own IH. The step closes on the identity digitCodes(A*10+d) = digitCodes(A) ++ [d].

module VERIF4
  imports INT
  imports BOOL
  imports LIST
  imports MAP
  imports K-EQUAL

  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)

  // concatenation + its associativity (the one structural helper the step needs)
  syntax IntSeq ::= cat(IntSeq, IntSeq) [function, total]
  rule cat(.IntSeq, T:IntSeq)               => T
  rule cat(iCons(H:Int, X:IntSeq), T:IntSeq) => iCons(H, cat(X, T))
  rule cat(cat(X:IntSeq, Y:IntSeq), Z:IntSeq) => cat(X, cat(Y, Z)) [simplification]
  rule cat(X:IntSeq, .IntSeq) => X [simplification]

  // digitCodes as a function; recursive rule uses cat[last] so it aligns with the IH
  syntax IntSeq ::= digitCodes(Int) [function]
  rule digitCodes(N:Int) => iCons(N +Int 48, .IntSeq)                    requires 0 <=Int N andBool N <Int 10
  rule digitCodes(N:Int) => cat(digitCodes(N /Int 10), iCons((N modInt 10) +Int 48, .IntSeq)) requires N >=Int 10

  // arithmetic normalization the step needs: (A*10 + D)/10 = A and %10 = D when 0<=D<10
  rule (A:Int *Int 10 +Int D:Int) /Int 10   => A requires 0 <=Int D andBool D <Int 10 [simplification]
  rule (A:Int *Int 10 +Int D:Int) modInt 10 => D requires 0 <=Int D andBool D <Int 10 [simplification]

  // allDig exposes the HEAD bound even for a symbolic tail (single iCons rule)
  syntax Bool ::= allDig(IntSeq) [function, total]
  rule allDig(.IntSeq)                => true
  rule allDig(iCons(C:Int, T:IntSeq)) => (48 <=Int C andBool C <=Int 57) andBool allDig(T)

  // #intOf: Horner over DS in the <k> cell; base emits digitCodes(A) directly.
  syntax KItem ::= #intOf(IntSeq, Int)
  rule <k> #intOf(.IntSeq, A:Int)                => digitCodes(A) ... </k>
  rule <k> #intOf(iCons(C:Int, T:IntSeq), A:Int) => #intOf(T, A *Int 10 +Int (C -Int 48)) ... </k>
endmodule
