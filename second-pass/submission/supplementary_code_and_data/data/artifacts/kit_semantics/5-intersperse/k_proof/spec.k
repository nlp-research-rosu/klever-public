requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-invariant]:
    <k> #loop(list(REST:ValSeq), Name("number"), INTERSPERSE-BODY)
        => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
            "delimeter" |-> D:Int
            "number"    |-> (OLD:Val => ?LAST:Val)
            "numbers"   |-> list(ORIGINAL:ValSeq)
            "result"    |-> ref(H:Int),
            parent(0))
      ...
    </scopes>
    <heap>
      ... H |-> list(
            vCons(A:Val, AS:ValSeq)
            => intersperseAcc(vCons(A, AS), REST, D))
      ...
    </heap>
  claim [intersperse-correct]:
    <k> Call(Name("intersperse"), list(INPUT:ValSeq), D:Int)
        => ref(0) </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
              "intersperse" |->
                closureVal("numbers", "delimeter", .ParamNames,
                  Assign(Name("result"), ListExpr(.Exprs))
                  For(Name("number"), Name("numbers"), INTERSPERSE-BODY)
                  Return(Name("result"))
                  .Stmts,
                  0),
              parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map => 0 |-> list(intersperseAcc(.ValSeq, INPUT, D))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
