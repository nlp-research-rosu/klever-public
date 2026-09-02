requires "spec.k"

module SPEC-VACUITY
  imports SPEC

  // Deliberately false: the exact program returns [1] for "()", not [2].
  claim [wrong-result]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("parse_nested_parens"),
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
