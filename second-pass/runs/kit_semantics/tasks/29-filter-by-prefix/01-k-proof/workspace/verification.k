requires "verification-core.k"

module VERIFICATION
  imports VERIFICATION-CORE

  // Exact operational summary established bridge-free by
  // LOOP-CONNECTION-SPEC.filter-loop-connection.  The match domain is the
  // theorem's complete configuration: exact continuation, call stack,
  // bindings, state cells, and allStrings guard.
  rule
    <k>
      #loop(
        list(INPUT:ValSeq),
        Name("string"),
        filterLoopBody)
      ~> (Return(Name("result")) .Stmts):Stmts
      ~> #endcall
      => ref(H:Int)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (SC:Map
       1 |-> scope(
              "strings" |-> list(ORIGINAL:ValSeq)
              "prefix" |-> str(P:IntSeq)
              "result" |-> ref(H)
              "string" |-> str(OLD:IntSeq),
              parent(0)))
      => SC
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap>
      HP:Map
      H |-> list(
             ACC:ValSeq
             => filterPrefixAcc(ACC, INPUT, P))
    </heap>
    <heapLoc> NEXT:Int </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires allStrings(INPUT)
    [priority(40)]
endmodule
