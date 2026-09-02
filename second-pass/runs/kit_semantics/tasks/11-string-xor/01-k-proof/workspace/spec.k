requires "verification.k"

module LOOP-SPEC
  imports VERIFICATION-BASE

  claim [loop-invariant]:
    <k>
      #loop(
        zipObjS(A:IntSeq, B:IntSeq),
        TupleExpr(Name("x"), Name("y")),
        If(
          Compare(Name("x"), CmpOp("==", Name("y"))),
          AugAssign(Name("result"), "+", Str("0")),
          AugAssign(Name("result"), "+", Str("1"))
        )
      )
      =>
      .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "a"      |-> str(A0:IntSeq)
        "b"      |-> str(B0:IntSeq)
        "result" |-> (str(R:IntSeq) => str(xorAcc(R, A, B)))
        "x"      |-> (X0:Val => lastX(X0, A, B))
        "y"      |-> (Y0:Val => lastY(Y0, A, B)),
        P:Parent
      )
      ...
    </scopes>
endmodule

module SPEC
  imports VERIFICATION

  claim [string-xor]:
    <k>
      Call(Name("string_xor"), str(A:IntSeq), str(B:IntSeq))
      =>
      str(?OUT:IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
        "string_xor" |->
          closureVal(
            ("a", "b"),
            Assign(Name("result"), Str(""))
            Assign(Name("x"), Str(""))
            Assign(Name("y"), Str(""))
            For(
              TupleExpr(Name("x"), Name("y")),
              Call(Name("zip"), Name("a"), Name("b")),
              If(
                Compare(Name("x"), CmpOp("==", Name("y"))),
                AugAssign(Name("result"), "+", Str("0")),
                AugAssign(Name("result"), "+", Str("1"))
              )
            )
            Return(Name("result")),
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
    requires bitString(A) andBool bitString(B)
    ensures ?OUT ==K xorAcc(.IntSeq, A, B)
endmodule
