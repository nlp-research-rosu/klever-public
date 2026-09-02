requires "verification.k"

module SPEC
  imports VERIFICATION

  // Circularity at the exact range-loop head and exact call continuation.
  // C is the number of mismatches already seen; mismatchCount summarizes the
  // still-unvisited indices I .. STOP-1.
  claim [loop-invariant]:
    <k>
      #while(
        Compare(
          Name("i"),
          CmpOp(
            "<",
            BinOp(
              "//",
              Call(Name("len"), Name("arr")),
              Int(2)))),
        smallestLoopBody)
      ~> (Return(Name("changes")) .Stmts):Stmts
      ~> #endcall
      => C +Int mismatchCount(VS, I, halfLen(VS))
    </k>
    <env> 1 => 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
             "smallest_change"
               |-> closureVal("arr", smallestBody, 0),
             parent(-1))
      1 |-> scope(
             "arr" |-> list(VS:ValSeq)
             "changes" |-> C:Int
             "i" |-> I:Int,
             parent(0))
      =>
      -1 |-> builtinsScope
      0 |-> scope(
             "smallest_change"
               |-> closureVal("arr", smallestBody, 0),
             parent(-1))
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires
      allInts(VS)
      andBool 0 <=Int I

  // Whole-program target: load the submitted definition, resolve its binding,
  // call it on an arbitrary finite integer list, and constrain the result.
  claim [smallest-change]:
    <k>
      #loadAll(Module(smallestDef))
      ~> Call(Name("smallest_change"), list(VS:ValSeq))
      =>
      mismatchCount(VS, 0, halfLen(VS))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
             "smallest_change"
               |-> closureVal("arr", smallestBody, 0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
endmodule
