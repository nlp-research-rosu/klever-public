requires "spec.k"

module SPEC-VACUITY
  imports SPEC

  // Deliberately false: the unmodified implementation result is off by one.
  claim [false-post]:
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
    ensures ?R ==Int fizzResult(0, N) +Int 1
endmodule
