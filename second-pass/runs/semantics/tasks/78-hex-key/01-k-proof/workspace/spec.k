requires "verification.k"

module HEX-KEY-SPEC
  imports HEX-KEY-VERIFICATION

  // Inductive loop lemma: count accumulates the mathematical count, and the
  // induction variable retains its old value on empty input or the final
  // character otherwise.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("digit"), hexKeyLoopBody)
      ~> CONT:K
      => CONT
    </k>
    <env> L:Int </env>
    <scopes>
      (L |-> scope("count" |-> ACC
                   "digit" |-> DIGIT:Val
                   "num" |-> NUM:Val,
                   parent(0))) CALLERSCOPES:Map
      =>
      (L |-> scope("count" |-> (ACC +Int hexCount(CS))
                   "digit" |-> finalDigit(CS, DIGIT)
                   "num" |-> NUM,
                   parent(0))) CALLERSCOPES
    </scopes>
    <scopeLoc> _SCOPELOC:Int </scopeLoc>
    <heap> _HEAP:Map </heap>
    <heapLoc> _HEAPLOC:Int </heapLoc>
    <stack> _STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(loop-lemma)]

  // Entry-point theorem for every symbolic string.
  claim
    <k>
      #loadAll(Module(
        FuncDef("hex_key", Params("num"), hexKeyBody)))
      ~> Call(Name("hex_key"), str(CS:IntSeq))
      => hexCount(CS)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       =>
       0 |-> scope(
         "hex_key" |-> closureVal(("num", .ParamNames), hexKeyBody, 0),
         parent(-1)))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(entry-point)]
endmodule
