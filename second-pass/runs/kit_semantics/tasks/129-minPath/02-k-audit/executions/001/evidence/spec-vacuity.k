requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation of the independently closing result-loop theorem.
  // The operational LHS, cells, and precondition are unchanged.  Only the
  // result constraint is negated; N=2, P=[1,2,3,4], K=3, R=1, A=.ValSeq is a
  // satisfying witness whose actual result [1,2,1] makes this ensures false.
  claim [false-result-loop-tail]:
    <k>
      Compare(R:Int, CmpOp(">", 0))
      ~> #whileCond(
           Compare(Name("pairs"), CmpOp(">", Int(0))), resultBody)
      ~> oddTail ~> Return(Name("result")) .Stmts ~> #endcall
      => Return(Name("result")) .Stmts ~> #endcall
    </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(
        ("$perm" |-> str(P:IntSeq))
        ("minPath" |-> closureVal(("grid", "k", .ParamNames),
                                   minPathBody, 0)),
        parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
        ("grid" |-> list(gridRows(P, N:Int)))
        ("k" |-> K:Int)
        ("n" |-> N)
        ("row" |-> oneRow(P, N))
        ("col" |-> oneCol(P, N))
        ("i" |-> N)
        ("j" |-> N)
        ("neighbor" |-> neighborMin(P, N, oneRow(P, N), oneCol(P, N)))
        ("result" |-> ref(0))
        ("pairs" |-> (R:Int => 0)),
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> 0 |-> list(A:ValSeq => ?OUT:ValSeq) </heap>
    <heapLoc> 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 2 andBool K >Int 0
      andBool validPerm(P, N *Int N)
      andBool oneRow(P, N) >=Int 0 andBool oneRow(P, N) <Int N
      andBool oneCol(P, N) >=Int 0 andBool oneCol(P, N) <Int N
      andBool R >Int 0
    ensures notBool finishRel(
      A, ?OUT, R,
      neighborMin(P, N, oneRow(P, N), oneCol(P, N)), K)

endmodule
