// verif3.k — the round-trip with intOf and digitCodes as <k>-CELL REWRITES (not functions),
// so kprove narrows on structure (DS = .IntSeq / iCons ; N > 0 / N == 0) instead of being
// stuck on a frozen function application. Tests whether that lets the round-trip proceed.

module VERIF3
  imports INT
  imports BOOL
  imports LIST
  imports MAP
  imports K-EQUAL

  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)

  // #intOf(DS, ACC): Horner over DS in the <k> cell — the iCons rule NARROWS DS.
  // When DS is exhausted, hand the value V to #digits to rebuild the sequence.
  syntax KItem ::= #intOf(IntSeq, Int) | #digits(Int, IntSeq)
  rule <k> #intOf(.IntSeq, A:Int)               => #digits(A, .IntSeq) ... </k>
  rule <k> #intOf(iCons(C:Int, T:IntSeq), A:Int) => #intOf(T, A *Int 10 +Int (C -Int 48)) ... </k>

  // #digits(N, ACC): peel N lsb-first, PREPEND each digit code → rebuilds msb-first.
  // The N>0 rule NARROWS N. Result lands as an IntSeq in the <k> cell.
  rule <k> #digits(N:Int, ACC:IntSeq) => #digits(N /Int 10, iCons((N modInt 10) +Int 48, ACC)) ... </k>
       requires N >Int 0
  rule <k> #digits(0, ACC:IntSeq) => ACC ... </k>

  // validity (no leading zero, all digit codes) — to scope the claim
  syntax Bool ::= allDig(IntSeq) [function, total]
  rule allDig(.IntSeq)                => true
  rule allDig(iCons(C:Int, T:IntSeq)) => (48 <=Int C andBool C <=Int 57) andBool allDig(T)
  syntax Bool ::= validDec(IntSeq) [function, total]
  rule validDec(iCons(C:Int, .IntSeq))          => 49 <=Int C andBool C <=Int 57
  rule validDec(iCons(C:Int, iCons(D:Int, T:IntSeq)))
       => (49 <=Int C andBool C <=Int 57) andBool allDig(iCons(D, T))
  rule validDec(.IntSeq)                         => false
endmodule
