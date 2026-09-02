requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  claim [mutated-loop]:
    <k>
      #while(
        Compare(Name("b"), CmpOp("!=", Int(0))),
        Assign(Name("remainder"), Int(1))
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
