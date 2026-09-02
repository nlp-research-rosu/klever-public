// verif-parametric.k — DEAD END (does not kompile): the ideal notation, a user-defined
// parametric sort family ValList{S}. kompile: "User-defined parametric sorts are currently unsupported: ValList{S}";
// K's own regression test checkParametricSort.k pins the intent:
// "User-defined parametric sorts are currently unsupported" (still on master, v7.1.337).
module VERIF-PARAMETRIC
  imports INT
  imports BOOL

  syntax {S} ValList{S}
  syntax {S} ValList{S} ::= ".ValList" | vlCons(S, ValList{S})

  syntax Val ::= Int | "other" | listV(ValList{Val})

  syntax KItem ::= floopV(Val)
  configuration <k> $PGM:K </k> <acc> 0 </acc>

  rule <k> floopV(listV(.ValList)) => .K ... </k>
  rule <k> floopV(listV(vlCons(V:Val, R:ValList{Val}))) => floopV(listV(R)) ... </k>
       <acc> A:Int => A ... </acc>
endmodule
