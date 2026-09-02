// verification.k — get_odd_collatz on the UNIFIED semantics. Return the SORTED list of the odd numbers
// in the Collatz sequence of n. solution.py uses integer `n//2` (the canonical's float `n/2` + `int(n)`
// are unnecessary) and list-`+` to collect (diff-tested 0/4999).
//
// Same DATA-DEPENDENT recursive-summary rung as trial-division #143/#142
// ([[trial-division-recursive-summary-rung]]): collatzFold(N, ACC) mirrors the loop's transitions
// (n//2 vs n*3+1 on n%2) with a THREADED ValSeq accumulator, plus the collect-if (append the new n when
// odd). PARTIAL correctness modulo termination: [total] TRUSTS the Collatz conjecture (the loop halts) —
// the same trust level as the sortVS at the end. The final `sorted` is the trusted sort
// ([[trusted-sort-rung-unified]]). Problem-local — no shared change.

requires "../../reference/src/lemmas.k"

module GET-ODD-COLLATZ-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // collatzFold(N, ACC) = ACC followed by the odd numbers reached from N in the Collatz sequence (the new
  // value after each step, collected when odd). Mirrors the body: even N -> N//2 (collect if odd); odd
  // N>1 -> N*3+1 (always even, never collected). ACC threaded (= the body's `odd_collatz = odd_collatz +
  // [n]` = valSeqConcat). [total]: it lands in the odd_collatz scope during the fold AND trusts Collatz
  // termination. reference's pyMod-based // and %.
  syntax ValSeq ::= collatzFold(Int, ValSeq) [function, total]
  rule collatzFold(N:Int, ACC:ValSeq) => ACC requires N <=Int 1 [simplification]
  // odd N > 1: n = n*3+1 (even, not collected)
  rule collatzFold(N:Int, ACC:ValSeq) => collatzFold(N *Int 3 +Int 1, ACC)
    requires N >Int 1 andBool pyMod(N, 2) ==Int 1 [simplification]
  // even N: n = n//2; collect n//2 iff it is odd
  rule collatzFold(N:Int, ACC:ValSeq)
    => collatzFold((N -Int pyMod(N, 2)) /Int 2,
                   valSeqConcat(ACC, vCons((N -Int pyMod(N, 2)) /Int 2, .ValSeq)))
    requires N >Int 1 andBool pyMod(N, 2) ==Int 0
      andBool pyMod((N -Int pyMod(N, 2)) /Int 2, 2) ==Int 1 [simplification]
  rule collatzFold(N:Int, ACC:ValSeq) => collatzFold((N -Int pyMod(N, 2)) /Int 2, ACC)
    requires N >Int 1 andBool pyMod(N, 2) ==Int 0
      andBool pyMod((N -Int pyMod(N, 2)) /Int 2, 2) ==Int 0 [simplification]

  // result = sorted(odd_collatz). Initial odd_collatz = [n] if n odd else []; then the fold; then sort.
  syntax Val ::= getOddCollatzRes(Int) [function]
  rule getOddCollatzRes(N:Int) => list(sortVS(collatzFold(N, vCons(N, .ValSeq))))
    requires pyMod(N, 2) ==Int 1 [simplification]
  rule getOddCollatzRes(N:Int) => list(sortVS(collatzFold(N, .ValSeq)))
    requires pyMod(N, 2) ==Int 0 [simplification]
endmodule
