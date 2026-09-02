requires "verification.k"

// The bridge erases the loop without assigning score/prediction.  Therefore
// the following claim closes only in the bridge-enabled theory: the observable
// continuation reads the stale pre-loop score 99.
module BRIDGE-CONTEXT-FALSE
  imports COMPARE-VERIFICATION

  claim
    <k>
      #loop(
        zipObj(vCons(1, .ValSeq), vCons(2, .ValSeq)),
        TupleExpr(Name("score"), Name("prediction")),
        appendBody)
      ~> Name("score")
      => 99
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "result" |-> ref(0)
             "score" |-> 99
             "prediction" |-> 88,
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      0 |-> list(.ValSeq => vCons(1, .ValSeq))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule

// This is the identical false conclusion with the bridge removed.  It must
// fail because fixed execution binds score=1 and prediction=2.
module FIXED-CONTEXT-REJECT-FALSE
  imports COMPARE-COMMON

  claim
    <k>
      #loop(
        zipObj(vCons(1, .ValSeq), vCons(2, .ValSeq)),
        TupleExpr(Name("score"), Name("prediction")),
        appendBody)
      ~> Name("score")
      => 99
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "result" |-> ref(0)
             "score" |-> 99
             "prediction" |-> 88,
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      0 |-> list(.ValSeq => vCons(1, .ValSeq))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule

// The fixed semantics' correct outcome from the same initial state.
module FIXED-CONTEXT-CORRECT
  imports COMPARE-COMMON

  claim
    <k>
      #loop(
        zipObj(vCons(1, .ValSeq), vCons(2, .ValSeq)),
        TupleExpr(Name("score"), Name("prediction")),
        appendBody)
      ~> Name("score")
      => 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "result" |-> ref(0)
             "score" |-> 99
             "prediction" |-> 88,
             parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
             "result" |-> ref(0)
             "score" |-> 1
             "prediction" |-> 2,
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      0 |-> list(.ValSeq => vCons(1, .ValSeq))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
