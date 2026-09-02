requires "verification-base.k"

module VERIFICATION
  imports VERIFICATION-BASE

  // Exact operational form of the independently proved LOOP-SPEC.loop
  // connection theorem.  No continuation or state cell is generalized.
  rule
    <k>
      #loop(str(IS:IntSeq), Name("c"), BORED-LOOP-BODY)
      ~> ( If(
             Name("pending_i"),
             AugAssign(Name("count"), "+", Int(1)) .Stmts,
             .Stmts)
           Return(Name("count"))
           .Stmts )
      ~> #endcall
      => scanResult(IS, N:Int, A:Bool, P:Bool)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( 0 |-> scope(
          "is_bored" |-> closureVal(
            ("S", .ParamNames),
            BORED-FUNCTION-BODY,
            0),
          parent(-1))
        -1 |-> B:Scope
        1 |-> scope(
          ( "S"         |-> str(ORIG:IntSeq)
            "count"     |-> N
            "at_start"  |-> A
            "pending_i" |-> P
            "c"         |-> str(CUR:IntSeq) ),
          parent(0)) )
      =>
      ( 0 |-> scope(
          "is_bored" |-> closureVal(
            ("S", .ParamNames),
            BORED-FUNCTION-BODY,
            0),
          parent(-1))
        -1 |-> B )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [priority(40)]
endmodule
