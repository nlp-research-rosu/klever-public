requires "verification.k"

module GROUND-WITNESS
  imports VERIFICATION

  claim [empty]:
    <k> Call(Name("fix_spaces"), str(.IntSeq)) => str(.IntSeq) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "fix_spaces" |->
          closureVal(("text", .ParamNames), #fixSpacesBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [one-space]:
    <k>
      Call(Name("fix_spaces"), str(iCons(32, .IntSeq)))
      =>
      str(iCons(95, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "fix_spaces" |->
          closureVal(("text", .ParamNames), #fixSpacesBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [two-spaces]:
    <k>
      Call(
        Name("fix_spaces"),
        str(iCons(32, iCons(32, .IntSeq))))
      =>
      str(iCons(95, iCons(95, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "fix_spaces" |->
          closureVal(("text", .ParamNames), #fixSpacesBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [three-spaces]:
    <k>
      Call(
        Name("fix_spaces"),
        str(iCons(32, iCons(32, iCons(32, .IntSeq)))))
      =>
      str(iCons(45, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "fix_spaces" |->
          closureVal(("text", .ParamNames), #fixSpacesBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [interior-two]:
    <k>
      Call(
        Name("fix_spaces"),
        str(iCons(97, iCons(32, iCons(32, iCons(98, .IntSeq))))))
      =>
      str(iCons(97, iCons(95, iCons(95, iCons(98, .IntSeq)))))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "fix_spaces" |->
          closureVal(("text", .ParamNames), #fixSpacesBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
