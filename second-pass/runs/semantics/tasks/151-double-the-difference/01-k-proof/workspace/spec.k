requires "verification.k"

module DOUBLE-THE-DIFFERENCE-SPEC
  imports DOUBLE-THE-DIFFERENCE-VERIFICATION

  claim [loop-invariant]:
    <k>
      #loop(
        list(numVals(NUMBERS)),
        Name("number"),
        If(
          BoolOp(
            "and",
            Call(
              Name("isinstance"),
              Name("number"),
              Name("int")),
            Compare(
              Name("number"),
              CmpOp(">", Int(0))),
            Compare(
              BinOp("%", Name("number"), Int(2)),
              CmpOp("==", Int(1)))),
          AugAssign(
            Name("total"),
            "+",
            BinOp("**", Name("number"), Int(2))),
          .Stmts))
      ~> CONT
    =>
      CONT
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "lst" |-> _INPUT
        "total" |->
          (ACC => ACC +Int doubleDifferenceSpec(NUMBERS))
        "number" |->
          (OLDNUMBER => finalNumber(NUMBERS, OLDNUMBER)),
        parent(0))
      0 |-> scope(
        "double_the_difference" |-> _FUNCTION,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>

  claim [double-the-difference-correct]:
    <k>
      Call(
        Name("double_the_difference"),
        list(numVals(NUMBERS)))
      => doubleDifferenceSpec(NUMBERS)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "double_the_difference" |->
          closureVal(
            "lst",
            Assign(Name("total"), Int(0))
            Assign(Name("number"), Int(0))
            For(
              Name("number"),
              Name("lst"),
              If(
                BoolOp(
                  "and",
                  Call(
                    Name("isinstance"),
                    Name("number"),
                    Name("int")),
                  Compare(
                    Name("number"),
                    CmpOp(">", Int(0))),
                  Compare(
                    BinOp("%", Name("number"), Int(2)),
                    CmpOp("==", Int(1)))),
                AugAssign(
                  Name("total"),
                  "+",
                  BinOp("**", Name("number"), Int(2))),
                .Stmts))
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
endmodule
