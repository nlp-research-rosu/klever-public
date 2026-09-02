requires "verification.k"

module SPEC
  imports VERIFICATION

  // The inner loop scans the suffix j..N-1 of one row.  Its continuation is
  // framed, so the claim can be used both by the outer loop and by itself at
  // the exact while back-edge.
  claim [inner-one-ahead]:
    <k> innerWhile => .K ... </k>
    <env> L:Int </env>
    <scopes>
      L |-> scope(
        ("grid" |-> list(gridRows(P:IntSeq, N:Int)))
        ("k" |-> _K:Int)
        ("n" |-> N)
        ("i" |-> I:Int)
        ("j" |-> (J:Int => N))
        ("row" |-> (_R:Int => oneRow(P, N)))
        ("col" |-> (_C:Int => oneCol(P, N))),
        parent(0))
      0 |-> scope(("$perm" |-> str(P)) GLOBALS:Map, parent(-1))
      RESTSCOPES:Map
    </scopes>
    requires N >=Int 2 andBool validPerm(P, N *Int N)
      andBool I >=Int 0 andBool I <Int N
      andBool J >=Int 0 andBool J <=Int N
      andBool I ==Int oneRow(P, N) andBool J <=Int oneCol(P, N)
      andBool oneRow(P, N) >=Int 0 andBool oneRow(P, N) <Int N
      andBool oneCol(P, N) >=Int 0 andBool oneCol(P, N) <Int N

  claim [inner-no-one]:
    <k> innerWhile => .K ... </k>
    <env> L:Int </env>
    <scopes>
      L |-> scope(
        ("grid" |-> list(gridRows(P:IntSeq, N:Int)))
        ("k" |-> _K:Int)
        ("n" |-> N)
        ("i" |-> I:Int)
        ("j" |-> (J:Int => N))
        ("row" |-> R:Int)
        ("col" |-> C:Int),
        parent(0))
      0 |-> scope(("$perm" |-> str(P)) GLOBALS:Map, parent(-1))
      RESTSCOPES:Map
    </scopes>
    requires N >=Int 2 andBool validPerm(P, N *Int N)
      andBool I >=Int 0 andBool I <Int N
      andBool J >=Int 0 andBool J <=Int N
      andBool notBool (I ==Int oneRow(P, N)
                       andBool J <=Int oneCol(P, N))
      andBool oneRow(P, N) >=Int 0 andBool oneRow(P, N) <Int N
      andBool oneCol(P, N) >=Int 0 andBool oneCol(P, N) <Int N

  // The outer loop scans rows I..N-1.  The inner-loop claim supplies the
  // exact effect of each row scan before the outer circularity advances I.
  claim [outer-one-ahead]:
    <k> outerWhile => .K ... </k>
    <env> L:Int </env>
    <scopes>
      L |-> scope(
        ("grid" |-> list(gridRows(P:IntSeq, N:Int)))
        ("k" |-> _K:Int)
        ("n" |-> N)
        ("i" |-> (I:Int => N))
        ("j" |-> (_J:Int => N))
        ("row" |-> (_R:Int => oneRow(P, N)))
        ("col" |-> (_C:Int => oneCol(P, N))),
        parent(0))
      0 |-> scope(("$perm" |-> str(P)) GLOBALS:Map, parent(-1))
      RESTSCOPES:Map
    </scopes>
    requires N >=Int 2 andBool validPerm(P, N *Int N)
      andBool I >=Int 0 andBool I <=Int N
      andBool I <=Int oneRow(P, N)
      andBool oneRow(P, N) >=Int 0 andBool oneRow(P, N) <Int N
      andBool oneCol(P, N) >=Int 0 andBool oneCol(P, N) <Int N

  claim [outer-one-past]:
    <k> outerWhile => .K ... </k>
    <env> L:Int </env>
    <scopes>
      L |-> scope(
        ("grid" |-> list(gridRows(P:IntSeq, N:Int)))
        ("k" |-> _K:Int)
        ("n" |-> N)
        ("i" |-> (I:Int => N))
        ("j" |-> (J:Int => N))
        ("row" |-> R:Int)
        ("col" |-> C:Int),
        parent(0))
      0 |-> scope(("$perm" |-> str(P)) GLOBALS:Map, parent(-1))
      RESTSCOPES:Map
    </scopes>
    requires N >=Int 2 andBool validPerm(P, N *Int N)
      andBool I >=Int 0 andBool I <=Int N
      andBool I >Int oneRow(P, N)
      andBool (I <Int N orBool J ==Int N)
      andBool oneRow(P, N) >=Int 0 andBool oneRow(P, N) <Int N
      andBool oneCol(P, N) >=Int 0 andBool oneCol(P, N) <Int N

  // Exact source-level cut for the nested scan.  The local-map rewrite also
  // records the j binding created by the first outer iteration.
  claim [scan-finish]:
    <k> outerLoop TAIL:Stmts => TAIL ... </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        (("grid" |-> list(gridRows(P:IntSeq, N:Int)))
         ("k" |-> K:Int)
         ("n" |-> N)
         ("row" |-> 0)
         ("col" |-> 0)
         ("i" |-> 0)
         =>
         ("grid" |-> list(gridRows(P, N)))
         ("k" |-> K)
         ("n" |-> N)
         ("row" |-> oneRow(P, N))
         ("col" |-> oneCol(P, N))
         ("i" |-> N)
         ("j" |-> N)),
        parent(0))
      0 |-> scope(("$perm" |-> str(P)) GLOBALS:Map, parent(-1))
      RESTSCOPES:Map
    </scopes>
    requires N >=Int 2 andBool validPerm(P, N *Int N)
      andBool oneRow(P, N) >=Int 0 andBool oneRow(P, N) <Int N
      andBool oneCol(P, N) >=Int 0 andBool oneCol(P, N) <Int N

  // Sequential cut for the complete neighbor phase.  This exact
  // reachability claim is proved directly from the four conditionals.
  claim [neighbor-finish]:
    <k> upIf downIf leftIf rightIf TAIL:Stmts => TAIL ... </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        ("grid" |-> list(gridRows(P:IntSeq, N:Int)))
        ("k" |-> K:Int) ("n" |-> N)
        ("row" |-> R:Int) ("col" |-> C:Int)
        ("i" |-> N) ("j" |-> _J:Int)
        ("neighbor" |->
          (N *Int N +Int 1 => neighborMin(P, N, R, C))),
        parent(0))
      0 |-> scope(("$perm" |-> str(P)) GLOBALS:Map, parent(-1))
      RESTSCOPES:Map
    </scopes>
    requires N >=Int 2 andBool validPerm(P, N *Int N)
      andBool R ==Int oneRow(P, N) andBool C ==Int oneCol(P, N)
      andBool R >=Int 0 andBool R <Int N
      andBool C >=Int 0 andBool C <Int N

  // Exact generalized state at the result loop head.  R is the
  // remaining iteration count and A is the accumulated structural prefix.
  // The exact continuation and call frame ensure this circularity can apply
  // only to this loop, while the base branch executes the odd tail and return.
  claim [result-loop-tail]:
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
    ensures finishRel(
      A, ?OUT, R,
      neighborMin(P, N, oneRow(P, N), oneCol(P, N)), K)

  // Required full-domain target: exact call binding and exact solution body,
  // for every N>=2 permutation grid and every positive K.
  claim [minpath-full-contract]:
    <k>
      Call(Name("minPath"),
           (list(gridRows(P:IntSeq, N:Int)), K:Int, .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        ("$perm" |-> str(P))
        ("minPath" |-> closureVal(("grid", "k", .ParamNames),
                                   minPathBody, 0)),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map => 0 |-> list(?OUT:ValSeq)
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 2 andBool K >Int 0
      andBool validPerm(P, N *Int N)
      andBool oneRow(P, N) >=Int 0 andBool oneRow(P, N) <Int N
      andBool oneCol(P, N) >=Int 0 andBool oneCol(P, N) <Int N
    ensures finishRel(
      .ValSeq,
      ?OUT,
      (K -Int pyMod(K, 2)) /Int 2,
      neighborMin(P, N, oneRow(P, N), oneCol(P, N)),
      K)

endmodule
