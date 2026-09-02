requires "verification.k"

module FIB4-SPEC
  imports FIB4-VERIFICATION

  // Symbolic preservation step for the loop invariant.  For arbitrary
  // integer state, the body rotates the four previous terms, stores their
  // sum, and advances i exactly once.
  claim [loop-step]:
    <k>
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
      Assign(Name("i"), BinOp("+", Name("i"), Int(1)))
      => .K
    </k>
    <env> L:Int </env>
    <scopes>
      L |-> scope(
        ( "a"          |-> (A:Int => B)
          "b"          |-> (B:Int => C)
          "c"          |-> (C:Int => D)
          "d"          |-> (D:Int => A +Int B +Int C +Int D)
          "next_value" |-> (_E:Int => A +Int B +Int C +Int D)
          "i"          |-> (I:Int => I +Int 1) ),
        P:Parent)
    </scopes>

  // The closure below is exactly the FuncDef body emitted in solution.mpy.
  // This operational claim checks all base cases, the prompt examples, and
  // additional recurrence points through n=12 under the supplied MPY rules.
  claim [operational-cases]:
    <k>
      Assert(Compare(Call(Name("fib4"), Int(0)),  CmpOp("==", Int(0))))
      Assert(Compare(Call(Name("fib4"), Int(1)),  CmpOp("==", Int(0))))
      Assert(Compare(Call(Name("fib4"), Int(2)),  CmpOp("==", Int(2))))
      Assert(Compare(Call(Name("fib4"), Int(3)),  CmpOp("==", Int(0))))
      Assert(Compare(Call(Name("fib4"), Int(4)),  CmpOp("==", Int(2))))
      Assert(Compare(Call(Name("fib4"), Int(5)),  CmpOp("==", Int(4))))
      Assert(Compare(Call(Name("fib4"), Int(6)),  CmpOp("==", Int(8))))
      Assert(Compare(Call(Name("fib4"), Int(7)),  CmpOp("==", Int(14))))
      Assert(Compare(Call(Name("fib4"), Int(8)),  CmpOp("==", Int(28))))
      Assert(Compare(Call(Name("fib4"), Int(9)),  CmpOp("==", Int(54))))
      Assert(Compare(Call(Name("fib4"), Int(10)), CmpOp("==", Int(104))))
      Assert(Compare(Call(Name("fib4"), Int(11)), CmpOp("==", Int(200))))
      Assert(Compare(Call(Name("fib4"), Int(12)), CmpOp("==", Int(386))))
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
