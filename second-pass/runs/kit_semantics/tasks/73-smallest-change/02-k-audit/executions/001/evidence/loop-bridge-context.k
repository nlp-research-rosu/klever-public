requires "/tmp/audit-work/candidate-src/verification.k"

module LOOP-BRIDGE-CONTEXT
  imports VERIFICATION

  // The loop bridge is justified only for Return(changes) ~> #endcall.
  // This observable assignment before Return must make that bridge inapplicable.
  claim [different-suffix-rejected]:
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
      ~> (Assign(Name("changes"), Int(99))
          Return(Name("changes")) .Stmts):Stmts
      ~> #endcall
      =>
      99
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
