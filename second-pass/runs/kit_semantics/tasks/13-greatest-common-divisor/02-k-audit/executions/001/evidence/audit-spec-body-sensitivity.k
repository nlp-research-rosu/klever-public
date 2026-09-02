requires "verification.k"

module AUDIT-SPEC-BODY-SENSITIVITY
  imports VERIFICATION

  // Reviewer-authored terminating body mutation. It changes the actual
  // executed remainder assignment from a % b to 0 while retaining the real
  // theorem target. At A=25, B=15 it returns 15 rather than gcd 5.
  claim [audit-mutated-remainder-zero]:
    <k>
      #while(
        Compare(Name("b"), CmpOp("!=", Int(0))),
        Assign(Name("remainder"), Int(0))
        Assign(Name("a"), Name("b"))
        Assign(Name("b"), Name("remainder"))
      )
      ~> (Return(Call(Name("abs"), Name("a"))) .Stmts)
      ~> #endcall
      =>
      gcdEuclid(A, B) ~> CONT
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
