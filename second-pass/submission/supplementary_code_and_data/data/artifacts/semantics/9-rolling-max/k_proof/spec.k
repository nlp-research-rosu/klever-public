requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [rolling-max-loop]:
    <k> #loop(list(intsVS(INPUT)), Name("number"), rollingMaxLoopBody) ~> CONT
      => CONT
    </k>
    <env> 1 </env>
    <scopes>
      (1 |-> scope(("result"  |-> ref(H)
                    "first"   |-> FIRST
                    "maximum" |-> MAXIMUM
                    "number"  |-> NUMBER
                    "numbers" |-> NUMBERS), parent(0))
       0 |-> scope(("rolling_max" |-> CLOSURE), parent(-1))
       -1 |-> builtinsScope)
      =>
      (1 |-> scope(("result"  |-> ref(H)
                    "first"   |-> firstAfter(INPUT, FIRST)
                    "maximum" |-> maximumAfter(INPUT, FIRST, MAXIMUM)
                    "number"  |-> numberAfter(INPUT, NUMBER)
                    "numbers" |-> NUMBERS), parent(0))
       0 |-> scope(("rolling_max" |-> CLOSURE), parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <heap>
      (H |-> list(ACC) HEAP_REST)
      => (H |-> list(rollingAcc(INPUT, FIRST, MAXIMUM, ACC)) HEAP_REST)
    </heap>

  claim [rolling-max-correct]:
    <k> #loadAll(rollingMaxModule)
         ~> Call(Name("rolling_max"), (list(intsVS(INPUT)), .Exprs))
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
      .Map => (0 |-> list(rollingAcc(INPUT, true, 0, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
