module PY-LIST-DOMAIN
  imports INT
  imports BOOL

  // A deliberately explicit value representation keeps symbolic list tails
  // constructor-based and makes concrete krun input unambiguous.
  syntax IntList ::= "Nil" [symbol(nil)]
                   | "Cons" "(" Int "," IntList ")" [symbol(cons)]

  syntax IntList ::= insertInt(Int, IntList) [function]
  rule insertInt(I, Nil) => Cons(I, Nil)
  rule insertInt(I, Cons(J, JS)) => Cons(I, Cons(J, JS)) requires I <=Int J
  rule insertInt(I, Cons(J, JS)) => Cons(J, insertInt(I, JS)) requires I >Int J

  syntax IntList ::= sortInts(IntList) [function]
  rule sortInts(Nil) => Nil
  rule sortInts(Cons(I, IS)) => insertInt(I, sortInts(IS))

  syntax Bool ::= eqIntLists(IntList, IntList) [function]
  rule eqIntLists(Nil, Nil) => true
  rule eqIntLists(Nil, Cons(_, _)) => false
  rule eqIntLists(Cons(_, _), Nil) => false
  rule eqIntLists(Cons(I, IS), Cons(J, JS))
    => (I ==Int J) andBool eqIntLists(IS, JS)

  syntax Int ::= countInt(Int, IntList) [function]
  rule countInt(_, Nil) => 0
  rule countInt(I, Cons(J, JS)) => 1 +Int countInt(I, JS)
    requires I ==Int J
  rule countInt(I, Cons(J, JS)) => countInt(I, JS)
    requires I =/=Int J

  // countsAtMost(SOURCE, ITEMS, LIMIT) checks each item drawn from ITEMS in
  // SOURCE. Calling it with the same list twice models Python's all over count.
  syntax Bool ::= countsAtMost(IntList, IntList, Int) [function]
  rule countsAtMost(_, Nil, _) => true
  rule countsAtMost(SOURCE, Cons(I, IS), LIMIT)
    => (countInt(I, SOURCE) <=Int LIMIT)
       andBool countsAtMost(SOURCE, IS, LIMIT)

  syntax Bool ::= countsAtMostTwo(IntList, IntList) [function]
  rule countsAtMostTwo(SOURCE, ITEMS) => countsAtMost(SOURCE, ITEMS, 2)
endmodule
