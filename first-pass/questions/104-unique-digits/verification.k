// verification.k — unique_digits on the UNIFIED semantics, TRAP-FREE (P104).
// solution.py is the sheet-sanctioned 1-fn shape: the all_odd helper (and its
// Call trap) is GONE; the genexp-over-str(i) predicate is the sanctioned
// numeric digit while-loop. The while folds via a recursive transition-
// matching summary; sorted() is the shared trusted sortVS.
//
// The flag summary is INT-VALUED (oddI, 0/1) and the branch condition is the
// hooked `oddI(...) ==Int 1`: #branch never splits on a non-hooked Bool
// function term (the P17 lesson, integer-split idiom).

requires "../../reference/src/lemmas.k"

module UNIQUE-DIGITS-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // vsLen is nonnegative (entry: variant-A nonempty discharge after vCons narrowing)
  rule 0 <Int 1 +Int vsLen(_:ValSeq) => true [simplification]
  rule 0 <=Int vsLen(_:ValSeq)       => true [simplification]

  // ---- the digit while summary, transitions in EXACT EXECUTION FORM --------
  // (cond n>0; body: if pyMod(pyMod(n,10),2)==0 -> is_odd=False; n //= 10 with
  // // reducing to (N - pyMod(N,10)) /Int 10). Value 1 iff the flag ends true.
  syntax Int ::= oddI(Int, Bool) [function, total]
  rule oddI(N:Int, B:Bool) => #if B #then 1 #else 0 #fi
    requires notBool (N >Int 0) [simplification]
  rule oddI(N:Int, _:Bool) => oddI((N -Int pyMod(N, 10)) /Int 10, false)
    requires N >Int 0 andBool pyMod(pyMod(N, 10), 2) ==Int 0 [simplification]
  rule oddI(N:Int, B:Bool) => oddI((N -Int pyMod(N, 10)) /Int 10, B)
    requires N >Int 0 andBool notBool (pyMod(pyMod(N, 10), 2) ==Int 0) [simplification]

  // ---- the outer filter-append fold, arms guarded by the folded flag -------
  syntax ValSeq ::= filterOdd2(ValSeq, ValSeq) [function, total]
  rule filterOdd2(.ValSeq, ACC:ValSeq) => ACC [simplification]
  rule filterOdd2(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => filterOdd2(R, valSeqConcat(ACC, vCons(V, .ValSeq)))
    requires isInt(V) andBool oddI(projectIntTotal(V), true) ==Int 1 [simplification]
  rule filterOdd2(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => filterOdd2(R, ACC)
    requires isInt(V) andBool notBool (oddI(projectIntTotal(V), true) ==Int 1) [simplification]
endmodule
