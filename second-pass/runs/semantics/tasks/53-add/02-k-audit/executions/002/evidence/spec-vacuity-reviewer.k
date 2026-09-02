requires "verification.k"

module ADD-SPEC-VACUITY-REVIEWER
  imports ADD-VERIFICATION

  // Reviewer-authored false postcondition. At X=2,Y=3 it demands 5 = 6.
  claim
    <k> #callAdd(X:Int, Y:Int) => (X +Int Y) +Int 1 </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (0 |-> scope(
        "add" |-> closureVal(
          ("x", "y"),
          Return(BinOp("+", Name("x"), Name("y"))),
          0),
        parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
