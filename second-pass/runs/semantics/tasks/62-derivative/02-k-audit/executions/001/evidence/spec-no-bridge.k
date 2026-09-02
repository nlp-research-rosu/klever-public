requires "verification-no-bridge.k"

module SPEC-NO-BRIDGE
  imports VERIFICATION-NO-BRIDGE

  claim
    <k>
      #loop(
        list(enumVS(asValSeq(INPUT:IntVals), N:Int)),
        derivativeTarget,
        derivativeLoopStep
        .Stmts
      )
      ~> CONT:K
      => CONT
    </k>
    <env> LOCAL:Int </env>
    <scopes>
      OTHER:Map
      LOCAL |->
        scope(
          "xs" |-> XSLIST:Val
          "result" |-> ref(RESULT:Int)
          "i" |-> PREVIOUSI:Int
          "x" |-> PREVIOUSX:Int,
          PARENT:Parent
        )
      =>
      OTHER
      LOCAL |->
        scope(
          "xs" |-> XSLIST
          "result" |-> ref(RESULT)
          "i" |-> ?FINALI:Int
          "x" |-> ?FINALX:Int,
          PARENT
        )
    </scopes>
    <heap>
      RESULT |-> list(ACC:ValSeq)
      REST:Map
      =>
      RESULT |-> list(derivativeAcc(ACC, INPUT, N))
      REST
    </heap>
    requires N >Int 0
    [label(loop-invariant-no-bridge)]

  claim
    <k>
      Call(Name("derivative"), list(asValSeq(.IntVals)))
      => ref(?RESULT:Int)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("derivative" |-> derivativeClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      ?RESULT |-> list(derivativeSeq(.IntVals))
      ?REST:Map
    </heap>
    <heapLoc> 0 => ?NEXT:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    [label(entry-empty-no-bridge)]

  claim
    <k>
      Call(
        Name("derivative"),
        list(asValSeq(ivCons(HEAD:Int, TAIL:IntVals)))
      )
      => ref(?RESULT:Int)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("derivative" |-> derivativeClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      ?RESULT |-> list(derivativeSeq(ivCons(HEAD, TAIL)))
      ?REST:Map
    </heap>
    <heapLoc> 0 => ?NEXT:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    [label(entry-cons-no-bridge)]
endmodule
