requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-ADEQUACY
  imports VERIFICATION

  // The empty sequence is a concrete satisfier of nonNegativeInts(VALUES).
  claim [empty-witness]:
    <k> #loadAll(isSortedModule)
        ~> Call(Name("is_sorted"), (list(.ValSeq), .Exprs))
        => true
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
              "is_sorted" |->
                closureVal(
                  ("lst", .ParamNames),
                  isSortedBody,
                  0),
              parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // A concrete false result exercises the third-equal-element boundary.
  claim [triple-zero-witness]:
    <k> #loadAll(isSortedModule)
        ~> Call(
             Name("is_sorted"),
             (list(vCons(0, vCons(0, vCons(0, .ValSeq)))), .Exprs))
        => false
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
              "is_sorted" |->
                closureVal(
                  ("lst", .ParamNames),
                  isSortedBody,
                  0),
              parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

endmodule
