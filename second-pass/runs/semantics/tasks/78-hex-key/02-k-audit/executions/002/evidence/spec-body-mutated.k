requires "verification-body-mutated.k"

module HEX-KEY-SPEC-BODY-MUTATED
  imports HEX-KEY-VERIFICATION-BODY-MUTATED

  claim
    <k>
      #loop(str(CS:IntSeq), Name("digit"), hexKeyLoopBodyMutated)
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
      (L |-> scope("count" |-> (ACC +Int hexCountMutated(CS))
                   "digit" |-> finalDigitMutated(CS, DIGIT)
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
    [label(body-mutated-loop)]

  claim
    <k>
      #loadAll(Module(
        FuncDef("hex_key", Params("num"), hexKeyBodyMutated)))
      ~> Call(Name("hex_key"), str(CS:IntSeq))
      => hexCountMutated(CS)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       =>
       0 |-> scope(
         "hex_key" |-> closureVal(("num", .ParamNames), hexKeyBodyMutated, 0),
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
    [label(body-mutated-entry)]
endmodule
