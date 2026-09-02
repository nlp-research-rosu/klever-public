requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // False body-sensitivity probe: the executed program computes N % 9 in its
  // units-place term, while the unchanged postcondition specifies decimal
  // digit sum.  N = 9 is a satisfying counterexample ("0" versus "1001").
  claim
    <k>
      #loadAll(
        Module(
          FuncDef("solve", Params("N"),
            Assign(
              Name("digit_sum"),
              BinOp(
                "+",
                BinOp(
                  "+",
                  BinOp(
                    "+",
                    BinOp(
                      "+",
                      BinOp("%", Name("N"), Int(9)),
                      BinOp("%", BinOp("//", Name("N"), Int(10)), Int(10))),
                    BinOp("%", BinOp("//", Name("N"), Int(100)), Int(10))),
                  BinOp("%", BinOp("//", Name("N"), Int(1000)), Int(10))),
                BinOp("%", BinOp("//", Name("N"), Int(10000)), Int(10))))
            Return(
              Subscript(
                Call(Name("bin"), Name("digit_sum")),
                Slice(Int(2), NoBound, NoBound)))))
      ) ~> Call(Name("solve"), Int(N))
      => binaryNumeral(decimalDigitSum(N))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => .Map [
          "solve" <-
            closureVal(
              ("N", .ParamNames),
              Assign(
                Name("digit_sum"),
                BinOp(
                  "+",
                  BinOp(
                    "+",
                    BinOp(
                      "+",
                      BinOp(
                        "+",
                        BinOp("%", Name("N"), Int(9)),
                        BinOp("%", BinOp("//", Name("N"), Int(10)), Int(10))),
                      BinOp("%", BinOp("//", Name("N"), Int(100)), Int(10))),
                    BinOp("%", BinOp("//", Name("N"), Int(1000)), Int(10))),
                  BinOp("%", BinOp("//", Name("N"), Int(10000)), Int(10))))
              Return(
                Subscript(
                  Call(Name("bin"), Name("digit_sum")),
                  Slice(Int(2), NoBound, NoBound)))
              .Stmts,
              0)
        ],
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires 0 <=Int N andBool N <=Int 10000
endmodule
