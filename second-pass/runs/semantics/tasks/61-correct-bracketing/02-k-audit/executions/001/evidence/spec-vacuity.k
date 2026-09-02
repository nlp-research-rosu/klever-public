requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Reviewer-authored false result mutation. The source loop returns true for
  // S=.IntSeq and B=0, while this destination requires false.
  claim
    <k>
      #loop(
        str(S:IntSeq),
        Name("bracket"),
        If(Compare(Name("bracket"), CmpOp("==", Str("("))),
          AugAssign(Name("balance"), "+", Int(1)),
          AugAssign(Name("balance"), "-", Int(1)))
        If(Compare(Name("balance"), CmpOp("<", Int(0))),
          Return(Bool(false)),
          .Stmts))
      ~> Return(Compare(Name("balance"), CmpOp("==", Int(0))))
      ~> #endcall
      => notBool (correctCodes(S, B)) ~> CONT
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( -1 |-> builtinsScope
        0  |-> scope(GLOBALS, parent(-1))
        1  |-> scope(
          "balance"  |-> B:Int
          "bracket"  |-> OLD:Str
          "brackets" |-> str(INPUT:IntSeq),
          parent(0))
      )
      =>
      ( -1 |-> builtinsScope
        0  |-> scope(GLOBALS, parent(-1))
      )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP </heap>
    <heapLoc> HLOC </heapLoc>
    <stack> ListItem(frame(CONT:K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires B >=Int 0
    [label(false-result)]
endmodule
