// verif-overload.k — the WORKING encoding: Int-refined lists as [overload]s of the Val lists,
// in both flavors (user-list Vals/Ints and hand-rolled vCons ValSeq/IntVs), NO cast layer
// (no projectIntTotal, no #Ceil lemma, no allInt). The overload tags emit the identification
// equations inj(.IntVs)=.ValSeq and inj(vCons{IntVs}(I,IS))=vCons{ValSeq}(inj I, inj IS) —
// one value, two typings — and demote the SUPER-sort cons/nil to `anywhere` symbols (the
// canonical form of an all-int list is the injected refined term). Also carries the cast-free
// length loop for the 3-way differential.
//
//   kompile verif-overload.k --backend haskell --main-module VERIF-OVERLOAD --syntax-module VERIF-OVERLOAD --output-definition verif-overload-kompiled
module VERIF-OVERLOAD
  imports INT
  imports BOOL
  imports K-EQUAL
  imports STRING

  // ---- user-list flavor -----------------------------------------------------
  syntax Val  ::= Int | "other" | listU(Vals) | list(ValSeq)
  syntax Vals ::= List{Val, ","} [symbol(valsL), terminator-symbol(.valsL), overload(uList)]
  syntax Ints ::= List{Int, ","} [symbol(intsL), terminator-symbol(.intsL), overload(uList)]
  syntax Vals ::= Ints

  // ---- hand-rolled flavor (the reference's shape) ----------------------------
  syntax ValSeq ::= ".ValSeq" [overload(vNil)] | vCons(Val, ValSeq) [overload(vCons)]
  syntax IntVs  ::= ".IntVs"  [overload(vNil)] | vCons(Int, IntVs)  [overload(vCons)]
  syntax ValSeq ::= IntVs

  syntax KItem ::= floopU(Val) | loopU(Val) | decideU(Bool, Val, Vals)
                 | floop(Val)  | cloop(Val) | loopLbl(K)
  configuration <k> $PGM:K </k> <acc> 0 </acc>

  // ---- real-shaped ops (Int,Int only) — deliberately NO cast lemmas ----------
  syntax Val  ::= applyBin(String, Val, Val) [function]
  syntax Bool ::= applyCmp(String, Val, Val) [function]
  rule applyBin("+", I:Int, J:Int) => I +Int J
  rule applyCmp("<", I:Int, J:Int) => I <Int J

  // ---- FOLD + BREAK over listU(Vals) -----------------------------------------
  rule <k> floopU(listU(.Vals)) => .K ... </k>
  rule <k> floopU(listU((V:Val, R:Vals))) => loopLbl(floopU(listU(R))) ... </k>
       <acc> A:Int => {applyBin("+", A, V)}:>Int </acc>

  rule <k> loopU(listU(.Vals)) => .K ... </k>
  rule <k> loopU(listU((V:Val, R:Vals))) => decideU(applyCmp("<", V, 0), V, R) ... </k>
  rule <k> decideU(true,  _V:Val, _R:Vals) => .K ... </k>
  rule <k> decideU(false, V:Val, R:Vals) => loopLbl(loopU(listU(R))) ... </k>
       <acc> A:Int => {applyBin("+", A, V)}:>Int </acc>

  // ---- FOLD over list(ValSeq) -------------------------------------------------
  rule <k> floop(list(.ValSeq)) => .K ... </k>
  rule <k> floop(list(vCons(V:Val, R:ValSeq))) => loopLbl(floop(list(R))) ... </k>
       <acc> A:Int => {applyBin("+", A, V)}:>Int </acc>

  rule <k> loopLbl(NEXT:K) => NEXT ... </k>

  // ---- cast-free length loop (the 3-way differential harness) -----------------
  rule <k> cloop(list(.ValSeq)) => .K ... </k>
  rule <k> cloop(list(vCons(_:Val, R:ValSeq))) => cloop(list(R)) ... </k>
       <acc> A:Int => A +Int 1 </acc>

  // ---- summaries over the REFINED sorts — pure Int, no projection -------------
  syntax Int ::= sumU(Ints, Int) [function, total]
  rule sumU(.Ints, A:Int) => A [simplification]
  rule sumU((I:Int, R:Ints), A:Int) => sumU(R, A +Int I) [simplification]

  syntax Int ::= prefixSumU(Ints, Int) [function, total]
  rule prefixSumU(.Ints, A:Int) => A [simplification]
  rule prefixSumU((I:Int, R:Ints), A:Int)
    => #if I <Int 0 #then A #else prefixSumU(R, A +Int I) #fi [simplification]

  syntax Int ::= sumV(IntVs, Int) [function, total]
  rule sumV(.IntVs, A:Int) => A [simplification]
  rule sumV(vCons(I:Int, R:IntVs), A:Int) => sumV(R, A +Int I) [simplification]

  syntax Int ::= lenAcc(ValSeq, Int) [function, total]
  rule lenAcc(.ValSeq, A:Int) => A [simplification]
  rule lenAcc(vCons(_:Val, R:ValSeq), A:Int) => lenAcc(R, A +Int 1) [simplification]
endmodule
