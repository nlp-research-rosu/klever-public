requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION-NO-BRIDGE

  // Deliberately mutated displaced execution: write the sorted value at
  // 2*i+1 instead of 2*i.  The original fillEven postcondition must fail.
  claim [mutated-loop]:
    <k>
      #loop(
        rangeObj(0, 1, 1),
        Name("i"),
        ( Assign(
            Subscript(
              Name("result"),
              BinOp(
                "+",
                BinOp("*", Int(2), Name("i")),
                Int(1))),
            Subscript(Name("evens"), Name("i")))
          .Stmts ))
      ~> (Return(Name("result")) .Stmts)
      ~> #endcall
      => ref(0)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( 0 |-> scope(
          "sort_even" |-> closureVal("l", sortEvenBody, 0),
          parent(-1))
        1 |-> scope(
          ( "l"      |-> list(vCons(9, vCons(8, .ValSeq)))
            "result" |-> ref(0)
            "evens"  |-> ref(2)
            "i"      |-> 0 ),
          parent(0))
        -1 |-> builtinsScope )
      =>
      ( 0 |-> scope(
          "sort_even" |-> closureVal("l", sortEvenBody, 0),
          parent(-1))
        -1 |-> builtinsScope )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap>
      ( 0 |-> list(
          vCons(9, vCons(8, .ValSeq))
          => fillEven(
               vCons(9, vCons(8, .ValSeq)),
               vCons(3, .ValSeq),
               0,
               1))
        1 |-> list(vCons(9, .ValSeq))
        2 |-> list(vCons(3, .ValSeq)) )
    </heap>
    <heapLoc> 3 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      => .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
