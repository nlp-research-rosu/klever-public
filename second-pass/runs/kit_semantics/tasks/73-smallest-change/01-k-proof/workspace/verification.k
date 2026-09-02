requires "verification-base.k"

module VERIFICATION
  imports VERIFICATION-BASE

  // Exact loop-summary bridge.  loop-connection-spec.k proves this complete
  // configuration transition in a definition that imports VERIFICATION-BASE
  // but does not contain this rule.
  rule
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
      => mismatchCount(VS, 0, halfLen(VS))
    </k>
    <env> 1 => 0 </env>
    <scopes>
      -1 |-> fixedBuiltins
      0 |-> scope(
             "smallest_change"
               |-> closureVal("arr", smallestBody, 0),
             parent(-1))
      1 |-> scope(
             "arr" |-> list(VS:ValSeq)
             "changes" |-> 0
             "i" |-> 0,
             parent(0))
      =>
      -1 |-> fixedBuiltins
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
    requires allInts(VS)
    [priority(40)]
endmodule
