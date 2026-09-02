// bf-probe/verif.k — isolate HumanEval/148's blocker: does idxOf(P) reduce to -1 when the
// symbolic string P is NONE of the literals, i.e. under a path condition of negated ==K atoms?
// Two literals "A","B" (mechanism identical to the 8 planets). Compares idxOf formulations.

module BF-PROBE
  imports INT
  imports BOOL
  imports STRING
  imports K-EQUAL
  imports MAP

  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
  syntax IntSeq ::= strToCodes(String) [function]
  rule strToCodes("") => .IntSeq
  rule strToCodes(S:String)
    => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String ""

  // (1) #if cascade (the current 148-bf attempt)
  syntax Int ::= idxIf(IntSeq) [function, total]
  rule idxIf(P:IntSeq) =>
    #if P ==K strToCodes("A") #then 0
    #else #if P ==K strToCodes("B") #then 1
    #else -1 #fi #fi [simplification]

  // (2) original: positive per-atom requires + a =/=K conjunction fallback
  syntax Int ::= idxConj(IntSeq) [function, total]
  rule idxConj(P:IntSeq) => 0 requires P ==K strToCodes("A") [simplification]
  rule idxConj(P:IntSeq) => 1 requires P ==K strToCodes("B") [simplification]
  rule idxConj(P:IntSeq) => -1
    requires P =/=K strToCodes("A") andBool P =/=K strToCodes("B") [simplification]

  // (3) conjunction fallback but stated with notBool(==K) (matches the branch atom form)
  syntax Int ::= idxConjNB(IntSeq) [function, total]
  rule idxConjNB(P:IntSeq) => 0 requires P ==K strToCodes("A") [simplification]
  rule idxConjNB(P:IntSeq) => 1 requires P ==K strToCodes("B") [simplification]
  rule idxConjNB(P:IntSeq) => -1
    requires notBool (P ==K strToCodes("A")) andBool notBool (P ==K strToCodes("B")) [simplification]

  // drivers (a claim reduces chkX(P) to true; forces idxX(P) to reduce under the path cond)
  syntax Bool ::= chkIf(IntSeq)     [function]  rule chkIf(P:IntSeq)     => idxIf(P)     ==Int -1
  syntax Bool ::= chkConj(IntSeq)   [function]  rule chkConj(P:IntSeq)   => idxConj(P)   ==Int -1
  syntax Bool ::= chkConjNB(IntSeq) [function]  rule chkConjNB(P:IntSeq) => idxConjNB(P) ==Int -1
  syntax Bool ::= chkIfPos(IntSeq)  [function]  rule chkIfPos(P:IntSeq)  => idxIf(P)     ==Int 0

  configuration <k> $PGM:K </k>
endmodule
