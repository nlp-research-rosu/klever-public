requires "mutation.k"

module MUTATION-SPEC
  imports MUTATION

  // The original summary must not prove for the mutated empty body.
  claim [mutated-loop]:
    <k>
      #loop(str(IS:IntSeq), Name("c"), MUTATED-LOOP-BODY)
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
endmodule
