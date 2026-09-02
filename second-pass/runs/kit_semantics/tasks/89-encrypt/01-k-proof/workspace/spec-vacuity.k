requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Expected to fail: encrypt("") returns "", not "a".
  claim [false-result]:
    <k>
      Call(Name("encrypt"), str(.IntSeq))
      =>
      str(iCons(97, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "encrypt" |->
          closureVal(
            "s",
            Expr(
              Str("Rotate lowercase letters four places and preserve other characters."))
            Assign(Name("out"), Str(""))
            Assign(Name("c"), Str(""))
            For(
              Name("c"),
              Name("s"),
              If(
                BoolOp(
                  "and",
                  Compare(
                    Call(Name("ord"), Name("c")),
                    CmpOp(">=", Int(97))),
                  Compare(
                    Call(Name("ord"), Name("c")),
                    CmpOp("<=", Int(122)))),
                AugAssign(
                  Name("out"),
                  "+",
                  Call(
                    Name("chr"),
                    BinOp(
                      "+",
                      BinOp(
                        "%",
                        BinOp(
                          "+",
                          BinOp("-", Call(Name("ord"), Name("c")), Int(97)),
                          Int(4)),
                        Int(26)),
                      Int(97)))),
                AugAssign(Name("out"), "+", Name("c"))))
            Return(Name("out")),
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
endmodule
