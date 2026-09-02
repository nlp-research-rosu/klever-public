// verification.k — split_words on the UNIFIED semantics, TRAP-FREE (de-escape
// rework P125). solution.py is canonical's one function (the comprehension-len
// branch is a diff-tested count loop); NO Call interceptions — the membership
// tests, splits, and per-char class tests all reduce through the shared
// semantics; the count folds via the guarded evenLowerCount summary.

requires "../../reference/src/lemmas.k"

module SPLIT-WORDS-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // (atI + the intSeqAt bounds bridge are SHARED: lemmas/subscript.k; the
  // INLINE txt[i] atoms land on the total accessor so folds match sans #Ceil)

  // ---- the per-char test as the inline body produces it: isLowerC(atI(CS,I))
  // (txt[i].islower() over the 1-char subscript) and pyMod(atI(CS,I),2)==0
  // (ord(txt[i]) % 2 == 0). Guarded RULE-based predicate for the fold.
  syntax Bool ::= evenLowerV(Val, Val) [function, total, symbol(evenLowerV)]
  rule evenLowerV(str(CS:IntSeq), I:Int) => true
    requires 0 <=Int I andBool I <Int isLen(CS)
     andBool isLowerC(atI(CS, I)) andBool pyMod(atI(CS, I), 2) ==Int 0
    [simplification]
  rule evenLowerV(str(CS:IntSeq), I:Int) => false
    requires 0 <=Int I andBool I <Int isLen(CS)
     andBool notBool (isLowerC(atI(CS, I)) andBool pyMod(atI(CS, I), 2) ==Int 0)
    [simplification]

  // count fold over i in [I, N): count += 1 when evenLowerV(txt, i). Guarded
  // case-split (the primeAcc pattern).
  syntax Int ::= evenLowerCount(Val, Int, Int, Int) [function, total]
  rule evenLowerCount(_T:Val, I:Int, N:Int, C:Int) => C requires I >=Int N [simplification]
  rule evenLowerCount(T:Val, I:Int, N:Int, C:Int) => evenLowerCount(T, I +Int 1, N, C +Int 1)
    requires I <Int N andBool evenLowerV(T, I) [simplification]
  rule evenLowerCount(T:Val, I:Int, N:Int, C:Int) => evenLowerCount(T, I +Int 1, N, C)
    requires I <Int N andBool notBool evenLowerV(T, I) [simplification]
endmodule
