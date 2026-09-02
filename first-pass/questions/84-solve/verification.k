// verification.k — solve on the UNIFIED semantics. solve(N) = bin(sum-of-digits(N))[2:], the binary
// string of N's decimal digit sum. solution.py rewrites `bin(sum(int(i) for i in str(N)))[2:]` (which
// hits the str-of-symbolic-int wall) as two numeric whiles: (1) arithmetic digit-sum
// `while N>0: s+=N%10; N//=10`, (2) base-2 code build `while s>0: ret=str(s%2)+ret; s//=2`, with an
// `if s==0: return '0'` for N==0 (bin(0)[2:]='0'). Diff-tested 0/40010.
//
// A COMPOSITION of two proven rungs: the digit-sum numeric-while (digitAcc,
// Q94 skjkasdkd) + the base-B code build (baseFold, Q44 change_base; the
// single-digit str rides the SHARED digitCodes bridge + pyMod range facts).
// See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module SOLVE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // Loop 1: decimal digit sum (digitAcc, the reference's pyMod-based // and %). digitAcc(N, R) = R plus
  // the sum of N's decimal digits. [total]: it lands in the scope during the fold.
  syntax Int ::= digitAcc(Int, Int) [function, total]
  rule digitAcc(N:Int, R:Int) => R requires N <=Int 0 [simplification]
  rule digitAcc(N:Int, R:Int) => digitAcc((N -Int pyMod(N, 10)) /Int 10, R +Int pyMod(N, 10))
    requires N >Int 0 [simplification]

  // Loop 2: base-B digit CODES (baseFold, from change_base). baseFold(X, B, RC) = the base-B digit codes
  // of X (most-significant first) prepended before RC. B=2 here. [total]: scope-map value.
  syntax IntSeq ::= baseFold(Int, Int, IntSeq) [function, total]
  rule baseFold(X:Int, _B:Int, RC:IntSeq) => RC requires X <=Int 0 [simplification]
  rule baseFold(X:Int, B:Int, RC:IntSeq)
    => baseFold((X -Int pyMod(X, B)) /Int B, B, iCons(48 +Int pyMod(X, B), RC))
    requires X >Int 0 [simplification]

  // result = bin(digitAcc(N,0))[2:]. digit sum 0 (iff N<=0) -> "0"; else the base-2 code string of it.
  syntax Val ::= solveRes(Int) [function]
  rule solveRes(N:Int) => str(iCons(48, .IntSeq)) requires digitAcc(N, 0) ==Int 0 [simplification]
  rule solveRes(N:Int) => str(baseFold(digitAcc(N, 0), 2, .IntSeq))
    requires notBool (digitAcc(N, 0) ==Int 0) [simplification]
endmodule
