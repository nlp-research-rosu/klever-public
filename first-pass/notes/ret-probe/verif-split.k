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

  // SPLIT: ret stashes the value + discards the frame body (~> _); #pop pops the frame later.
  // NOTE no trailing `...` here: `~> _` already discards the whole rest of the computation
  // (cf. real mpy-functions.k `V:Val ~> #ret ~> _ => #pop`). A spurious `...` makes K read `_`
  // as a single KItem and keep a tail var, which then breaks the circularity (see INVESTIGATION).
  rule <k> ret(V:Int) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>
  rule <k> endcall      => #pop ... </k> <ret> noRet => retV(0) </ret>
  rule <k> #pop => V ~> CONT </k>
       <ret> retV(V:Int) => noRet </ret>
       <stack> ListItem(frame(CONT:K)) => .List ... </stack>

  syntax Int ::= anyPos(IntSeq) [function, total]
  rule anyPos(.IntSeq) => 0 [simplification]
  rule anyPos(iCons(X:Int, _R:IntSeq)) => 1        requires X >Int 0 [simplification]
  rule anyPos(iCons(X:Int, R:IntSeq))  => anyPos(R) requires notBool (X >Int 0) [simplification]
endmodule
