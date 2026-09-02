// verification.k — odd_count on the UNIFIED semantics, TRAP-FREE (P113).
// solution.py is the sheet-sanctioned 1-fn shape: the make_msg helper (and
// its Call trap) is GONE; the genexp-sum is the sanctioned inline count loop.
// int(d) reduces symbolically under the digit-domain premise (the shared
// single-char rule); str(n) of the symbolic count stays HONEST-OPAQUE as
// strToCodes(Int2String(N)) spliced into the real concat chain.

requires "../../reference/src/lemmas.k"

module ODD-COUNT-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  rule 0 <Int 1 +Int vsLen(_:ValSeq) => true [simplification]

  // (strP + the #loop str-bridge are SHARED now: lemmas/str.k)

  // ---- domain: every element is a digits-only string ----------------------
  syntax Bool ::= allDigS(ValSeq) [function, total]
  rule allDigS(.ValSeq) => true
  rule allDigS(vCons(V:Val, R:ValSeq))
    => strP(V) andBool allDigit(codesProj(V))
       andBool 0 <Int isLen(codesProj(V)) andBool allDigS(R)

  // ---- the inner count fold, transitions in EXACT EXECUTION FORM ----------
  // (int(d) => C -Int 48; the If atom is pyMod(C -Int 48, 2) ==Int 1)
  syntax Int ::= oddCnt2(IntSeq, Int) [function, total]
  rule oddCnt2(.IntSeq, N:Int) => N [simplification]
  rule oddCnt2(iCons(C:Int, CS:IntSeq), N:Int) => oddCnt2(CS, N +Int 1)
    requires pyMod(C -Int 48, 2) ==Int 1 [simplification]
  rule oddCnt2(iCons(C:Int, CS:IntSeq), N:Int) => oddCnt2(CS, N)
    requires notBool (pyMod(C -Int 48, 2) ==Int 1) [simplification]

  // ---- the message value, in the right-assoc seqConcat normal form --------
  syntax IntSeq ::= numCodes(Int) [function, total]
  rule numCodes(N:Int) => strToCodes(Int2String(N))
  syntax Val ::= mkMsg(Val) [function, total]
  rule mkMsg(V:Val)
    => str(seqConcat(iCons(116, iCons(104, iCons(101, iCons(32, iCons(110, iCons(117, iCons(109, iCons(98, iCons(101, iCons(114, iCons(32, iCons(111, iCons(102, iCons(32, iCons(111, iCons(100, iCons(100, iCons(32, iCons(101, iCons(108, iCons(101, iCons(109, iCons(101, iCons(110, iCons(116, iCons(115, iCons(32, .IntSeq))))))))))))))))))))))))))),
         seqConcat(numCodes(oddCnt2(codesProj(V), 0)),
         seqConcat(iCons(110, iCons(32, iCons(116, iCons(104, iCons(101, iCons(32, iCons(115, iCons(116, iCons(114, .IntSeq))))))))),
         seqConcat(numCodes(oddCnt2(codesProj(V), 0)),
         seqConcat(iCons(110, iCons(103, iCons(32, .IntSeq))),
         seqConcat(numCodes(oddCnt2(codesProj(V), 0)),
         seqConcat(iCons(32, iCons(111, iCons(102, iCons(32, iCons(116, iCons(104, iCons(101, iCons(32, .IntSeq)))))))),
         seqConcat(numCodes(oddCnt2(codesProj(V), 0)),
                   iCons(110, iCons(112, iCons(117, iCons(116, iCons(46, .IntSeq))))))))))))))

  // ---- the outer append fold ----------------------------------------------
  syntax ValSeq ::= msgFold(ValSeq, ValSeq) [function, total]
  rule msgFold(.ValSeq, ACC:ValSeq) => ACC [simplification]
  rule msgFold(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => msgFold(R, valSeqConcat(ACC, vCons(mkMsg(V), .ValSeq)))
    requires strP(V) [simplification]
endmodule
