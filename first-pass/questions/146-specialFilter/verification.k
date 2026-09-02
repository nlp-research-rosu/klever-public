// verification.k — specialFilter on the UNIFIED semantics, TRAP-FREE (P146).
// solution.py is canonical verbatim: element loop, per-element str(num) on an
// abstract element (SHARED digitCodes echo, lemmas/str-int-decimal.k),
// first/last digit via the real subscripts, int() via the SHARED intDigAcc
// echo (lemmas/builtins.k), tuple membership.

requires "../../reference/src/lemmas.k"

module SPECIALFILTER-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // digit strings are never empty (digitCodes is cons-headed on its domain)
  rule isLen(digitCodes(N:Int)) >Int 0 => true requires N >=Int 0 [simplification]
  rule 0 <Int isLen(digitCodes(N:Int)) => true requires N >=Int 0 [simplification]

  // the executed `in` compare on an Int value vs the concrete tuple: echo to
  // the shared memberVS fold (the k-cell #memberAcc route sticks on fn terms)
  rule applyCmp("in", V:Val, tuple(TS:ValSeq)) => memberVS(V, TS)
    requires isInt(V) [simplification]

  // first/last digit through the ONE-STEP-unfolded digitCodes spine the
  // defining rules produce under N>=10: route atI across seqConcat
  rule atI(seqConcat(A:IntSeq, _B:IntSeq), I:Int) => atI(A, I)
    requires 0 <=Int I andBool I <Int isLen(A) [simplification]
  rule atI(seqConcat(A:IntSeq, B:IntSeq), I:Int) => atI(B, I -Int isLen(A))
    requires isLen(A) <=Int I [simplification]

  // A floored-division `N /Int 10` inside a non-smtlib head (digitCodes) makes the resulting
  // memberVS(atI(..),odds) atom un-case-splittable, so the `if first and last` #if FLOATS
  // (differential-probed: same atom with a bare Int folds fine; adding /Int breaks it). Fold the
  // executed leading-digit code atI(digitCodes(N/10),0) into an OPAQUE TOTAL helper that hides the
  // /Int — both the model (atI(digitCodes(V),0) via the seqConcat routing) and the execution reach
  // it, and memberVS(fdc(V)-48, odds) then case-splits normally.
  syntax Int ::= fdc(Int) [function, total]
  rule atI(digitCodes(N:Int /Int 10), 0) => fdc(N) [simplification]

  // the executed str[-1] uses intSeqAt (partial) over the same seqConcat spine — route it like atI,
  // then fold the last code (which carries the pyMod (N%10+10)%10 form) into an opaque total helper
  // so memberVS(ldc(N)-48, odds) case-splits (same /Int-inside issue, here %Int).
  rule intSeqAt(seqConcat(A:IntSeq, _B:IntSeq), I:Int) => intSeqAt(A, I)
    requires 0 <=Int I andBool I <Int isLen(A) [simplification]
  rule intSeqAt(seqConcat(A:IntSeq, B:IntSeq), I:Int) => intSeqAt(B, I -Int isLen(A))
    requires isLen(A) <=Int I [simplification]
  // exact-boundary (last element): the general routing's isLen(A) <=Int isLen(A) guard does not
  // discharge on the opaque isLen, so spell the boundary index directly.
  rule atI(seqConcat(A:IntSeq, B:IntSeq), isLen(A)) => atI(B, 0) [simplification]
  rule intSeqAt(seqConcat(A:IntSeq, B:IntSeq), isLen(A)) => intSeqAt(B, 0) [simplification]

  // the units digit (N%10+10)%10 is a %Int inside the membership — same un-case-splittable issue as
  // the /Int leading digit. Fold to an opaque total helper AT THE memberVS LEVEL (not the raw
  // arithmetic, which would also rewrite the identical form inside digitCodes's last code and break
  // the fdc leading-digit match).
  syntax Int ::= ldc(Int) [function, total]
  rule memberVS((N:Int %Int 10 +Int 10) %Int 10, TS:ValSeq) => memberVS(ldc(N), TS) [simplification]

  // membership of a digit value in (1,3,5,7,9) — spelled EXACTLY as the
  // shared memberVS atom over the concrete tuple spine
  syntax Bool ::= inOdd(Int) [function, total]
  rule inOdd(X:Int)
    => memberVS(X, vCons(1, vCons(3, vCons(5, vCons(7, vCons(9, .ValSeq))))))
    [simplification]

  // the count fold; guards over the EXACT execution atoms. atI (TOTAL twin) not intSeqAt
  // (partial): the executed str[0]/str[-1] bridges to atI over the seqConcat-unfolded digitCodes,
  // and a partial intSeqAt in the guard neither lifts nor matches that total-fn atom.
  syntax Int ::= sfCount(ValSeq, Int) [function, total]
  rule sfCount(.ValSeq, C:Int) => C [simplification]
  rule sfCount(vCons(V:Val, R:ValSeq), C:Int) => sfCount(R, C)
    requires notBool (projectIntTotal(V) >Int 10) [simplification]
  rule sfCount(vCons(V:Val, R:ValSeq), C:Int) => sfCount(R, C +Int 1)
    requires projectIntTotal(V) >Int 10
     andBool inOdd(intDigAcc(iCons(atI(digitCodes(projectIntTotal(V)), 0), .IntSeq), 0))
     andBool inOdd(intDigAcc(iCons(atI(digitCodes(projectIntTotal(V)),
                isLen(digitCodes(projectIntTotal(V))) -Int 1), .IntSeq), 0))
    [simplification]
  rule sfCount(vCons(V:Val, R:ValSeq), C:Int) => sfCount(R, C)
    requires projectIntTotal(V) >Int 10
     andBool notBool (inOdd(intDigAcc(iCons(atI(digitCodes(projectIntTotal(V)), 0), .IntSeq), 0))
       andBool inOdd(intDigAcc(iCons(atI(digitCodes(projectIntTotal(V)),
                isLen(digitCodes(projectIntTotal(V))) -Int 1), .IntSeq), 0)))
    [simplification]
endmodule
