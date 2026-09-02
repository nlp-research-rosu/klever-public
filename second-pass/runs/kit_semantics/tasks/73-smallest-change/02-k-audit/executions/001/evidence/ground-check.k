requires "/tmp/audit-work/candidate-src/verification.k"

module GROUND-CHECK
  imports VERIFICATION

  // This sequence is a concrete witness for allInts(VS).
  claim [all-ints-witness]:
    <k>
      allInts(vCons(1, vCons(2, .ValSeq))) => true
      ...
    </k>

  // The result term in the symbolic postcondition evaluates to 1.
  claim [summary-witness]:
    <k>
      mismatchCount(
        vCons(1, vCons(2, .ValSeq)),
        0,
        halfLen(vCons(1, vCons(2, .ValSeq))))
      => 1
      ...
    </k>

  // Concrete instance of the whole-program entry claim for arr = [1, 2].
  claim [entry-witness]:
    <k>
      #loadAll(Module(smallestDef))
      ~> Call(
           Name("smallest_change"),
           list(vCons(1, vCons(2, .ValSeq))))
      =>
      1
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

  // Concrete state satisfying the loop claim: VS=[1,2], C=0, I=0.
  claim [loop-witness]:
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
      =>
      1
    </k>
    <env> 1 => 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
             "smallest_change"
               |-> closureVal("arr", smallestBody, 0),
             parent(-1))
      1 |-> scope(
             "arr" |-> list(vCons(1, vCons(2, .ValSeq)))
             "changes" |-> 0
             "i" |-> 0,
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
endmodule
