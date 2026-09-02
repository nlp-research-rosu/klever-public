// verification.k — factorize on the UNIFIED semantics. Return the ascending list of prime factors of n
// (with multiplicity), product == n. solution.py is the trial-division loop `while i<=n: if n%i==0:
// fact+=[i]; n//=i else i+=1` (reduces n to 1, so the canonical's sqrt bound + final append are
// unnecessary; behavior-equal, diff-tested 0/19998).
//
// SAME trial-division rung as is_multiply_prime #143 (factorCount), but building the factor LIST instead
// of counting: factorList(N, I, ACC) — a recursive summary matching the loop's own transitions with a
// THREADED ValSeq accumulator (the digitAcc / factorCount shape; matches `fact = fact + [i]` exactly, so
// the circularity closes without a list-association lemma). Problem-local — no shared change.

requires "../../reference/src/lemmas.k"

module FACTORIZE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // factorList(N, I, ACC) = ACC followed by the prime factors of N (ascending, with multiplicity) found
  // by trial division from divisor I: ACC once I > N; else if I divides N append it and recurse on N//I
  // (reference's pyMod-based // and %); else try I+1. ACC threaded (matches the body's `fact = fact + [i]`
  // = valSeqConcat). [total]: it lands in the `fact` scope during the fold (I >= 2 always, divisor != 0).
  syntax ValSeq ::= factorList(Int, Int, ValSeq) [function, total]
  rule factorList(N:Int, I:Int, ACC:ValSeq) => ACC requires I >Int N [simplification]
  rule factorList(N:Int, I:Int, ACC:ValSeq)
    => factorList((N -Int pyMod(N, I)) /Int I, I, valSeqConcat(ACC, vCons(I, .ValSeq)))
    requires I <=Int N andBool pyMod(N, I) ==Int 0 [simplification]
  rule factorList(N:Int, I:Int, ACC:ValSeq) => factorList(N, I +Int 1, ACC)
    requires I <=Int N andBool notBool (pyMod(N, I) ==Int 0) [simplification]

  // result = the prime factorization list of N.
  syntax Val ::= factorizeRes(Int) [function]
  rule factorizeRes(N:Int) => list(factorList(N, 2, .ValSeq)) [simplification]
endmodule
