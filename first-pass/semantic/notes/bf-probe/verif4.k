module BF-PROBE4
  imports INT
  imports BOOL
  imports STRING
  imports K-EQUAL
  imports MAP
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
  syntax IntSeq ::= strToCodes(String) [function]
  rule strToCodes("") => .IntSeq
  rule strToCodes(S:String) => iCons(ordChar(substrString(S,0,1)), strToCodes(substrString(S,1,lengthString(S)))) requires S =/=String ""
  // #if cascade (produces a #if term)
  syntax Int ::= idx(IntSeq) [function, total]
  rule idx(P:IntSeq) => #if P ==K strToCodes("A") #then 0 #else #if P ==K strToCodes("B") #then 1 #else -1 #fi #fi [simplification]
  // rule-based (reduces to a BARE Int per branch)
  syntax Int ::= idxCNB(IntSeq) [function, total]
  rule idxCNB(P:IntSeq) => 0 requires P ==K strToCodes("A") [simplification]
  rule idxCNB(P:IntSeq) => 1 requires P ==K strToCodes("B") [simplification]
  rule idxCNB(P:IntSeq) => -1 requires notBool (P ==K strToCodes("A")) andBool notBool (P ==K strToCodes("B")) [simplification]
  // guard-buried variants:
  syntax Int ::= combDirect(IntSeq) [function, total]
  rule combDirect(P:IntSeq) => #if (idx(P) <Int 0) #then -99 #else idx(P) +Int 100 #fi [simplification]
  syntax Int ::= combCNB(IntSeq) [function, total]
  rule combCNB(P:IntSeq) => #if (idxCNB(P) <Int 0) #then -99 #else idxCNB(P) +Int 100 #fi [simplification]
  syntax KItem ::= dispatchC(IntSeq) | res(Int) | selC(Bool, Int, KItem)
  rule <k> dispatchC(P:IntSeq) => selC(P==K strToCodes("A"),0, selC(P==K strToCodes("B"),1, res(-99))) ... </k>
  rule <k> selC(true,  N:Int, _:KItem) => res(N +Int 100) ... </k>
  rule <k> selC(false, _:Int, K:KItem) => K ... </k>
  configuration <k> $PGM:K </k>
endmodule
