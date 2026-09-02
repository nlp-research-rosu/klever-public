requires "verification.k"

module GROUND-INSTANCES
  imports VERIFICATION

  // Satisfiable instance of the loop claim's exact precondition.
  claim [loop-witness]:
    <k> #loop(list(intsVS(iCons(4, iCons(2, iCons(7, .IntSeq))))),
              Name("number"), rollingMaxLoopBody)
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      (1 |-> scope(("result"  |-> ref(9)
                    "first"   |-> true
                    "maximum" |-> 0
                    "number"  |-> 0
                    "numbers" |-> list(intsVS(iCons(4, iCons(2, iCons(7, .IntSeq)))))),
                   parent(0))
       0 |-> scope(("rolling_max" |->
                     closureVal(("numbers", .ParamNames), rollingMaxBody, 0)),
                    parent(-1))
       -1 |-> builtinsScope)
      =>
      (1 |-> scope(("result"  |-> ref(9)
                    "first"   |-> false
                    "maximum" |-> 7
                    "number"  |-> 7
                    "numbers" |-> list(intsVS(iCons(4, iCons(2, iCons(7, .IntSeq)))))),
                   parent(0))
       0 |-> scope(("rolling_max" |->
                     closureVal(("numbers", .ParamNames), rollingMaxBody, 0)),
                    parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <heap>
      9 |-> list(.ValSeq)
      =>
      9 |-> list(vCons(4, vCons(4, vCons(7, .ValSeq))))
    </heap>

  claim [entry-empty]:
    <k> #loadAll(rollingMaxModule)
         ~> Call(Name("rolling_max"), (list(intsVS(.IntSeq)), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0  |-> scope(("rolling_max" |->
                       closureVal(("numbers", .ParamNames), rollingMaxBody, 0)),
                    parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => (0 |-> list(.ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [entry-negative]:
    <k> #loadAll(rollingMaxModule)
         ~> Call(Name("rolling_max"),
                 (list(intsVS(iCons(-8, iCons(-9, iCons(-3, iCons(-3, iCons(-10, .IntSeq))))))),
                  .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0  |-> scope(("rolling_max" |->
                       closureVal(("numbers", .ParamNames), rollingMaxBody, 0)),
                    parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      (0 |-> list(vCons(-8, vCons(-8, vCons(-3, vCons(-3, vCons(-3, .ValSeq)))))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [entry-branches]:
    <k> #loadAll(rollingMaxModule)
         ~> Call(Name("rolling_max"),
                 (list(intsVS(iCons(5, iCons(5, iCons(4, iCons(6, iCons(1, .IntSeq))))))),
                  .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0  |-> scope(("rolling_max" |->
                       closureVal(("numbers", .ParamNames), rollingMaxBody, 0)),
                    parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      (0 |-> list(vCons(5, vCons(5, vCons(5, vCons(6, vCons(6, .ValSeq)))))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
