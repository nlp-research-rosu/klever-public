// bf-probe/verif2.k — FAITHFUL reproduction of the 148-bf context: the negated ==K atoms come
// from a <k>-cell #branch (not a `requires`), and idxOf is pinned in the POSTCONDITION (spec RHS,
// checked by implication) — exactly where the full-spec cascade failed to collapse. 2 literals.

module BF-PROBE2
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

  // (1) #if cascade
  syntax Int ::= idxIf(IntSeq) [function, total]
  rule idxIf(P:IntSeq) =>
    #if P ==K strToCodes("A") #then 0 #else #if P ==K strToCodes("B") #then 1 #else -1 #fi #fi
    [simplification]

  // (2) rule-based, notBool(==K) conjunction fallback
  syntax Int ::= idxCNB(IntSeq) [function, total]
  rule idxCNB(P:IntSeq) => 0 requires P ==K strToCodes("A") [simplification]
  rule idxCNB(P:IntSeq) => 1 requires P ==K strToCodes("B") [simplification]
  rule idxCNB(P:IntSeq) => -1
    requires notBool (P ==K strToCodes("A")) andBool notBool (P ==K strToCodes("B")) [simplification]

  // mini "program": dispatch(P) branches on P==A / P==B via #branch, landing res(0/1/-1).
  // This makes kprove generate the SAME negated-==K path condition the real if/elif chain does.
  syntax KItem ::= dispatch(IntSeq) | res(Int) | sel(Bool, Int, KItem)
  rule <k> dispatch(P:IntSeq)
        => sel(P ==K strToCodes("A"), 0, sel(P ==K strToCodes("B"), 1, res(-1))) ... </k>
  rule <k> sel(true,  N:Int, _:KItem) => res(N) ... </k>
  rule <k> sel(false, _:Int, K:KItem) => K ... </k>

  configuration <k> $PGM:K </k>
endmodule
