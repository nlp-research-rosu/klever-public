// verification.k — get_max_triples on the UNIFIED semantics. TRIPLE nested COUNT. The list
// A = [i*i-i+1 | i in 1..n] is INDEX-based, so A[i] (0-based) = (i+1)^2-(i+1)+1 is inlined as
// aVal(i) — no symbolic list elements, no isInt echo. Counts triples i<j<k with
// (A[i]+A[j]+A[k]) % 3 == 0. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module GET-MAX-TRIPLES-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // A[m] (0-based) = (m+1)^2 - (m+1) + 1 (the list-comprehension value, index-inlined).
  syntax Int ::= aVal(Int) [function, total]
  rule aVal(M:Int) => (((M +Int 1) *Int (M +Int 1)) -Int (M +Int 1)) +Int 1 [simplification]

  // innermost k-count over k in [K, N): +1 when (A[i]+A[j]+A[k]) % 3 == 0 (i, j fixed).
  // Guarded case-split (the primeAcc/#40 pattern); guard = the program's If condition inlined.
  syntax Int ::= kFold(Int, Int, Int, Int, Int) [function, total]
  rule kFold(K:Int, N:Int, _I:Int, _J:Int, C:Int) => C requires K >=Int N [simplification]
  rule kFold(K:Int, N:Int, I:Int, J:Int, C:Int) => kFold(K +Int 1, N, I, J, C +Int 1)
    requires K <Int N andBool pyMod((aVal(I) +Int aVal(J)) +Int aVal(K), 3) ==Int 0 [simplification]
  rule kFold(K:Int, N:Int, I:Int, J:Int, C:Int) => kFold(K +Int 1, N, I, J, C)
    requires K <Int N andBool pyMod((aVal(I) +Int aVal(J)) +Int aVal(K), 3) =/=Int 0 [simplification]

  // middle j-count over j in [J, N): each runs the k-count from k = j+1 (i fixed).
  syntax Int ::= jFold(Int, Int, Int, Int) [function, total]
  rule jFold(J:Int, N:Int, _I:Int, C:Int) => C requires J >=Int N [simplification]
  rule jFold(J:Int, N:Int, I:Int, C:Int)
    => jFold(J +Int 1, N, I, kFold(J +Int 1, N, I, J, C)) requires J <Int N [simplification]

  // outer i-count over i in [I, N): each runs the j-count from j = i+1.
  syntax Int ::= iFold(Int, Int, Int) [function, total]
  rule iFold(I:Int, N:Int, C:Int) => C requires I >=Int N [simplification]
  rule iFold(I:Int, N:Int, C:Int)
    => iFold(I +Int 1, N, jFold(I +Int 1, N, I, C)) requires I <Int N [simplification]

  // result: number of triples i < j < k with (A[i] + A[j] + A[k]) % 3 == 0.
  syntax Val ::= maxTriplesRes(Int) [function]
  rule maxTriplesRes(N:Int) => iFold(0, N, 0) [simplification]
endmodule
