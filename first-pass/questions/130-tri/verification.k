// verification.k — tri on the UNIFIED semantics. Return the first n+1 Tribonacci-variant numbers.
// The canonical uses float `/2` (e.g. tri(3) = [1, 3, 2.0, 8.0]); but `i/2` (even i) and `(i+3)/2` (odd i)
// are EXACT integers, so solution.py uses `//2` — the resulting int list compares `==` to the canonical's
// float list (2.0 == 2), so NO float is needed (diff-tested 0/300). solution.py also THREADS the last two
// values `a`, `b` as scalars instead of re-reading `my_tri[i-1]`/`my_tri[i-2]` (a self-referencing
// subscript into the growing list), so the recurrence is a clean fib4-style sliding pair.
//
// A range-loop LIST-BUILD with a threaded 2-term lookback + an even/odd branch: triFold(I, HI, A, B, ACC)
// mirrors the loop, appending C (= i//2+1 for even i, = b+a+(i+3)//2 for odd i) via valSeqConcat and
// sliding (a,b)->(b,C). Problem-local — no shared change.

requires "../../reference/src/lemmas.k"

module TRI-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // triFold(I, HI, A, B, ACC) = ACC extended with the Tribonacci-variant terms for i in [I, HI). A/B are
  // the last two terms (my_tri[i-2], my_tri[i-1]); C is appended and (A,B) slides to (B,C). // and % are
  // the reference's pyMod forms. [total]: it lands in the my_tri scope during the fold.
  syntax ValSeq ::= triFold(Int, Int, Int, Int, ValSeq) [function, total]
  rule triFold(I:Int, HI:Int, _A:Int, _B:Int, ACC:ValSeq) => ACC requires I >=Int HI [simplification]
  // even i: c = i//2 + 1
  rule triFold(I:Int, HI:Int, _A:Int, B:Int, ACC:ValSeq)
    => triFold(I +Int 1, HI, B, (I -Int pyMod(I, 2)) /Int 2 +Int 1,
               valSeqConcat(ACC, vCons((I -Int pyMod(I, 2)) /Int 2 +Int 1, .ValSeq)))
    requires I <Int HI andBool pyMod(I, 2) ==Int 0 [simplification]
  // odd i: c = b + a + (i+3)//2
  rule triFold(I:Int, HI:Int, A:Int, B:Int, ACC:ValSeq)
    => triFold(I +Int 1, HI, B, B +Int A +Int (I +Int 3 -Int pyMod(I +Int 3, 2)) /Int 2,
               valSeqConcat(ACC, vCons(B +Int A +Int (I +Int 3 -Int pyMod(I +Int 3, 2)) /Int 2, .ValSeq)))
    requires I <Int HI andBool pyMod(I, 2) ==Int 1 [simplification]

  // result: [1] if n==0, else [1,3] extended by the fold over i in [2, n+1).
  syntax Val ::= triRes(Int) [function]
  rule triRes(N:Int) => list(vCons(1, .ValSeq)) requires N ==Int 0 [simplification]
  rule triRes(N:Int) => list(triFold(2, N +Int 1, 1, 3, vCons(1, vCons(3, .ValSeq))))
    requires N =/=Int 0 [simplification]
endmodule
