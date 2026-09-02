requires "spec.k"

module FALSE-RESULT
  imports SPEC

  // "()" satisfies the target precondition and both Python implementations
  // return [1]. This mutation deliberately demands the false result [2].
  claim [wrong-depth-for-one-pair]:
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("parse_nested_parens"),
           str(iCons(40, iCons(41, .IntSeq))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      ( 0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope )
      =>
      ( 0  |-> scope(
          "parse_nested_parens"
            |-> closureVal("paren_string", solutionBody, 0),
          parent(-1))
        -1 |-> builtinsScope )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(2, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
