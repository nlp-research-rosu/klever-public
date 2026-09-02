requires "verification-base.k"

module CONNECTION-MUTATION
  imports VERIFICATION-BASE

  // Deliberately false ground witness: stepping 0 -> 2 skips the cube root 1.
  claim [mutated-step-breaks-summary]:
    <k>
      #while(
        Compare(
          BinOp(
            "*",
            BinOp("*", Name("candidate"), Name("candidate")),
            Name("candidate")),
          CmpOp("<", Name("a"))),
        AugAssign(Name("candidate"), "+", Int(2)))
      ~> (Return(
           Compare(
             BinOp(
               "*",
               BinOp("*", Name("candidate"), Name("candidate")),
               Name("candidate")),
             CmpOp("==", Name("a")))) .Stmts)
      ~> #endcall
      =>
      cubeSearch(1, 0)
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
