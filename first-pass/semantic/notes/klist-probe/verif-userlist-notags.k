// verif-userlist-notags.k — DEAD END: two user-list sorts + subsort, NO [overload] tags.
// Kompiles with ZERO relating axioms; spec-userlist-headexposed.k then cannot even parse
// (the sub/super cons pair is a genuine ambiguity — resolving it is the overload tag's job).
//
//   kompile verif-userlist-notags.k --backend haskell --main-module VERIF-USERLIST-NOTAGS --syntax-module VERIF-USERLIST-NOTAGS --output-definition verif-userlist-notags-kompiled
module VERIF-USERLIST-NOTAGS
  imports INT
  imports BOOL
  imports K-EQUAL
  imports STRING

  syntax ValsP ::= List{Val, ","}
  syntax IntsP ::= List{Int, ","}
  syntax ValsP ::= IntsP
  syntax Val   ::= Int | "other" | listP(ValsP)

  syntax KItem ::= floopP(Val) | lblP(K)
  configuration <k> $PGM:K </k> <acc> 0 </acc>

  syntax Val ::= applyBin(String, Val, Val) [function]
  rule applyBin("+", I:Int, J:Int) => I +Int J

  rule <k> floopP(listP(.ValsP)) => .K ... </k>
  rule <k> floopP(listP((V:Val, R:ValsP))) => lblP(floopP(listP(R))) ... </k>
       <acc> A:Int => {applyBin("+", A, V)}:>Int </acc>
  rule <k> lblP(NEXT:K) => NEXT ... </k>

  syntax Int ::= sumP(IntsP, Int) [function, total]
  rule sumP(.IntsP, A:Int) => A [simplification]
  rule sumP((I:Int, R:IntsP), A:Int) => sumP(R, A +Int I) [simplification]
endmodule
