// verif-hooked.k — DEAD END (does not kompile): domains.md's hooked List stamped out at two
// element sorts (wasm-semantics ListInt precedent) + the subsort between them. kompile:
// "Cannot add new constructors to hooked sort ListVal" — hooked sorts cannot participate in
// subsorting at all, so the builtin List can never resolve an element-refined subsort.
module VERIF-HOOKED
  imports INT
  imports BOOL
  imports K-EQUAL
  imports STRING

  syntax Val ::= Int | "other" | listH(ListVal)

  syntax ListVal [hook(LIST.List)]
  syntax ListVal ::= ListVal ListVal
      [left, function, total, hook(LIST.concat), symbol(_ListVal_), assoc, unit(.ListVal),
       element(ListValItem)]
  syntax ListVal ::= ".ListVal" [function, total, hook(LIST.unit), symbol(.ListVal)]
  syntax ListVal ::= ListValItem(Val) [function, total, hook(LIST.element), symbol(ListValItem)]

  syntax ListInt [hook(LIST.List)]
  syntax ListInt ::= ListInt ListInt
      [left, function, total, hook(LIST.concat), symbol(_ListInt_), assoc, unit(.ListInt),
       element(ListIntItem)]
  syntax ListInt ::= ".ListInt" [function, total, hook(LIST.unit), symbol(.ListInt)]
  syntax ListInt ::= ListIntItem(Int) [function, total, hook(LIST.element), symbol(ListIntItem)]

  syntax ListVal ::= ListInt   // the subsort under test -> structural compile error

  syntax KItem ::= floopH(Val)
  configuration <k> $PGM:K </k> <acc> 0 </acc>
endmodule
