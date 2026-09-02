requires "verification.k"

module MAX-ELEMENT-SPEC
  imports MAX-ELEMENT-VERIFICATION

  // Inductive fold lemma for the reference semantics' max accumulator.
  claim
    <k> #maxAcc(list(intVals(REST:IntSeq)), ACC:Int) ~> CONT:K
      => maxOf(ACC, REST) ~> CONT </k>

  // Universal contract: for every non-empty finite sequence of integers, the
  // translated max_element program returns its mathematical maximum.
  claim
    <k> #loadAll(maxElementProgram)
         ~> Call(Name("max_element"),
                 (list(vCons(FIRST:Int, intVals(REST:IntSeq))), .Exprs))
      => maxOf(FIRST, REST) </k>
    <env> 0 </env>
    <scopes> (0 |-> scope(.Map, parent(-1))
              -1 |-> builtinsScope)
          => ?FINALSCOPES:Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  // Prompt examples, retained as independently closed regression claims.
  claim
    <k> #loadAll(maxElementProgram)
         ~> Call(Name("max_element"),
                 (list(vCons(1, vCons(2, vCons(3, .ValSeq)))), .Exprs))
      => 3 </k>
    <env> 0 </env>
    <scopes> (0 |-> scope(.Map, parent(-1))
              -1 |-> builtinsScope)
          => ?FINALSCOPES:Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim
    <k> #loadAll(maxElementProgram)
         ~> Call(Name("max_element"),
                 (list(vCons(5,
                       vCons(3,
                       vCons(0 -Int 5,
                       vCons(2,
                       vCons(0 -Int 3,
                       vCons(3,
                       vCons(9,
                       vCons(0,
                       vCons(123,
                       vCons(1,
                       vCons(0 -Int 10, .ValSeq)))))))))))),
                  .Exprs))
      => 123 </k>
    <env> 0 </env>
    <scopes> (0 |-> scope(.Map, parent(-1))
              -1 |-> builtinsScope)
          => ?FINALSCOPES:Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
