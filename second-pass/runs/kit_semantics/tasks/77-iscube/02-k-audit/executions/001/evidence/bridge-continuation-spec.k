requires "verification-base.k"

module BRIDGE-CONTINUATION-SPEC
  imports VERIFICATION-BASE

  // The exact operational bridge only accepts the source Return comparison.
  // This reachable alternate continuation returns false instead; fixed
  // semantics must execute it, and a broadened bridge would return true.
  claim [alternate-return-is-observed]:
    <k>
      #while(
        Compare(
          BinOp(
            "*",
            BinOp("*", Name("candidate"), Name("candidate")),
            Name("candidate")),
          CmpOp("<", Name("a"))),
        AugAssign(Name("candidate"), "+", Int(1)))
      ~> (Return(Bool(false)) .Stmts)
      ~> #endcall
      =>
      false
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( 0 |-> scope(.Map, parent(-1))
        1 |-> scope(
               "a"         |-> 1
               "candidate" |-> 0,
               parent(0))
      =>
        0 |-> scope(.Map, parent(-1))
      )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
