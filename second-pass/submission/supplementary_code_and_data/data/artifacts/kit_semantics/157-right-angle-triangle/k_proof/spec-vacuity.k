requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: (3, 4, 5) returns true, not false.
  claim [false-right-angle-result]:
    <k>
      Call(Name("right_angle_triangle"), 3, 4, 5)
      =>
      ?RESULT:Bool
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "right_angle_triangle" |->
          closureVal(
            ("a", "b", "c"),
            Return(
              BoolOp(
                "or",
                Compare(
                  BinOp("*", Name("a"), Name("a")),
                  CmpOp(
                    "==",
                    BinOp(
                      "+",
                      BinOp("*", Name("b"), Name("b")),
                      BinOp("*", Name("c"), Name("c"))
                    )
                  )
                ),
                Compare(
                  BinOp("*", Name("b"), Name("b")),
                  CmpOp(
                    "==",
                    BinOp(
                      "+",
                      BinOp("*", Name("a"), Name("a")),
                      BinOp("*", Name("c"), Name("c"))
                    )
                  )
                ),
                Compare(
                  BinOp("*", Name("c"), Name("c")),
                  CmpOp(
                    "==",
                    BinOp(
                      "+",
                      BinOp("*", Name("a"), Name("a")),
                      BinOp("*", Name("b"), Name("b"))
                    )
                  )
                )
              )
            ),
            0
          ),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?RESULT ==Bool false
endmodule
