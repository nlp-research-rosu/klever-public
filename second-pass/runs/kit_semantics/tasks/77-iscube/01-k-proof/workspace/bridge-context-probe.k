requires "verification.k"

module BRIDGE-CONTEXT-PROBE
  imports VERIFICATION

  // The source bridge only accepts a singleton Return continuation.  This
  // deliberately adds another statement; a depth-1 run must not use either
  // operational bridge to jump to the target.
  claim [broader-suffix-does-not-match]:
    <k>
      While(
        Compare(
          BinOp(
            "*",
            BinOp("*", Name("candidate"), Name("candidate")),
            Name("candidate")),
          CmpOp("<", Name("a"))),
        AugAssign(Name("candidate"), "+", Int(1)))
      ~> (Return(
           Compare(
             BinOp(
               "*",
               BinOp("*", Name("candidate"), Name("candidate")),
               Name("candidate")),
             CmpOp("==", Name("a"))))
          Assign(Name("probe"), Int(7))
          .Stmts)
      ~> #endcall
      =>
      cubeSearch(8, 0)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( 0 |-> scope(.Map, parent(-1))
        1 |-> scope(
               "a"         |-> 8
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
