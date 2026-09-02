// notes/iter-probe/verif-rw.k — iterNext as a <k>-CELL STEP (the WORKING wiring).
// Identical to verif-fn.k EXCEPT iterNext reduces on the <k> cell (not a function),
// and #drive drives it via ~> instead of nesting it as an argument.

module ITER-RW
  imports INT
  imports BOOL

  syntax ValSeq ::= ".ValSeq" | vCons(Int, ValSeq)
  syntax Val    ::= list(ValSeq)

  // the iterator step, as a <k>-CELL REWRITE — kprove NARROWS a symbolic arg.
  syntax KItem ::= iterNext(Val) | "iDone" | iYield(Int, Val)
  rule <k> iterNext(list(.ValSeq))                => iDone ... </k>
  rule <k> iterNext(list(vCons(X:Int, R:ValSeq))) => iYield(X, list(R)) ... </k>

  // driver: iterNext(V) is DRIVEN on the cell; #step consumes its result via ~>.
  syntax KItem ::= #drive(Val) | "#step"
  rule <k> #drive(V:Val)                     => iterNext(V) ~> #step ... </k>
  rule <k> iDone ~> #step                    => .K ... </k>
  rule <k> iYield(_X:Int, REST:Val) ~> #step => #drive(REST) ... </k>

  configuration <k> $PGM:KItem </k>
endmodule
