requires "verification.k"

module HEX-KEY-SPEC-VACUITY
  imports HEX-KEY-VERIFICATION

  // Unchanged candidate loop lemma, needed by the symbolic entry proof.
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
    [label(loop-lemma-vacuity)]

  // Fresh false mutation: the real result is hexCount(CS), not one more.
  // The satisfying empty-input witness makes the false obligation 0 == 1.
  claim
    <k>
      #loadAll(Module(
        FuncDef("hex_key", Params("num"), hexKeyBody)))
      ~> Call(Name("hex_key"), str(CS:IntSeq))
      => hexCount(CS) +Int 1
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
    [label(false-off-by-one)]
endmodule
