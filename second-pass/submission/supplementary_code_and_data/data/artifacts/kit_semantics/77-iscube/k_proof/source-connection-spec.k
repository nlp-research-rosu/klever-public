requires "connection-rule.k"

module SOURCE-CONNECTION
  imports CONNECTION-RULE

  // Universal connection theorem for the source-While bridge in
  // verification.k.  It does not import that proposed bridge.  Its only
  // proof extension affecting execution is CONNECTION-RULE, whose identical
  // #while behavior is proved bridge-free by CONNECTION.search-loop.
  claim [search-loop-source]:
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
