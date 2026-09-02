requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately mutated binding: return [] cannot meet the original result
  // requirement for input "a".
  claim [mutated-body]:
    <k>
      Call(Name("words_string"), str(iCons(97, .IntSeq)))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "words_string" |-> closureVal(
          ("s", .ParamNames),
          (Return(ListExpr(.Exprs)) .Stmts),
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(str(iCons(97, .IntSeq)), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
