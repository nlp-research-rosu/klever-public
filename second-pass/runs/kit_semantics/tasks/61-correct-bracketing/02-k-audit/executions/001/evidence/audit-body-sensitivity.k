requires "verification.k"

module AUDIT-BODY-SENSITIVITY
  imports VERIFICATION

  // Reviewer-authored operational-sensitivity mutation: the executed opening
  // branch adds 2 instead of 1, while the original summary obligation remains.
  claim [mutated-opening-update]:
    <k>
      #loop(
        str(iCons(40, iCons(41, .IntSeq))),
        Name("bracket"),
        If(
          Compare(Name("bracket"), CmpOp("==", Str("("))),
          AugAssign(Name("balance"), "+", Int(2)),
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
      scanBrackets(iCons(40, iCons(41, .IntSeq)), 0, true)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( -1 |-> BUILTINS:Scope
         0 |-> scope(MODULE:Map, parent(-1))
         1 |-> scope(
                "bracket" |-> OLD:Val
                "brackets" |-> str(iCons(40, iCons(41, .IntSeq)))
                "balance" |-> 0
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
