requires "verification.k"

module FIB4-SPEC-VACUITY
  imports FIB4-VERIFICATION

  // Fresh reviewer mutation: the actual program returns 14 for n = 7.
  // Requiring 15 changes a reachable, result-constraining obligation.
  claim [operational-cases-false]:
    <k>
      Assert(Compare(Call(Name("fib4"), Int(7)), CmpOp("==", Int(15))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "fib4" |-> closureVal(
          ("n", .ParamNames),
          If(Compare(Name("n"), CmpOp("==", Int(0))),
            Return(Int(0)) .Stmts,
            .Stmts)
          If(Compare(Name("n"), CmpOp("==", Int(1))),
            Return(Int(0)) .Stmts,
            .Stmts)
          If(Compare(Name("n"), CmpOp("==", Int(2))),
            Return(Int(2)) .Stmts,
            .Stmts)
          If(Compare(Name("n"), CmpOp("==", Int(3))),
            Return(Int(0)) .Stmts,
            .Stmts)
          Assign(Name("a"), Int(0))
          Assign(Name("b"), Int(0))
          Assign(Name("c"), Int(2))
          Assign(Name("d"), Int(0))
          Assign(Name("next_value"), Int(0))
          Assign(Name("i"), Int(4))
          While(Compare(Name("i"), CmpOp("<=", Name("n"))),
            Assign(
              Name("next_value"),
              BinOp(
                "+",
                BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")),
                Name("d")))
            Assign(Name("a"), Name("b"))
            Assign(Name("b"), Name("c"))
            Assign(Name("c"), Name("d"))
            Assign(Name("d"), Name("next_value"))
            Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
          Return(Name("d"))
          .Stmts,
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
