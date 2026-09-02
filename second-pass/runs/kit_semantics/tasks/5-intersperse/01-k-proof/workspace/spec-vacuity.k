requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // False postcondition: the correct result [1, 4, 2] is required to have
  // an additional trailing delimiter, [1, 4, 2, 4].
  claim [false-postcondition-rejected]:
    <k> Call(Name("intersperse"),
             list(vCons(1, vCons(2, .ValSeq))), 4)
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
      .Map => 0 |-> list(
                    vCons(1, vCons(4, vCons(2, vCons(4, .ValSeq)))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
