requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [gcd-loop]:
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

  claim [gcd-entry]:
    <k>
      Call(
        Name("greatest_common_divisor"),
        Int(A),
        Int(B)
      )
      =>
      #while(
        Compare(Name("b"), CmpOp("!=", Int(0))),
        Assign(Name("remainder"), BinOp("%", Name("a"), Name("b")))
        Assign(Name("a"), Name("b"))
        Assign(Name("b"), Name("remainder"))
      )
      ~> (Return(Call(Name("abs"), Name("a"))) .Stmts)
      ~> #endcall
    </k>
    <env> 0 => 1 </env>
    <scopes>
      ( 0 |-> scope(
          "greatest_common_divisor" |->
            closureVal(
              ("a", "b"),
              Expr(
                Str("Return the non-negative greatest common divisor of a and b.")
              )
              Assign(Name("remainder"), Int(0))
              While(
                Compare(Name("b"), CmpOp("!=", Int(0))),
                Assign(Name("remainder"), BinOp("%", Name("a"), Name("b")))
                Assign(Name("a"), Name("b"))
                Assign(Name("b"), Name("remainder"))
              )
              Return(Call(Name("abs"), Name("a"))),
              0
            ),
          parent(-1)
        )
       -1 |-> builtinsScope )
      =>
      ( 0 |-> scope(
          "greatest_common_divisor" |->
            closureVal(
              ("a", "b"),
              Expr(
                Str("Return the non-negative greatest common divisor of a and b.")
              )
              Assign(Name("remainder"), Int(0))
              While(
                Compare(Name("b"), CmpOp("!=", Int(0))),
                Assign(Name("remainder"), BinOp("%", Name("a"), Name("b")))
                Assign(Name("a"), Name("b"))
                Assign(Name("b"), Name("remainder"))
              )
              Return(Call(Name("abs"), Name("a"))),
              0
            ),
          parent(-1)
        )
        1 |-> scope(
          "a" |-> A
          "b" |-> B
          "remainder" |-> 0,
          parent(0)
        )
       -1 |-> builtinsScope )
    </scopes>
    <scopeLoc> 1 => 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      .List => ListItem(frame(.K, 0, 1))
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
