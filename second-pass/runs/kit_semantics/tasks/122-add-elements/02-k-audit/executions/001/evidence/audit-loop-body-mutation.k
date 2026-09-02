requires "verification-base.k"

module AUDIT-LOOP-BODY-MUTATION
  imports VERIFICATION-BASE

  // Reviewer-authored sensitivity probe: execute a genuinely changed body
  // (upper inclusion bound 98) while retaining the original 99-inclusive
  // qualifyingPrefix postcondition.
  claim [changed-upper-bound]:
    <k>
      #loop(
        list(VS:ValSeq),
        Name("element"),
        If(
          Compare(Name("remaining"), CmpOp("==", Int(0))),
          Break .Stmts,
          .Stmts
        )
        If(
          BoolOp(
            "and",
            Compare(Name("element"), CmpOp(">=", UnaryOp("-", Int(99)))),
            Compare(Name("element"), CmpOp("<=", Int(98)))
          ),
          AugAssign(Name("total"), "+", Name("element")) .Stmts,
          .Stmts
        )
        AugAssign(Name("remaining"), "-", Int(1))
      )
      ~> (Return(Name("total")) .Stmts)
      ~> #endcall
      =>
      S:Int +Int qualifyingPrefix(VS, N)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      0 |-> scope(GLOBALS:Map, parent(-1))
      -1 |-> BUILTINS:Scope
      1 |-> scope(
        "arr" |-> ARRAY:Val
        "k" |-> KVALUE:Int
        "total" |-> S
        "element" |-> OLD:Val
        "remaining" |-> N:Int,
        parent(0)
      )
      =>
      0 |-> scope(GLOBALS, parent(-1))
      -1 |-> BUILTINS
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HEAPLOC:Int </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1)) => .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
     andBool 0 <=Int N
     andBool N <=Int vsLen(VS)
endmodule
