// verification.k — Strongest_Extension on the UNIFIED semantics, TRAP-FREE
// (P153). solution.py is canonical verbatim: the strength helper (and its
// Call trap) is GONE; four real listcomps over strings compute CAP/SM counts
// per extension, argmax with first-wins tie, real string concat result.
// Every branch atom reduces to hooked integer range comparisons (isAlphaC/
// isUpperC/isLowerC are unconditional range rewrites), so no opaque-int
// bridging is needed anywhere.

requires "../../reference/src/lemmas.k"

module STRONGEST-EXTENSION-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // ---- domain: extensions are strings (kills #loop iterable narrowing) ----
  // a cons IntSeq is never the empty IntSeq (the isalpha nonempty test on a
  // singleton char sticks as an opaque ==K atom otherwise, poisoning every
  // downstream guard entailment)
  rule iCons(_:Int, _:IntSeq) ==K .IntSeq => false [simplification]
  rule .IntSeq ==K iCons(_:Int, _:IntSeq) => false [simplification]

  rule 0 <Int 1 +Int vsLen(_:ValSeq) => true [simplification]

  // (strP + the #loop str-bridge are SHARED now: lemmas/str.k)
  syntax Bool ::= allStrV(ValSeq) [function, total]
  rule allStrV(.ValSeq)                => true
  rule allStrV(vCons(V:Val, R:ValSeq)) => strP(V) andBool allStrV(R)

  // ---- the two char-filter builder folds (kept chars as singleton strs),
  // guards in the execution's atom forms (alpha & upper-only / lower-only)
  syntax ValSeq ::= upSeq(IntSeq, ValSeq) [function, total]
  rule upSeq(.IntSeq, ACC:ValSeq) => ACC [simplification]
  rule upSeq(iCons(C:Int, R:IntSeq), ACC:ValSeq)
    => upSeq(R, valSeqConcat(ACC, vCons(str(iCons(C, .IntSeq)), .ValSeq)))
    requires isAlphaC(C) andBool isUpperC(C) andBool notBool isLowerC(C) [simplification]
  rule upSeq(iCons(C:Int, R:IntSeq), ACC:ValSeq) => upSeq(R, ACC)
    requires notBool (isAlphaC(C) andBool isUpperC(C) andBool notBool isLowerC(C)) [simplification]

  syntax ValSeq ::= loSeq(IntSeq, ValSeq) [function, total]
  rule loSeq(.IntSeq, ACC:ValSeq) => ACC [simplification]
  rule loSeq(iCons(C:Int, R:IntSeq), ACC:ValSeq)
    => loSeq(R, valSeqConcat(ACC, vCons(str(iCons(C, .IntSeq)), .ValSeq)))
    requires isAlphaC(C) andBool isLowerC(C) andBool notBool isUpperC(C) [simplification]
  rule loSeq(iCons(C:Int, R:IntSeq), ACC:ValSeq) => loSeq(R, ACC)
    requires notBool (isAlphaC(C) andBool isLowerC(C) andBool notBool isUpperC(C)) [simplification]

  // strength of an extension, in the execution's normal form
  syntax Int ::= stCS(IntSeq) [function, total]
  rule stCS(CS:IntSeq) => vsLen(upSeq(CS, .ValSeq)) -Int vsLen(loSeq(CS, .ValSeq))

  // str + opaque-str-Val concat (the result line: class_name + '.' + strong)
  rule applyBin("+", str(A:IntSeq), V:Val) => str(seqConcat(A, codesProj(V)))
    requires strP(V) [simplification]

  // ---- the argmax folds (strict >, first-wins tie) over RAW Val elements,
  // strengths via codesProj; selSV returns the selected element Val ---------
  syntax Val ::= selSV(ValSeq, Val, Int) [function, total]
  rule selSV(.ValSeq, CUR:Val, _:Int) => CUR [simplification]
  rule selSV(vCons(V:Val, R:ValSeq), _:Val, MV:Int) => selSV(R, V, stCS(codesProj(V)))
    requires strP(V) andBool stCS(codesProj(V)) >Int MV [simplification]
  rule selSV(vCons(V:Val, R:ValSeq), CUR:Val, MV:Int) => selSV(R, CUR, MV)
    requires strP(V) andBool notBool (stCS(codesProj(V)) >Int MV) [simplification]

  // the selection preserves str-ness (its arms only keep isStrV elements),
  // so the final concat's bridge guard discharges on the opaque selSV term
  rule strP(selSV(VS:ValSeq, CUR:Val, _:Int)) => true
    requires allStrV(VS) andBool strP(CUR) [simplification]

  // deref-narrowing killers: the k-top cellRef (and consumer ref) deref rules
  // unify their redex with ANY Val-sorted function term; a selSV of strings is
  // never a heap handle (the lemmas/subscript.k disjointness-killer pattern)
  rule { cellRef(_:Int) #Equals selSV(VS:ValSeq, CUR:Val, _:Int) } => #Bottom
    requires allStrV(VS) andBool strP(CUR) [simplification]
  rule { selSV(VS:ValSeq, CUR:Val, _:Int) #Equals cellRef(_:Int) } => #Bottom
    requires allStrV(VS) andBool strP(CUR) [simplification]
  rule { ref(_:Int) #Equals selSV(VS:ValSeq, CUR:Val, _:Int) } => #Bottom
    requires allStrV(VS) andBool strP(CUR) [simplification]
  rule { selSV(VS:ValSeq, CUR:Val, _:Int) #Equals ref(_:Int) } => #Bottom
    requires allStrV(VS) andBool strP(CUR) [simplification]

  syntax Int ::= selMV(ValSeq, Int) [function, total]
  rule selMV(.ValSeq, MV:Int) => MV [simplification]
  rule selMV(vCons(V:Val, R:ValSeq), MV:Int) => selMV(R, stCS(codesProj(V)))
    requires strP(V) andBool stCS(codesProj(V)) >Int MV [simplification]
  rule selMV(vCons(V:Val, R:ValSeq), MV:Int) => selMV(R, MV)
    requires strP(V) andBool notBool (stCS(codesProj(V)) >Int MV) [simplification]
endmodule
