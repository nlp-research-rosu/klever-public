// verification.k — valid_date on the UNIFIED semantics, TRAP-FREE (P124).
// solution.py is the sheet-sanctioned 1-fn shape (try/except -> the len-3 +
// isdigit guards; everything else canonical verbatim). Straight-line proof:
// result == vDate(SW) over the stripped codes, atoms kept PARTIAL-FREE
// (splitSep is partial -> bridged to total splitCount/fieldSeq; isdigit/int
// evaluated for REAL (dg composite / intDigAcc Horner); month membership as the
// shared memberVS fold over the concrete month lists — the executed atom).

requires "../../reference/src/lemmas.k"

module VALID-DATE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // ---- total split vocabulary (old P124 kit, kept) --------------------------
  syntax Int ::= splitCount(IntSeq) [function, total]
  rule splitCount(.IntSeq)                => 1
  rule splitCount(iCons(C:Int, T:IntSeq)) => 1 +Int splitCount(T) requires C ==Int 45
  rule splitCount(iCons(C:Int, T:IntSeq)) => splitCount(T)        requires C =/=Int 45
  syntax IntSeq ::= takeField(IntSeq) [function, total]
  rule takeField(.IntSeq)                => .IntSeq
  rule takeField(iCons(C:Int, _))        => .IntSeq requires C ==Int 45
  rule takeField(iCons(C:Int, T:IntSeq)) => iCons(C, takeField(T)) requires C =/=Int 45
  syntax IntSeq ::= fieldSeq(Int, IntSeq) [function, total]
  rule fieldSeq(0, CS:IntSeq)                  => takeField(CS)
  rule fieldSeq(I:Int, .IntSeq)                => .IntSeq requires I >Int 0
  rule fieldSeq(I:Int, iCons(C:Int, T:IntSeq)) => fieldSeq(I -Int 1, T) requires I >Int 0 andBool C ==Int 45
  rule fieldSeq(I:Int, iCons(C:Int, T:IntSeq)) => fieldSeq(I, T)        requires I >Int 0 andBool C =/=Int 45

  // the split's length is the total dash count (partial splitSep leaves the atom)
  rule vsLen(splitSep(CS:IntSeq, 45, .IntSeq)) => splitCount(CS) [simplification]
  // a 3-field split IS the cons of its three fields (lets the tuple-unpack
  // destructure the symbolic split)
  rule splitSep(CS:IntSeq, 45, .IntSeq)
    => vCons(str(fieldSeq(0, CS)), vCons(str(fieldSeq(1, CS)), vCons(str(fieldSeq(2, CS)), .ValSeq)))
    requires splitCount(CS) ==Int 3 [simplification]

  // ---- real vocabulary: the digit test and the parse -------------------------
  // isdigit runs the REAL applyMethod rule; its value is this exact composite
  syntax Bool ::= dg(IntSeq) [function, total]
  rule dg(F:IntSeq) => notBool (isLen(F) ==Int 0) andBool dgN(F) ==Int 1
  // int(field) is the REAL Horner fold under the digit atoms already in the
  // path condition (single-char included: intDigAcc(iCons(C,.IntSeq),0)=C-48)
  rule applyBuiltin("int", str(F:IntSeq), .Vals) => intDigAcc(F, 0)
    requires notBool (isLen(F) ==Int 0) andBool dgN(F) ==Int 1 [simplification]
  // the parsed month/day are intDigAcc(..) (Int-sorted, hence isInt), so month<1 / month>12 / etc.
  // reduce via the SHARED applyCmp isInt rule (lemmas/core.k) — no problem-local compare echo /
  // knownPF opaque predicate needed. intDigAcc's cast idempotence keeps {..}:>Int clean.
  rule projectIntTotal(intDigAcc(F:IntSeq, A:Int)) => intDigAcc(F, A) [simplification]
  // the month membership runs the REAL #memberAcc fold over the concrete
  // lists; its leaf atoms are E ==K needle equations (see in31/in30 below)

  // ---- the result model ------------------------------------------------------
  syntax Int ::= vdM(IntSeq) [function, total]
  rule vdM(SW:IntSeq) => intDigAcc(fieldSeq(0, SW), 0)
  syntax Int ::= vdD(IntSeq) [function, total]
  rule vdD(SW:IntSeq) => intDigAcc(fieldSeq(1, SW), 0)
  syntax Bool ::= dgOK(IntSeq) [function, total]
  rule dgOK(SW:IntSeq)
    => dg(fieldSeq(0, SW)) andBool dg(fieldSeq(1, SW)) andBool dg(fieldSeq(2, SW))
  syntax Bool ::= mOK(IntSeq) [function, total]
  rule mOK(SW:IntSeq) => notBool (vdM(SW) <Int 1) andBool notBool (vdM(SW) >Int 12)
  // `month in [..]` folds via the shared #memberAcc route to memberVS (NOT the unrolled ==K leaves),
  // so in31/in30 must be spelled as the SAME memberVS atom the execution produces (over the exact
  // list the ListExpr builds) — else the model's disjunction never connects to the executed atom.
  syntax Bool ::= in31(IntSeq) [function, total]
  rule in31(SW:IntSeq)
    => memberVS(vdM(SW), vCons(1, vCons(3, vCons(5, vCons(7, vCons(8, vCons(10, vCons(12, .ValSeq))))))))
  syntax Bool ::= in30(IntSeq) [function, total]
  rule in30(SW:IntSeq)
    => memberVS(vdM(SW), vCons(4, vCons(6, vCons(9, vCons(11, .ValSeq)))))
  syntax Bool ::= d31OK(IntSeq) [function, total]
  rule d31OK(SW:IntSeq)
    => notBool ((in31(SW) andBool vdD(SW) <Int 1) orBool vdD(SW) >Int 31)
  syntax Bool ::= d30OK(IntSeq) [function, total]
  rule d30OK(SW:IntSeq)
    => notBool ((in30(SW) andBool vdD(SW) <Int 1) orBool vdD(SW) >Int 30)
  syntax Bool ::= d29OK(IntSeq) [function, total]
  rule d29OK(SW:IntSeq)
    => notBool ((vdM(SW) ==Int 2 andBool vdD(SW) <Int 1) orBool vdD(SW) >Int 29)

  syntax Bool ::= vDate(IntSeq) [function, total]
  rule vDate(SW:IntSeq) => false
    requires notBool (splitCount(SW) ==Int 3) [simplification]
  rule vDate(SW:IntSeq) => false
    requires splitCount(SW) ==Int 3 andBool notBool dgOK(SW) [simplification]
  rule vDate(SW:IntSeq) => false
    requires splitCount(SW) ==Int 3 andBool dgOK(SW) andBool notBool mOK(SW) [simplification]
  rule vDate(SW:IntSeq) => false
    requires splitCount(SW) ==Int 3 andBool dgOK(SW) andBool mOK(SW)
     andBool notBool d31OK(SW) [simplification]
  rule vDate(SW:IntSeq) => false
    requires splitCount(SW) ==Int 3 andBool dgOK(SW) andBool mOK(SW)
     andBool d31OK(SW) andBool notBool d30OK(SW) [simplification]
  rule vDate(SW:IntSeq) => false
    requires splitCount(SW) ==Int 3 andBool dgOK(SW) andBool mOK(SW)
     andBool d31OK(SW) andBool d30OK(SW) andBool notBool d29OK(SW) [simplification]
  rule vDate(SW:IntSeq) => true
    requires splitCount(SW) ==Int 3 andBool dgOK(SW) andBool mOK(SW)
     andBool d31OK(SW) andBool d30OK(SW) andBool d29OK(SW) [simplification]
endmodule
