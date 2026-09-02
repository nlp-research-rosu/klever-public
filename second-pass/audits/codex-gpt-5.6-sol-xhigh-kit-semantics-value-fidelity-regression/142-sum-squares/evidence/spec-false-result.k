requires "verification.k"

module SPEC-FALSE-RESULT
  imports VERIFICATION

  claim [loop-invariant]:
    <k>
      #loop(
        list(VS:ValSeq),
        Name("value"),
        If(
          Compare(
            BinOp("%", Name("index"), Int(3)),
            CmpOp("==", Int(0))),
          AugAssign(
            Name("total"),
            "+",
            BinOp("*", Name("value"), Name("value"))),
          If(
            Compare(
              BinOp("%", Name("index"), Int(4)),
              CmpOp("==", Int(0))),
            AugAssign(
              Name("total"),
              "+",
              BinOp(
                "*",
                BinOp("*", Name("value"), Name("value")),
                Name("value"))),
            AugAssign(Name("total"), "+", Name("value"))))
        AugAssign(Name("index"), "+", Int(1)))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      (L |-> scope(
        ("lst"   |-> list(ORIG:ValSeq))
        ("total" |-> (R:Int => sumSquares(VS, I, R)))
        ("index" |-> (I:Int => advanceIndex(VS, I)))
        ("value" |-> (_OLD:Val => ?LAST:Val)),
        parent(0)))
      SC:Map
    </scopes>
    requires allInts(VS)

  // Fresh reviewer mutation: for the satisfying input [1,2,3], the real and
  // claimed result is 6, so requiring the universal result plus one demands 7.
  claim [sum-squares-plus-one]:
    <k>
      Call(
        Name("sum_squares"),
        list(VS:ValSeq))
      => sumSquares(VS, 0, 0) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "sum_squares" |->
          closureVal(
            "lst",
            Assign(Name("total"), Int(0))
            Assign(Name("index"), Int(0))
            Assign(Name("value"), Int(0))
            For(
              Name("value"),
              Name("lst"),
              If(
                Compare(
                  BinOp("%", Name("index"), Int(3)),
                  CmpOp("==", Int(0))),
                AugAssign(
                  Name("total"),
                  "+",
                  BinOp("*", Name("value"), Name("value"))),
                If(
                  Compare(
                    BinOp("%", Name("index"), Int(4)),
                    CmpOp("==", Int(0))),
                  AugAssign(
                    Name("total"),
                    "+",
                    BinOp(
                      "*",
                      BinOp("*", Name("value"), Name("value")),
                      Name("value"))),
                  AugAssign(Name("total"), "+", Name("value"))))
              AugAssign(Name("index"), "+", Int(1)))
            Return(Name("total")),
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
    requires allInts(VS)
endmodule
