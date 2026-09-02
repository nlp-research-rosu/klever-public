requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports VERIFICATION

  // Reviewer-authored false mutation: the real loop result is changed by +2.
  // A=25, B=15, GLOBALS=.Map, _R=0, CONT=.K is a satisfying witness;
  // the actual and specified results are respectively 5 and 7.
  claim [audit-false-plus-two]:
    <k>
      #while(
        Compare(Name("b"), CmpOp("!=", Int(0))),
        Assign(Name("remainder"), BinOp("%", Name("a"), Name("b")))
        Assign(Name("a"), Name("b"))
        Assign(Name("b"), Name("remainder"))
      )
      ~> (Return(Call(Name("abs"), Name("a"))) .Stmts)
      ~> #endcall
      =>
      gcdEuclid(A, B) +Int 2 ~> CONT
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( 0 |-> scope(GLOBALS, parent(-1))
        1 |-> scope(
          "a" |-> A
          "b" |-> B
          "remainder" |-> _R,
          parent(0)
        )
       -1 |-> builtinsScope )
      =>
      ( 0 |-> scope(GLOBALS, parent(-1))
       -1 |-> builtinsScope )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(CONT, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool ("abs" in_keys(GLOBALS))
endmodule
