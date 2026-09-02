requires "verification-no-bridge.k"

module SPEC-NO-BRIDGE
  imports VERIFICATION-NO-BRIDGE

  // Inductive loop invariant.  It states that iterating over the still
  // unprocessed coefficients extends the one stable result object with the
  // mathematical derivative fold.
  claim
    <k>
      #loop(
        list(enumIntSeq(INPUT:IntVals, N:Int)),
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
    [label(loop-invariant)]

  // The two entry claims are exhaustive over IntVals: the empty case and an
  // arbitrary head followed by an arbitrary finite tail.
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
    [label(entry-empty)]

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
    [label(entry-cons)]
endmodule
