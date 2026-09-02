requires "verification-with-loop.k"

module SPEC-VALUE-MUTATION
  imports VERIFICATION-WITH-LOOP

  // Opposite-value probe for a false-producing bridge state: one unmatched
  // opening bracket remains in the balance, so the actual result is false.
  claim [unmatched-open-is-true]:
    <k>
      #loop(
        str(.IntSeq),
        Name("bracket"),
        If(
          Compare(Name("bracket"), CmpOp("==", Str("("))),
          AugAssign(Name("balance"), "+", Int(1)),
          AugAssign(Name("balance"), "-", Int(1)))
        If(
          Compare(Name("balance"), CmpOp("<", Int(0))),
          Assign(Name("valid"), Bool(false)),
          .Stmts))
      ~> (Return(
            BoolOp(
              "and",
              Name("valid"),
              Compare(Name("balance"), CmpOp("==", Int(0)))))
          .Stmts)
      ~> #endcall
      =>
      true
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( -1 |-> BUILTINS:Scope
         0 |-> scope(MODULE:Map, parent(-1))
         1 |-> scope(
                "bracket" |-> str(iCons(40, .IntSeq))
                "brackets" |-> str(iCons(40, .IntSeq))
                "balance" |-> 1
                "valid" |-> true,
                parent(0)) )
      =>
      ( -1 |-> BUILTINS
         0 |-> scope(MODULE, parent(-1)) )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
