requires "stage5-body-mutation.k"

module STAGE5-BODY-MUTATION-SPEC
  imports STAGE5-BODY-MUTATION

  // For input "I", the real body returns 1. The mutated empty loop body
  // returns 0, so the original result obligation must be rejected.
  claim [mutated-body-is-sensitive]:
    <k>
      #loop(
        str(iCons(73, .IntSeq)),
        Name("c"),
        AUDIT-MUTATED-LOOP-BODY)
      ~> ( If(
             Name("pending_i"),
             AugAssign(Name("count"), "+", Int(1)) .Stmts,
             .Stmts)
           Return(Name("count"))
           .Stmts )
      ~> #endcall
      => 1
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( 0 |-> scope(
          "is_bored" |-> closureVal(
            ("S", .ParamNames),
            AUDIT-MUTATED-FUNCTION-BODY,
            0),
          parent(-1))
        -1 |-> builtinsScope
        1 |-> scope(
          ( "S"         |-> str(iCons(73, .IntSeq))
            "count"     |-> 0
            "at_start"  |-> true
            "pending_i" |-> false
            "c"         |-> str(.IntSeq) ),
          parent(0)) )
      =>
      ( 0 |-> scope(
          "is_bored" |-> closureVal(
            ("S", .ParamNames),
            AUDIT-MUTATED-FUNCTION-BODY,
            0),
          parent(-1))
        -1 |-> builtinsScope )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
