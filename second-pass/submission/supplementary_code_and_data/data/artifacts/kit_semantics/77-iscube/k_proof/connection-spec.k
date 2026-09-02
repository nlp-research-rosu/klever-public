requires "verification-base.k"

module CONNECTION
  imports VERIFICATION-BASE

  // Bridge-free universal connection theorem for the operational rule in
  // verification.k.  Its LHS, guard, continuation, stack, bindings, and every
  // state cell are identical to that rule's complete match domain.
  claim [search-loop]:
    <k>
      #while(
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
             CmpOp("==", Name("a")))) .Stmts)
      ~> #endcall
      =>
      cubeSearch(A, C)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( SC:Map
        1 |-> scope(
               "a"         |-> A:Int
               "candidate" |-> C:Int,
               parent(0))
      =>
        SC
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
