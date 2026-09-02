requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false-postcondition probe: N=0 executes to "0", while this
  // off-by-one postcondition requires binaryNumeral(1), namely "1".
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
                      BinOp("%", Name("N"), Int(10)),
                      BinOp("%", BinOp("//", Name("N"), Int(10)), Int(10))),
                    BinOp("%", BinOp("//", Name("N"), Int(100)), Int(10))),
                  BinOp("%", BinOp("//", Name("N"), Int(1000)), Int(10))),
                BinOp("%", BinOp("//", Name("N"), Int(10000)), Int(10))))
            Return(
              Subscript(
                Call(Name("bin"), Name("digit_sum")),
                Slice(Int(2), NoBound, NoBound)))))
      ) ~> Call(Name("solve"), Int(N))
      => binaryNumeral(decimalDigitSum(N) +Int 1)
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
                        BinOp("%", Name("N"), Int(10)),
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
