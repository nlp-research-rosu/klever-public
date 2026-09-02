requires "candidate/spec.k"

module PROGRAM-PINNING
  imports DIGITS-SPEC

  claim [program-pinned]:
    <k>
      #loadAll(
        Module(
          FuncDef("digits", Params("n"),
            Assign(Name("product"), Int(0))
            While(Compare(Name("n"), CmpOp(">", Int(0))),
              If(
                Compare(
                  BinOp("%", Name("n"), Int(2)),
                  CmpOp("==", Int(1))),
                If(
                  Compare(Name("product"), CmpOp("==", Int(0))),
                  Assign(
                    Name("product"),
                    BinOp("%", Name("n"), Int(10))),
                  AugAssign(
                    Name("product"),
                    "*",
                    BinOp("%", Name("n"), Int(10)))),
                .Stmts)
              AugAssign(Name("n"), "//", Int(10)))
            Return(Name("product")))))
      ~> Call(Name("digits"), Int(N:Int))
      =>
      oddDigitProduct(N, 0)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(.Map, parent(-1))
      =>
      -1 |-> builtinsScope
      0  |-> scope(
              "digits" |->
                closureVal(
                  "n",
                  Assign(Name("product"), Int(0))
                  While(
                    Compare(Name("n"), CmpOp(">", Int(0))),
                    If(
                      Compare(
                        BinOp("%", Name("n"), Int(2)),
                        CmpOp("==", Int(1))),
                      If(
                        Compare(Name("product"), CmpOp("==", Int(0))),
                        Assign(
                          Name("product"),
                          BinOp("%", Name("n"), Int(10))),
                        AugAssign(
                          Name("product"),
                          "*",
                          BinOp("%", Name("n"), Int(10)))),
                      .Stmts)
                    AugAssign(Name("n"), "//", Int(10)))
                  Return(Name("product")),
                  0),
              parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >Int 0
endmodule
