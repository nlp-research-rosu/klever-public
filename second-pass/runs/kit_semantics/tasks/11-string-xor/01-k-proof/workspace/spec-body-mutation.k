requires "verification.k"

module LOOP-SPEC-BODY-MUTATION
  imports VERIFICATION-BASE

  // Deliberately wrong connection claim: the source body has its "0" and
  // "1" appends exchanged while the original xorAcc postcondition is kept.
  claim [swapped-branches]:
    <k>
      #loop(
        zipObjS(A:IntSeq, B:IntSeq),
        TupleExpr(Name("x"), Name("y")),
        If(
          Compare(Name("x"), CmpOp("==", Name("y"))),
          AugAssign(Name("result"), "+", Str("1")),
          AugAssign(Name("result"), "+", Str("0"))
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
