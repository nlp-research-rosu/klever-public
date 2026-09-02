requires "verification.k"

module DIGITS-SPEC-AUDIT-VACUITY
  imports DIGITS-VERIFICATION

  claim [digits-loop]:
    <k>
      #while(
        Compare(Name("n"), CmpOp(">", Int(0))),
        If(
          Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(1))),
          If(
            Compare(Name("product"), CmpOp("==", Int(0))),
            Assign(Name("product"), BinOp("%", Name("n"), Int(10))),
            AugAssign(
              Name("product"),
              "*",
              BinOp("%", Name("n"), Int(10)))),
          .Stmts)
        AugAssign(Name("n"), "//", Int(10)))
      ~> CONT:K
      =>
      CONT
    </k>
    <env> 1 </env>
    <scopes>
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
      1  |-> scope(
              .Map [ "n" <- N:Int ] [ "product" <- A:Int ],
              parent(0))
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
      1  |-> scope(
              .Map
                [ "n" <- 0 ]
                [ "product" <- oddDigitProduct(N, A) ],
              parent(0))
    </scopes>
    requires N >=Int 0 andBool A >=Int 0

  claim [digits-correct]:
    <k>
      Call(Name("digits"), Int(N:Int))
      =>
      oddDigitProduct(N, 0) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
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
