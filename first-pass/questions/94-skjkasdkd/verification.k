// verification.k — skjkasdkd on the UNIFIED semantics, TRAP-FREE and
// INTERCEPTION-FREE (P94). solution.py = canonical minus docstring with the
// two sheet 1a workarounds (early-return -> flag p; digit genexp -> for).
// The REAL nested isPrime runs under kprove (callee-span claims); its
// returned flag is stated as the hooked `primeI(..) ==Int 1` so #branch
// splits. Only [simplification] lemmas below — no k-cell rules at all.

requires "../../reference/src/lemmas.k"

module SKJKASDKD-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // ---- structural echoes: shared PLAIN dispatch rules match only
  // constructor-headed args; these fire on the specific fn-term heads the
  // program builds (same equations as the shared rules, simplification class)
  rule applyBin("**", projectIntTotal(V:Val), F:Float)
    => powF(intToF(projectIntTotal(V)), F) [simplification]
  rule applyBuiltin("int", powF(F1:Float, F2:Float), .Vals)
    => truncF(powF(F1, F2)) [simplification]
  rule applyBin("+", truncF(F:Float), I:Int) => truncF(F) +Int I [simplification]
  rule applyBuiltin("range", LO:Int, truncF(F:Float) +Int I:Int, .Vals)
    => rangeObj(LO, truncF(F) +Int I, 1) [simplification]
  rule applyCmp("<", I:Int, vsLen(VS:ValSeq)) => I <Int vsLen(VS) [simplification]
  rule applyBuiltin("str", maxSel(VS:ValSeq, I:Int, MV:Val), .Vals)
    => str(strToCodes(Int2String(projectIntTotal(maxSel(VS, I, MV))))) [simplification]

  // decimal digits of a nonnegative int are digit codes; maxFold is nonneg
  rule allDigit(strToCodes(Int2String(N:Int))) => true
    requires 0 <=Int N [simplification]
  rule 0 <=Int projectIntTotal(maxSel(VS:ValSeq, I:Int, MV:Val)) => true
    requires 0 <=Int projectIntTotal(MV) [simplification]
  rule 0 <Int isLen(strToCodes(Int2String(_:Int))) => true [simplification]

  // okV: the claim-premise element predicate (isInt(valSeqAt(..)) has no
  // provider rule and simplifications on the auto-generated isInt are
  // rejected; a problem-local total head is legal). True on ints and on
  // same-list elements under allInt; false on the narrowing junk shapes.
  syntax Bool ::= okV(Val) [function, total, no-evaluators]
  rule okV(I:Int) => true [simplification]
  rule okV(valSeqAt(VS:ValSeq, _:Int)) => true requires allInt(VS) [simplification]
  rule okV(ref(_:Int))      => false [simplification]
  rule okV(cellRef(_:Int))  => false [simplification]
  rule okV(list(_:ValSeq))  => false [simplification]
  rule okV(tuple(_:ValSeq)) => false [simplification]
  rule okV(str(_:IntSeq))   => false [simplification]
  rule okV(rangeObj(_:Int, _:Int, _:Int)) => false [simplification]
  rule okV(noneV) => false [simplification]

  // okV-guarded projection echoes (the P90 cast-bridge form): function-rule
  // matching never narrows, so raw Val operands project explicitly
  rule applyBin(OP:String, V:Val, W:Val)
    => applyBin(OP, projectIntTotal(V), projectIntTotal(W))
    requires okV(V) andBool okV(W) [simplification]
  rule applyCmp(OP:String, V:Val, W:Val)
    => applyCmp(OP, projectIntTotal(V), projectIntTotal(W))
    requires okV(V) andBool okV(W) [simplification]
  rule applyBin("**", V:Val, F:Float)
    => applyBin("**", projectIntTotal(V), F)
    requires okV(V) [simplification]

  // ---- the isPrime flag fold, hooked-Int-valued (exact execution form:
  // range peel on I <Int HI, pyMod test, flag sticks at false)
  syntax Int ::= primeI(Int, Int, Int, Bool) [function, total]
  rule primeI(_:Int, I:Int, HI:Int, P:Bool) => #if P #then 1 #else 0 #fi
    requires notBool (I <Int HI) [simplification]
  rule primeI(N:Int, I:Int, HI:Int, _:Bool) => primeI(N, I +Int 1, HI, false)
    requires I <Int HI andBool pyMod(N, I) ==Int 0 [simplification]
  rule primeI(N:Int, I:Int, HI:Int, P:Bool) => primeI(N, I +Int 1, HI, P)
    requires I <Int HI andBool notBool (pyMod(N, I) ==Int 0) [simplification]

  // ---- the while's max-of-primes fold ---------------------------------------
  syntax Int ::= hiOf(Int) [function, total]
  rule hiOf(N:Int) => truncF(powF(intToF(N), 0.5)) +Int 1
  syntax Val ::= maxSel(ValSeq, Int, Val) [function, total]
  rule maxSel(VS:ValSeq, I:Int, MV:Val) => MV
    requires notBool (I <Int vsLen(VS)) [simplification]
  rule maxSel(VS:ValSeq, I:Int, MV:Val)
    => maxSel(VS, I +Int 1, valSeqAt(VS, I))
    requires I <Int vsLen(VS)
     andBool projectIntTotal(valSeqAt(VS, I)) >Int projectIntTotal(MV)
     andBool primeI(projectIntTotal(valSeqAt(VS, I)), 2,
                    hiOf(projectIntTotal(valSeqAt(VS, I))), true) ==Int 1
    [simplification]
  rule maxSel(VS:ValSeq, I:Int, MV:Val) => maxSel(VS, I +Int 1, MV)
    requires I <Int vsLen(VS)
     andBool notBool (projectIntTotal(valSeqAt(VS, I)) >Int projectIntTotal(MV)
     andBool primeI(projectIntTotal(valSeqAt(VS, I)), 2,
                    hiOf(projectIntTotal(valSeqAt(VS, I))), true) ==Int 1)
    [simplification]

  // ---- the digit-sum fold -----------------------------------------------------
  syntax Int ::= sumDig(IntSeq, Int) [function, total]
  rule sumDig(.IntSeq, R:Int) => R [simplification]
  rule sumDig(iCons(C:Int, T:IntSeq), R:Int) => sumDig(T, R +Int (C -Int 48)) [simplification]
endmodule
