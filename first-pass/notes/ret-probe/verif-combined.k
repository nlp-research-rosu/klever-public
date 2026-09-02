module RET
  imports INT
  imports BOOL
  imports LIST
  imports K-EQUAL
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
  syntax Frame  ::= frame(K)
  syntax KItem  ::= callAny(IntSeq) | loop(IntSeq) | ret(Int) | "endcall" | "#pop"
  syntax RetS   ::= "noRet" | retV(Int)
  configuration <k> $PGM:K </k> <stack> .List </stack> <ret> noRet </ret>

  rule <k> callAny(S:IntSeq) ~> CONT:K => loop(S) ~> endcall </k>
       <stack> .List => ListItem(frame(CONT)) ... </stack>
  rule <k> loop(iCons(X:Int, _R:IntSeq)) => ret(1) ... </k> requires X >Int 0          // early return
  rule <k> loop(iCons(X:Int, R:IntSeq))  => loop(R) ... </k> requires notBool (X >Int 0)
  rule <k> loop(.IntSeq) => .K ... </k>

  // COMBINED: one rule pops the frame, delivers V, discards the frame body

  rule <k> ret(V:Int) ~> _ => V ~> CONT </k> <stack> ListItem(frame(CONT:K)) => .List ... </stack>
  rule <k> endcall      => 0 ~> CONT </k> <stack> ListItem(frame(CONT:K)) => .List ... </stack>

  syntax Int ::= anyPos(IntSeq) [function, total]
  rule anyPos(.IntSeq) => 0 [simplification]
  rule anyPos(iCons(X:Int, _R:IntSeq)) => 1        requires X >Int 0 [simplification]
  rule anyPos(iCons(X:Int, R:IntSeq))  => anyPos(R) requires notBool (X >Int 0) [simplification]
endmodule
