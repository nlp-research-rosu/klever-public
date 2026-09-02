// verification.k — do_algebra on the UNIFIED semantics (reference/src/).
//
// do_algebra(operator, operand) builds an arithmetic expression from a list of operator strings and
// a list of integer operands and evaluates it with Python precedence (** right-assoc, then * //,
// then + -).  eval / operator precedence is DOMAIN KNOWLEDGE — a TRUSTED primitive, like len/eval or
// a trusted sort.  This is a THIN proof: it verifies the wrapper returns doAlgebraV(operator,
// operand); the precedence evaluator is trusted (run CONCRETELY in krun, matched vs CPython eval).
//
// kprove: doAlgebraV(list, list) stays one opaque [total] Int over the symbolic list args.
// krun: doAlgebraV reduces via the pass-based precedence evaluator below (projecting the
// operator strings / operand ints out of the unified list(ValSeq)).  Problem-local; no shared change.

requires "../../reference/src/lemmas.k"

module DOALG-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports STRING

  // proof-only: let a Val (symbolic list) sit in Call-argument position without forking the path.
  syntax Expr ::= Val

  // ---- verified result summary (STEP 4): the whole do_algebra value, composed from the three
  // proven passes — NO interception. (1) powFold = the ** pass (right-assoc, right-to-left) leaving
  // (r_nds, r_ops, cur); (2) append cur then reverse both lists (post-** processing); (3) mulAddFold
  // = the combined * // + - pass over the reversed lists; (4) return total + sign*term. The entry
  // claim folds the two real loops to powFold/mulAddFold, so this evaluation is VERIFIED not trusted.
  syntax Int ::= daResult(ValSeq, ValSeq) [function, total]
  rule daResult(OPS:ValSeq, NDS:ValSeq)
    => daCombine(powFold(OPS, NDS, 0, vsLen(OPS), .ValSeq, .ValSeq,
                         projectIntTotal(valSeqAt(NDS, vsLen(OPS))))) [simplification]
  syntax Int ::= daCombine(P3) [function, total]
  rule daCombine(P:P3)
    => daFin(revVS(p3ops(P)), revVS(valSeqConcat(p3nds(P), vCons(p3cur(P), .ValSeq)))) [simplification]
  syntax Int ::= daFin(ValSeq, ValSeq) [function, total]
  rule daFin(OPS2:ValSeq, NDS2:ValSeq)
    => daRet(mulAddFold(OPS2, NDS2, 0, projectIntTotal(valSeqAt(NDS2, 0)), 1, 0, vsLen(OPS2))) [simplification]
  syntax Int ::= daRet(MAF) [function, total]
  rule daRet(F:MAF) => mafT(F) +Int mafS(F) *Int mafM(F) [simplification]

  syntax StrSeq ::= ".StrSeq" | sCons(String, StrSeq)
  syntax StrSeq ::= projOps(ValSeq) [function, total]
  rule projOps(.ValSeq)                    => .StrSeq                         
  rule projOps(vCons(str(CS:IntSeq), R:ValSeq)) => sCons(codesToStr(CS), projOps(R))
  syntax IntSeq ::= projNds(ValSeq) [function, total]
  rule projNds(.ValSeq)               => .IntSeq                              
  rule projNds(vCons(I:Int, R:ValSeq)) => iCons(I, projNds(R))                
  syntax String ::= codesToStr(IntSeq) [function, total]
  rule codesToStr(.IntSeq)               => ""                                
  rule codesToStr(iCons(C:Int, R:IntSeq)) => chrChar(C) +String codesToStr(R) 

  syntax EPair ::= ep(StrSeq, IntSeq)
  syntax Int ::= firstNd(EPair) [function, total]
  rule firstNd(ep(_:StrSeq, iCons(N:Int, _:IntSeq))) => N

  syntax Int ::= applyOp(String, Int, Int) [function, total]
  rule applyOp("+",  A:Int, B:Int) => A +Int B  
  rule applyOp("-",  A:Int, B:Int) => A -Int B  
  rule applyOp("*",  A:Int, B:Int) => A *Int B  
  rule applyOp("//", A:Int, B:Int) => A divInt B
  rule applyOp("**", A:Int, B:Int) => A ^Int B  

  // ** pass (right-associative)
  syntax EPair ::= passPow(StrSeq, IntSeq) [function, total]
  rule passPow(.StrSeq, NDS:IntSeq) => ep(.StrSeq, NDS)
  rule passPow(sCons("**", OPS:StrSeq), iCons(N:Int, NDS:IntSeq)) => powCombine(N, passPow(OPS, NDS))
  rule passPow(sCons(O:String, OPS:StrSeq), iCons(N:Int, NDS:IntSeq)) => powCarry(O, N, passPow(OPS, NDS))
       requires O =/=String "**"
  syntax EPair ::= powCombine(Int, EPair) [function, total]
  rule powCombine(N:Int, ep(OPS:StrSeq, iCons(M:Int, REST:IntSeq))) => ep(OPS, iCons(N ^Int M, REST))
  syntax EPair ::= powCarry(String, Int, EPair) [function, total]
  rule powCarry(O:String, N:Int, ep(OPS:StrSeq, NDS:IntSeq)) => ep(sCons(O, OPS), iCons(N, NDS))

  // * // and + - passes (left-associative)
  syntax EPair ::= passMul(EPair) [function, total] | passAdd(EPair) [function]
  rule passMul(ep(OPS:StrSeq, iCons(N0:Int, NDS:IntSeq))) => passLGo("mul", N0, OPS, NDS, .StrSeq, .IntSeq)
  rule passAdd(ep(OPS:StrSeq, iCons(N0:Int, NDS:IntSeq))) => passLGo("add", N0, OPS, NDS, .StrSeq, .IntSeq)
  syntax EPair ::= passLGo(String, Int, StrSeq, IntSeq, StrSeq, IntSeq) [function, total]
  rule passLGo(_L:String, CUR:Int, .StrSeq, _NDS:IntSeq, OO:StrSeq, ON:IntSeq) => ep(OO, appendI(ON, CUR))
  rule passLGo(L:String, CUR:Int, sCons(O:String, OPS:StrSeq), iCons(N:Int, NDS:IntSeq), OO:StrSeq, ON:IntSeq)
        => passLGo(L, applyOp(O, CUR, N), OPS, NDS, OO, ON) requires inLevel(L, O)
  rule passLGo(L:String, CUR:Int, sCons(O:String, OPS:StrSeq), iCons(N:Int, NDS:IntSeq), OO:StrSeq, ON:IntSeq)
        => passLGo(L, N, OPS, NDS, appendS(OO, O), appendI(ON, CUR)) requires notBool inLevel(L, O)
  syntax Bool ::= inLevel(String, String) [function, total]
  rule inLevel("mul", O:String) => O ==String "*" orBool O ==String "//"
  rule inLevel("add", O:String) => O ==String "+" orBool O ==String "-"

  syntax StrSeq ::= appendS(StrSeq, String) [function, total]
  rule appendS(.StrSeq, S:String) => sCons(S, .StrSeq)
  rule appendS(sCons(X:String, R:StrSeq), S:String) => sCons(X, appendS(R, S))
  syntax IntSeq ::= appendI(IntSeq, Int) [function, total]
  rule appendI(.IntSeq, X:Int) => iCons(X, .IntSeq)
  rule appendI(iCons(Y:Int, R:IntSeq), X:Int) => iCons(Y, appendI(R, X))

  // ==== EXECUTION-side machinery for the pure-Python 3-pass proof (ValSeq level) ================
  // str-operator-list compare bridge: an operator ops[i] = valSeqAt(OPS,I) is an opaque str Val under
  // allStr(OPS); `ops[i] == "+"` -> applyCmp over it reduces via codesProj (shared, str.k) to the code
  // ==K compare — symbolic-vs-CONCRETE, so #branch narrows it (unlike 154's two-symbolic window eq).
  rule applyCmp("==", valSeqAt(VS:ValSeq, I:Int), str(B:IntSeq)) => codesProj(valSeqAt(VS, I)) ==K B
    requires allStr(VS) [simplification]
  rule applyCmp("==", str(B:IntSeq), valSeqAt(VS:ValSeq, I:Int)) => B ==K codesProj(valSeqAt(VS, I))
    requires allStr(VS) [simplification]

  // the operator element valSeqAt(OPS,I) under allStr is a str, NEVER a heap ref — kill the deref
  // narrower's { valSeqAt #Equals ref(_) } junk branch (the portable ref-narrow killer, allStr twin).
  rule { ref(_:Int) #Equals valSeqAt(VS:ValSeq, _:Int) } => #Bottom requires allStr(VS) [simplification]
  rule { valSeqAt(VS:ValSeq, _:Int) #Equals ref(_:Int) } => #Bottom requires allStr(VS) [simplification]

  // + - pass summary (the last loop: cur = nds[0]; for i in range(len(ops)): cur = cur +/- nds[i+1]).
  // '+' is code 43. addFold folds cur over the operators; guard matches the bridge's codesProj ==K form.
  syntax Int ::= addFold(ValSeq, ValSeq, Int, Int, Int) [function, total]
  rule addFold(_OPS:ValSeq, _NDS:ValSeq, CUR:Int, I:Int, M:Int) => CUR
    requires I >=Int M [simplification]
  rule addFold(OPS:ValSeq, NDS:ValSeq, CUR:Int, I:Int, M:Int)
    => addFold(OPS, NDS, CUR +Int projectIntTotal(valSeqAt(NDS, I +Int 1)), I +Int 1, M)
    requires I <Int M andBool codesProj(valSeqAt(OPS, I)) ==K iCons(43, .IntSeq) [simplification]
  rule addFold(OPS:ValSeq, NDS:ValSeq, CUR:Int, I:Int, M:Int)
    => addFold(OPS, NDS, CUR -Int projectIntTotal(valSeqAt(NDS, I +Int 1)), I +Int 1, M)
    requires I <Int M andBool notBool (codesProj(valSeqAt(OPS, I)) ==K iCons(43, .IntSeq)) [simplification]

  // Python // with a SYMBOLIC (unknown-sign) divisor is partial: the reference expands it to
  // (A -Int pyMod(A,B)) /Int B, whose /Int needs B =/= 0 to be defined, so the raw term will not
  // cool. fdivP keeps floored-div as an opaque TOTAL atom (like ipow for symbolic **), and the fold
  // lemma rewrites the executed partial spelling (pyMod fully expanded) to it. Structure-only:
  // smoke.py runs the real floored div; the proof only threads the (opaque) result through the fold.
  syntax Int ::= fdivP(Int, Int) [function, total]
  rule (A:Int -Int ((A %Int B:Int) +Int B) %Int B) /Int B => fdivP(A, B) [simplification]

  // ==== COMBINED * // + - pass summary (solution.py pass 2). maf(total, term, sign) folded over the
  // reduced (all +-*//) ops: '*' (code 42) / '//' (47,47) multiply/floor-div into `term`; '+' (43) /
  // '-' (45, the else) flush `total +Int sign*term` then start a new term with sign +1/-1.
  syntax MAF ::= maf(Int, Int, Int)
  syntax Int ::= mafT(MAF) [function, total]
  rule mafT(maf(T:Int, _:Int, _:Int)) => T
  syntax Int ::= mafM(MAF) [function, total]
  rule mafM(maf(_:Int, TM:Int, _:Int)) => TM
  syntax Int ::= mafS(MAF) [function, total]
  rule mafS(maf(_:Int, _:Int, S:Int)) => S

  syntax MAF ::= mulAddFold(ValSeq, ValSeq, Int, Int, Int, Int, Int) [function, total]
  rule mulAddFold(_OPS:ValSeq, _NDS:ValSeq, TOTAL:Int, TERM:Int, SIGN:Int, I:Int, M:Int)
    => maf(TOTAL, TERM, SIGN) requires I >=Int M [simplification]
  rule mulAddFold(OPS:ValSeq, NDS:ValSeq, TOTAL:Int, TERM:Int, SIGN:Int, I:Int, M:Int)
    => mulAddFold(OPS, NDS, TOTAL, TERM *Int projectIntTotal(valSeqAt(NDS, I +Int 1)), SIGN, I +Int 1, M)
    requires I <Int M andBool codesProj(valSeqAt(OPS, I)) ==K iCons(42, .IntSeq) [simplification]
  rule mulAddFold(OPS:ValSeq, NDS:ValSeq, TOTAL:Int, TERM:Int, SIGN:Int, I:Int, M:Int)
    => mulAddFold(OPS, NDS, TOTAL,
         fdivP(TERM, projectIntTotal(valSeqAt(NDS, I +Int 1))),
         SIGN, I +Int 1, M)
    requires I <Int M andBool codesProj(valSeqAt(OPS, I)) ==K iCons(47, iCons(47, .IntSeq)) [simplification]
  rule mulAddFold(OPS:ValSeq, NDS:ValSeq, TOTAL:Int, TERM:Int, SIGN:Int, I:Int, M:Int)
    => mulAddFold(OPS, NDS, TOTAL +Int SIGN *Int TERM, projectIntTotal(valSeqAt(NDS, I +Int 1)), 1, I +Int 1, M)
    requires I <Int M andBool codesProj(valSeqAt(OPS, I)) ==K iCons(43, .IntSeq) [simplification]
  rule mulAddFold(OPS:ValSeq, NDS:ValSeq, TOTAL:Int, TERM:Int, SIGN:Int, I:Int, M:Int)
    => mulAddFold(OPS, NDS, TOTAL +Int SIGN *Int TERM, projectIntTotal(valSeqAt(NDS, I +Int 1)), -1, I +Int 1, M)
    requires I <Int M
     andBool notBool (codesProj(valSeqAt(OPS, I)) ==K iCons(42, .IntSeq))
     andBool notBool (codesProj(valSeqAt(OPS, I)) ==K iCons(47, iCons(47, .IntSeq)))
     andBool notBool (codesProj(valSeqAt(OPS, I)) ==K iCons(43, .IntSeq)) [simplification]

  // ==== ** pass summary (solution.py pass 1). Scan RIGHT-TO-LEFT (i = M-1-K over k in range(M)):
  // '**' (code 42,42, right-assoc) folds nds[i] ** cur into cur (ipow); every other operator flushes
  // cur into the growing r_nds list and ops[i] into r_ops, then starts a fresh cur = nds[i]. p3 carries
  // the (r_nds, r_ops, cur) triple; the two lists grow by append (valSeqConcat with a singleton).
  syntax P3 ::= p3(ValSeq, ValSeq, Int)
  syntax ValSeq ::= p3nds(P3) [function, total]
  rule p3nds(p3(RN:ValSeq, _:ValSeq, _:Int)) => RN
  syntax ValSeq ::= p3ops(P3) [function, total]
  rule p3ops(p3(_:ValSeq, RO:ValSeq, _:Int)) => RO
  syntax Int ::= p3cur(P3) [function, total]
  rule p3cur(p3(_:ValSeq, _:ValSeq, C:Int)) => C

  syntax P3 ::= powFold(ValSeq, ValSeq, Int, Int, ValSeq, ValSeq, Int) [function, total]
  rule powFold(_OPS:ValSeq, _NDS:ValSeq, K:Int, M:Int, RN:ValSeq, RO:ValSeq, C:Int)
    => p3(RN, RO, C) requires K >=Int M [simplification]
  // '**' branch: cur = nds[i] ** cur, i = M-1-K
  rule powFold(OPS:ValSeq, NDS:ValSeq, K:Int, M:Int, RN:ValSeq, RO:ValSeq, C:Int)
    => powFold(OPS, NDS, K +Int 1, M, RN, RO,
         ipow(projectIntTotal(valSeqAt(NDS, M -Int 1 -Int K)), C))
    requires K <Int M
     andBool codesProj(valSeqAt(OPS, M -Int 1 -Int K)) ==K iCons(42, iCons(42, .IntSeq)) [simplification]
  // else branch: flush cur -> r_nds, ops[i] -> r_ops, cur = nds[i]
  rule powFold(OPS:ValSeq, NDS:ValSeq, K:Int, M:Int, RN:ValSeq, RO:ValSeq, C:Int)
    => powFold(OPS, NDS, K +Int 1, M,
         valSeqConcat(RN, vCons(C, .ValSeq)),
         valSeqConcat(RO, vCons(valSeqAt(OPS, M -Int 1 -Int K), .ValSeq)),
         projectIntTotal(valSeqAt(NDS, M -Int 1 -Int K)))
    requires K <Int M
     andBool notBool (codesProj(valSeqAt(OPS, M -Int 1 -Int K)) ==K iCons(42, iCons(42, .IntSeq))) [simplification]

  // ** exponent stays >= 0: HumanEval/160 operands are NON-NEGATIVE, so each nds[j] >= 0 and
  // ipow(nonneg base, nonneg exp) >= 0 — needed for the shared ipow bridge guard (arith.k:41 RV >= 0)
  // to keep firing across a ** chain (cur = nds[i] ** cur, cur = ipow(...) fed as the next exponent).
  syntax Bool ::= allNonNeg(ValSeq) [function, total]
  rule allNonNeg(.ValSeq) => true
  rule allNonNeg(vCons(V:Val, R:ValSeq)) => isInt(V) andBool projectIntTotal(V) >=Int 0 andBool allNonNeg(R)
  rule projectIntTotal(valSeqAt(NDS:ValSeq, J:Int)) >=Int 0 => true
    requires allNonNeg(NDS) andBool 0 <=Int J andBool J <Int vsLen(NDS) [simplification]
  rule ipow(B:Int, E:Int) >=Int 0 => true requires B >=Int 0 andBool E >=Int 0 [simplification]

  // ops[::-1] / nds[::-1] (STEP 4 post-** reversal): the slice reduces to buildVS with a symbolic
  // start vsLen(VS)-1, stop -1, step -1 (subscript.k slStart/slStop/slStep), which is exactly revVS.
  // buildVS stays unreduced on a symbolic VS (recursion guards undecidable), so this bridges it.
  rule buildVS(VS:ValSeq, vsLen(VS) +Int -1, -1, -1) => revVS(VS) [simplification]

  // allInt of the reversed operand list nds2 = revVS(p3nds(powFold(..)) ++ [cur]) reduces to true in
  // ONE step (not a cascade — the broad allInt(revVSAcc(VS,A)) form BLEW UP by rewriting allInt(NDS2)
  // into a conjunction that broke the combined invariant's premise match). Needed for the empty-ops
  // (all-**) branches, where the combined loop invariant never fires so nds2[0]*1 must project directly.
  rule allInt(revVSAcc(valSeqConcat(p3nds(powFold(_O:ValSeq, ND:ValSeq, _K:Int, _M:Int, RN:ValSeq, _R:ValSeq, _C:Int)),
                       vCons(_CC:Int, .ValSeq)), .ValSeq)) => true
    requires allInt(ND) andBool allInt(RN) [simplification]
endmodule
