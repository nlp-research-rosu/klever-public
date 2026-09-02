requires "verification.k"

module BRIDGE-CONTEXT-SPEC
  imports COMPARE-COMMON

  // The proof-local loop rule preserves the old loop-target bindings, but the
  // supplied semantics updates them on every nonempty iteration.  Both lists
  // are one-element integer inputs; the loop target/body exactly match compare.
  claim
    <k>
      #loop(
        zipObj(vCons(1, .ValSeq), vCons(2, .ValSeq)),
        TupleExpr(Name("score"), Name("prediction")),
        appendBody)
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "prediction" |-> 88
             "result"     |-> ref(0)
             "score"      |-> 99,
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      0 |-> list(.ValSeq)
      =>
      0 |-> list(vCons(1, .ValSeq))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
