requires "verification.k"

module SPEC-GROUND-WITNESS
  imports VERIFICATION

  claim [ground-loop-witness]:
    <k> #loop(
          list(intsVS(iCons(3, iCons(1, iCons(4, .IntSeq))))),
          Name("number"),
          rollingMaxLoopBody)
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      (1 |-> scope(("result"  |-> ref(7)
                    "first"   |-> true
                    "maximum" |-> 99
                    "number"  |-> -5
                    "numbers" |-> list(intsVS(iCons(3, iCons(1, iCons(4, .IntSeq)))))),
                   parent(0))
       0 |-> scope(("rolling_max" |-> noneV), parent(-1))
       -1 |-> builtinsScope)
      =>
      (1 |-> scope(("result"  |-> ref(7)
                    "first"   |-> false
                    "maximum" |-> 4
                    "number"  |-> 4
                    "numbers" |-> list(intsVS(iCons(3, iCons(1, iCons(4, .IntSeq)))))),
                   parent(0))
       0 |-> scope(("rolling_max" |-> noneV), parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <heap>
      7 |-> list(vCons(2, .ValSeq))
      =>
      7 |-> list(vCons(2, vCons(3, vCons(3, vCons(4, .ValSeq)))))
    </heap>

  claim [ground-entry-witness]:
    <k> #loadAll(rollingMaxModule)
         ~> Call(
              Name("rolling_max"),
              (list(intsVS(iCons(3, iCons(1, iCons(4, .IntSeq))))), .Exprs))
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
      .Map =>
      (0 |-> list(vCons(3, vCons(3, vCons(4, .ValSeq)))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
