// verification.k — is_multiply_prime on the UNIFIED semantics. The canonical's triple-nested prime loop
// (i*j*k == a over primes i,j,k) is behavior-equal to "a has exactly 3 prime factors with multiplicity"
// for a < 100. solution.py computes that count by trial division and returns `count == 3` (diff-tested
// 0/100 over the whole domain a < 100).
//
// The trial-division while has no CLOSED-FORM fold, but it DOES have a recursive summary matching its own
// transitions: factorCount(A, I) — like the digitAcc numeric-while (numeric-while-digitsum-rung) but with
// a data-dependent %-branch (divide vs. increment). The [all-path] loop invariant folds count via it;
// each branch of the body lines up 1:1 with one factorCount rule. Problem-local — no shared change.

requires "../../reference/src/lemmas.k"

module IS-MULTIPLY-PRIME-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // factorCount(A, I, ACC) = ACC plus the number of prime factors of A (with multiplicity) found by
  // trial division from divisor I: ACC once I > A; else if I divides A bump ACC and recurse on A//I
  // (reference's pyMod-based // and %); else try I+1. The count accumulator ACC is THREADED (the digitAcc
  // pattern) — matching the body's `count = count + 1` exactly, so the circularity closes without an
  // arithmetic-association lemma. [total]: it lands in the `count` scope during the fold (only ever called
  // with I >= 2, so the pyMod divisor is never 0).
  syntax Int ::= factorCount(Int, Int, Int) [function, total]
  rule factorCount(A:Int, I:Int, ACC:Int) => ACC requires I >Int A [simplification]
  rule factorCount(A:Int, I:Int, ACC:Int) => factorCount((A -Int pyMod(A, I)) /Int I, I, ACC +Int 1)
    requires I <=Int A andBool pyMod(A, I) ==Int 0 [simplification]
  rule factorCount(A:Int, I:Int, ACC:Int) => factorCount(A, I +Int 1, ACC)
    requires I <=Int A andBool notBool (pyMod(A, I) ==Int 0) [simplification]

  // result = (count == 3): a is the product of exactly 3 primes (with multiplicity).
  syntax Bool ::= mulPrimeRes(Int) [function]
  rule mulPrimeRes(A:Int) => factorCount(A, 2, 0) ==Int 3 [simplification]
endmodule
