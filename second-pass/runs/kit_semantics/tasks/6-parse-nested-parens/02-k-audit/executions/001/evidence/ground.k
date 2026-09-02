requires "spec.k"

module GROUND
  imports SPEC

  claim [empty-input]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("parse_nested_parens"), str(.IntSeq))
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
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Input "(()) ()", encoded as character codes; expected result [2, 1].
  claim [two-groups]:
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("parse_nested_parens"),
           str(
             iCons(40,
             iCons(40,
             iCons(41,
             iCons(41,
             iCons(32,
             iCons(40,
             iCons(41, .IntSeq)))))))))
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
    <heap>
      .Map => 0 |-> list(vCons(2, vCons(1, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
