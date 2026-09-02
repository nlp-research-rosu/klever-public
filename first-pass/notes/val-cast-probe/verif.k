// verif.k — can a circularity iterate the reference's REAL heterogeneous list(ValSeq) over a
// symbolic all-int payload? Folds: yes (threaded summary). Branches: yes, via the RV ceils.k
// total-cast pattern (projectIntTotal [total, no-evaluators]). This file is the WORKING semantics;
// verif-partial.k is identical except projectIntTotal is a bare [function] (the contrast).
//
//   kompile verif.k --backend haskell --main-module VERIF --syntax-module VERIF --output-definition verif-kompiled
module VERIF
  imports INT
  imports BOOL
  imports K-EQUAL
  imports STRING

  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
  syntax Val    ::= Int | "other" | list(ValSeq) | seq(IntSeq)
  syntax KItem  ::= floop(Val) | loop(Val) | iloop(Val) | loopLbl(K)
                  | decide(Bool, Val, ValSeq) | idecide(Bool, Int, IntSeq)
  configuration <k> $PGM:K </k> <acc> 0 </acc>

  // ==== the TOTAL cast (RV kasmer-multiversx .../ceils.k) ====================
  // projectIntTotal is a DECLARED-total, abstract (no-evaluators) symbol: K trusts it total, so Z3
  // treats it as an unknown integer -> a comparison on it is decidable -> a branch can split.
  syntax Bool ::= definedProjectInt(KItem) [function, total]
  rule definedProjectInt(K:KItem) => isInt(K)
  syntax Int  ::= projectIntTotal(KItem) [function, total, symbol(projectIntTotal), no-evaluators]
  rule #Ceil({@Arg0:KItem}:>Int) => ({ definedProjectInt(@Arg0) #Equals true } #And #Ceil(@Arg0)) [simplification]
  rule projectIntTotal(Arg0:KItem) => {Arg0}:>Int requires definedProjectInt(Arg0) [concrete, simplification(10), preserves-definedness]
  rule {Arg0:KItem}:>Int => projectIntTotal(Arg0) requires definedProjectInt(Arg0) [symbolic(Arg0), simplification, preserves-definedness]

  // ==== real-shaped ops (Int,Int only) + the cast lemmas ====================
  syntax Val  ::= applyBin(String, Val, Val) [function]
  syntax Bool ::= applyCmp(String, Val, Val) [function]
  rule applyBin("+", I:Int, J:Int) => I +Int J
  rule applyCmp("<", I:Int, J:Int) => I <Int J
  rule applyBin(OP:String, I:Int, V:Val) => applyBin(OP, I, {V}:>Int) requires isInt(V) [simplification]
  rule applyCmp(OP:String, V:Val, J:Int) => applyCmp(OP, {V}:>Int, J) requires isInt(V) [simplification]

  // ==== FOLD over list(ValSeq): sum every element (no branch) ================
  rule <k> floop(list(.ValSeq)) => .K ... </k>
  rule <k> floop(list(vCons(V:Val, R:ValSeq))) => loopLbl(floop(list(R))) ... </k>
       <acc> A:Int => {applyBin("+", A, V)}:>Int </acc>

  // ==== BRANCH over list(ValSeq): loop-break (if x<0: break) =================
  rule <k> loop(list(.ValSeq)) => .K ... </k>
  rule <k> loop(list(vCons(V:Val, R:ValSeq))) => decide(applyCmp("<", V, 0), V, R) ... </k>
  rule <k> decide(true,  _V:Val, _R:ValSeq) => .K ... </k>
  rule <k> decide(false, V:Val, R:ValSeq) => loopLbl(loop(list(R))) ... </k>
       <acc> A:Int => {applyBin("+", A, V)}:>Int </acc>

  // ==== CONTROL: the SAME loop-break over seq(IntSeq) — a GENUINE Int head ===
  rule <k> iloop(seq(.IntSeq)) => .K ... </k>
  rule <k> iloop(seq(iCons(I:Int, R:IntSeq))) => idecide(I <Int 0, I, R) ... </k>
  rule <k> idecide(true,  _I:Int, _R:IntSeq) => .K ... </k>
  rule <k> idecide(false, I:Int, R:IntSeq) => loopLbl(iloop(seq(R))) ... </k>
       <acc> A:Int => A +Int I </acc>

  rule <k> loopLbl(NEXT:K) => NEXT ... </k>

  // ==== precondition + the buried-variable constructor ======================
  syntax Bool ::= allInt(ValSeq) [function, total]
  rule allInt(.ValSeq) => true
  rule allInt(vCons(V:Val, R:ValSeq)) => isInt(V) andBool allInt(R)
  syntax ValSeq ::= ints2vals(IntSeq) [function, total]   // for the buried-variable test
  rule ints2vals(.IntSeq) => .ValSeq
  rule ints2vals(iCons(I:Int, R:IntSeq)) => vCons(I, ints2vals(R))

  // ==== threaded summaries ==================================================
  syntax Int ::= sumAcc(ValSeq, Int) [function]            // fold
  rule sumAcc(.ValSeq, A:Int) => A [simplification]
  rule sumAcc(vCons(V:Val, R:ValSeq), A:Int) => sumAcc(R, A +Int {V}:>Int) requires isInt(V) [simplification]

  syntax Int ::= prefixSumAcc(ValSeq, Int) [function]      // break over list(ValSeq)
  rule prefixSumAcc(.ValSeq, A:Int) => A [simplification]
  rule prefixSumAcc(vCons(V:Val, R:ValSeq), A:Int)
    => #if {V}:>Int <Int 0 #then A #else prefixSumAcc(R, A +Int {V}:>Int) #fi requires isInt(V) [simplification]
  rule prefixSumAcc(vCons(V:Val, _R:ValSeq), A:Int) => A requires notBool isInt(V) [simplification]
  rule #Ceil(prefixSumAcc(_VS:ValSeq, _A:Int)) => #Top [simplification]

  syntax Int ::= prefixSumI(IntSeq, Int) [function, total]        // break over seq(IntSeq) control
  rule prefixSumI(.IntSeq, A:Int) => A [simplification]
  rule prefixSumI(iCons(I:Int, R:IntSeq), A:Int)
    => #if I <Int 0 #then A #else prefixSumI(R, A +Int I) #fi [simplification]
endmodule
