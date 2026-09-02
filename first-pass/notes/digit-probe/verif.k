// verif.k — minimal model to probe how a proof can reason about the decimal digits of a
// SYMBOLIC non-negative integer. Three questions:
//   (A) can an arithmetic digit-peel  while(n>0){ acc+=f(n%10); n/=10 }  close by induction on n?
//   (B) can the round-trip  digitCodes(intOf(DS)) == DS  be PROVEN (not trusted)?
//   (C) does iterating str(N)=digitCodes(N) for symbolic N unfold at all? (expected: no)

module VERIF
  imports INT
  imports BOOL
  imports LIST
  imports MAP
  imports K-EQUAL

  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)

  // even-ness bump of a single digit value D (0..9): 1 if even else 0
  syntax Int ::= ev(Int) [function, total]
  rule ev(D:Int) => #if D modInt 2 ==Int 0 #then 1 #else 0 #fi

  // ---- (A) arithmetic peel, as a <k>-cell loop, + its recurrence summary ----
  syntax KItem ::= #peel(Int, Int)               // (remaining n, accumulated even-count)
  rule <k> #peel(N:Int, A:Int) => #peel(N /Int 10, A +Int ev(N modInt 10)) ... </k> requires N >Int 0
  rule <k> #peel(N:Int, A:Int) => A ... </k>                                          requires N <=Int 0

  syntax Int ::= evenOfInt(Int, Int) [function]
  rule evenOfInt(N:Int, A:Int) => A                                                requires N <=Int 0
  rule evenOfInt(N:Int, A:Int) => evenOfInt(N /Int 10, A +Int ev(N modInt 10))     requires N >Int 0

  // ---- (B) digitCodes / intOfDigits / round-trip ----------------------------
  // decimal digit codes of a non-negative int (recursive; concrete-friendly)
  syntax IntSeq ::= digitCodes(Int) [function]
  rule digitCodes(N:Int) => iCons(N +Int 48, .IntSeq)                       requires 0 <=Int N andBool N <Int 10
  rule digitCodes(N:Int) => snocD(digitCodes(N /Int 10), (N modInt 10) +Int 48) requires N >=Int 10

  syntax IntSeq ::= snocD(IntSeq, Int) [function, total]
  rule snocD(.IntSeq, C:Int)               => iCons(C, .IntSeq)
  rule snocD(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocD(T, C))

  // value of a digit-code sequence (Horner, most-significant first)
  syntax Int ::= intOf(IntSeq) [function]
  rule intOf(DS:IntSeq) => intOfAcc(DS, 0)
  syntax Int ::= intOfAcc(IntSeq, Int) [function]
  rule intOfAcc(.IntSeq, ACC:Int)               => ACC
  rule intOfAcc(iCons(C:Int, T:IntSeq), ACC:Int) => intOfAcc(T, ACC *Int 10 +Int (C -Int 48))

  // even-digit count fold over a code sequence
  syntax Int ::= evenSeq(IntSeq, Int) [function]
  rule evenSeq(.IntSeq, EC:Int)               => EC
  rule evenSeq(iCons(C:Int, T:IntSeq), EC:Int) => evenSeq(T, EC +Int ev(C -Int 48))

  // validity of a decimal code sequence: non-empty, all codes 48..57, and no leading zero
  // unless it is exactly "0". (used to scope the round-trip claim)
  syntax Bool ::= allDig(IntSeq) [function, total]
  rule allDig(.IntSeq)               => true
  rule allDig(iCons(C:Int, T:IntSeq)) => (48 <=Int C andBool C <=Int 57) andBool allDig(T)

  syntax Bool ::= validDec(IntSeq) [function, total]
  rule validDec(iCons(C:Int, .IntSeq))          => 48 <=Int C andBool C <=Int 57
  rule validDec(iCons(C:Int, iCons(D:Int, T:IntSeq)))
       => (49 <=Int C andBool C <=Int 57) andBool allDig(iCons(D, T))
  rule validDec(.IntSeq)                         => false

  // ---- (C) a str-iteration model over digitCodes(N) -------------------------
  syntax KItem ::= #iter(IntSeq, Int)            // walk the seq accumulating even count
  rule <k> #iter(.IntSeq, A:Int)               => A ... </k>
  rule <k> #iter(iCons(C:Int, T:IntSeq), A:Int) => #iter(T, A +Int ev(C -Int 48)) ... </k>
endmodule
