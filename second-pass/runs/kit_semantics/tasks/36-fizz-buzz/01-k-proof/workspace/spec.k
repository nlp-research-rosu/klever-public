requires "verification.k"

module SPEC
  imports VERIFICATION

  // Exact inner while-loop: add the number of 7 digits in X to count.
  claim [inner-loop]:
    <k>
      #while(Compare(Name("x"), CmpOp(">", Int(0))),
        Assign(
          Name("count"),
          BinOp(
            "+",
            Name("count"),
            Compare(
              BinOp("%", Name("x"), Int(10)),
              CmpOp("==", Int(7)))))
        Assign(Name("x"), BinOp("//", Name("x"), Int(10))))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "count" |-> (C:Int => digitResult(C, X))
        "i"     |-> I:Int
        "n"     |-> N:Int
        "x"     |-> (X:Int => 0),
        parent(0))
      ...
    </scopes>
    requires X >=Int 0

  // Exact outer while-loop: process all candidates below I.
  claim [outer-loop]:
    <k>
      #while(Compare(Name("i"), CmpOp(">", Int(0))),
        Assign(Name("i"), BinOp("-", Name("i"), Int(1)))
        If(BoolOp(
          "or",
          Compare(
            BinOp("%", Name("i"), Int(11)),
            CmpOp("==", Int(0))),
          Compare(
            BinOp("%", Name("i"), Int(13)),
            CmpOp("==", Int(0)))),
          Assign(Name("x"), Name("i"))
          While(Compare(Name("x"), CmpOp(">", Int(0))),
            Assign(
              Name("count"),
              BinOp(
                "+",
                Name("count"),
                Compare(
                  BinOp("%", Name("x"), Int(10)),
                  CmpOp("==", Int(7)))))
            Assign(Name("x"), BinOp("//", Name("x"), Int(10)))),
          .Stmts))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "count" |-> (C:Int => fizzResult(C, I))
        "i"     |-> (I:Int => 0)
        "n"     |-> N:Int
        "x"     |-> 0,
        parent(0))
      ...
    </scopes>
    requires I >=Int 0

  // Exact closure invocation for the implementation in solution.mpy.
  claim [fizz-buzz]:
    <k>
      Call(Name("fizz_buzz"), Int(N:Int))
      => ?R:Int
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "fizz_buzz" |->
          closureVal(
            "n",
            Assign(Name("count"), Int(0))
            Assign(Name("i"), Name("n"))
            Assign(Name("x"), Int(0))
            While(Compare(Name("i"), CmpOp(">", Int(0))),
              Assign(Name("i"), BinOp("-", Name("i"), Int(1)))
              If(BoolOp(
                "or",
                Compare(
                  BinOp("%", Name("i"), Int(11)),
                  CmpOp("==", Int(0))),
                Compare(
                  BinOp("%", Name("i"), Int(13)),
                  CmpOp("==", Int(0)))),
                Assign(Name("x"), Name("i"))
                While(Compare(Name("x"), CmpOp(">", Int(0))),
                  Assign(
                    Name("count"),
                    BinOp(
                      "+",
                      Name("count"),
                      Compare(
                        BinOp("%", Name("x"), Int(10)),
                        CmpOp("==", Int(7)))))
                  Assign(
                    Name("x"),
                    BinOp("//", Name("x"), Int(10)))),
                .Stmts))
            Return(Name("count")),
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
    ensures ?R ==Int fizzResult(0, N)
endmodule
