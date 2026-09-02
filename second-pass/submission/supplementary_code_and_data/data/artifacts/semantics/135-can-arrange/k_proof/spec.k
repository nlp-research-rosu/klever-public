requires "verification.k"

module SPEC
  imports VERIFICATION

  // Inductive loop invariant.  This claim is a circularity over the remaining
  // ValSeq: one semantic loop step exposes its head and the recursive state
  // matches the same claim on its tail.
  claim
    <k> #loop(list(VS:ValSeq), Name("current"), arrangeBody)
        ~> (Return(Name("result")) .Stmts):Stmts ~> #endcall
      => #pop
    </k>
    <env> L:Int </env>
    <scopes>
      (L |-> scope(("arr" |-> ARRAY:Val
                    "current" |-> OLD_CURRENT:Val
                    "index" |-> INDEX:Int
                    "previous" |-> PREVIOUS:Val
                    "result" |-> RESULT:Int),
                   PARENT:Parent)
       OTHER:Map)
      =>
      (L |-> scope(?FINALMAP:Map, PARENT)
       OTHER)
    </scopes>
    <ret>
      noRet
      =>
      retV(arrangeScan(VS, INDEX, PREVIOUS, RESULT))
    </ret>
    requires ints(VS)
     andBool INDEX >=Int 1
     andBool isInt(PREVIOUS)
    [label(loop-correct)]

  // End-to-end correctness of the translated function from a fresh module
  // configuration, for every finite integer ValSeq.
  claim
    <k> #loadAll(solutionProgram)
        ~> Call(Name("can_arrange"), list(VS:ValSeq))
      => arrangeResult(VS)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 => ?FINALSCOPELOC:Int </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List => ?FINALSTACK:List </stack>
    <ret> noRet => ?FINALRET:RetState </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires ints(VS)
    [label(function-correct)]
endmodule
